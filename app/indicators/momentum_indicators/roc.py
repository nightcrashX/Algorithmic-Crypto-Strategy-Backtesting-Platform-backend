from ta.momentum import ROCIndicator

def add_roc(df, period=12):
    df["ROC"] = ROCIndicator(
        close=df["close"],
        window=period
    ).roc()

    return df