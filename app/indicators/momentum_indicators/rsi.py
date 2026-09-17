from ta.momentum import RSIIndicator

def add_rsi(df, period=14):
    df["RSI"] = RSIIndicator(
        close=df["close"],
        window=period
    ).rsi()

    return df