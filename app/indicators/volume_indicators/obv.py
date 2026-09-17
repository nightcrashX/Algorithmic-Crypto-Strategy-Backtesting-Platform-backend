from ta.volume import OnBalanceVolumeIndicator

def add_obv(df):
    df["OBV"] = OnBalanceVolumeIndicator(
        close=df["close"],
        volume=df["volume"]
    ).on_balance_volume()

    return df