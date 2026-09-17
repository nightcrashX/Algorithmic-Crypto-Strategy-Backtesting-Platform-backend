from ta.momentum import StochasticOscillator


def add_stochastic(
    df,
    k_period=14,
    smooth_k=3,
    smooth_d=3
):

    stoch = StochasticOscillator(
        high=df["high"],
        low=df["low"],
        close=df["close"],
        window=smooth_k,
        smooth_window=smooth_d
    )

    df["STOCH_K"] = stoch.stoch()

    # ta library already applies smooth_window to signal (%D)
    df["STOCH_D"] = stoch.stoch_signal()

    return df