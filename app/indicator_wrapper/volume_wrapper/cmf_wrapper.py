import pandas as pd

from app.services.exchange_service import get_ohlcv
from app.services.chart_service import create_dataframe
from app.indicators.volume_indicators.cmf import add_cmf


def get_cmf(
    exchange,
    symbol,
    timeframe,
    period=20,
    **kwargs
):

    ohlcv = get_ohlcv(exchange, symbol, timeframe)

    df = create_dataframe(ohlcv)

    df = add_cmf(
        df,
        period
    )

    cmf_data = []

    for _, row in df.iterrows():

        if not pd.isna(row["CMF"]):

            cmf_data.append({
                "time": int(row["time"].timestamp()),
                "value": float(row["CMF"])
            })

    return cmf_data