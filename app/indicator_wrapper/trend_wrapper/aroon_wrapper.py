import pandas as pd
from app.services.chart_service import create_dataframe
from app.services.exchange_service import get_ohlcv
from app.indicators.trend_indicators.aroon import add_aroon
def get_aroon(exchange,symbol,timeframe,period,**kwargs):

    ohlcv = get_ohlcv(exchange,symbol,timeframe)
    df = create_dataframe(ohlcv)
    df = add_aroon(df, period)
    up = []
    down = []
    osc = []
    for _, row in df.iterrows():
    
        if not pd.isna(row[f"AROON_UP_{period}"]):
        
            up.append({
                "time": int(row["time"].timestamp()),
                "value": float(row[f"AROON_UP_{period}"])
            })
            down.append({
                "time": int(row["time"].timestamp()),
                "value": float(row[f"AROON_DOWN_{period}"])
            })
            osc.append({
                "time": int(row["time"].timestamp()),
                "value": float(row[f"AROON_OSC_{period}"])
            })

    return {
        "up": up,
        "down": down,
        "osc": osc
    }
