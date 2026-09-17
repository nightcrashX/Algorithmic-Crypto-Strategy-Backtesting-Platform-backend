from ta.trend import MACD


def add_macd(
    df,
    fast=12,
    slow=26,
    signal=9
):

    macd = MACD(
        close=df["close"],
        window_fast=fast,
        window_slow=slow,
        window_sign=signal
    )

    df["MACD"] = macd.macd()
    df["MACD_SIGNAL"] = macd.macd_signal()
    df["MACD_HIST"] = macd.macd_diff()

    return df