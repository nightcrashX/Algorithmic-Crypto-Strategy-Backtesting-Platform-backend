import pandas as pd

from app.services.exchange_service import get_ohlcv
from app.services.chart_service import create_dataframe
from app.indicators.volume_indicators.vwap import add_vwap


def get_vwap(
    exchange,
    symbol,
    timeframe,
    **kwargs
):

    ohlcv = get_ohlcv(exchange, symbol, timeframe)

    df = create_dataframe(ohlcv)

    # Your VWAP implementation expects timestamp
    df["timestamp"] = df["time"]

    df = add_vwap(df)

    vwap_data = []

    for _, row in df.iterrows():

        if not pd.isna(row["VWAP"]):

            vwap_data.append({
                "time": int(row["time"].timestamp()),
                "value": float(row["VWAP"])
            })

    return vwap_data