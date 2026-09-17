#app/services/indicator_service.py

import logging
import pandas as pd
from app.services.exchange_service import get_ohlcv
from app.services.chart_service import create_dataframe
from app.indicator_registry.indicator_registry import INDICATOR_MAP

from app.indicators.trend_indicators.ema import add_ema
from app.indicators.trend_indicators.sma import add_sma
from app.indicators.trend_indicators.macd import add_macd
from app.indicators.trend_indicators.adx import add_adx
from app.indicators.trend_indicators.aroon import add_aroon
from app.indicators.trend_indicators.cci import add_cci
from app.indicators.trend_indicators.ichimoku import add_ichimoku
from app.indicators.trend_indicators.psar import add_psar
from app.indicators.trend_indicators.supertrend import add_supertrend
from app.indicators.momentum_indicators.roc import add_roc
from app.indicators.momentum_indicators.rsi import add_rsi
from app.indicators.momentum_indicators.stoch_rsi import add_stoch_rsi
from app.indicators.momentum_indicators.stochastic import add_stochastic
from app.indicators.momentum_indicators.williams_r import add_williams_r
from app.indicators.volume_indicators.ad import add_ad
from app.indicators.volume_indicators.cmf import add_cmf
from app.indicators.volume_indicators.mfi import add_mfi
from app.indicators.volume_indicators.obv import add_obv
from app.indicators.volume_indicators.vwap import add_vwap
from app.indicators.volatility_indicators.atr import add_atr
from app.indicators.volatility_indicators.bollinger_bands import add_bollinger
from app.indicators.volatility_indicators.donchian import add_donchian
from app.indicators.volatility_indicators.keltner import add_keltner


def get_indicators(req):
    result = {}
    for indicator in req.indicators:
        config = INDICATOR_MAP.get(indicator.type)
        if not config:
            continue
        params = config["defaults"].copy()
        params.update(indicator.settings)
        result[indicator.id] = config["function"](
            req.exchange,
            req.symbol,
            req.timeframe,
            **params
        )
    # print(result)
    return result


def create_candles_dataframe(ohlcv):
    if isinstance(ohlcv, pd.DataFrame):
        return ohlcv.copy()
    if not ohlcv:
        return pd.DataFrame(columns=["time", "open", "high", "low", "close", "volume"])

    first = ohlcv[0]
    if isinstance(first, dict):
        df = pd.DataFrame(ohlcv)
    else:
        df = pd.DataFrame(
            ohlcv, columns=["time", "open", "high", "low", "close", "volume"]
        )

    for col in ["open", "high", "low", "close", "volume"]:
        if col in df.columns:
            df[col] = df[col].astype(float)

    if len(df) > 0 and "time" in df.columns:
        first_time = float(df["time"].iloc[0])
        unit = "ms" if first_time > 1e11 else "s"
        df["time"] = pd.to_datetime(df["time"], unit=unit)

    return df


def calculate_live_indicators(ohlcv_data, indicators):
    """
    Calculates the latest indicator value(s) from the current OHLCV candle history.
    Uses the exact existing backend indicator functions.
    """
    if not ohlcv_data or not indicators:
        return {}

    base_df = create_candles_dataframe(ohlcv_data)
    if len(base_df) < 2:
        return {}

    live_results = {}

    for ind in indicators:
        ind_id = ind.get("id")
        ind_type = (ind.get("type") or "").upper()
        settings = ind.get("settings") or {}

        try:
            df = base_df.copy()

            if ind_type == "EMA":
                period = int(settings.get("period", 20))
                if len(df) >= period:
                    df = add_ema(df, period)
                    val = df[f"EMA_{period}"].iloc[-1]
                    if not pd.isna(val):
                        live_results[ind_id] = float(val)

            elif ind_type == "SMA":
                period = int(settings.get("period", 20))
                if len(df) >= period:
                    df = add_sma(df, period)
                    val = df[f"SMA_{period}"].iloc[-1]
                    if not pd.isna(val):
                        live_results[ind_id] = float(val)

            elif ind_type == "RSI":
                period = int(settings.get("period", 14))
                if len(df) >= period:
                    df = add_rsi(df, period)
                    val = df["RSI"].iloc[-1]
                    if not pd.isna(val):
                        live_results[ind_id] = float(val)

            elif ind_type == "MACD":
                fast = int(settings.get("fast", 12))
                slow = int(settings.get("slow", 26))
                signal = int(settings.get("signal", 9))
                if len(df) >= slow:
                    df = add_macd(df, fast, slow, signal)
                    m = df["MACD"].iloc[-1]
                    s = df["MACD_SIGNAL"].iloc[-1]
                    h = df["MACD_HIST"].iloc[-1]
                    if not (pd.isna(m) or pd.isna(s) or pd.isna(h)):
                        live_results[ind_id] = {
                            "MACD": float(m),
                            "SIGNAL": float(s),
                            "HISTOGRAM": float(h),
                        }

            elif ind_type in ["BOLLINGER_BANDS", "BOLLINGER", "BB"]:
                period = int(settings.get("period", 20))
                std = float(settings.get("std", 2))
                if len(df) >= period:
                    df = add_bollinger(df, period, std)
                    u = df["BB_UPPER"].iloc[-1]
                    m = df["BB_MIDDLE"].iloc[-1]
                    l = df["BB_LOWER"].iloc[-1]
                    if not (pd.isna(u) or pd.isna(m) or pd.isna(l)):
                        live_results[ind_id] = {
                            "UPPER": float(u),
                            "MIDDLE": float(m),
                            "LOWER": float(l),
                        }

            elif ind_type == "SUPERTREND":
                atr_period = int(settings.get("atr_period", 10))
                multiplier = float(settings.get("multiplier", 3))
                if len(df) >= atr_period:
                    df = add_supertrend(df, atr_period, multiplier)
                    val = df["Supertrend"].iloc[-1]
                    trend = df["ST_Direction"].iloc[-1]
                    if not pd.isna(val):
                        live_results[ind_id] = {
                            "value": float(val),
                            "trend": float(trend),
                        }

            elif ind_type == "ATR":
                period = int(settings.get("period", 14))
                if len(df) >= period:
                    df = add_atr(df, period)
                    val = df["ATR"].iloc[-1]
                    if not pd.isna(val):
                        live_results[ind_id] = float(val)

            elif ind_type == "VWAP":
                df = add_vwap(df)
                val = df["VWAP"].iloc[-1]
                if not pd.isna(val):
                    live_results[ind_id] = float(val)

            elif ind_type == "OBV":
                df = add_obv(df)
                val = df["OBV"].iloc[-1]
                if not pd.isna(val):
                    live_results[ind_id] = float(val)

            elif ind_type == "ROC":
                period = int(settings.get("period", 12))
                if len(df) > period:
                    df = add_roc(df, period)
                    val = df["ROC"].iloc[-1]
                    if not pd.isna(val):
                        live_results[ind_id] = float(val)

            elif ind_type == "CCI":
                period = int(settings.get("period", 20))
                if len(df) >= period:
                    df = add_cci(df, period)
                    val = df[f"CCI_{period}"].iloc[-1]
                    if not pd.isna(val):
                        live_results[ind_id] = float(val)

            elif ind_type in ["WILLIAMS_R", "WILLIAM_R"]:
                period = int(settings.get("period", 14))
                if len(df) >= period:
                    df = add_williams_r(df, period)
                    val = df["WILLIAMS_R"].iloc[-1]
                    if not pd.isna(val):
                        live_results[ind_id] = float(val)

            elif ind_type == "STOCHASTIC":
                smooth_k = int(settings.get("smooth_k", 14))
                smooth_d = int(settings.get("smooth_d", 3))
                if len(df) >= smooth_k:
                    df = add_stochastic(df, smooth_k=smooth_k, smooth_d=smooth_d)
                    k = df["STOCH_K"].iloc[-1]
                    d = df["STOCH_D"].iloc[-1]
                    if not (pd.isna(k) or pd.isna(d)):
                        live_results[ind_id] = {
                            "K": float(k),
                            "D": float(d),
                        }

            elif ind_type in ["STOCHASTIC_RSI", "STOCH_RSI"]:
                rsi_period = int(settings.get("rsi_period", 14))
                stoch_period = int(settings.get("stoch_period", 14))
                k = int(settings.get("k", 3))
                d = int(settings.get("d", 3))
                if len(df) >= rsi_period + stoch_period:
                    df = add_stoch_rsi(df, rsi_period, stoch_period, k, d)
                    sr = df["STOCH_RSI"].iloc[-1]
                    sk = df["STOCH_RSI_K"].iloc[-1]
                    sd = df["STOCH_RSI_D"].iloc[-1]
                    if not (pd.isna(sr) or pd.isna(sk) or pd.isna(sd)):
                        live_results[ind_id] = {
                            "STOCH_RSI": float(sr),
                            "K": float(sk),
                            "D": float(sd),
                        }

            elif ind_type == "ADX":
                period = int(settings.get("period", 14))
                if len(df) >= period:
                    df = add_adx(df, period)
                    val = df[f"ADX_{period}"].iloc[-1]
                    if not pd.isna(val):
                        live_results[ind_id] = float(val)

            elif ind_type == "AROON":
                period = int(settings.get("period", 14))
                if len(df) >= period:
                    df = add_aroon(df, period)
                    u = df[f"AROON_UP_{period}"].iloc[-1]
                    d = df[f"AROON_DOWN_{period}"].iloc[-1]
                    o = df[f"AROON_OSC_{period}"].iloc[-1]
                    if not (pd.isna(u) or pd.isna(d) or pd.isna(o)):
                        live_results[ind_id] = {
                            "up": float(u),
                            "down": float(d),
                            "osc": float(o),
                        }

            elif ind_type == "CMF":
                period = int(settings.get("period", 20))
                if len(df) >= period:
                    df = add_cmf(df, period)
                    val = df["CMF"].iloc[-1]
                    if not pd.isna(val):
                        live_results[ind_id] = float(val)

            elif ind_type == "MFI":
                period = int(settings.get("period", 14))
                if len(df) >= period:
                    df = add_mfi(df, period)
                    val = df[f"MFI_{period}"].iloc[-1]
                    if not pd.isna(val):
                        live_results[ind_id] = float(val)

            elif ind_type in ["A/D", "AD"]:
                df = add_ad(df)
                val = df["AD"].iloc[-1]
                if not pd.isna(val):
                    live_results[ind_id] = float(val)

            elif ind_type in ["DONCHIAN_CHANNEL", "DONCHIAN"]:
                period = int(settings.get("period", 20))
                if len(df) >= period:
                    df = add_donchian(df, period)
                    u = df["DC_UPPER"].iloc[-1]
                    m = df["DC_MIDDLE"].iloc[-1]
                    l = df["DC_LOWER"].iloc[-1]
                    if not (pd.isna(u) or pd.isna(m) or pd.isna(l)):
                        live_results[ind_id] = {
                            "UPPER": float(u),
                            "MIDDLE": float(m),
                            "LOWER": float(l),
                        }

            elif ind_type in ["KELTNER_CHANNEL", "KELTNER"]:
                period = int(settings.get("period", 20))
                atr_period = int(settings.get("atr_period", 10))
                multiplier = float(settings.get("multiplier", 2))
                if len(df) >= max(period, atr_period):
                    df = add_keltner(df, period, atr_period, multiplier)
                    u = df["KC_UPPER"].iloc[-1]
                    m = df["KC_MIDDLE"].iloc[-1]
                    l = df["KC_LOWER"].iloc[-1]
                    if not (pd.isna(u) or pd.isna(m) or pd.isna(l)):
                        live_results[ind_id] = {
                            "UPPER": float(u),
                            "MIDDLE": float(m),
                            "LOWER": float(l),
                        }

            elif ind_type == "ICHIMOKU":
                conversion = int(settings.get("conversion", 9))
                base = int(settings.get("base", 26))
                span_b = int(settings.get("span_b", 52))
                if len(df) >= max(conversion, base):
                    df = add_ichimoku(df, conversion, base, span_b)
                    t = df["TENKAN"].iloc[-1]
                    k = df["KIJUN"].iloc[-1]
                    sa = df["SENKOU_A"].iloc[-1]
                    sb = df["SENKOU_B"].iloc[-1]
                    if not (pd.isna(t) or pd.isna(k) or pd.isna(sa) or pd.isna(sb)):
                        live_results[ind_id] = {
                            "TENKAN": float(t),
                            "KIJUN": float(k),
                            "SENKOU_A": float(sa),
                            "SENKOU_B": float(sb),
                        }

            elif ind_type in ["PARABOLIC_SAR", "PSAR"]:
                step = float(settings.get("step", 0.02))
                max_step = float(settings.get("max_step", 0.2))
                if len(df) >= 2:
                    df = add_psar(df, step, max_step)
                    val = df["PSAR"].iloc[-1]
                    if not pd.isna(val):
                        live_results[ind_id] = float(val)

        except Exception as e:
            logging.error(f"Error calculating live indicator {ind_type}: {e}")

    return live_results


def calculate_historical_indicators(ohlcv_data, indicators):
    """
    Calculates the full historical series for each active indicator
    given a list of OHLCV candles.
    Uses the exact existing backend indicator algorithms.
    """
    if not ohlcv_data or not indicators:
        return {}

    base_df = create_candles_dataframe(ohlcv_data)
    if len(base_df) < 2:
        return {}

    hist_results = {}

    for ind in indicators:
        ind_id = ind.get("id")
        ind_type = (ind.get("type") or "").upper()
        settings = ind.get("settings") or {}

        try:
            df = base_df.copy()

            if ind_type == "EMA":
                period = int(settings.get("period", 20))
                if len(df) >= period:
                    df = add_ema(df, period)
                    col = f"EMA_{period}"
                    hist_results[ind_id] = [
                        {"time": int(r["time"].timestamp()), "value": float(r[col])}
                        for _, r in df.iterrows()
                        if not pd.isna(r[col])
                    ]

            elif ind_type == "SMA":
                period = int(settings.get("period", 20))
                if len(df) >= period:
                    df = add_sma(df, period)
                    col = f"SMA_{period}"
                    hist_results[ind_id] = [
                        {"time": int(r["time"].timestamp()), "value": float(r[col])}
                        for _, r in df.iterrows()
                        if not pd.isna(r[col])
                    ]

            elif ind_type == "RSI":
                period = int(settings.get("period", 14))
                if len(df) >= period:
                    df = add_rsi(df, period)
                    hist_results[ind_id] = [
                        {"time": int(r["time"].timestamp()), "value": float(r["RSI"])}
                        for _, r in df.iterrows()
                        if not pd.isna(r["RSI"])
                    ]

            elif ind_type == "MACD":
                fast = int(settings.get("fast", 12))
                slow = int(settings.get("slow", 26))
                signal = int(settings.get("signal", 9))
                if len(df) >= slow:
                    df = add_macd(df, fast, slow, signal)
                    m_list, s_list, h_list = [], [], []
                    for _, r in df.iterrows():
                        t = int(r["time"].timestamp())
                        if not pd.isna(r["MACD"]):
                            m_list.append({"time": t, "value": float(r["MACD"])})
                        if not pd.isna(r["MACD_SIGNAL"]):
                            s_list.append({"time": t, "value": float(r["MACD_SIGNAL"])})
                        if not pd.isna(r["MACD_HIST"]):
                            h_list.append({"time": t, "value": float(r["MACD_HIST"])})
                    hist_results[ind_id] = {
                        "MACD": m_list,
                        "SIGNAL": s_list,
                        "HISTOGRAM": h_list,
                    }

            elif ind_type in ["BOLLINGER_BANDS", "BOLLINGER", "BB"]:
                period = int(settings.get("period", 20))
                std = float(settings.get("std", 2))
                if len(df) >= period:
                    df = add_bollinger(df, period, std)
                    u_list, m_list, l_list = [], [], []
                    for _, r in df.iterrows():
                        t = int(r["time"].timestamp())
                        if not pd.isna(r["BB_UPPER"]):
                            u_list.append({"time": t, "value": float(r["BB_UPPER"])})
                        if not pd.isna(r["BB_MIDDLE"]):
                            m_list.append({"time": t, "value": float(r["BB_MIDDLE"])})
                        if not pd.isna(r["BB_LOWER"]):
                            l_list.append({"time": t, "value": float(r["BB_LOWER"])})
                    hist_results[ind_id] = {
                        "UPPER": u_list,
                        "MIDDLE": m_list,
                        "LOWER": l_list,
                    }

            elif ind_type == "SUPERTREND":
                atr_period = int(settings.get("atr_period", 10))
                multiplier = float(settings.get("multiplier", 3))
                if len(df) >= atr_period:
                    df = add_supertrend(df, atr_period, multiplier)
                    st_list = []
                    for _, r in df.iterrows():
                        if not pd.isna(r["Supertrend"]):
                            st_list.append({
                                "time": int(r["time"].timestamp()),
                                "value": float(r["Supertrend"]),
                                "trend": float(r["ST_Direction"]),
                            })
                    hist_results[ind_id] = st_list

            elif ind_type == "ATR":
                period = int(settings.get("period", 14))
                if len(df) >= period:
                    df = add_atr(df, period)
                    hist_results[ind_id] = [
                        {"time": int(r["time"].timestamp()), "value": float(r["ATR"])}
                        for _, r in df.iterrows()
                        if not pd.isna(r["ATR"])
                    ]

            elif ind_type == "VWAP":
                df = add_vwap(df)
                hist_results[ind_id] = [
                    {"time": int(r["time"].timestamp()), "value": float(r["VWAP"])}
                    for _, r in df.iterrows()
                    if not pd.isna(r["VWAP"])
                ]

            elif ind_type == "OBV":
                df = add_obv(df)
                hist_results[ind_id] = [
                    {"time": int(r["time"].timestamp()), "value": float(r["OBV"])}
                    for _, r in df.iterrows()
                    if not pd.isna(r["OBV"])
                ]

            elif ind_type == "ROC":
                period = int(settings.get("period", 12))
                if len(df) > period:
                    df = add_roc(df, period)
                    hist_results[ind_id] = [
                        {"time": int(r["time"].timestamp()), "value": float(r["ROC"])}
                        for _, r in df.iterrows()
                        if not pd.isna(r["ROC"])
                    ]

            elif ind_type == "CCI":
                period = int(settings.get("period", 20))
                if len(df) >= period:
                    df = add_cci(df, period)
                    col = f"CCI_{period}"
                    hist_results[ind_id] = [
                        {"time": int(r["time"].timestamp()), "value": float(r[col])}
                        for _, r in df.iterrows()
                        if not pd.isna(r[col])
                    ]

            elif ind_type in ["WILLIAMS_R", "WILLIAM_R"]:
                period = int(settings.get("period", 14))
                if len(df) >= period:
                    df = add_williams_r(df, period)
                    hist_results[ind_id] = [
                        {"time": int(r["time"].timestamp()), "value": float(r["WILLIAMS_R"])}
                        for _, r in df.iterrows()
                        if not pd.isna(r["WILLIAMS_R"])
                    ]

            elif ind_type == "STOCHASTIC":
                smooth_k = int(settings.get("smooth_k", 14))
                smooth_d = int(settings.get("smooth_d", 3))
                if len(df) >= smooth_k:
                    df = add_stochastic(df, smooth_k=smooth_k, smooth_d=smooth_d)
                    k_list, d_list = [], []
                    for _, r in df.iterrows():
                        t = int(r["time"].timestamp())
                        if not pd.isna(r["STOCH_K"]):
                            k_list.append({"time": t, "value": float(r["STOCH_K"])})
                        if not pd.isna(r["STOCH_D"]):
                            d_list.append({"time": t, "value": float(r["STOCH_D"])})
                    hist_results[ind_id] = {"K": k_list, "D": d_list}

            elif ind_type in ["STOCHASTIC_RSI", "STOCH_RSI"]:
                rsi_period = int(settings.get("rsi_period", 14))
                stoch_period = int(settings.get("stoch_period", 14))
                k = int(settings.get("k", 3))
                d = int(settings.get("d", 3))
                if len(df) >= rsi_period + stoch_period:
                    df = add_stoch_rsi(df, rsi_period, stoch_period, k, d)
                    sr_list, k_list, d_list = [], [], []
                    for _, r in df.iterrows():
                        t = int(r["time"].timestamp())
                        if not pd.isna(r["STOCH_RSI"]):
                            sr_list.append({"time": t, "value": float(r["STOCH_RSI"])})
                        if not pd.isna(r["STOCH_RSI_K"]):
                            k_list.append({"time": t, "value": float(r["STOCH_RSI_K"])})
                        if not pd.isna(r["STOCH_RSI_D"]):
                            d_list.append({"time": t, "value": float(r["STOCH_RSI_D"])})
                    hist_results[ind_id] = {
                        "STOCH_RSI": sr_list,
                        "K": k_list,
                        "D": d_list,
                    }

            elif ind_type == "ADX":
                period = int(settings.get("period", 14))
                if len(df) >= period:
                    df = add_adx(df, period)
                    col = f"ADX_{period}"
                    hist_results[ind_id] = [
                        {"time": int(r["time"].timestamp()), "value": float(r[col])}
                        for _, r in df.iterrows()
                        if not pd.isna(r[col])
                    ]

            elif ind_type == "AROON":
                period = int(settings.get("period", 14))
                if len(df) >= period:
                    df = add_aroon(df, period)
                    u_col = f"AROON_UP_{period}"
                    d_col = f"AROON_DOWN_{period}"
                    o_col = f"AROON_OSC_{period}"
                    u_list, d_list, o_list = [], [], []
                    for _, r in df.iterrows():
                        t = int(r["time"].timestamp())
                        if not pd.isna(r[u_col]):
                            u_list.append({"time": t, "value": float(r[u_col])})
                        if not pd.isna(r[d_col]):
                            d_list.append({"time": t, "value": float(r[d_col])})
                        if not pd.isna(r[o_col]):
                            o_list.append({"time": t, "value": float(r[o_col])})
                    hist_results[ind_id] = {
                        "up": u_list,
                        "down": d_list,
                        "osc": o_list,
                    }

            elif ind_type == "CMF":
                period = int(settings.get("period", 20))
                if len(df) >= period:
                    df = add_cmf(df, period)
                    hist_results[ind_id] = [
                        {"time": int(r["time"].timestamp()), "value": float(r["CMF"])}
                        for _, r in df.iterrows()
                        if not pd.isna(r["CMF"])
                    ]

            elif ind_type == "MFI":
                period = int(settings.get("period", 14))
                if len(df) >= period:
                    df = add_mfi(df, period)
                    col = f"MFI_{period}"
                    hist_results[ind_id] = [
                        {"time": int(r["time"].timestamp()), "value": float(r[col])}
                        for _, r in df.iterrows()
                        if not pd.isna(r[col])
                    ]

            elif ind_type in ["A/D", "AD"]:
                df = add_ad(df)
                hist_results[ind_id] = [
                    {"time": int(r["time"].timestamp()), "value": float(r["AD"])}
                    for _, r in df.iterrows()
                    if not pd.isna(r["AD"])
                ]

            elif ind_type in ["DONCHIAN_CHANNEL", "DONCHIAN"]:
                period = int(settings.get("period", 20))
                if len(df) >= period:
                    df = add_donchian(df, period)
                    u_list, m_list, l_list = [], [], []
                    for _, r in df.iterrows():
                        t = int(r["time"].timestamp())
                        if not pd.isna(r["DC_UPPER"]):
                            u_list.append({"time": t, "value": float(r["DC_UPPER"])})
                        if not pd.isna(r["DC_MIDDLE"]):
                            m_list.append({"time": t, "value": float(r["DC_MIDDLE"])})
                        if not pd.isna(r["DC_LOWER"]):
                            l_list.append({"time": t, "value": float(r["DC_LOWER"])})
                    hist_results[ind_id] = {
                        "UPPER": u_list,
                        "MIDDLE": m_list,
                        "LOWER": l_list,
                    }

            elif ind_type in ["KELTNER_CHANNEL", "KELTNER"]:
                period = int(settings.get("period", 20))
                atr_period = int(settings.get("atr_period", 10))
                multiplier = float(settings.get("multiplier", 2))
                if len(df) >= max(period, atr_period):
                    df = add_keltner(df, period, atr_period, multiplier)
                    u_list, m_list, l_list = [], [], []
                    for _, r in df.iterrows():
                        t = int(r["time"].timestamp())
                        if not pd.isna(r["KC_UPPER"]):
                            u_list.append({"time": t, "value": float(r["KC_UPPER"])})
                        if not pd.isna(r["KC_MIDDLE"]):
                            m_list.append({"time": t, "value": float(r["KC_MIDDLE"])})
                        if not pd.isna(r["KC_LOWER"]):
                            l_list.append({"time": t, "value": float(r["KC_LOWER"])})
                    hist_results[ind_id] = {
                        "UPPER": u_list,
                        "MIDDLE": m_list,
                        "LOWER": l_list,
                    }

            elif ind_type == "ICHIMOKU":
                conversion = int(settings.get("conversion", 9))
                base = int(settings.get("base", 26))
                span_b = int(settings.get("span_b", 52))
                if len(df) >= max(conversion, base):
                    df = add_ichimoku(df, conversion, base, span_b)
                    t_list, k_list, sa_list, sb_list = [], [], [], []
                    for _, r in df.iterrows():
                        t = int(r["time"].timestamp())
                        if not pd.isna(r["TENKAN"]):
                            t_list.append({"time": t, "value": float(r["TENKAN"])})
                        if not pd.isna(r["KIJUN"]):
                            k_list.append({"time": t, "value": float(r["KIJUN"])})
                        if not pd.isna(r["SENKOU_A"]):
                            sa_list.append({"time": t, "value": float(r["SENKOU_A"])})
                        if not pd.isna(r["SENKOU_B"]):
                            sb_list.append({"time": t, "value": float(r["SENKOU_B"])})
                    hist_results[ind_id] = {
                        "TENKAN": t_list,
                        "KIJUN": k_list,
                        "SENKOU_A": sa_list,
                        "SENKOU_B": sb_list,
                    }

            elif ind_type in ["PARABOLIC_SAR", "PSAR"]:
                step = float(settings.get("step", 0.02))
                max_step = float(settings.get("max_step", 0.2))
                if len(df) >= 2:
                    df = add_psar(df, step, max_step)
                    hist_results[ind_id] = [
                        {"time": int(r["time"].timestamp()), "value": float(r["PSAR"])}
                        for _, r in df.iterrows()
                        if not pd.isna(r["PSAR"])
                    ]

        except Exception as e:
            logging.error(f"Error calculating historical indicator {ind_type}: {e}")

    return hist_results
