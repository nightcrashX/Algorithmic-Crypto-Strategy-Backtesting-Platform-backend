
import asyncio
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import ccxt.async_support as ccxt  
import logging
from app.services.exchange_service import get_ohlcv
from app.services.indicator_service import calculate_live_indicators
# from app.utils.redis_client import redis_client
import json

ws_router = APIRouter(prefix="/live", tags=["LIVE_STREAM"])

@ws_router.websocket("/ws/candles/{exchange_id}/{symbol}/{timeframe}")
async def websocket_candle_stream(websocket: WebSocket, exchange_id: str, symbol: str, timeframe: str):
    print("enter in websocket route")
    await websocket.accept()
    
    # Safely instantiate exchange classes using ccxt's native initialization
    exchange_id_lower = exchange_id.lower()
    if exchange_id_lower not in ccxt.exchanges:
        await websocket.close(code=4001, reason=f"Exchange '{exchange_id}' not supported")
        return

    # Dynamically grab the class and instantiate it
    exchange_class = getattr(ccxt, exchange_id_lower)
    exchange = exchange_class({'enableRateLimit': True})
    
    # Format symbol: Frontend sends "BTCUSDT", CCXT expects "BTC/USDT"
    formatted_symbol = symbol
    if "/" not in symbol and len(symbol) > 4:
        if symbol.endswith("USDT"):
            formatted_symbol = f"{symbol[:-4]}/USDT"
        elif symbol.endswith("BTC"):
            formatted_symbol = f"{symbol[:-3]}/BTC"

    active_indicators = []
    indicators_param = websocket.query_params.get("indicators")
    if indicators_param:
        try:
            active_indicators = json.loads(indicators_param)
            print(f"📊 Initial active indicators from query: {[i.get('type') for i in active_indicators]}")
        except Exception as e:
            logging.warning(f"Failed to parse initial indicators query param: {e}")

    receive_task = None
    all_candles = []

    async def receive_messages():
        nonlocal active_indicators
        try:
            while True:
                msg_text = await websocket.receive_text()
                try:
                    msg = json.loads(msg_text)
                    if msg.get("type") == "subscribe_indicators":
                        active_indicators = msg.get("indicators", [])
                        print(f"🔄 Active indicators updated via WS: {[i.get('type') for i in active_indicators]}")
                except Exception as parse_err:
                    logging.warning(f"Error parsing ws message: {parse_err}")
        except (WebSocketDisconnect, asyncio.CancelledError):
            pass
        except Exception as e:
            logging.error(f"Error in receive_messages: {e}")

    try:
        print(f"📡 Original Stream Started for {exchange_id_lower} - {formatted_symbol}")

        ohlcv = await exchange.fetch_ohlcv(formatted_symbol, timeframe)
        all_candles = list(ohlcv) if ohlcv else []

        # send historical data 
        await websocket.send_json({
            "type":"history",
            "data": ohlcv,
            "symbol": symbol,
            "timeframe": timeframe
        })

        receive_task = asyncio.create_task(receive_messages())

        while True:
            try:
                # FETCH ORIGINAL LIVE CANDLE FROM EXCHANGE API
                latest_ohlcv = await exchange.fetch_ohlcv(formatted_symbol, timeframe, limit=2)
                
                if latest_ohlcv and len(latest_ohlcv) > 0:
                    for candle in latest_ohlcv:
                        c_time = candle[0]
                        if all_candles:
                            if c_time == all_candles[-1][0]:
                                all_candles[-1] = candle
                            elif c_time > all_candles[-1][0]:
                                all_candles.append(candle)
                                if len(all_candles) > 1000:
                                    all_candles = all_candles[-1000:]
                            elif len(all_candles) >= 2 and c_time == all_candles[-2][0]:
                                all_candles[-2] = candle
                        else:
                            all_candles.append(candle)

                    latest_candle = latest_ohlcv[-1]
                    
                    original_live_candle = {
                        "time": int(latest_candle[0] / 1000),  # Milliseconds to seconds
                        "open": float(latest_candle[1]),
                        "high": float(latest_candle[2]),
                        "low": float(latest_candle[3]),
                        "close": float(latest_candle[4]),
                        "volume": float(latest_candle[5])
                    }
                    
                    # Calculate live indicators using backend service
                    live_indicators = {}
                    if active_indicators and all_candles:
                        try:
                            live_indicators = calculate_live_indicators(all_candles, active_indicators)
                        except Exception as ind_err:
                            logging.error(f"Error calculating live indicators: {ind_err}")

                    # Stream it down the pipe to your React code
                    await websocket.send_json({
                        "type":"update",
                        "data":original_live_candle,
                        "indicators": live_indicators
                    })
                
                # Sleep sequence to match exchange pacing
                await asyncio.sleep(1)
                
            except WebSocketDisconnect:
                raise
            except Exception as inner_error:
                logging.error(f"Error fetching from exchange: {inner_error}")
                await asyncio.sleep(5) 
                
    except WebSocketDisconnect:
        print(f"❌ Client disconnected from stream: {exchange_id_lower} | {formatted_symbol}")
        
    finally:
        if receive_task and not receive_task.done():
            receive_task.cancel()
            try:
                await receive_task
            except asyncio.CancelledError:
                pass
        # Always close async connections cleanly to prevent memory leaks
        await exchange.close()
