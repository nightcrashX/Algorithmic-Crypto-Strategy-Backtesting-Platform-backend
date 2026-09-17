import pandas as pd

from app.services.exchange_service import get_ohlcv
from app.services.chart_service import create_dataframe
from app.indicators.momentum_indicators.williams_r import add_williams_r


def get_williams_r(
    exchange,
    symbol,
    timeframe,
    period=14,
    **kwargs
):

    ohlcv = get_ohlcv(exchange, symbol, timeframe)

    df = create_dataframe(ohlcv)

    df = add_williams_r(
        df,
        period
    )

    williams_data = []

    for _, row in df.iterrows():

        if not pd.isna(row["WILLIAMS_R"]):

            williams_data.append({
                "time": int(row["time"].timestamp()),
                "value": float(row["WILLIAMS_R"])
            })

    return williams_data