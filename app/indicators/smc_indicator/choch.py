import numpy as np


def add_choch(df, swing_length=5):
    """
    Detect Change of Character (CHOCH).

    Required Columns:
        high
        low
        close

    Added Columns:
        SWING_HIGH
        SWING_LOW
        BULLISH_CHOCH
        BEARISH_CHOCH
        TREND
    """

    df = df.copy()

    n = len(df)

    swing_high = np.zeros(n, dtype=bool)
    swing_low = np.zeros(n, dtype=bool)

    bullish_choch = np.zeros(n, dtype=bool)
    bearish_choch = np.zeros(n, dtype=bool)

    last_swing_high = np.nan
    last_swing_low = np.nan

    # -----------------------------------
    # Detect Swing High / Swing Low
    # -----------------------------------
    for i in range(swing_length, n - swing_length):

        if (
            df["high"].iloc[i]
            >
            df["high"].iloc[i-swing_length:i].max()
            and
            df["high"].iloc[i]
            >
            df["high"].iloc[i+1:i+swing_length+1].max()
        ):
            swing_high[i] = True

        if (
            df["low"].iloc[i]
            <
            df["low"].iloc[i-swing_length:i].min()
            and
            df["low"].iloc[i]
            <
            df["low"].iloc[i+1:i+swing_length+1].min()
        ):
            swing_low[i] = True

    trend = 0
    # 1 = Bullish
    # -1 = Bearish

    for i in range(n):

        if swing_high[i]:
            last_swing_high = df["high"].iloc[i]

        if swing_low[i]:
            last_swing_low = df["low"].iloc[i]

        # -----------------------------
        # Bullish CHOCH
        # Previous trend was bearish
        # -----------------------------
        if (
            trend == -1
            and
            not np.isnan(last_swing_high)
            and
            df["close"].iloc[i] > last_swing_high
        ):
            bullish_choch[i] = True
            trend = 1

        # -----------------------------
        # Bearish CHOCH
        # Previous trend was bullish
        # -----------------------------
        elif (
            trend == 1
            and
            not np.isnan(last_swing_low)
            and
            df["close"].iloc[i] < last_swing_low
        ):
            bearish_choch[i] = True
            trend = -1

        # -----------------------------
        # Initialize Trend
        # -----------------------------
        elif trend == 0:

            if (
                not np.isnan(last_swing_high)
                and
                df["close"].iloc[i] > last_swing_high
            ):
                trend = 1

            elif (
                not np.isnan(last_swing_low)
                and
                df["close"].iloc[i] < last_swing_low
            ):
                trend = -1

    df["SWING_HIGH"] = swing_high
    df["SWING_LOW"] = swing_low

    df["BULLISH_CHOCH"] = bullish_choch
    df["BEARISH_CHOCH"] = bearish_choch

    df["TREND"] = trend

    return df