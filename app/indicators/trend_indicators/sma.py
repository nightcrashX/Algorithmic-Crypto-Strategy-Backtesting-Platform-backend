from ta.trend import SMAIndicator

def add_sma(df, period=20):
    df[f"SMA_{period}"] = SMAIndicator(df["close"], window=period).sma_indicator()
    return df