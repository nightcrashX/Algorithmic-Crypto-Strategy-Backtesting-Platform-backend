from fastapi import APIRouter, Query
import json
from app.services.exchange_service import (
    load_market,
    get_market_order_detail,
    get_ohlcv,
    get_ohlcv_paginated,
    get_ticker,
    get_exchange_list,
    get_trades,
)
from app.services.indicator_service import calculate_historical_indicators
from app.config import settings

exchange_router = APIRouter(prefix="/exchange",tags=['Exchange'])

@exchange_router.get("/dashboard/defaults")
def dashboard_defaults():
    return {
         "exchange": settings.DEFAULT_EXCHANGE,
        "symbol": settings.DEFAULT_SYMBOL,
        "timeframe": settings.DEFAULT_TIMEFRAME,
        "limit": settings.DEFAULT_LIMIT,
        "theme": settings.DEFAULT_THEME,
        "chart_type": settings.DEFAULT_CHART_TYPE
    }
@exchange_router.get("/exchange_list")
def exchange_list():
    return get_exchange_list()

@exchange_router.get("/symbols")
def get_symbol(exchange:str):
    return {
        "symbols":load_market(exchange)
    }

@exchange_router.get("/order_book")
def order(exchange:str,symbol):
    return {
        "orders":get_market_order_detail(exchange,symbol)
    }

@exchange_router.get("/ohlcv")
def ohlcv(
    exchange: str,
    symbol: str,
    timeframe: str,
    page: int = Query(1, ge=1),
    limit: int = Query(300, ge=1, le=1000),
    to_time: int | None = Query(None),
    indicators: str | None = Query(None)
):
    ind_list = []
    if indicators:
        try:
            ind_list = json.loads(indicators)
        except Exception:
            ind_list = []

    result = get_ohlcv_paginated(
        exchange_name=exchange,
        symbol=symbol,
        timeframe=timeframe,
        page=page,
        limit=limit,
        to_time=to_time
    )

    if ind_list and result.get("candles"):
        result["indicators"] = calculate_historical_indicators(
            result["candles"],
            ind_list
        )
    else:
        result["indicators"] = {}

    return result
    
@exchange_router.get("/ticker")
def ticker(exchange:str,symbol):
    return {
        "ticker data": get_ticker(exchange,symbol)
    }

@exchange_router.get("/trades")
def trade(exchange:str,symbol):
    return {
        "trades": get_trades(exchange,symbol)
    }