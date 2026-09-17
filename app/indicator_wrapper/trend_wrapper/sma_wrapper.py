import pandas as pd
from app.services.chart_service import create_dataframe
from app.services.exchange_service import get_ohlcv
from app.indicators.trend_indicators.sma import add_sma

def get_sma(exchange,symbol,timeframe,period,**kwargs):

    ohlcv = get_ohlcv(exchange,symbol,timeframe)
    df = create_dataframe(ohlcv)
    df = add_sma(df, period)
    sma_data = []
    for _, row in df.iterrows():
        if not pd.isna(row[f"SMA_{period}"]):
            sma_data.append({
                "time": int(row["time"].timestamp()),
                "value": float(row[f"SMA_{period}"])
            })

    return sma_data