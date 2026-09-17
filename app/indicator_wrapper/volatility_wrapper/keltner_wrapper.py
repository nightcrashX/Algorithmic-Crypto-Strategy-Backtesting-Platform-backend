import pandas as pd

from app.services.exchange_service import get_ohlcv
from app.services.chart_service import create_dataframe
from app.indicators.volatility_indicators.keltner import add_keltner


def get_keltner(
    exchange,
    symbol,
    timeframe,
    period=20,
    atr_period=10,
    multiplier=2,
    **kwargs
):

    ohlcv = get_ohlcv(exchange, symbol, timeframe)

    df = create_dataframe(ohlcv)

    df = add_keltner(
        df,
        period,
        atr_period,
        multiplier
    )

    upper = []
    middle = []
    lower = []

    for _, row in df.iterrows():

        if (
            not pd.isna(row["KC_UPPER"]) and
            not pd.isna(row["KC_MIDDLE"]) and
            not pd.isna(row["KC_LOWER"])
        ):

            time = int(row["time"].timestamp())

            upper.append({"time": time, "value": float(row["KC_UPPER"])})
            middle.append({"time": time, "value": float(row["KC_MIDDLE"])})
            lower.append({"time": time, "value": float(row["KC_LOWER"])})

    return {
        "UPPER": upper,
        "MIDDLE": middle,
        "LOWER": lower
    }