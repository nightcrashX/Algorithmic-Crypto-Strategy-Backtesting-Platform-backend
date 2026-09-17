import pandas as pd

from app.services.exchange_service import get_ohlcv
from app.services.chart_service import create_dataframe
from app.indicators.momentum_indicators.roc import add_roc


def get_roc(
    exchange,
    symbol,
    timeframe,
    period=12,
    **kwargs
):

    ohlcv = get_ohlcv(exchange, symbol, timeframe)

    df = create_dataframe(ohlcv)

    df = add_roc(
        df,
        period
    )

    roc_data = []

    for _, row in df.iterrows():

        if not pd.isna(row["ROC"]):

            roc_data.append({
                "time": int(row["time"].timestamp()),
                "value": float(row["ROC"])
            })

    return roc_data