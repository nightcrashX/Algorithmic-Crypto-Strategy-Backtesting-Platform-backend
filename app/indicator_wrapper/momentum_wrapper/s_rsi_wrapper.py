import pandas as pd

from app.services.exchange_service import get_ohlcv
from app.services.chart_service import create_dataframe
from app.indicators.momentum_indicators.stoch_rsi import add_stoch_rsi


def get_stoch_rsi(
    exchange,
    symbol,
    timeframe,
    rsi_period=14,
    stoch_period=14,
    k=3,
    d=3,
    **kwargs
):

    ohlcv = get_ohlcv(exchange, symbol, timeframe)

    df = create_dataframe(ohlcv)

    df = add_stoch_rsi(
        df,
        rsi_period,
        stoch_period,
        k,
        d
    )

    stoch_rsi = []
    k_line = []
    d_line = []

    for _, row in df.iterrows():

        if (
            not pd.isna(row["STOCH_RSI"]) and
            not pd.isna(row["STOCH_RSI_K"]) and
            not pd.isna(row["STOCH_RSI_D"])
        ):

            time = int(row["time"].timestamp())

            stoch_rsi.append({
                "time": time,
                "value": float(row["STOCH_RSI"])
            })

            k_line.append({
                "time": time,
                "value": float(row["STOCH_RSI_K"])
            })

            d_line.append({
                "time": time,
                "value": float(row["STOCH_RSI_D"])
            })

    return {
        "STOCH_RSI": stoch_rsi,
        "K": k_line,
        "D": d_line
    }