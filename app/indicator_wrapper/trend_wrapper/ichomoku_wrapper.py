import pandas as pd

from app.services.chart_service import create_dataframe
from app.services.exchange_service import get_ohlcv
from app.indicators.trend_indicators.ichimoku import add_ichimoku


def get_ichimoku(exchange,symbol,timeframe,conversion=9,base=26,span_b=52,**kwargs):

    ohlcv = get_ohlcv(exchange, symbol, timeframe)

    df = create_dataframe(ohlcv)

    df = add_ichimoku(df, conversion, base, span_b)

    tenkan = []
    kijun = []
    senkou_a = []
    senkou_b = []

    for _, row in df.iterrows():

        if (
            not pd.isna(row["TENKAN"]) and
            not pd.isna(row["KIJUN"]) and
            not pd.isna(row["SENKOU_A"]) and
            not pd.isna(row["SENKOU_B"])
        ):

            tenkan.append({
                "time": int(row["time"].timestamp()),
                "value": float(row["TENKAN"])
            })

            kijun.append({
                "time": int(row["time"].timestamp()),
                "value": float(row["KIJUN"])
            })

            senkou_a.append({
                "time": int(row["time"].timestamp()),
                "value": float(row["SENKOU_A"])
            })

            senkou_b.append({
                "time": int(row["time"].timestamp()),
                "value": float(row["SENKOU_B"])
            })

    return {
        "TENKAN": tenkan,
        "KIJUN": kijun,
        "SENKOU_A": senkou_a,
        "SENKOU_B": senkou_b
    }