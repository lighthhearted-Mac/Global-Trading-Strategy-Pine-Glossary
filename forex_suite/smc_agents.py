"""
smc_agents.py — Autonomous Institutional Smart Money Concepts (SMC) & Fair Value Gap (FVG) Agents.
Upgrades static heuristic indicators into stateful, lifecycle-aware trading agents.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any
import numpy as np
import pandas as pd

from core.models import Proposal


def get_pip_size(symbol: str) -> float:
    """Returns pip scaling factor based on Forex asset class convention."""
    sym = (symbol or "").upper().replace("/", "_")
    if "JPY" in sym:
        return 0.01
    elif "XAU" in sym or "GOLD" in sym:
        return 0.10
    return 0.0001


@dataclass
class OrderBlock:
    id: str
    symbol: str
    direction: str  # "bullish" or "bearish"
    top: float
    bottom: float
    timestamp: float
    mitigated: bool = False
    sweep_confirmed: bool = False
    volume_surge: float = 1.0


@dataclass
class FairValueGap:
    id: str
    symbol: str
    direction: str  # "bullish" or "bearish"
    top: float
    bottom: float
    consequent_encroachment: float  # 50% midpoint
    timestamp: float
    status: str = "virgin"  # "virgin", "partially_mitigated", "filled", "invalidated"
    size_pips: float = 0.0


class SMCOrderBlockAgent:
    """
    Autonomous Institutional Order Block & Liquidity Sweep Agent.
    Maintains memory of active, unmitigated institutional order blocks and validates
    sweeps across London and New York session killzones.
    """

    def __init__(self, swing_lookback: int = 20, pip_size: float = 0.0001):
        self.swing_lookback = swing_lookback
        self.pip_size = pip_size
        self.active_blocks: Dict[str, List[OrderBlock]] = {}

    def scan_and_evaluate(self, symbol: str, df: pd.DataFrame, current_hour_utc: Optional[int] = None) -> List[Proposal]:
        """
        Scans for liquidity sweeps, Change of Character (CHoCH), and Order Block retests.
        Emits high-conviction institutional proposals.
        """
        if len(df) < self.swing_lookback + 2:
            return []

        if symbol not in self.active_blocks:
            self.active_blocks[symbol] = []

        proposals = []
        high = df["high"]
        low = df["low"]
        close = df["close"]
        open_px = df["open"]
        vol = df["volume"] if "volume" in df.columns else pd.Series([1000] * len(df))

        # Check Killzone: London Open (07-10 UTC) or NY Open (12-16 UTC)
        in_killzone = True
        if current_hour_utc is not None:
            in_killzone = (7 <= current_hour_utc <= 10) or (12 <= current_hour_utc <= 16)

        curr_close = float(close.iloc[-1])
        curr_high = float(high.iloc[-1])
        curr_low = float(low.iloc[-1])

        pip = get_pip_size(symbol)
        # 1. Update existing Order Blocks: Check for mitigations
        for ob in self.active_blocks[symbol]:
            if not ob.mitigated:
                if ob.direction == "bullish" and curr_low <= ob.top and curr_close >= ob.bottom:
                    ob.mitigated = True
                    # Re-test bounce trigger
                    sl = ob.bottom - (pip * 4)
                    risk = curr_close - sl
                    tp = curr_close + (risk * 2.5) if risk > 0 else curr_close + (pip * 15)
                    prop = Proposal(
                        id=f"P-SMC-OB-RETEST-{symbol}-{int(df['timestamp'].iloc[-1] if 'timestamp' in df else len(df))}",
                        symbol=symbol,
                        source="smc_orderblock_agent",
                        kind="trade_entry",
                        confidence=0.88 if in_killzone else 0.78,
                        rationale=f"Bullish Order Block Mitigated at {ob.top:.5f} with rejection. Killzone={in_killzone}",
                        payload={
                            "direction": "buy",
                            "strategy": "SMC-ORDER-BLOCK-RETEST",
                            "stop_loss": sl,
                            "take_profit": tp,
                            "order_block_id": ob.id,
                            "killzone": in_killzone,
                        }
                    )
                    proposals.append(prop)
                elif ob.direction == "bearish" and curr_high >= ob.bottom and curr_close <= ob.top:
                    ob.mitigated = True
                    sl = ob.top + (pip * 4)
                    risk = sl - curr_close
                    tp = curr_close - (risk * 2.5) if risk > 0 else curr_close - (pip * 15)
                    prop = Proposal(
                        id=f"P-SMC-OB-RETEST-{symbol}-{int(df['timestamp'].iloc[-1] if 'timestamp' in df else len(df))}",
                        symbol=symbol,
                        source="smc_orderblock_agent",
                        kind="trade_entry",
                        confidence=0.88 if in_killzone else 0.78,
                        rationale=f"Bearish Order Block Mitigated at {ob.bottom:.5f} with rejection. Killzone={in_killzone}",
                        payload={
                            "direction": "sell",
                            "strategy": "SMC-ORDER-BLOCK-RETEST",
                            "stop_loss": sl,
                            "take_profit": tp,
                            "order_block_id": ob.id,
                            "killzone": in_killzone,
                        }
                    )
                    proposals.append(prop)
                elif (ob.direction == "bullish" and curr_close < ob.bottom) or (ob.direction == "bearish" and curr_close > ob.top):
                    # Violated completely
                    ob.mitigated = True

        # 2. Detect New Liquidity Sweeps & Order Blocks
        prior_high = float(high.iloc[-self.swing_lookback:-2].max())
        prior_low = float(low.iloc[-self.swing_lookback:-2].min())
        prev_candle_high = float(high.iloc[-2])
        prev_candle_low = float(low.iloc[-2])
        prev_candle_close = float(close.iloc[-2])

        # Bullish Sweep: Prior swing low swept by wick, candle closed back inside
        bullish_sweep = (prev_candle_low < prior_low) and (prev_candle_close > prior_low)
        displacement_up = curr_close > float(high.iloc[-2]) and (curr_close - float(open_px.iloc[-1])) > (self.pip_size * 5)

        if bullish_sweep and displacement_up:
            ob_id = f"OB-BULL-{symbol}-{len(self.active_blocks[symbol])+1}"
            new_ob = OrderBlock(
                id=ob_id,
                symbol=symbol,
                direction="bullish",
                top=float(high.iloc[-2]),
                bottom=float(low.iloc[-2]),
                timestamp=float(df["timestamp"].iloc[-1] if "timestamp" in df else len(df)),
                sweep_confirmed=True,
                volume_surge=float(vol.iloc[-1] / (vol.rolling(10).mean().iloc[-1] + 1e-10))
            )
            self.active_blocks[symbol].append(new_ob)

            prop = Proposal(
                id=f"P-SMC-SWEEP-{symbol}-{int(new_ob.timestamp)}",
                symbol=symbol,
                source="smc_orderblock_agent",
                kind="trade_entry",
                confidence=0.90 if in_killzone else 0.80,
                rationale=f"SMC Bullish Liquidity Sweep of Swing Low {prior_low:.5f} with violent displacement. Killzone={in_killzone}",
                payload={
                    "direction": "buy",
                    "strategy": "SMC-LIQUIDITY-SWEEP",
                    "stop_loss": new_ob.bottom - (self.pip_size * 3),
                    "take_profit": curr_close + (curr_close - new_ob.bottom) * 2.8,
                    "order_block_id": ob_id,
                    "killzone": in_killzone,
                }
            )
            proposals.append(prop)

        # Bearish Sweep: Prior swing high swept by wick, candle closed back inside
        bearish_sweep = (prev_candle_high > prior_high) and (prev_candle_close < prior_high)
        displacement_down = curr_close < float(low.iloc[-2]) and (float(open_px.iloc[-1]) - curr_close) > (self.pip_size * 5)

        if bearish_sweep and displacement_down:
            ob_id = f"OB-BEAR-{symbol}-{len(self.active_blocks[symbol])+1}"
            new_ob = OrderBlock(
                id=ob_id,
                symbol=symbol,
                direction="bearish",
                top=float(high.iloc[-2]),
                bottom=float(low.iloc[-2]),
                timestamp=float(df["timestamp"].iloc[-1] if "timestamp" in df else len(df)),
                sweep_confirmed=True,
                volume_surge=float(vol.iloc[-1] / (vol.rolling(10).mean().iloc[-1] + 1e-10))
            )
            self.active_blocks[symbol].append(new_ob)

            prop = Proposal(
                id=f"P-SMC-SWEEP-{symbol}-{int(new_ob.timestamp)}",
                symbol=symbol,
                source="smc_orderblock_agent",
                kind="trade_entry",
                confidence=0.90 if in_killzone else 0.80,
                rationale=f"SMC Bearish Liquidity Sweep of Swing High {prior_high:.5f} with violent displacement. Killzone={in_killzone}",
                payload={
                    "direction": "sell",
                    "strategy": "SMC-LIQUIDITY-SWEEP",
                    "stop_loss": new_ob.top + (self.pip_size * 3),
                    "take_profit": curr_close - (new_ob.top - curr_close) * 2.8,
                    "order_block_id": ob_id,
                    "killzone": in_killzone,
                }
            )
            proposals.append(prop)

        # Keep memory clean (max 10 recent order blocks per symbol)
        if len(self.active_blocks[symbol]) > 10:
            self.active_blocks[symbol] = self.active_blocks[symbol][-10:]

        return proposals


class FairValueGapAgent:
    """
    Autonomous Fair Value Gap (FVG) Auction Imbalance Agent.
    Identifies 3-bar institutional imbalances and calculates exact limit execution
    at Consequent Encroachment (50% midpoint) to minimize stop-loss distance.
    """

    def __init__(self, min_fvg_pips: float = 3.0, pip_size: float = 0.0001):
        self.min_fvg_pips = min_fvg_pips
        self.pip_size = pip_size
        self.active_gaps: Dict[str, List[FairValueGap]] = {}

    def scan_and_evaluate(self, symbol: str, df: pd.DataFrame) -> List[Proposal]:
        """
        Scans for 3-bar Fair Value Gaps, calculates Consequent Encroachment (CE),
        and emits high-R limit/entry proposals.
        """
        if len(df) < 3:
            return []

        if symbol not in self.active_gaps:
            self.active_gaps[symbol] = []

        proposals = []
        high = df["high"]
        low = df["low"]
        close = df["close"]
        open_px = df["open"]

        curr_close = float(close.iloc[-1])
        curr_high = float(high.iloc[-1])
        curr_low = float(low.iloc[-1])

        # 1. Update Existing Gaps (check for fills / touches of Consequent Encroachment)
        for fvg in self.active_gaps[symbol]:
            if fvg.status == "virgin":
                if fvg.direction == "bullish":
                    # Retest of Consequent Encroachment (50% level)
                    if curr_low <= fvg.consequent_encroachment and curr_close >= fvg.bottom:
                        fvg.status = "partially_mitigated"
                        prop = Proposal(
                            id=f"P-FVG-CE-FILL-{symbol}-{int(df['timestamp'].iloc[-1] if 'timestamp' in df else len(df))}",
                            symbol=symbol,
                            source="fair_value_gap_agent",
                            kind="trade_entry",
                            confidence=0.86,
                            rationale=f"Bullish FVG Consequent Encroachment (50%) filled at {fvg.consequent_encroachment:.5f} with bounce",
                            payload={
                                "direction": "buy",
                                "strategy": "SMC-FVG-CONSEQUENT-ENCROACHMENT",
                                "stop_loss": fvg.bottom - (self.pip_size * 2),
                                "take_profit": curr_close + (curr_close - fvg.bottom) * 3.0,
                                "fvg_id": fvg.id,
                                "ce_price": fvg.consequent_encroachment,
                            }
                        )
                        proposals.append(prop)
                    elif curr_close < fvg.bottom:
                        fvg.status = "invalidated"
                elif fvg.direction == "bearish":
                    if curr_high >= fvg.consequent_encroachment and curr_close <= fvg.top:
                        fvg.status = "partially_mitigated"
                        prop = Proposal(
                            id=f"P-FVG-CE-FILL-{symbol}-{int(df['timestamp'].iloc[-1] if 'timestamp' in df else len(df))}",
                            symbol=symbol,
                            source="fair_value_gap_agent",
                            kind="trade_entry",
                            confidence=0.86,
                            rationale=f"Bearish FVG Consequent Encroachment (50%) filled at {fvg.consequent_encroachment:.5f} with rejection",
                            payload={
                                "direction": "sell",
                                "strategy": "SMC-FVG-CONSEQUENT-ENCROACHMENT",
                                "stop_loss": fvg.top + (self.pip_size * 2),
                                "take_profit": curr_close - (fvg.top - curr_close) * 3.0,
                                "fvg_id": fvg.id,
                                "ce_price": fvg.consequent_encroachment,
                            }
                        )
                        proposals.append(prop)
                    elif curr_close > fvg.top:
                        fvg.status = "invalidated"

        # 2. Detect Fresh 3-Bar Imbalance (Candles -3, -2, -1)
        c1_high = float(high.iloc[-3])
        c1_low = float(low.iloc[-3])
        c2_open = float(open_px.iloc[-2])
        c2_close = float(close.iloc[-2])
        c3_high = float(high.iloc[-1])
        c3_low = float(low.iloc[-1])

        min_gap_dist = self.min_fvg_pips * self.pip_size

        # Bullish FVG: Low of candle 3 is strictly above High of candle 1
        if (c3_low - c1_high) >= min_gap_dist and (c2_close > c2_open):
            gap_size = c3_low - c1_high
            ce = c1_high + (gap_size * 0.50)
            fvg_id = fvg_id = f"FVG-BULL-{symbol}-{len(self.active_gaps[symbol])+1}"
            fresh_fvg = FairValueGap(
                id=fvg_id,
                symbol=symbol,
                direction="bullish",
                top=c3_low,
                bottom=c1_high,
                consequent_encroachment=ce,
                timestamp=float(df["timestamp"].iloc[-1] if "timestamp" in df else len(df)),
                size_pips=gap_size / self.pip_size
            )
            self.active_gaps[symbol].append(fresh_fvg)

            pip = get_pip_size(symbol)
            sl = fresh_fvg.bottom - (pip * 2)
            risk = curr_close - sl
            tp = curr_close + (risk * 2.5) if risk > 0 else curr_close + (pip * 15)
            prop = Proposal(
                id=f"P-FVG-FRESH-{symbol}-{int(fresh_fvg.timestamp)}",
                symbol=symbol,
                source="fair_value_gap_agent",
                kind="trade_entry",
                confidence=0.85,
                rationale=f"Fresh Bullish FVG Discovered ({fresh_fvg.size_pips:.1f} pips). Limit entry armed at CE={ce:.5f}",
                payload={
                    "direction": "buy",
                    "strategy": "SMC-FVG-IMBALANCE",
                    "stop_loss": sl,
                    "take_profit": tp,
                    "fvg_id": fvg_id,
                    "ce_price": ce,
                }
            )
            proposals.append(prop)

        # Bearish FVG: High of candle 3 is strictly below Low of candle 1
        if (c1_low - c3_high) >= min_gap_dist and (c2_close < c2_open):
            pip = get_pip_size(symbol)
            gap_size = c1_low - c3_high
            ce = c3_high + (gap_size * 0.50)
            fvg_id = f"FVG-BEAR-{symbol}-{len(self.active_gaps[symbol])+1}"
            fresh_fvg = FairValueGap(
                id=fvg_id,
                symbol=symbol,
                direction="bearish",
                top=c1_low,
                bottom=c3_high,
                consequent_encroachment=ce,
                timestamp=float(df["timestamp"].iloc[-1] if "timestamp" in df else len(df)),
                size_pips=gap_size / pip
            )
            self.active_gaps[symbol].append(fresh_fvg)

            sl = fresh_fvg.top + (pip * 2)
            risk = sl - curr_close
            tp = curr_close - (risk * 2.5) if risk > 0 else curr_close - (pip * 15)
            prop = Proposal(
                id=f"P-FVG-FRESH-{symbol}-{int(fresh_fvg.timestamp)}",
                symbol=symbol,
                source="fair_value_gap_agent",
                kind="trade_entry",
                confidence=0.85,
                rationale=f"Fresh Bearish FVG Discovered ({fresh_fvg.size_pips:.1f} pips). Limit entry armed at CE={ce:.5f}",
                payload={
                    "direction": "sell",
                    "strategy": "SMC-FVG-IMBALANCE",
                    "stop_loss": sl,
                    "take_profit": tp,
                    "fvg_id": fvg_id,
                    "ce_price": ce,
                }
            )
            proposals.append(prop)

        # Keep memory clean (max 10 recent FVGs per symbol)
        if len(self.active_gaps[symbol]) > 10:
            self.active_gaps[symbol] = self.active_gaps[symbol][-10:]

        return proposals
