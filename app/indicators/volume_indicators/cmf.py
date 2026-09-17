from ta.volume import ChaikinMoneyFlowIndicator


def add_cmf(
    df,
    period=20
):

    df["CMF"] = ChaikinMoneyFlowIndicator(
        high=df["high"],
        low=df["low"],
        close=df["close"],
        volume=df["volume"],
        window=period
    ).chaikin_money_flow()

    return df