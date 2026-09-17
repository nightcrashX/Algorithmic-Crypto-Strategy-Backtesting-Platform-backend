import pandas as pd


def add_fibonacci(df, lookback=100):
    """
    Adds Fibonacci Retracement Levels.

    Required Columns:
        high
        low

    Parameters
    ----------
    lookback : int
        Number of candles used to find swing high/low.

    Added Columns
    -------------
        FIB_0
        FIB_23_6
        FIB_38_2
        FIB_50
        FIB_61_8
        FIB_78_6
        FIB_100
    """

    df = df.copy()

    swing_high = df["high"].rolling(lookback).max()
    swing_low = df["low"].rolling(lookback).min()

    diff = swing_high - swing_low

    df["FIB_0"] = swing_high
    df["FIB_23_6"] = swing_high - (0.236 * diff)
    df["FIB_38_2"] = swing_high - (0.382 * diff)
    df["FIB_50"] = swing_high - (0.500 * diff)
    df["FIB_61_8"] = swing_high - (0.618 * diff)
    df["FIB_78_6"] = swing_high - (0.786 * diff)
    df["FIB_100"] = swing_low

    return df