from ta.volatility import BollingerBands


def add_bollinger(
    df,
    period=20,
    std=2
):

    bb = BollingerBands(
        close=df["close"],
        window=period,
        window_dev=std
    )

    df["BB_UPPER"] = bb.bollinger_hband()
    df["BB_MIDDLE"] = bb.bollinger_mavg()
    df["BB_LOWER"] = bb.bollinger_lband()

    return df