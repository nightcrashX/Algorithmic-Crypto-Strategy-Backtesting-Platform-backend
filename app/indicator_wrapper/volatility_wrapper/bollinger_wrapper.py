import pandas as pd

from app.services.exchange_service import get_ohlcv
from app.services.chart_service import create_dataframe
from app.indicators.volatility_indicators.bollinger_bands import add_bollinger


def get_bollinger(
    exchange,
    symbol,
    timeframe,
    period=20,
    std=2,
    **kwargs
):

    ohlcv = get_ohlcv(exchange, symbol, timeframe)

    df = create_dataframe(ohlcv)

    df = add_bollinger(
        df,
        period,
        std
    )

    upper = []
    middle = []
    lower = []

    for _, row in df.iterrows():

        if (
            not pd.isna(row["BB_UPPER"]) and
            not pd.isna(row["BB_MIDDLE"]) and
            not pd.isna(row["BB_LOWER"])
        ):

            time = int(row["time"].timestamp())

            upper.append({"time": time, "value": float(row["BB_UPPER"])})
            middle.append({"time": time, "value": float(row["BB_MIDDLE"])})
            lower.append({"time": time, "value": float(row["BB_LOWER"])})

    return {
        "UPPER": upper,
        "MIDDLE": middle,
        "LOWER": lower
    }