import pandas as pd

from app.services.exchange_service import get_ohlcv
from app.services.chart_service import create_dataframe
from app.indicators.volatility_indicators.donchian import add_donchian


def get_donchian(
    exchange,
    symbol,
    timeframe,
    period=20,
    **kwargs
):

    ohlcv = get_ohlcv(exchange, symbol, timeframe)

    df = create_dataframe(ohlcv)

    df = add_donchian(
        df,
        period
    )

    upper = []
    middle = []
    lower = []

    for _, row in df.iterrows():

        if (
            not pd.isna(row["DC_UPPER"]) and
            not pd.isna(row["DC_MIDDLE"]) and
            not pd.isna(row["DC_LOWER"])
        ):

            time = int(row["time"].timestamp())

            upper.append({"time": time, "value": float(row["DC_UPPER"])})
            middle.append({"time": time, "value": float(row["DC_MIDDLE"])})
            lower.append({"time": time, "value": float(row["DC_LOWER"])})

    return {
        "UPPER": upper,
        "MIDDLE": middle,
        "LOWER": lower
    }
    