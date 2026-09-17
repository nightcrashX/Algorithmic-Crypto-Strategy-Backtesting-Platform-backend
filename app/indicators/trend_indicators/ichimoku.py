from ta.trend import IchimokuIndicator

def add_ichimoku(df,conversion=9,base=26,span_b=52):

    ichi = IchimokuIndicator(
        high=df["high"],
        low=df["low"],
        window1=conversion,
        window2=base,
        window3=span_b
    )

    df["TENKAN"] = ichi.ichimoku_conversion_line()
    df["KIJUN"] = ichi.ichimoku_base_line()
    df["SENKOU_A"] = ichi.ichimoku_a()
    df["SENKOU_B"] = ichi.ichimoku_b()

    return df