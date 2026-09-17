import pandas as pd

from app.services.exchange_service import get_ohlcv
from app.services.chart_service import create_dataframe
from app.indicators.trend_indicators.psar import add_psar


def get_psar(
    exchange,
    symbol,
    timeframe,
    step=0.02,
    max_step=0.2,
    **kwargs
):

    ohlcv = get_ohlcv(exchange, symbol, timeframe)

    df = create_dataframe(ohlcv)

    df = add_psar(
        df,
        step,
        max_step
    )

    psar_data = []

    for _, row in df.iterrows():

        if not pd.isna(row["PSAR"]):

            psar_data.append({
                "time": int(row["time"].timestamp()),
                "value": float(row["PSAR"])
            })

    return psar_data