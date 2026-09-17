import pandas as pd

from app.services.chart_service import create_dataframe
from app.services.exchange_service import get_ohlcv
from app.indicators.trend_indicators.macd import add_macd


def get_macd(
    exchange,
    symbol,
    timeframe,
    fast=12,
    slow=26,
    signal=9,
    **kwargs
):

    ohlcv = get_ohlcv(exchange, symbol, timeframe)

    df = create_dataframe(ohlcv)

    df = add_macd(
        df,
        fast,
        slow,
        signal
    )

    macd_data = []
    signal_data = []
    histogram_data = []

    for _, row in df.iterrows():

        if (
            not pd.isna(row["MACD"]) and
            not pd.isna(row["MACD_SIGNAL"]) and
            not pd.isna(row["MACD_HIST"])
        ):

            time = int(row["time"].timestamp())

            macd_data.append({
                "time": time,
                "value": float(row["MACD"])
            })

            signal_data.append({
                "time": time,
                "value": float(row["MACD_SIGNAL"])
            })

            histogram_data.append({
                "time": time,
                "value": float(row["MACD_HIST"])
            })

    return {
        "MACD": macd_data,
        "SIGNAL": signal_data,
        "HISTOGRAM": histogram_data
    }