import pandas as pd
from app.services.chart_service import create_dataframe
from app.services.exchange_service import get_ohlcv
from app.indicators.trend_indicators.adx import add_adx

def get_adx(exchange,symbol,timeframe,period,**kwargs):

    ohlcv = get_ohlcv(exchange,symbol,timeframe)
    df = create_dataframe(ohlcv)
    df = add_adx(df, period)
    adx_data = []
    for _, row in df.iterrows():
        if not pd.isna(row[f"ADX_{period}"]):
            adx_data.append({
                "time": int(row["time"].timestamp()),
                "value": float(row[f"ADX_{period}"])
            })

    return adx_data

   