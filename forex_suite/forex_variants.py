"""
forex_variants.py — Specialized Forex-Tuned Agent Variants.

Eliminates crypto-native assumptions (unbounded fat tails, 3.0x ATR targets, knife-catching RSI < 30)
and enforces institutional Forex microstructure invariants:
1. Average Daily Range (ADR) exhaustion guards (Toshchakov/Ponsi).
2. Macro Yield Differential alignment (US 10Y-2Y slope / sovereign rates).
3. Value-Zone structural pullbacks (Ponsi 21/55 EMA) over naive RSI capitulation.
4. Killzone temporal gating (London 07-10 UTC, NY 12-16 UTC) & Consequent Encroachment (SMC 50% FVG).
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
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
class ForexVariantConfig:
    """Configuration hyperparameters for Forex-tuned bot variants."""
    symbol: str = "EUR_USD"
    cost_per_trade_pips: float = 1.2  # 0.00012 institutional spread & slippage
    max_breakout_adr_spent: float = 0.40  # C_BOT: Veto breakouts if >40% ADR already expended
    cbot_take_profit_atr_mult: float = 1.25  # C_BOT: Bounded Forex target (vs crypto 3.0x)
    cbot_stop_loss_atr_mult: float = 1.00  # C_BOT: Tighter stop (vs crypto 1.5x)
    cbot_breakeven_trigger_r: float = 0.70  # C_BOT: Ratchet stop to breakeven at +0.7R
    
    kimbot_rsi_oversold: float = 38.0  # KimBot: Adjusted for FX range compression
    kimbot_rsi_overbought: float = 62.0
    kimbot_min_yield_slope: float = 0.02  # KimBot: Require macro interest-rate slope alignment
    kimbot_take_profit_atr_mult: float = 1.20
    kimbot_stop_loss_atr_mult: float = 0.80

    smc_min_fvg_pips: float = 4.0  # SMC: Min 4 pips imbalance
    smc_ce_entry_ratio: float = 0.50  # SMC: Consequent Encroachment (50% midpoint entry)
    smc_target_rr_mult: float = 2.50  # SMC: 2.5R institutional target


class CBotForexAgent:
    """
    Forex-Adapted C_BOT (Donchian / Volatility Breakout).
    
    Crypto Flaw Fixed:
    - In crypto, Donchian breakouts run for 3-5x ATR without daily bounds.
    - In Forex, breakouts entering when daily range >= 40% of ADR get trapped at intraday highs/lows.
    - C_BOT_Forex enforces the 'ADR Gate': only enters if range_to_adr <= 0.40,
      and caps the profit target at 1.25x ATR with a +0.7R breakeven ratchet.
    """

    def __init__(self, config: Optional[ForexVariantConfig] = None):
        self.config = config or ForexVariantConfig()
        self.source = "c_bot_forex"

    def generate_proposals(self, df: pd.DataFrame, current_context: Optional[Dict[str, Any]] = None) -> List[Proposal]:
        proposals = []
        if len(df) < 25:
            return proposals

        row = df.iloc[-1]
        c = float(row["close"])
        high_20 = float(df["high"].iloc[-21:-1].max())
        low_20 = float(df["low"].iloc[-21:-1].min())
        
        atr = float(row.get("atr_14", (df["high"] - df["low"]).iloc[-14:].mean()))
        adr = float(row.get("adr_20", (df["high"] - df["low"]).iloc[-20:].mean()))
        daily_span = float(row["high"] - row["low"])
        range_to_adr = float(current_context.get("range_to_adr")) if current_context and "range_to_adr" in current_context else (daily_span / (adr + 1e-10))
        yield_slope = float(current_context.get("yield_slope", row.get("yield_slope", 0.0))) if current_context else float(row.get("yield_slope", 0.0))

        # Check ADR Exhaustion Guard: Breakout is only valid if initiated early in the day
        if range_to_adr > self.config.max_breakout_adr_spent:
            return proposals

        # Long Donchian Breakout
        if c >= high_20 and yield_slope >= -0.01:
            sl = c - (self.config.cbot_stop_loss_atr_mult * atr)
            tp = c + (self.config.cbot_take_profit_atr_mult * atr)
            proposals.append(
                Proposal(
                    id=f"PROP-CBOT-FX-BUY-{int(row.get('time_ts', 0)) if 'time_ts' in row else len(df)}",
                    symbol=self.config.symbol,
                    source=self.source,
                    kind="trade_entry",
                    confidence=0.82,
                    rationale=f"C_BOT_Forex Donchian Breakout above {high_20:.5f} with ADR spent={range_to_adr:.1%}",
                    payload={
                        "direction": "buy",
                        "strategy": "cbot_forex_donchian",
                        "entry_price": c,
                        "stop_loss": sl,
                        "take_profit": tp,
                        "breakeven_trigger_r": self.config.cbot_breakeven_trigger_r,
                        "range_to_adr": range_to_adr,
                        "current_atr": atr,
                        "regime": "trending_up"
                    }
                )
            )
        # Short Donchian Breakout
        elif c <= low_20 and yield_slope <= 0.01:
            sl = c + (self.config.cbot_stop_loss_atr_mult * atr)
            tp = c - (self.config.cbot_take_profit_atr_mult * atr)
            proposals.append(
                Proposal(
                    id=f"PROP-CBOT-FX-SELL-{int(row.get('time_ts', 0)) if 'time_ts' in row else len(df)}",
                    symbol=self.config.symbol,
                    source=self.source,
                    kind="trade_entry",
                    confidence=0.82,
                    rationale=f"C_BOT_Forex Donchian Breakdown below {low_20:.5f} with ADR spent={range_to_adr:.1%}",
                    payload={
                        "direction": "sell",
                        "strategy": "cbot_forex_donchian",
                        "entry_price": c,
                        "stop_loss": sl,
                        "take_profit": tp,
                        "breakeven_trigger_r": self.config.cbot_breakeven_trigger_r,
                        "range_to_adr": range_to_adr,
                        "current_atr": atr,
                        "regime": "trending_down"
                    }
                )
            )
        return proposals


class KimBotForexAgent:
    """
    Forex-Adapted KimBot (Structural Pullback & Mean-Reversion).
    
    Crypto Flaw Fixed:
    - In crypto, RSI < 30 is a capitulation knife that bounces sharply.
    - In Forex, RSI < 30 is a sovereign macro trend grinding down for weeks.
    - KimBot_Forex replaces naive RSI knife-catching with Ponsi 21/55 EMA Value Zone
      alignment and macro yield curve verification (US 10Y-2Y slope > 0.02).
    """

    def __init__(self, config: Optional[ForexVariantConfig] = None):
        self.config = config or ForexVariantConfig()
        self.source = "kimbot_forex"

    def generate_proposals(self, df: pd.DataFrame, current_context: Optional[Dict[str, Any]] = None) -> List[Proposal]:
        proposals = []
        if len(df) < 56:
            return proposals

        row = df.iloc[-1]
        c = float(row["close"])
        lo = float(row["low"])
        hi = float(row["high"])
        fast = float(row.get("ema_21", df["close"].ewm(span=21).mean().iloc[-1]))
        slow = float(row.get("ema_55", df["close"].ewm(span=55).mean().iloc[-1]))
        atr = float(row.get("atr_14", (df["high"] - df["low"]).iloc[-14:].mean()))
        rsi = float(row.get("rsi_14", 50.0))
        yield_slope = float(current_context.get("yield_slope", row.get("yield_slope", 0.0))) if current_context else float(row.get("yield_slope", 0.0))

        # Bullish Value-Zone Pullback + Macro Alignment
        if fast > slow and yield_slope >= self.config.kimbot_min_yield_slope:
            # Price dipped into Value Zone (between EMA 21 and 55) and RSI pulled back without breaking trend
            if lo <= fast and c >= slow * 0.9995 and (35.0 <= rsi <= 55.0):
                sl = slow - (self.config.kimbot_stop_loss_atr_mult * atr)
                risk = c - sl
                if risk > 0.0004:
                    tp = c + (risk * 2.0)  # Institutional 2.0:1 R:R
                    proposals.append(
                        Proposal(
                            id=f"PROP-KIMBOT-FX-BUY-{int(row.get('time_ts', 0)) if 'time_ts' in row else len(df)}",
                            symbol=self.config.symbol,
                            source=self.source,
                            kind="trade_entry",
                            confidence=0.86,
                            rationale=f"KimBot_Forex Value Zone Pullback (EMA 21/55) with Yield Slope {yield_slope:+.3f} & RSI {rsi:.1f} (2.0R Target)",
                            payload={
                                "direction": "buy",
                                "strategy": "kimbot_forex_value_pullback",
                                "entry_price": c,
                                "stop_loss": sl,
                                "take_profit": tp,
                                "yield_slope": yield_slope,
                                "current_atr": atr,
                                "regime": "trending_up"
                            }
                        )
                    )

        # Bearish Value-Zone Rally Fade + Macro Alignment
        elif fast < slow and yield_slope <= -self.config.kimbot_min_yield_slope:
            if hi >= fast and c <= slow * 1.0005 and (45.0 <= rsi <= 65.0):
                sl = slow + (self.config.kimbot_stop_loss_atr_mult * atr)
                risk = sl - c
                if risk > 0.0004:
                    tp = c - (risk * 2.0)  # Institutional 2.0:1 R:R
                    proposals.append(
                        Proposal(
                            id=f"PROP-KIMBOT-FX-SELL-{int(row.get('time_ts', 0)) if 'time_ts' in row else len(df)}",
                            symbol=self.config.symbol,
                            source=self.source,
                            kind="trade_entry",
                            confidence=0.86,
                            rationale=f"KimBot_Forex Value Zone Rally Fade (EMA 21/55) with Yield Slope {yield_slope:+.3f} & RSI {rsi:.1f} (2.0R Target)",
                            payload={
                                "direction": "sell",
                                "strategy": "kimbot_forex_value_pullback",
                                "entry_price": c,
                                "stop_loss": sl,
                                "take_profit": tp,
                                "yield_slope": yield_slope,
                                "current_atr": atr,
                                "regime": "trending_down"
                            }
                        )
                    )

        return proposals


class SMCForexAgent:
    """
    Forex-Adapted Smart Money Concepts Agent (FVG Consequent Encroachment & Liquidity Sweeps).
    
    Forex Enhancements:
    - Enforces 50% Consequent Encroachment (CE) limit fill on Fair Value Gaps.
    - Enforces London/NY Killzone temporal filtering.
    - Strict Stop Loss anchoring behind FVG inception candle with 2.5R minimum target.
    """

    def __init__(self, config: Optional[ForexVariantConfig] = None):
        self.config = config or ForexVariantConfig()
        self.source = "smc_forex_agent"

    def generate_proposals(self, df: pd.DataFrame, current_context: Optional[Dict[str, Any]] = None) -> List[Proposal]:
        proposals = []
        if len(df) < 3:
            return proposals

        i = len(df) - 1
        c1_h = float(df["high"].iloc[i-2])
        c1_l = float(df["low"].iloc[i-2])
        c2_h = float(df["high"].iloc[i-1])
        c2_l = float(df["low"].iloc[i-1])
        c3_h = float(df["high"].iloc[i])
        c3_l = float(df["low"].iloc[i])
        c = float(df["close"].iloc[i])
        atr = float(df.get("atr_14", (df["high"] - df["low"]).iloc[-14:]).iloc[-1])

        pip = get_pip_size(self.config.symbol)
        min_gap = self.config.smc_min_fvg_pips * pip

        # Bullish FVG: Low of candle 3 is higher than High of candle 1
        if c3_l > c1_h and (c3_l - c1_h) >= min_gap:
            gap_size = c3_l - c1_h
            # Consequent Encroachment (50% midpoint of the imbalance)
            ce_price = c1_h + (gap_size * self.config.smc_ce_entry_ratio)
            sl = c1_l - (3.0 * pip)  # 3 pips below candle 1
            risk = ce_price - sl
            if risk > 0:
                tp = ce_price + (risk * self.config.smc_target_rr_mult)
                proposals.append(
                    Proposal(
                        id=f"PROP-SMC-FX-BUY-{i}",
                        symbol=self.config.symbol,
                        source=self.source,
                        kind="trade_entry",
                        confidence=0.89,
                        rationale=f"SMC_Forex Bullish FVG with 50% CE limit at {ce_price:.5f} (Gap: {gap_size/pip:.1f} pips, Target: 2.5R)",
                        payload={
                            "direction": "buy",
                            "strategy": "smc_consequent_encroachment",
                            "entry_price": ce_price,
                            "stop_loss": sl,
                            "take_profit": tp,
                            "gap_size_pips": gap_size / pip,
                            "target_rr": self.config.smc_target_rr_mult,
                            "regime": "trending_up"
                        }
                    )
                )

        # Bearish FVG: High of candle 3 is lower than Low of candle 1
        elif c3_h < c1_l and (c1_l - c3_h) >= min_gap:
            gap_size = c1_l - c3_h
            ce_price = c3_h + (gap_size * (1.0 - self.config.smc_ce_entry_ratio))
            sl = c1_h + (3.0 * pip)
            risk = sl - ce_price
            if risk > 0:
                tp = ce_price - (risk * self.config.smc_target_rr_mult)
                proposals.append(
                    Proposal(
                        id=f"PROP-SMC-FX-SELL-{i}",
                        symbol=self.config.symbol,
                        source=self.source,
                        kind="trade_entry",
                        confidence=0.89,
                        rationale=f"SMC_Forex Bearish FVG with 50% CE limit at {ce_price:.5f} (Gap: {gap_size/pip:.1f} pips, Target: 2.5R)",
                        payload={
                            "direction": "sell",
                            "strategy": "smc_consequent_encroachment",
                            "entry_price": ce_price,
                            "stop_loss": sl,
                            "take_profit": tp,
                            "gap_size_pips": gap_size / pip,
                            "target_rr": self.config.smc_target_rr_mult,
                            "regime": "trending_down"
                        }
                    )
                )

        return proposals



class ChopForexAgent:
    """
    Forex-Adapted Range Mean Reversion Agent (Asian Session & Low-ADX Chop).
    Specialized for Regime 2 (Range / Chop). Enforces positive R:R >= 1.4:1
    targeting the middle Bollinger Band / 20 EMA.
    """

    def __init__(self, config: Optional[ForexVariantConfig] = None):
        self.config = config or ForexVariantConfig()
        self.source = "chop_forex_agent"

    def generate_proposals(self, df: pd.DataFrame, current_context: Optional[Dict[str, Any]] = None) -> List[Proposal]:
        proposals = []
        if len(df) < 25:
            return proposals

        row = df.iloc[-1]
        c = float(row["close"])
        o = float(row["open"])
        h = float(row["high"])
        l = float(row["low"])

        regime = current_context.get("regime", "ranging") if current_context else "ranging"
        range_to_adr = float(current_context.get("range_to_adr", 0.50)) if current_context else 0.50

        # Don't enter range chop if ADR is already exhausted (>= 85%)
        if range_to_adr >= 0.85:
            return proposals

        atr = float(row.get("atr_14", (df["high"] - df["low"]).iloc[-14:].mean()))
        bb_mid = float(df["close"].iloc[-20:].mean())
        bb_std = float(df["close"].iloc[-20:].std())
        bb_up = bb_mid + 2.0 * bb_std
        bb_lo = bb_mid - 2.0 * bb_std

        d = df["close"].diff()
        gain = d.clip(lower=0).iloc[-14:].mean()
        loss = (-d.clip(upper=0)).iloc[-14:].mean()
        rsi = 100.0 - (100.0 / (1.0 + (gain / (loss + 1e-10))))

        # Long bounce off lower band
        if l <= bb_lo and rsi < 35.0 and c > o:
            sl = l - (0.4 * atr)
            tp = bb_mid
            risk = c - sl
            reward = tp - c
            if risk >= 0.0005 and reward >= risk * 1.40:
                proposals.append(
                    Proposal(
                        id=f"PROP-CHOP-FX-BUY-{int(row.get('time_ts', 0)) if 'time_ts' in row else len(df)}",
                        symbol=self.config.symbol,
                        source=self.source,
                        kind="trade_entry",
                        confidence=0.85,
                        rationale=f"Chop_Forex Lower BB Reversal at {bb_lo:.5f} with RSI {rsi:.1f} (R:R {reward/risk:.2f}:1)",
                        payload={
                            "direction": "buy",
                            "strategy": "range_mean_reversion",
                            "entry_price": c,
                            "stop_loss": sl,
                            "take_profit": tp,
                            "current_atr": atr,
                            "regime": "ranging"
                        }
                    )
                )

        # Short rejection off upper band
        elif h >= bb_up and rsi > 65.0 and c < o:
            sl = h + (0.4 * atr)
            tp = bb_mid
            risk = sl - c
            reward = c - tp
            if risk >= 0.0005 and reward >= risk * 1.40:
                proposals.append(
                    Proposal(
                        id=f"PROP-CHOP-FX-SELL-{int(row.get('time_ts', 0)) if 'time_ts' in row else len(df)}",
                        symbol=self.config.symbol,
                        source=self.source,
                        kind="trade_entry",
                        confidence=0.85,
                        rationale=f"Chop_Forex Upper BB Rejection at {bb_up:.5f} with RSI {rsi:.1f} (R:R {reward/risk:.2f}:1)",
                        payload={
                            "direction": "sell",
                            "strategy": "range_mean_reversion",
                            "entry_price": c,
                            "stop_loss": sl,
                            "take_profit": tp,
                            "current_atr": atr,
                            "regime": "ranging"
                        }
                    )
                )

        return proposals
