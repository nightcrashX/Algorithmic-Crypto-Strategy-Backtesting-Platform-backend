from ta.volume import MFIIndicator

def add_mfi(df,period=14):
    df["MFI"] = MFIIndicator(
        high=df["high"],
        low=df["low"],
        close=df["close"],
        volume=df["volume"],
        window=period
    ).money_flow_index()

    return df