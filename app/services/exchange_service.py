#backend/services/exchange_service.py
import ccxt as ct
from fastapi import HTTPException,status
from app.config.settings import DEFAULT_LIMIT
import time



def get_exchange(exchange_name:str):    #y object return krega jaise ccxt.binance()

    exchange_name = exchange_name.lower().strip()   # ct.exchanges ke andr sare exchange lower me hote h isliye isko lower me convert kiya h 

    if not hasattr(ct,exchange_name):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid exchange")
    
    exchange_class = getattr(ct,exchange_name)({'enableRateLimit': True})   # getattr ik class return krta h 

    exchange = exchange_class
    
    return exchange
    

def get_exchange_list():

    bad_exchange_id = ['aftermath','alpaca']
    active_exchanges = [ex for ex in ct.exchanges if ex not in bad_exchange_id]

    return sorted(active_exchanges) # y list return krega sare exchnges ki

def load_market(exchange_name:str):

    exchange = get_exchange(exchange_name)
    get_data = exchange.load_markets()
    return list(get_data.keys())

def get_market_order_detail(exchange_name:str, symbol):

    exchange = get_exchange(exchange_name)
    orders= exchange.fetch_order_book(symbol)
    return orders

def get_ohlcv_paginated(
    exchange_name: str,
    symbol: str,
    timeframe: str,
    page: int = 1,
    limit: int = 300,
    to_time: int | None = None
):
    exchange = get_exchange(exchange_name)

    formatted_symbol = symbol
    if "/" not in symbol and len(symbol) > 4:
        if symbol.endswith("USDT"):
            formatted_symbol = f"{symbol[:-4]}/USDT"
        elif symbol.endswith("BTC"):
            formatted_symbol = f"{symbol[:-3]}/BTC"

    tf_seconds = 60
    if hasattr(exchange, 'parse_timeframe'):
        try:
            tf_seconds = exchange.parse_timeframe(timeframe)
        except Exception:
            tf_seconds = 60

    now_ms = exchange.milliseconds()

    if to_time is not None:
        to_time_ms = int(to_time * 1000)
        since_ms = max(0, to_time_ms - (limit * tf_seconds * 1000))
    else:
        # Page 1 = most recent 'limit' candles
        # Page 2 = previous 'limit' candles, etc.
        since_ms = max(0, now_ms - (page * limit * tf_seconds * 1000))

    try:
        raw_candles = exchange.fetch_ohlcv(
            formatted_symbol,
            timeframe,
            since=since_ms if page > 1 or to_time is not None else None,
            limit=limit
        )
    except Exception as e:
        print(f"⚠️ Error fetching ohlcv from {exchange_name}: {e}")
        raw_candles = []

    candles = []
    for c in raw_candles:
        c_time = int(c[0] // 1000)
        if to_time is not None and c_time >= to_time:
            continue
        candles.append({
            "time": c_time,
            "open": float(c[1]),
            "high": float(c[2]),
            "low": float(c[3]),
            "close": float(c[4]),
            "volume": float(c[5]),
        })

    has_more = len(candles) > 0 and since_ms > 0
    next_page = (page + 1) if has_more else None

    return {
        "success": True,
        "data": candles,
        "candles": candles,
        "pagination": {
            "page": page,
            "limit": limit,
            "has_more": has_more,
            "next_page": next_page,
            "oldest_timestamp": candles[0]["time"] if candles else None,
            "newest_timestamp": candles[-1]["time"] if candles else None,
        }
    }

def get_ohlcv(
    exchange_name: str,
    symbol: str,
    timeframe: str,
    limit: int = 500
):
    exchange = get_exchange(exchange_name)

    formatted_symbol = symbol
    if "/" not in symbol and len(symbol) > 4:
        if symbol.endswith("USDT"):
            formatted_symbol = f"{symbol[:-4]}/USDT"
        elif symbol.endswith("BTC"):
            formatted_symbol = f"{symbol[:-3]}/BTC"

    candles = exchange.fetch_ohlcv(
        formatted_symbol,
        timeframe,
        limit=limit
    )

    return [
        {
            "time": candle[0] // 1000,
            "open": float(candle[1]),
            "high": float(candle[2]),
            "low": float(candle[3]),
            "close": float(candle[4]),
            "volume": float(candle[5]),
        }
        for candle in candles
    ]

def get_ticker(exchange_name:str,symbol):

    exchange = get_exchange(exchange_name)
    ticker = exchange.fetch_ticker(symbol)

    return ticker

def get_trades(exchange_name:str,symbol):
    
    exchange = get_exchange(exchange_name)
    trade = exchange.fetch_trades(symbol)

