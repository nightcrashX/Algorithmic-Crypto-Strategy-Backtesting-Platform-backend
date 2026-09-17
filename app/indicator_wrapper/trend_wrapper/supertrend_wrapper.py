import pandas as pd

from app.services.exchange_service import get_ohlcv
from app.services.chart_service import create_dataframe
from app.indicators.trend_indicators.supertrend import add_supertrend


def get_supertrend(
    exchange,
    symbol,
    timeframe,
    atr_period=10,
    multiplier=3,
    **kwargs
):

    ohlcv = get_ohlcv(exchange, symbol, timeframe)

    df = create_dataframe(ohlcv)

    df = add_supertrend(
        df,
        atr_period,
        multiplier
    )

    supertrend = []

    for _, row in df.iterrows():

        if not pd.isna(row["Supertrend"]):

            supertrend.append({
                "time": int(row["time"].timestamp()),
                "value": float(row["Supertrend"]),
                "trend": float(row["ST_Direction"])
            })

    return supertrend