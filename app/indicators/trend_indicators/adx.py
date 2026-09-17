from ta.trend import ADXIndicator

def add_adx(df, period=14):
    indicator = ADXIndicator(
        df["high"],
        df["low"],
        df["close"],
        window=period
    )

    df[f"ADX_{period}"] = indicator.adx()
    df[f"PLUS_DI_{period}"] = indicator.adx_pos()
    df[f"MINUS_DI_{period}"] = indicator.adx_neg()

    return df