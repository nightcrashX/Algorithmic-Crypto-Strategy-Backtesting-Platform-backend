import numpy as np
import pandas as pd
from ta.volatility import AverageTrueRange


def add_supertrend(df, atr_period=10, multiplier=3):
    """
    Adds Supertrend indicator to DataFrame.

    Required Columns:
        open, high, low, close

    Added Columns:
        ATR
        Supertrend
        ST_Direction (1 = Bullish, -1 = Bearish)
    """

    df = df.copy()

    # ATR
    atr = AverageTrueRange(
        high=df["high"],
        low=df["low"],
        close=df["close"],
        window=atr_period
    )

    df["ATR"] = atr.average_true_range()

    # Basic Bands
    hl2 = (df["high"] + df["low"]) / 2

    upperband = hl2 + (multiplier * df["ATR"])
    lowerband = hl2 - (multiplier * df["ATR"])

    final_upperband = upperband.copy()
    final_lowerband = lowerband.copy()

    # Trend Arrays
    supertrend = np.zeros(len(df))
    direction = np.ones(len(df))

    for i in range(1, len(df)):

        # Final Upper Band
        if (
            upperband.iloc[i] < final_upperband.iloc[i - 1]
            or df["close"].iloc[i - 1] > final_upperband.iloc[i - 1]
        ):
            final_upperband.iloc[i] = upperband.iloc[i]
        else:
            final_upperband.iloc[i] = final_upperband.iloc[i - 1]

        # Final Lower Band
        if (
            lowerband.iloc[i] > final_lowerband.iloc[i - 1]
            or df["close"].iloc[i - 1] < final_lowerband.iloc[i - 1]
        ):
            final_lowerband.iloc[i] = lowerband.iloc[i]
        else:
            final_lowerband.iloc[i] = final_lowerband.iloc[i - 1]

        # Trend Detection
        if supertrend[i - 1] == final_upperband.iloc[i - 1]:

            if df["close"].iloc[i] <= final_upperband.iloc[i]:
                supertrend[i] = final_upperband.iloc[i]
                direction[i] = -1
            else:
                supertrend[i] = final_lowerband.iloc[i]
                direction[i] = 1

        else:

            if df["close"].iloc[i] >= final_lowerband.iloc[i]:
                supertrend[i] = final_lowerband.iloc[i]
                direction[i] = 1
            else:
                supertrend[i] = final_upperband.iloc[i]
                direction[i] = -1

    df["Supertrend"] = supertrend
    df["ST_Direction"] = direction

    return df