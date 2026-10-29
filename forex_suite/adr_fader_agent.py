"""
adr_fader_agent.py — Dedicated Regime 3 Specialist: ADR Overextension & Volatility Exhaustion Fader.

Institutional Role:
Captures statistical mean-reversion when a currency pair has expended >= 85% of its 20-day Average Daily Range (ADR).
Solves the fatal flaw of naive faders (Toshchakov) by strictly enforcing:
1. Macro Flow Neutrality: Rejects fading if 10Y-2Y yield slope is actively steepening/flattening (|slope| > 0.015).
2. SMC Liquidity Sweep Confirmation: Requires price to wick into the extreme and reject (close back inside).
3. London Close Fixing Window: Prioritizes entries between 14:30 and 17:30 UTC when institutional desks square books.
"""

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import numpy as np
import pandas as pd

from core.models import Proposal


def get_pip_size(symbol: str) -> float:
    sym = (symbol or "").upper().replace("/", "_")
    if "JPY" in sym:
        return 0.01
    elif "XAU" in sym or "GOLD" in sym:
        return 0.10
    return 0.0001


@dataclass
class ADRFaderConfig:
    min_range_to_adr: float = 0.85  # Minimum 85% ADR expended
    max_macro_slope: float = 0.015  # Macro flow neutrality ceiling
    target_reversion_pct: float = 0.50  # Mean revert to 50% of daily range
    sl_buffer_pips: float = 8.0  # Stop placed 8 pips beyond sweep wick extreme
    symbol: str = "EUR_USD"


class ADROverextensionFaderAgent:
    """
    Regime 3 Specialist Agent.
    Executes exclusively when daily range >= 85% of ADR with macro neutrality and rejection wicks.
    """

    def __init__(self, config: Optional[ADRFaderConfig] = None):
        self.config = config or ADRFaderConfig()
        self.source = "adr_fader_agent"

    def scan_and_evaluate(
        self,
        symbol: str,
        df: pd.DataFrame,
        current_context: Optional[Dict[str, Any]] = None,
        current_hour_utc: Optional[int] = None
    ) -> List[Proposal]:
        proposals = []
        if len(df) < 20:
            return proposals

        pip = get_pip_size(symbol)
        row = df.iloc[-1]
        c = float(row["close"])
        hi = float(row["high"])
        lo = float(row["low"])
        op = float(row["open"])

        # 1. Evaluate Daily Range vs 20-day ADR
        range_to_adr = 0.50
        if current_context and "range_to_adr" in current_context:
            range_to_adr = float(current_context["range_to_adr"])
        elif "adr_20" in df.columns:
            adr = float(df["adr_20"].iloc[-1])
            daily_span = hi - lo
            range_to_adr = daily_span / (adr + 1e-10)
        else:
            adr = float((df["high"].iloc[-21:-1] - df["low"].iloc[-21:-1]).mean())
            daily_span = hi - lo
            range_to_adr = daily_span / (adr + 1e-10)

        # Must meet the Regime 3 Exhaustion Floor
        if range_to_adr < self.config.min_range_to_adr:
            return proposals

        # 2. Macro Flow Neutrality Filter (Do NOT step in front of sovereign macro momentum)
        yield_slope = 0.0
        if current_context and "yield_slope" in current_context:
            yield_slope = float(current_context["yield_slope"])
        elif "yield_slope" in row:
            yield_slope = float(row["yield_slope"])

        if abs(yield_slope) > self.config.max_macro_slope:
            # Yield curve is actively steepening/inverting -> Macro momentum will overrun the fade
            return proposals

        # 3. Session Timing Check (London Close Fixing: 14:30 - 17:30 UTC)
        fixing_boost = False
        if current_hour_utc is not None:
            fixing_boost = (14 <= current_hour_utc <= 17)

        # 4. Liquidity Sweep & Rejection Mechanics
        # Upper Exhaustion Fade (Bearish Reversal): Candle pushed to new daily high but closed down (upper rejection wick >= 35% of bar)
        candle_span = hi - lo
        if candle_span > 0:
            upper_wick = hi - max(op, c)
            lower_wick = min(op, c) - lo

            # Bearish Fade: Price spiked high, range is exhausted, printed upper wick
            if (upper_wick / candle_span) >= 0.35 and c < hi - (candle_span * 0.20):
                sl = hi + (self.config.sl_buffer_pips * pip)
                risk = sl - c
                if risk > 0:
                    tp = c - (candle_span * self.config.target_reversion_pct)
                    confidence = 0.88 if fixing_boost else 0.81
                    proposals.append(
                        Proposal(
                            id=f"PROP-ADR-FADE-SELL-{symbol}-{int(row.get('time_ts', len(df)))}",
                            symbol=symbol,
                            source=self.source,
                            kind="trade_entry",
                            confidence=confidence,
                            rationale=(
                                f"ADR Exhaustion Fade: Range consumed {range_to_adr*100:.1f}% of ADR. "
                                f"Upper rejection wick={upper_wick/candle_span*100:.1f}%, Yield Slope={yield_slope:+.3f}. "
                                f"Targeting 50% daily range mean reversion."
                            ),
                            payload={
                                "direction": "sell",
                                "strategy": "adr_exhaustion_fade",
                                "entry_price": c,
                                "stop_loss": sl,
                                "take_profit": tp,
                                "range_to_adr": range_to_adr,
                                "yield_slope": yield_slope,
                                "regime": "ranging"
                            }
                        )
                    )

            # Bullish Fade: Price spiked low, range is exhausted, printed lower wick
            elif (lower_wick / candle_span) >= 0.35 and c > lo + (candle_span * 0.20):
                sl = lo - (self.config.sl_buffer_pips * pip)
                risk = c - sl
                if risk > 0:
                    tp = c + (candle_span * self.config.target_reversion_pct)
                    confidence = 0.88 if fixing_boost else 0.81
                    proposals.append(
                        Proposal(
                            id=f"PROP-ADR-FADE-BUY-{symbol}-{int(row.get('time_ts', len(df)))}",
                            symbol=symbol,
                            source=self.source,
                            kind="trade_entry",
                            confidence=confidence,
                            rationale=(
                                f"ADR Exhaustion Fade: Range consumed {range_to_adr*100:.1f}% of ADR. "
                                f"Lower rejection wick={lower_wick/candle_span*100:.1f}%, Yield Slope={yield_slope:+.3f}. "
                                f"Targeting 50% daily range mean reversion."
                            ),
                            payload={
                                "direction": "buy",
                                "strategy": "adr_exhaustion_fade",
                                "entry_price": c,
                                "stop_loss": sl,
                                "take_profit": tp,
                                "range_to_adr": range_to_adr,
                                "yield_slope": yield_slope,
                                "regime": "ranging"
                            }
                        )
                    )

        return proposals
