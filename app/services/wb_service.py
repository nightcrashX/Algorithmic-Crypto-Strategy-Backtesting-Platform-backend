from fastapi import APIRouter,WebSocketDisconnect
from fastapi import WebSocket 
import logging
import asyncio

from app.services.exchange_service import get_ohlcv

async def live_socket( ws:WebSocket ,exchange :str , symbol: str , timeframe: str ):
    await ws.accept()

    historical_data = get_ohlcv(exchange_name=exchange, symbol=symbol, timeframe=timeframe)
    # print(historical_data)

    try :
        print("websocket stream start ")
        await ws.send_json({
            "type":"history",
            "data":historical_data,
            "symbol": symbol,
            "timeframe": timeframe
        })
        formatted_symbol = symbol
        if "/" not in symbol and len(symbol) > 4:
            if symbol.endswith("USDT"):
                formatted_symbol = f"{symbol[:-4]}/USDT"
            elif symbol.endswith("BTC"):
                formatted_symbol = f"{symbol[:-3]}/BTC"

        while True:
            try:
                ohlcv = await get_ohlcv(symbol=symbol,timeframe=timeframe,limit=2)

                if ohlcv and len(ohlcv) > 0:
                    latest_candle = ohlcv[-1]
                    
                    original_live_candle = {
                        "time": int(latest_candle[0] / 1000),  # Milliseconds to seconds
                        "open": float(latest_candle[1]),
                        "high": float(latest_candle[2]),
                        "low": float(latest_candle[3]),
                        "close": float(latest_candle[4]),
                        "volume": float(latest_candle[5])
                    }
                    
                    # Stream it down the pipe to your React code
                    await ws.send_json({
                        "type":"update",
                        "data":original_live_candle
                    })

                await asyncio.sleep(1)

            except Exception as inner_error:
                logging.error(f"error fetching from exchange: {inner_error}")
                await asyncio.sleep(5)

    except WebSocketDisconnect:
        print(f" client disconnected from stream : {exchange} | {symbol}")



