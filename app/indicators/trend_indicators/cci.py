from ta.trend import CCIIndicator

def add_cci(df, period=20):
    df[f"CCI_{period}"] = CCIIndicator(
        high=df["high"],
        low=df["low"],
        close=df["close"],
        window=period
    ).cci()

    return df