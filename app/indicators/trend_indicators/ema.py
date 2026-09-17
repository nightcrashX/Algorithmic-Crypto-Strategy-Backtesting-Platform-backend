#ema.py

from ta.trend import EMAIndicator

def add_ema(df, period=20):
    df[f"EMA_{period}"] = EMAIndicator(df["close"], window=period).ema_indicator()
    return df 