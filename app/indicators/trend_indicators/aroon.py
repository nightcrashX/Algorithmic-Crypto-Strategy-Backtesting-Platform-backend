from ta.trend import AroonIndicator

def add_aroon(df, period=25):
    indicator = AroonIndicator(
        df["high"],
        df["low"],
        window=period
    )

    df[f"AROON_UP_{period}"] = indicator.aroon_up()
    df[f"AROON_DOWN_{period}"] = indicator.aroon_down()
    df[f"AROON_OSC_{period}"] = indicator.aroon_indicator()

    return df