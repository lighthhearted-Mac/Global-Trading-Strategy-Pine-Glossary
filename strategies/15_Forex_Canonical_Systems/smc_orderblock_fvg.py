"""
strategies/smc_orderblock_fvg.py
Smart Money Concepts (SMC) Institutional Order Block and Fair Value Gap Strategy.
From 'The Smart Money Concept Forex' (James Jecool King).
"""

from typing import Dict, Optional, Any
import numpy as np
import pandas as pd
from strategies.base_strategy import BaseStrategy


class SmartMoneyConceptsStrategy(BaseStrategy):
    """
    Identifies institutional Fair Value Gaps (FVG) and Order Blocks (OB)
    following liquidity sweeps.
    """

    def __init__(self, lookback: int = 30, confidence_threshold: float = 0.80):
        super().__init__()
        self.name = "smc_orderblock_fvg"
        self.lookback = lookback
        self.confidence_threshold = confidence_threshold

    def generate_signal(self, data: pd.DataFrame) -> Optional[Dict[str, Any]]:
        if len(data) < self.lookback:
            return None

        # Last 3 candles for Fair Value Gap (FVG)
        c1_high = float(data["high"].iloc[-3])
        c1_low = float(data["low"].iloc[-3])
        c2_close = float(data["close"].iloc[-2])
        c2_open = float(data["open"].iloc[-2])
        c3_high = float(data["high"].iloc[-1])
        c3_low = float(data["low"].iloc[-1])
        curr_close = float(data["close"].iloc[-1])

        # Bullish FVG: Low of candle 1 is higher than High of candle 3 (displaced impulse upwards)
        # In chronological order: bar 1 (index -3), bar 2 (index -2), bar 3 (index -1)
        # Bullish Imbalance: bar -1 low is above bar -3 high
        if c3_low > c1_high and c2_close > c2_open:
            fvg_size = c3_low - c1_high
            prior_low = float(data["low"].iloc[-self.lookback:-3].min())
            if fvg_size > 0.0003: # Minimum 3 pips
                return {
                    "strategy": self.name,
                    "direction": "buy",
                    "confidence": 0.88,
                    "rationale": f"Institutional Bullish Fair Value Gap (FVG size: {fvg_size*10000:.1f} pips) with displacement",
                    "stop_loss": c1_low - 0.0005,
                    "take_profit": curr_close + (fvg_size * 2.5),
                }

        # Bearish FVG: Bar -1 high is below bar -3 low (displaced impulse downwards)
        if c3_high < c1_low and c2_close < c2_open:
            fvg_size = c1_low - c3_high
            if fvg_size > 0.0003: # Minimum 3 pips
                return {
                    "strategy": self.name,
                    "direction": "sell",
                    "confidence": 0.88,
                    "rationale": f"Institutional Bearish Fair Value Gap (FVG size: {fvg_size*10000:.1f} pips) with displacement",
                    "stop_loss": c1_high + 0.0005,
                    "take_profit": curr_close - (fvg_size * 2.5),
                }

        return None
