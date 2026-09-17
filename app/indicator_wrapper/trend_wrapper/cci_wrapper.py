import pandas as pd
from app.services.chart_service import create_dataframe
from app.services.exchange_service import get_ohlcv
from app.indicators.trend_indicators.cci import add_cci

def get_cci(exchange,symbol,timeframe,period,**kwargs):

    ohlcv = get_ohlcv(exchange,symbol,timeframe)
    df = create_dataframe(ohlcv)
    df = add_cci(df, period)
    cci_data = []
    for _, row in df.iterrows():
        if not pd.isna(row[f"CCI_{period}"]):
            cci_data.append({
                "time": int(row["time"].timestamp()),
                "value": float(row[f"CCI_{period}"])
            })

    return cci_data