import pandas as pd

from app.services.exchange_service import get_ohlcv
from app.services.chart_service import create_dataframe
from app.indicators.momentum_indicators.rsi import add_rsi


def get_rsi(
    exchange,
    symbol,
    timeframe,
    period=14,
    **kwargs
):

    ohlcv = get_ohlcv(exchange, symbol, timeframe)

    df = create_dataframe(ohlcv)

    df = add_rsi(
        df,
        period
    )

    rsi_data = []

    for _, row in df.iterrows():

        if not pd.isna(row["RSI"]):

            rsi_data.append({
                "time": int(row["time"].timestamp()),
                "value": float(row["RSI"])
            })

    return rsi_data