from ta.trend import PSARIndicator


def add_psar(
    df,
    step=0.02,
    max_step=0.2
):

    indicator = PSARIndicator(
        high=df["high"],
        low=df["low"],
        close=df["close"],
        step=step,
        max_step=max_step
    )

    df["PSAR"] = indicator.psar()

    return df