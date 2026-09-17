from ta.momentum import StochRSIIndicator


def add_stoch_rsi(
    df,
    rsi_period=14,
    stoch_period=14,
    k=3,
    d=3
):

    srsi = StochRSIIndicator(
        close=df["close"],
        window=rsi_period,
        smooth1=k,
        smooth2=d
    )

    df["STOCH_RSI"] = srsi.stochrsi()
    df["STOCH_RSI_K"] = srsi.stochrsi_k()
    df["STOCH_RSI_D"] = srsi.stochrsi_d()

    return df