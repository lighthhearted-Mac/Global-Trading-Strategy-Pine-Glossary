"""
strategies/toshchakov_adr_igrok.py
Igor Toshchakov's Average Daily Range (ADR) Exhaustion and Session Timing Strategy.
From 'Beat the Odds in Forex Trading' (John Wiley & Sons).
"""

from typing import Dict, Optional, Any
import numpy as np
import pandas as pd
from strategies.base_strategy import BaseStrategy


class ToshchakovADRStrategy(BaseStrategy):
    """
    Implements Igor Toshchakov's Igrok Method: Fades moves when daily expansion
    hits >= 90% of the 20-day Average Daily Range (ADR).
    """

    def __init__(
        self,
        adr_period: int = 20,
        adr_threshold_pct: float = 0.90,
        confidence_threshold: float = 0.75,
    ):
        super().__init__()
        self.name = "toshchakov_adr_igrok"
        self.adr_period = adr_period
        self.adr_threshold_pct = adr_threshold_pct
        self.confidence_threshold = confidence_threshold

    def generate_signal(self, data: pd.DataFrame) -> Optional[Dict[str, Any]]:
        if len(data) < self.adr_period + 5:
            return None

        # Approximate daily range if intraday data
        high = data["high"]
        low = data["low"]
        close = data["close"]

        # 20-period range
        daily_ranges = high - low
        adr = float(daily_ranges.rolling(self.adr_period).mean().iloc[-1])
        if adr <= 0:
            return None

        recent_low = float(low.iloc[-self.adr_period:].min())
        recent_high = float(high.iloc[-self.adr_period:].max())
        curr_span = recent_high - recent_low
        curr_close = float(close.iloc[-1])

        # Exhaustion to upside -> Mean Reversion Sell
        if curr_span >= adr * self.adr_threshold_pct and (recent_high - curr_close) <= (adr * 0.15):
            return {
                "strategy": self.name,
                "direction": "sell",
                "confidence": 0.85,
                "rationale": f"Toshchakov ADR Exhaustion: Span {curr_span:.5f} >= {self.adr_threshold_pct*100}% of ADR {adr:.5f}",
                "stop_loss": recent_high + (adr * 0.20),
                "take_profit": curr_close - (adr * 0.45),
            }

        # Exhaustion to downside -> Mean Reversion Buy
        if curr_span >= adr * self.adr_threshold_pct and (curr_close - recent_low) <= (adr * 0.15):
            return {
                "strategy": self.name,
                "direction": "buy",
                "confidence": 0.85,
                "rationale": f"Toshchakov ADR Exhaustion: Span {curr_span:.5f} >= {self.adr_threshold_pct*100}% of ADR {adr:.5f}",
                "stop_loss": recent_low - (adr * 0.20),
                "take_profit": curr_close + (adr * 0.45),
            }

        return None
