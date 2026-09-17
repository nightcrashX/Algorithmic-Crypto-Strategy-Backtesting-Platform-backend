import pandas as pd

from app.services.exchange_service import get_ohlcv
from app.services.chart_service import create_dataframe
from app.indicators.volatility_indicators.atr import add_atr


def get_atr(
    exchange,
    symbol,
    timeframe,
    period=14,
    **kwargs
):

    ohlcv = get_ohlcv(exchange, symbol, timeframe)

    df = create_dataframe(ohlcv)

    df = add_atr(
        df,
        period
    )

    atr_data = []

    for _, row in df.iterrows():

        if not pd.isna(row["ATR"]):

            atr_data.append({
                "time": int(row["time"].timestamp()),
                "value": float(row["ATR"])
            })

    return atr_data