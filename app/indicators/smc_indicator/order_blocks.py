import numpy as np


def add_order_blocks(df, lookahead=5, breakout_threshold=0.005):
    """
    Detect Bullish & Bearish Order Blocks.

    Required Columns:
        open
        high
        low
        close

    Parameters
    ----------
    lookahead : int
        Number of future candles checked for breakout.

    breakout_threshold : float
        Minimum breakout percentage (0.005 = 0.5%)

    Added Columns
    -------------
        BULLISH_OB
        BEARISH_OB
        OB_HIGH
        OB_LOW
    """

    df = df.copy()

    n = len(df)

    bullish = np.zeros(n, dtype=bool)
    bearish = np.zeros(n, dtype=bool)

    ob_high = np.full(n, np.nan)
    ob_low = np.full(n, np.nan)

    for i in range(n - lookahead):

        open_price = df["open"].iloc[i]
        close_price = df["close"].iloc[i]

        high = df["high"].iloc[i]
        low = df["low"].iloc[i]

        future = df.iloc[i + 1:i + lookahead + 1]

        # --------------------------------------------------
        # Bullish Order Block
        # Last bearish candle before bullish breakout
        # --------------------------------------------------
        if close_price < open_price:

            breakout = future["high"].max()

            if breakout > high * (1 + breakout_threshold):

                bullish[i] = True
                ob_high[i] = high
                ob_low[i] = low

        # --------------------------------------------------
        # Bearish Order Block
        # Last bullish candle before bearish breakout
        # --------------------------------------------------
        elif close_price > open_price:

            breakout = future["low"].min()

            if breakout < low * (1 - breakout_threshold):

                bearish[i] = True
                ob_high[i] = high
                ob_low[i] = low

    df["BULLISH_OB"] = bullish
    df["BEARISH_OB"] = bearish

    df["OB_HIGH"] = ob_high
    df["OB_LOW"] = ob_low

    return df