import pandas as pd

from app.services.exchange_service import get_ohlcv
from app.services.chart_service import create_dataframe
from app.indicators.volume_indicators.mfi import add_mfi


def get_mfi(
    exchange,
    symbol,
    timeframe,
    period=14,
    **kwargs
):

    ohlcv = get_ohlcv(exchange, symbol, timeframe)

    df = create_dataframe(ohlcv)

    df = add_mfi(
        df,
        period
    )

    mfi_data = []

    for _, row in df.iterrows():

        if not pd.isna(row["MFI"]):

            mfi_data.append({
                "time": int(row["time"].timestamp()),
                "value": float(row["MFI"])
            })

    return mfi_data