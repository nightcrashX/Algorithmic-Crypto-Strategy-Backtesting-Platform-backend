from ta.volume import AccDistIndexIndicator

def add_ad(df):
    df["AD"] = AccDistIndexIndicator(
        high=df["high"],
        low=df["low"],
        close=df["close"],
        volume=df["volume"]
    ).acc_dist_index()

    return df