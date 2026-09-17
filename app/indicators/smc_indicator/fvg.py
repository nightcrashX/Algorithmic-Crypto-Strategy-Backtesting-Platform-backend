import numpy as np


def add_fair_value_gap(df):
    """
    Detect Fair Value Gaps (FVG).

    Required Columns:
        open
        high
        low
        close

    Added Columns:
        BULLISH_FVG
        BEARISH_FVG
        FVG_TOP
        FVG_BOTTOM
        FVG_SIZE
    """

    df = df.copy()

    n = len(df)

    bullish = np.zeros(n, dtype=bool)
    bearish = np.zeros(n, dtype=bool)

    top = np.full(n, np.nan)
    bottom = np.full(n, np.nan)
    size = np.full(n, np.nan)

    for i in range(2, n):

        first_high = df["high"].iloc[i - 2]
        first_low = df["low"].iloc[i - 2]

        third_high = df["high"].iloc[i]
        third_low = df["low"].iloc[i]

        # -----------------------------
        # Bullish FVG
        # -----------------------------
        if first_high < third_low:

            bullish[i] = True

            top[i] = third_low
            bottom[i] = first_high
            size[i] = third_low - first_high

        # -----------------------------
        # Bearish FVG
        # -----------------------------
        elif first_low > third_high:

            bearish[i] = True

            top[i] = first_low
            bottom[i] = third_high
            size[i] = first_low - third_high

    df["BULLISH_FVG"] = bullish
    df["BEARISH_FVG"] = bearish

    df["FVG_TOP"] = top
    df["FVG_BOTTOM"] = bottom
    df["FVG_SIZE"] = size

    return df