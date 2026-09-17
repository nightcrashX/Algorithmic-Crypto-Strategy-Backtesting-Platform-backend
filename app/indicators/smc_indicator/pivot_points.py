import pandas as pd


def add_pivot_points(df):
    """
    Adds Classic Pivot Points.

    Required Columns:
        high
        low
        close

    Added Columns:
        Pivot
        R1
        R2
        R3
        S1
        S2
        S3
    """

    df = df.copy()

    # Previous Candle Values
    prev_high = df["high"].shift(1)
    prev_low = df["low"].shift(1)
    prev_close = df["close"].shift(1)

    # Pivot
    pivot = (prev_high + prev_low + prev_close) / 3

    # Resistance
    r1 = (2 * pivot) - prev_low
    r2 = pivot + (prev_high - prev_low)
    r3 = prev_high + 2 * (pivot - prev_low)

    # Support
    s1 = (2 * pivot) - prev_high
    s2 = pivot - (prev_high - prev_low)
    s3 = prev_low - 2 * (prev_high - pivot)

    df["Pivot"] = pivot
    df["R1"] = r1
    df["R2"] = r2
    df["R3"] = r3

    df["S1"] = s1
    df["S2"] = s2
    df["S3"] = s3

    return df
