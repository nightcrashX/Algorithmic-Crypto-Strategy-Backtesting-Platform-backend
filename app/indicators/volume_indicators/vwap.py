import pandas as pd


def add_vwap(df):
    """
    Adds VWAP (Volume Weighted Average Price) to DataFrame.

    Required Columns:
        high, low, close, volume

    Optional:
        timestamp (datetime) -> VWAP resets each trading day

    Added Columns:
        VWAP
    """

    df = df.copy()

    # Typical Price
    tp = (df["high"] + df["low"] + df["close"]) / 3

    # Reset VWAP each day if timestamp exists
    if "timestamp" in df.columns:

        df["timestamp"] = pd.to_datetime(df["timestamp"])
        day = df["timestamp"].dt.date

        cumulative_tpv = (tp * df["volume"]).groupby(day).cumsum()
        cumulative_volume = df["volume"].groupby(day).cumsum()

    else:
        cumulative_tpv = (tp * df["volume"]).cumsum()
        cumulative_volume = df["volume"].cumsum()

    df["VWAP"] = cumulative_tpv / cumulative_volume

    return df