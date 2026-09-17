from ta.volatility import DonchianChannel


def add_donchian(
    df,
    period=20
):

    dc = DonchianChannel(
        high=df["high"],
        low=df["low"],
        close=df["close"],
        window=period
    )

    df["DC_UPPER"] = dc.donchian_channel_hband()
    df["DC_MIDDLE"] = dc.donchian_channel_mband()
    df["DC_LOWER"] = dc.donchian_channel_lband()

    return df