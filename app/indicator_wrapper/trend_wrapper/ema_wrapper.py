import pandas as pd
from app.services.chart_service import create_dataframe
from app.services.exchange_service import get_ohlcv
from app.indicators.trend_indicators.ema import add_ema


def get_ema(exchange,symbol, timeframe, period,**kwargs):
    
   
    ohclv = get_ohlcv(exchange, symbol , timeframe)
 
    df = create_dataframe(ohclv)

    df = add_ema(df,period)

    ema_data = []

    for _, row in df.iterrows():
        if not pd.isna(row[f"EMA_{period}"]):
            ema_data.append({
                "time": int(row["time"].timestamp()),
                "value": float(row[f"EMA_{period}"])
            })

    return ema_data



