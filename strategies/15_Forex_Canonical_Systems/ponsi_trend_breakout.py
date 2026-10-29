"""
strategies/ponsi_trend_breakout.py
Edward Ponsi's 21/55 EMA Value Zone Pullback and RSI Divergence Strategy.
From 'Forex Patterns and Probabilities' (John Wiley & Sons).
"""

from typing import Dict, Optional, Any
import numpy as np
import pandas as pd
from strategies.base_strategy import BaseStrategy


class PonsiTrendStrategy(BaseStrategy):
    """
    Implements Edward Ponsi's Dual EMA Value-Zone strategy with RSI momentum validation.
    """

    def __init__(
        self,
        fast_ema_period: int = 21,
        slow_ema_period: int = 55,
        rsi_period: int = 14,
        confidence_threshold: float = 0.70,
    ):
        super().__init__()
        self.name = "ponsi_trend_breakout"
        self.fast_ema_period = fast_ema_period
        self.slow_ema_period = slow_ema_period
        self.rsi_period = rsi_period
        self.confidence_threshold = confidence_threshold

    def generate_signal(self, data: pd.DataFrame) -> Optional[Dict[str, Any]]:
        """
        Scans for pullbacks into the 21/55 EMA value zone with RSI confirmation.
        """
        if len(data) < self.slow_ema_period + 10:
            return None

        close = data["close"]
        high = data["high"]
        low = data["low"]

        # Compute EMAs
        ema_fast = close.ewm(span=self.fast_ema_period, adjust=False).mean()
        ema_slow = close.ewm(span=self.slow_ema_period, adjust=False).mean()

        curr_close = float(close.iloc[-1])
        curr_high = float(high.iloc[-1])
        curr_low = float(low.iloc[-1])
        curr_fast = float(ema_fast.iloc[-1])
        curr_slow = float(ema_slow.iloc[-1])

        # Compute RSI
        delta = close.diff()
        gain = delta.clip(lower=0).rolling(self.rsi_period).mean()
        loss = (-delta.clip(upper=0)).rolling(self.rsi_period).mean()
        rs = gain / (loss + 1e-10)
        rsi = 100 - (100 / (1 + rs))
        curr_rsi = float(rsi.iloc[-1])

        # Value zone definition: band between EMA 21 and EMA 55
        upper_zone = max(curr_fast, curr_slow)
        lower_zone = min(curr_fast, curr_slow)

        # Bullish setup: 21 > 55, price tests value zone and bounces
        if curr_fast > curr_slow:
            in_value_zone = curr_low <= upper_zone and curr_close >= lower_zone
            bouncing_up = curr_close > curr_fast and float(close.iloc[-2]) <= curr_fast
            if (in_value_zone or bouncing_up) and curr_rsi >= 45:
                return {
                    "strategy": self.name,
                    "direction": "buy",
                    "confidence": 0.82 if curr_rsi > 50 else 0.72,
                    "rationale": f"Ponsi Bullish Value Zone bounce (EMA 21/55) with RSI={curr_rsi:.1f}",
                    "stop_loss": lower_zone - (upper_zone - lower_zone) * 0.5,
                    "take_profit": curr_close + (curr_close - lower_zone) * 1.8,
                }

        # Bearish setup: 21 < 55, price tests value zone and rejects
        elif curr_fast < curr_slow:
            in_value_zone = curr_high >= lower_zone and curr_close <= upper_zone
            rejecting_down = curr_close < curr_fast and float(close.iloc[-2]) >= curr_fast
            if (in_value_zone or rejecting_down) and curr_rsi <= 55:
                return {
                    "strategy": self.name,
                    "direction": "sell",
                    "confidence": 0.82 if curr_rsi < 50 else 0.72,
                    "rationale": f"Ponsi Bearish Value Zone rejection (EMA 21/55) with RSI={curr_rsi:.1f}",
                    "stop_loss": upper_zone + (upper_zone - lower_zone) * 0.5,
                    "take_profit": curr_close - (upper_zone - curr_close) * 1.8,
                }

        return None
