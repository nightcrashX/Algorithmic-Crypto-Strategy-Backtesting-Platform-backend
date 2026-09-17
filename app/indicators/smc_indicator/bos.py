import numpy as np


def add_bos(df, swing_length=5):
    """
    Detect Break of Structure (BOS).

    Required Columns:
        high
        low
        close

    Parameters
    ----------
    swing_length : int
        Number of candles on each side used to identify swing points.

    Added Columns
    -------------
        SWING_HIGH
        SWING_LOW
        BULLISH_BOS
        BEARISH_BOS
    """

    df = df.copy()

    n = len(df)

    swing_high = np.zeros(n, dtype=bool)
    swing_low = np.zeros(n, dtype=bool)

    bullish_bos = np.zeros(n, dtype=bool)
    bearish_bos = np.zeros(n, dtype=bool)

    last_swing_high = np.nan
    last_swing_low = np.nan

    # -----------------------------------
    # Detect Swing Highs & Swing Lows
    # -----------------------------------
    for i in range(swing_length, n - swing_length):

        current_high = df["high"].iloc[i]
        current_low = df["low"].iloc[i]

        left_high = df["high"].iloc[i - swing_length:i]
        right_high = df["high"].iloc[i + 1:i + swing_length + 1]

        left_low = df["low"].iloc[i - swing_length:i]
        right_low = df["low"].iloc[i + 1:i + swing_length + 1]

        if (
            current_high > left_high.max()
            and current_high > right_high.max()
        ):
            swing_high[i] = True

        if (
            current_low < left_low.min()
            and current_low < right_low.min()
        ):
            swing_low[i] = True

    # -----------------------------------
    # Detect BOS
    # -----------------------------------
    for i in range(n):

        if swing_high[i]:
            last_swing_high = df["high"].iloc[i]

        if swing_low[i]:
            last_swing_low = df["low"].iloc[i]

        if (
            not np.isnan(last_swing_high)
            and df["close"].iloc[i] > last_swing_high
        ):
            bullish_bos[i] = True

        if (
            not np.isnan(last_swing_low)
            and df["close"].iloc[i] < last_swing_low
        ):
            bearish_bos[i] = True

    df["SWING_HIGH"] = swing_high
    df["SWING_LOW"] = swing_low

    df["BULLISH_BOS"] = bullish_bos
    df["BEARISH_BOS"] = bearish_bos

    return df