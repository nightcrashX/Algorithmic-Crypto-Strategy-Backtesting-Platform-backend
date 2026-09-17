#indicator_registry.py
"""
Indicator Registry

This file contains metadata of all standard technical indicators.

Each indicator contains:
- Function Reference
- Default Parameters
- Category
- Pane Type
- Output Type
- Series Type
- Default Style
"""

# ============================================================
# TREND INDICATORS
# ============================================================

from app.indicator_wrapper.trend_wrapper.ema_wrapper import get_ema
from app.indicator_wrapper.trend_wrapper.sma_wrapper import get_sma
from app.indicator_wrapper.trend_wrapper.adx_wrapper import get_adx
from app.indicator_wrapper.trend_wrapper.aroon_wrapper import get_aroon
from app.indicator_wrapper.trend_wrapper.cci_wrapper import get_cci
from app.indicator_wrapper.trend_wrapper.ichomoku_wrapper import get_ichimoku
from app.indicator_wrapper.trend_wrapper.macd_wrapper import get_macd
from app.indicator_wrapper.trend_wrapper.psar_wrapper import get_psar
from app.indicator_wrapper.trend_wrapper.supertrend_wrapper import get_supertrend

# ============================================================
# MOMENTUM INDICATORS
# ============================================================

from app.indicator_wrapper.momentum_wrapper.roc_wrapper import get_roc
from app.indicator_wrapper.momentum_wrapper.rsi_wrapper import get_rsi
from app.indicator_wrapper.momentum_wrapper.s_rsi_wrapper import get_stoch_rsi
from app.indicator_wrapper.momentum_wrapper.stochastic_wrapper import get_stochastic
from app.indicator_wrapper.momentum_wrapper.william_r_wrapper import get_williams_r

# ============================================================
# VOLUME INDICATORS
# ============================================================

from app.indicator_wrapper.volume_wrapper.ad_wrapper import get_ad
from app.indicator_wrapper.volume_wrapper.cmf_wrapper import get_cmf
from app.indicator_wrapper.volume_wrapper.mfi_wrapper import get_mfi
from app.indicator_wrapper.volume_wrapper.obv_wrapper import get_obv
from app.indicator_wrapper.volume_wrapper.vwap_wrapper import get_vwap

# ============================================================
# VOLATILITY INDICATORS
# ============================================================

from app.indicator_wrapper.volatility_wrapper.atr_wrapper import get_atr
from app.indicator_wrapper.volatility_wrapper.bollinger_wrapper import get_bollinger
from app.indicator_wrapper.volatility_wrapper.doncahin_wrapper import get_donchian
from app.indicator_wrapper.volatility_wrapper.keltner_wrapper import get_keltner


# ============================================================
# INDICATOR REGISTRY
# ============================================================

INDICATOR_MAP = {

    # ========================================================
    # TREND INDICATORS
    # ========================================================

    "EMA": {

        "id": "ema",
        "function": get_ema,
        "display_name": "Exponential Moving Average",
        "short_name": "EMA",
        "category": "Trend",
        "pane": "overlay",
        "output": "single",
        "series_type": "line",
        "max_instances": None,
        "defaults": {
            "period": 20
        },
        "style": {
            "color": "#2962FF",
            "lineWidth": 2,
            "lineStyle": "solid",
            "visible": True,
            "priceLineVisible": False,
            "lastValueVisible": True
        },
        "editable": True,
        "enabled": True,
        # "supports_live": True,
        # "supports_alert":True,
        # "supports_backtest": True,
        # "supports_strategy": True,
        "min_period": 1,
        "max_period": 500
        # "frontend":{

        #     "draggable":True,

        #     "hideable":True,

        #     "deletable":True,

        #     "editable":True

        # }
    },
    # --------------------------------------------------------
    "SMA": {
        "id": "sma",
        "function": get_sma,
        "display_name": "Simple Moving Average",
        "short_name": "SMA",
        "category": "Trend",
        "pane": "overlay",
        "output": "single",
        "series_type": "line",
        "max_instances": None,
        "defaults": {
            "period": 20
        },
        "style": {
            "color": "#FF9800",
            "lineWidth": 2,
            "lineStyle": "solid",
            "visible": True,
            "priceLineVisible": False,
            "lastValueVisible": True
        },
        "editable": True,
        "enabled": True,
        # "supports_live": True,
        # "supports_alert":True,
        # "supports_backtest": True,
        # "supports_strategy": True,
        "min_period": 1,
        "max_period": 500
        # "frontend":{

        #     "draggable":True,
        
        #     "hideable":True,
        
        #     "deletable":True,
        
        #     "editable":True
        
        # }
    },
    # --------------------------------------------------------
    "SUPERTREND": {
        "id": "supertrend",
        "function": get_supertrend,
        "display_name": "Supertrend",
        "short_name": "Supertrend",
        "category": "Trend",
        "pane": "overlay",
        "output": "single",
        "series_type": "line",
        "defaults": {
            "atr_period": 10,
            "multiplier": 3
        },
        "style": {
            "upColor": "#00C853",
            "downColor": "#D50000",
            "lineWidth": 2,
            "visible": True
        },
        "editable": True,
        "enabled": True,
        # "supports_live": True,
        # "supports_alert":True,
        # "supports_backtest": True,
        # "supports_strategy": True,
        # "min_period": 1,
        # "max_period": 500,
        # "frontend":{

        #     "draggable":True,
        
        #     "hideable":True,
        
        #     "deletable":True,
        
        #     "editable":True
        
        # }
    },
    # --------------------------------------------------------
    "MACD": {
        "id":"macd",
        "function": get_macd,
        "display_name": "Moving Average Convergence Divergence",
        "short_name": "MACD",
        "category": "Trend",
        "pane": "macd",
        "output": "multi",
        "series_type": "macd",
        "defaults": {
            "fast": 12,
            "slow": 26,
            "signal": 9
        },
        "style": {
            "macdColor": "#2962FF",
            "signalColor": "#FF9800",
            "histogramUp": "#00C853",
            "histogramDown": "#D50000"
        },
        "editable": True,
        "enabled": True,
        # "supports_live": True,
        # "supports_alert":True,
        # "supports_backtest": True,
        # "supports_strategy": True,
        # "min_period": 1,
        # "max_period": 500,
        # "frontend":{

        #     "draggable":True,
        
        #     "hideable":True,
        
        #     "deletable":True,
        
        #     "editable":True
        
        # }
    },
    # --------------------------------------------------------
    "ADX": {
        "id":"adx",
        "function": get_adx,
        "display_name": "Average Directional Index",
        "short_name": "ADX",
        "category": "Trend",
        "pane": "adx",
        "output": "multi",     #signle to multi change manually
        "series_type": "line",
        "defaults": {
            "period": 14
        },
        "style": {
            "color": "#8E24AA",
            "lineWidth": 2,
            "visible": True
        },
        "editable": True,
        "enabled": True,
        # "supports_live": True,
        # "supports_alert":True,
        # "supports_backtest": True,
        # "supports_strategy": True,
        # "min_period": 1,
        # "max_period": 500,
        # "frontend":{

        #     "draggable":True,
        
        #     "hideable":True,
        
        #     "deletable":True,
        
        #     "editable":True
        
        # }
    },
    # --------------------------------------------------------
    "AROON": {
        "id":"aroon",
        "function": get_aroon,
        "display_name": "Aroon Indicator",
        "short_name": "Aroon",
        "category": "Trend",
        "pane": "aroon",
        "output": "multi",
        "series_type": "line",
        "defaults": {
            "period": 14
        },
        "style": {
            "upColor": "#00C853",
            "downColor": "#2962FF",
            "lineWidth": 2
        },
        "editable": True,
        "enabled": True,
        # "supports_live": True,
        # "supports_alert":True,
        # "supports_backtest": True,
        # "supports_strategy": True,
        # "min_period": 1,
        # "max_period": 500,
        # "frontend":{

        #     "draggable":True,
        
        #     "hideable":True,
        
        #     "deletable":True,
        
        #     "editable":True
        
        # }
    },
    # --------------------------------------------------------
    "CCI": {
        "id":"cci",
        "function": get_cci,
        "display_name": "Commodity Channel Index",
        "short_name": "CCI",
        "category": "Trend",
        "pane": "cci",
        "output": "single",
        "series_type": "line",
        "defaults": {
            "period": 20
        },
        "style": {
            "color": "#F44336",
            "lineWidth": 2
        },
        "editable": True,
        "enabled": True,
        # "supports_live": True,
        # "supports_alert":True,
        # "supports_backtest": True,
        # "supports_strategy": True,
        # "min_period": 1,
        # "max_period": 500,
        # "frontend":{

        #     "draggable":True,
        
        #     "hideable":True,
        
        #     "deletable":True,
        
        #     "editable":True
        
        # }
    },
    # --------------------------------------------------------
    "ICHIMOKU": {
        "id":"ichimoku",
        "function": get_ichimoku,
        "display_name": "Ichimoku Cloud",
        "short_name": "Ichimoku",
        "category": "Trend",
        "pane": "overlay",
        "output": "multi",
        "series_type": "ichimoku",
        "defaults": {
            "conversion": 9,
            "base": 26,
            "span_b": 52
        },
        "style": {
            "tenkan": "#F44336",
            "kijun": "#2962FF",
            "spanA": "#00C853",
            "spanB": "#D50000",
            "cloudBull": "rgba(0,200,83,0.20)",
            "cloudBear": "rgba(213,0,0,0.20)"
        },
        "editable": True,
        "enabled": True,
        # "supports_live": True,
        # "supports_alert":True,
        # "supports_backtest": True,
        # "supports_strategy": True,
        # "min_period": 1,
        # "max_period": 500,
        # "frontend":{

        #     "draggable":True,
        
        #     "hideable":True,
        
        #     "deletable":True,
        
        #     "editable":True
        
        # }
    },
    # --------------------------------------------------------
    "PARABOLIC_SAR": {
        "id":"parabolic_sar",
        "function": get_psar,
        "display_name": "Parabolic SAR",
        "short_name": "PSAR",
        "category": "Trend",
        "pane": "overlay",
        "output": "single",
        "series_type": "marker",
        "defaults": {
            "step": 0.02,
            "max_step": 0.2
        },
        "style": {
            "color": "#FF9800",
            "size": 2
        },
        "editable": True,
        "enabled": True,
        # "supports_live": True,
        # "supports_alert":True,
        # "supports_backtest": True,
        # "supports_strategy": True,
        # "min_period": 1,
        # "max_period": 500,
        # "frontend":{

        #     "draggable":True,
        
        #     "hideable":True,
        
        #     "deletable":True,
        
        #     "editable":True
        
        # }
    },
    # ========================================================
    # MOMENTUM INDICATORS
    # ========================================================
    "RSI": {
        "id":"rsi",
        "function": get_rsi,
        "display_name": "Relative Strength Index",
        "short_name": "RSI",
        "category": "Momentum",
        "pane": "rsi",
        "output": "single",
        "series_type": "line",
        "defaults": {
            "period": 14
        },
        "style": {
            "color": "#7E57C2",
            "lineWidth": 2,
            "visible": True
        },
        "editable": True,
        "enabled": True,
        # "supports_live": True,
        # "supports_alert":True,
        # "supports_backtest": True,
        # "supports_strategy": True,
        # "min_period": 1,
        # "max_period": 500,
        # "frontend":{

        #     "draggable":True,
        
        #     "hideable":True,
        
        #     "deletable":True,
        
        #     "editable":True
        
        # }
    },
    # --------------------------------------------------------
    "ROC": {
        "id":"roc",
        "function": get_roc,
        "display_name": "Rate of Change",
        "short_name": "ROC",
        "category": "Momentum",
        "pane": "roc",
        "output": "single",
        "series_type": "line",
        "defaults": {
            "period": 12
        },
        "style": {
            "color": "#00ACC1",
            "lineWidth": 2,
            "visible": True
        },
        "editable": True,
        "enabled": True,
        # "supports_live": True,
        # "supports_alert":True,
        # "supports_backtest": True,
        # "supports_strategy": True,
        # "min_period": 1,
        # "max_period": 500,
        # "frontend":{

        #     "draggable":True,
        
        #     "hideable":True,
        
        #     "deletable":True,
        
        #     "editable":True
        
        # }
    },
    # --------------------------------------------------------
    "STOCHASTIC": {
        "id":"stochastic",
        "function": get_stochastic,
        "display_name": "Stochastic Oscillator",
        "short_name": "Stochastic",
        "category": "Momentum",
        "pane": "stochastic",
        "output": "multi",
        "series_type": "stochastic",
        "defaults": {
            "smooth_k": 14,
            "smooth_d": 3
        },
        "style": {
            "kColor": "#2962FF",
            "dColor": "#FF9800",
            "lineWidth": 2
        },
        "editable": True,
        "enabled": True,
        # "supports_live": True,
        # "supports_alert":True,
        # "supports_backtest": True,
        # "supports_strategy": True,
        # "min_period": 1,
        # "max_period": 500,
        # "frontend":{

        #     "draggable":True,
        
        #     "hideable":True,
        
        #     "deletable":True,
        
        #     "editable":True
        
        # }
    },
    # --------------------------------------------------------
    "STOCHASTIC_RSI": {
        "id":"stochastic_rst",
        "function": get_stoch_rsi,
        "display_name": "Stochastic RSI",
        "short_name": "Stoch RSI",
        "category": "Momentum",
        "pane": "stochastic_rsi",
        "output": "multi",
        "series_type": "stochastic",
        "defaults": {
            "rsi_period": 14,
            "stoch_period": 14,
            "k": 3,
            "d": 3
        }, 
        "style": {
            "kColor": "#00C853",
            "dColor": "#D50000",
            "lineWidth": 2
        },
        "editable": True,
        "enabled": True,
        # "supports_live": True,
        # "supports_alert":True,
        # "supports_backtest": True,
        # "supports_strategy": True,
        # "min_period": 1,
        # "max_period": 500,
        # "frontend":{

        #     "draggable":True,
        
        #     "hideable":True,
        
        #     "deletable":True,
        
        #     "editable":True
        
        # }
    },
    # --------------------------------------------------------
    "WILLIAMS_R": {
        "id":"williams_r",
        "function": get_williams_r,
        "display_name": "Williams Percent Range",
        "short_name": "Williams %R",
        "category": "Momentum",
        "pane": "william_r",
        "output": "single",
        "series_type": "line",
        "defaults": {
            "period": 14
        },
        "style": {
            "color": "#E91E63",
            "lineWidth": 2
        },
        "editable": True,
        "enabled": True,
        # "supports_live": True,
        # "supports_alert":True,
        # "supports_backtest": True,
        # "supports_strategy": True,
        # "min_period": 1,
        # "max_period": 500,
        # "frontend":{

        #     "draggable":True,
        
        #     "hideable":True,
        
        #     "deletable":True,
        
        #     "editable":True
        # }
                
    },
    # ========================================================
    # VOLUME INDICATORS
    # ========================================================
    "VWAP": {
        "id":"vwap",
        "function": get_vwap,
        "display_name": "Volume Weighted Average Price",
        "short_name": "VWAP",
        "category": "Volume",
        "pane": "overlay",
        "output": "single",
        "series_type": "line",
        "defaults": {},
        "style": {
            "color": "#9C27B0",
            "lineWidth": 2,
            "visible": True
        },
        "editable": True,
        "enabled": True,
        # "supports_live": True,
        # "supports_alert":True,
        # "supports_backtest": True,
        # "supports_strategy": True,
        # "min_period": 1,
        # "max_period": 500,
        # "frontend":{

        #     "draggable":True,
        
        #     "hideable":True,
        
        #     "deletable":True,
        
        #     "editable":True
        
        # }
    },
    # --------------------------------------------------------
    "OBV": {
        "id":"obv",
        "function": get_obv,
        "display_name": "On Balance Volume",
        "short_name": "OBV",
        "category": "Volume",
        "pane": "obv",
        "output": "single",
        "series_type": "line",
        "defaults": {},
        "style": {
            "color": "#4CAF50",
            "lineWidth": 2
        },
        "editable": True,
        "enabled": True
    },
    # --------------------------------------------------------
    "CMF": {
        "id":"cmf",
        "function": get_cmf,
        "display_name": "Chaikin Money Flow",
        "short_name": "CMF",
        "category": "Volume",
        "pane": "cmf",
        "output": "single",
        "series_type": "line",
        "defaults": {
            "period": 20
        },
        "style": {
            "color": "#795548",
            "lineWidth": 2
        },
        "editable": True,
        "enabled": True
    },
    # --------------------------------------------------------
    "MFI": {
        "id":"mfi",
        "function": get_mfi,
        "display_name": "Money Flow Index",
        "short_name": "MFI",
        "category": "Volume",
        "pane": "mfi",
        "output": "single",
        "series_type": "line",
        "defaults": {
            "period": 14
        },
        "style": {
            "color": "#3F51B5",
            "lineWidth": 2
        },
        "editable": True,
        "enabled": True
    },
    #---------------------------------------------------------
    "A/D": {
        "id":"a/d",
        "function": get_ad,
        "display_name": "Accumulation Distribution",
        "short_name": "A/D",
        "category": "Volume",
        "pane": "a/d",
        "output": "single",
        "series_type": "line",
        "defaults": {},
        "style": {
            "color": "#009688",
            "lineWidth": 2
        },
        "editable": True,
        "enabled": True
    },
    # ========================================================
    # VOLATILITY INDICATORS
    # ========================================================
    "ATR": {
        "id":"atr",
        "function": get_atr,
        "display_name": "Average True Range",
        "short_name": "ATR",
        "category": "Volatility",
        "pane": "atr",
        "output": "single",
        "series_type": "line",
        "defaults": {
            "period": 14
        },
        "style": {
            "color": "#FF5722",
            "lineWidth": 2,
            "visible": True
        },
        "editable": True,
        "enabled": True
    },
    # --------------------------------------------------------
    "BOLLINGER_BANDS": {
        "id":"bollinger_bands",
        "function": get_bollinger,
        "display_name": "Bollinger Bands",
        "short_name": "BB",
        "category": "Volatility",
        "pane": "overlay",
        "output": "multi",
        "series_type": "bands",
        "defaults": {
            "period": 20,
            "std": 2
        },
        "style": {
            "upperColor": "#2962FF",
            "middleColor": "#FF9800",
            "lowerColor": "#2962FF",
            "fillColor": "rgba(41,98,255,0.12)",
            "lineWidth": 2
        },
        "editable": True,
        "enabled": True
    },
    # --------------------------------------------------------
    "DONCHIAN_CHANNEL": {
        "id":"doonchian_channel",
        "function": get_donchian,
        "display_name": "Donchian Channel",
        "short_name": "DC",
        "category": "Volatility",
        "pane": "overlay",
        "output": "multi",
        "series_type": "bands",
        "defaults": {
            "period": 20
        },
        "style": {
            "upperColor": "#00BCD4",
            "middleColor": "#9E9E9E",
            "lowerColor": "#00BCD4",
            "fillColor": "rgba(0,188,212,0.10)",
            "lineWidth": 2
        },
        "editable": True,
        "enabled": True
    },
    # --------------------------------------------------------
    "KELTNER_CHANNEL": {
        "id":"keltner_channel",
        "function": get_keltner,
        "display_name": "Keltner Channel",
        "short_name": "KC",
        "category": "Volatility",
        "pane": "overlay",
        "output": "multi",
        "series_type": "bands",
        "defaults": {
            "period": 20,
            "atr_period": 10,
            "multiplier": 2
        },
        "style": {
            "upperColor": "#4CAF50",
            "middleColor": "#FFC107",
            "lowerColor": "#4CAF50",
            "fillColor": "rgba(76,175,80,0.12)",
            "lineWidth": 2
        },
        "editable": True,
        "enabled": True
    }
}

# ============================================================
# Registry Metadata (Frontend Safe)
# ============================================================

def get_registry_metadata():
    """
    Returns indicator metadata for frontend.

    Removes non-serializable fields like function references.
    """

    registry = {}

    for name, indicator in INDICATOR_MAP.items():

        registry[name] = {
            key: value
            for key, value in indicator.items()
            if key != "function"
        }

    return registry