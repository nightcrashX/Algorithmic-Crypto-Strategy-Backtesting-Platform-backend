import pandas as pd

from app.services.exchange_service import get_ohlcv
from app.services.chart_service import create_dataframe
from app.indicators.momentum_indicators.stochastic import add_stochastic


def get_stochastic(
    exchange,
    symbol,
    timeframe,
    period=14,
    smooth_k=3,
    smooth_d=3,
    **kwargs
):

    ohlcv = get_ohlcv(exchange, symbol, timeframe)

    df = create_dataframe(ohlcv)

    df = add_stochastic(
        df,
        period,
        smooth_k,
        smooth_d
    )

    k_line = []
    d_line = []

    for _, row in df.iterrows():

        if (
            not pd.isna(row["STOCH_K"]) and
            not pd.isna(row["STOCH_D"])
        ):

            time = int(row["time"].timestamp())

            k_line.append({
                "time": time,
                "value": float(row["STOCH_K"])
            })

            d_line.append({
                "time": time,
                "value": float(row["STOCH_D"])
            })

    return {
        "K": k_line,
        "D": d_line
    }