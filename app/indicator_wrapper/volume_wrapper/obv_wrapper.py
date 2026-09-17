import pandas as pd

from app.services.exchange_service import get_ohlcv
from app.services.chart_service import create_dataframe
from app.indicators.volume_indicators.obv import add_obv


def get_obv(
    exchange,
    symbol,
    timeframe,
    **kwargs
):

    ohlcv = get_ohlcv(exchange, symbol, timeframe)

    df = create_dataframe(ohlcv)

    df = add_obv(df)

    obv_data = []

    for _, row in df.iterrows():

        if not pd.isna(row["OBV"]):

            obv_data.append({
                "time": int(row["time"].timestamp()),
                "value": float(row["OBV"])
            })

    return obv_data