from ta.volatility import KeltnerChannel


def add_keltner(
    df,
    period=20,
    atr_period=10,
    multiplier=2
):

    kc = KeltnerChannel(
        high=df["high"],
        low=df["low"],
        close=df["close"],
        window=period,
        window_atr=atr_period,
        multiplier=multiplier
    )

    df["KC_UPPER"] = kc.keltner_channel_hband()
    df["KC_MIDDLE"] = kc.keltner_channel_mband()
    df["KC_LOWER"] = kc.keltner_channel_lband()

    return df