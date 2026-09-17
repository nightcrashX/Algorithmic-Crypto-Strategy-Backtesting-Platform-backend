import pandas as pd

from app.services.exchange_service import get_ohlcv
from app.services.chart_service import create_dataframe
from app.indicators.volume_indicators.ad import add_ad


def get_ad(
    exchange,
    symbol,
    timeframe,
    **kwargs
):

    ohlcv = get_ohlcv(exchange, symbol, timeframe)

    df = create_dataframe(ohlcv)

    df = add_ad(df)

    ad_data = []

    for _, row in df.iterrows():

        if not pd.isna(row["AD"]):

            ad_data.append({
                "time": int(row["time"].timestamp()),
                "value": float(row["AD"])
            })

    return ad_data