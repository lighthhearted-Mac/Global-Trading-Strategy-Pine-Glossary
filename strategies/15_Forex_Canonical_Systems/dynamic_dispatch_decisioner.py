"""
decisioner.py — Pure-function Decision Engine.

Role: Adjudicates all evidence to produce ranked, actionable Decisions.
Invariants:
1. Pure function: Same inputs -> same rulings. No I/O, no network, no state mutation.
2. Two-stage sizing: Decisioner asks for size; RiskManager caps it.
3. Multi-criteria filtering: Falsified proposals or sub-threshold scores produce "no_action".
4. Capacity ranking: When candidates exceed available slots, ranks and allocates top N,
   preserving passed-over candidates in `declined_candidates` as shadow trades for attribution.
"""

import time
from typing import Any, Optional
import numpy as np

from core.models import Decision, Falsification, Proposal


class Decisioner:
    """Pure-function judge and priority allocator."""

    def __init__(
        self,
        confidence_floor: float = 0.45,
        quality_floor: float = 0.35,
        uncertainty_max: float = 0.55,
        base_risk_pct: float = 0.01,  # 1% base equity request
    ):
        self.confidence_floor = confidence_floor
        self.quality_floor = quality_floor
        self.uncertainty_max = uncertainty_max
        self.base_risk_pct = base_risk_pct

    def decide(
        self,
        cycle_id: str,
        proposals: list[Proposal],
        falsifications: dict[str, Falsification],
        risk_precheck: dict[str, dict[str, Any]],
        portfolio_state: dict[str, Any],
        scheduler_state: dict[str, Any],
        attribution_history: list[dict[str, Any]],
        market_context: dict[str, dict[str, Any]],
    ) -> list[Decision]:
        """
        Pure function transforming multi-agent cycle evidence into Decisions.
        """
        available_slots = portfolio_state.get("available_slots", 3)
        open_positions = portfolio_state.get("open_positions", {})
        candidates = []

        # Calculate prior win-rate from attribution history if available
        prior_win_rate = 0.50
        if attribution_history:
            wins = sum(1 for a in attribution_history if a.get("r", 0.0) > 0)
            prior_win_rate = float(wins / len(attribution_history))

        for p in proposals:
            f = falsifications.get(p.id)
            ctx = market_context.get(p.symbol, {})
            risk_chk = risk_precheck.get(p.symbol, {"tradeable": True})

            current_price = ctx.get("price", p.payload.get("current_price", 100.0))
            current_atr = ctx.get("atr", p.payload.get("current_atr", current_price * 0.01))
            regime = ctx.get("regime", p.payload.get("regime", "ranging"))
            quality = ctx.get("quality", p.payload.get("quality", 0.50))
            uncertainty_std = ctx.get("uncertainty_std", 0.10)

            # Check criteria
            falsified = f.verdict == "falsified" if f else False
            sceptic_ok = not falsified
            conf_ok = p.confidence >= self.confidence_floor
            qual_ok = quality >= self.quality_floor
            # For specialized engines with dedicated geometry, subsignal dispersion is expected (e.g. rally fade)
            unc_ok = (uncertainty_std <= self.uncertainty_max) or (p.source in ("bear_hammer", "bulkowski_encyclopedia", "sovereign_fx_desk", "altfins", "forex_mechanical_desk", "smc_orderblock_agent", "fair_value_gap_agent"))
            tradeable = risk_chk.get("tradeable", True)

            # Exclude already-open symbols from new entry
            not_open = p.symbol not in open_positions

            if conf_ok and qual_ok and unc_ok and sceptic_ok and tradeable and not_open:
                # Multi-Regime Dynamic Dispatch Multiplier (Tournament Calibrated)
                regime_mult = 1.0
                strat_tag = str(p.payload.get("strategy", p.source)).lower()
                range_to_adr = float(ctx.get("range_to_adr", 0.50))

                # Regime 1: Trend Expansion -> Boost breakout & value zone, penalize counter-trend
                if regime in ("trending_up", "trending_down"):
                    if any(k in strat_tag for k in ["breakout", "donchian", "ponsi", "trend", "gmma", "cbot", "turtle"]):
                        regime_mult = 1.45
                    elif any(k in strat_tag for k in ["reversion", "counter", "fade", "kimbot"]):
                        regime_mult = 0.65

                # Regime 2: Mean-Reversion / Range Chop -> Boost range fades & macro yield, penalize breakout
                elif regime in ("ranging", "choppy"):
                    if any(k in strat_tag for k in ["reversion", "value", "macro", "gem_4x", "fade", "toshchakov"]):
                        regime_mult = 1.40
                    elif any(k in strat_tag for k in ["breakout", "donchian", "cbot"]):
                        regime_mult = 0.65

                # Regime 3: Volatility & ADR Exhaustion -> Boost SMC institutional orderblocks & FVGs
                if range_to_adr >= 0.85:
                    if any(k in strat_tag for k in ["smc", "fvg", "orderblock", "liquidity_sweep", "igrok"]):
                        regime_mult = max(regime_mult, 1.55)

                # Regime 4: Macro Yield Flow -> Boost yield-directed flows
                if "macro" in strat_tag or "gem_4x" in strat_tag or float(ctx.get("yield_slope", 0.0)) > 0.03:
                    if "macro" in strat_tag or "gem_4x" in strat_tag or "pullback" in strat_tag:
                        regime_mult = max(regime_mult, 1.40)

                # Continuous composite score for ranking with Dynamic Dispatch
                rank_score = (
                    p.confidence
                    * quality
                    * (1.0 - uncertainty_std)
                    * (0.8 + 0.4 * prior_win_rate)
                    * regime_mult
                )

                # Direction determination (respect payload direction if explicitly defined by specialized agent)
                payload_dir = str(p.payload.get("direction", "")).lower()
                if payload_dir in ("short", "sell"):
                    side = "short"
                elif payload_dir in ("long", "buy"):
                    side = "long"
                else:
                    side = "long" if p.confidence > 0 else "short"

                # Stop distance & Target distance (use specialized setup geometry if available, else 1.5/2.5 ATR)
                if "stop_price" in p.payload and p.payload["stop_price"] is not None:
                    stop_dist = abs(current_price - float(p.payload["stop_price"]))
                elif "risk_distance" in p.payload:
                    stop_dist = float(p.payload["risk_distance"])
                else:
                    stop_dist = current_atr * 1.5

                if "take_profit" in p.payload and p.payload["take_profit"] is not None:
                    target_dist = abs(current_price - float(p.payload["take_profit"]))
                else:
                    target_dist = current_atr * 2.5

                # Dynamic Conviction-Scaled Sizing (Half-Kelly principle: go harder on high-conviction institutional setups)
                # Multiplier scales smoothly from 0.6x (at baseline threshold) to 1.6x-2.0x (at high conviction >= 0.85)
                excess_conf = max(0.0, abs(p.confidence) - self.confidence_floor) / (1.0 - self.confidence_floor)
                conviction_mult = float(np.clip(0.6 + 1.4 * (excess_conf ** 1.2), 0.5, 2.0))
                size_req = self.base_risk_pct * conviction_mult

                candidates.append({
                    "proposal": p,
                    "rank_score": rank_score,
                    "side": side,
                    "size_request": size_req,
                    "stop_distance": stop_dist,
                    "target_distance": target_dist,
                    "quality": quality,
                    "uncertainty_std": uncertainty_std,
                    "regime": regime,
                    "falsification": f,
                })

        if not candidates:
            return []

        # Sort descending by composite score
        candidates.sort(key=lambda c: c["rank_score"], reverse=True)

        taken_records = candidates[:available_slots]
        declined_records = candidates[available_slots:]

        # Serialized shadow metadata for declined candidates
        declined_payload = [
            {
                "symbol": d["proposal"].symbol,
                "score": d["rank_score"],
                "confidence": d["proposal"].confidence,
                "reason": "capacity_exceeded_available_slots",
            }
            for d in declined_records
        ]

        decisions = []
        for i, c in enumerate(taken_records, start=1):
            p = c["proposal"]
            f = c["falsification"]

            d = Decision(
                cycle_id=cycle_id,
                symbol=p.symbol,
                action="enter",
                side=c["side"],
                size_request=c["size_request"],
                stop_distance=c["stop_distance"],
                target_distance=c["target_distance"],
                priority=i,
                confidence=p.confidence,
                quality=c["quality"],
                regime_interpretation=c["regime"],
                evidence={
                    "proposal_id": p.id,
                    "rank_score": c["rank_score"],
                    "uncertainty_std": c["uncertainty_std"],
                    "sceptic_verdict": f.verdict if f else "untested",
                },
                reasoning=(
                    f"Approved candidate #{i} for {p.symbol}. "
                    f"Conviction={p.confidence:.2f}, Regime={c['regime']}, "
                    f"Sceptic={f.verdict if f else 'untested'}."
                ),
                declined_candidates=declined_payload,
            )
            decisions.append(d)

        return decisions
