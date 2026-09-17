from ta.momentum import WilliamsRIndicator


def add_williams_r(
    df,
    period=14
):

    df["WILLIAMS_R"] = WilliamsRIndicator(
        high=df["high"],
        low=df["low"],
        close=df["close"],
        lbp=period
    ).williams_r()

    return df