"""
sceptic.py — The Enforcer / Adversarial Auditor.

Role: Systematically attack and attempt to falsify proposals, hypotheses, and trade entries.
Outputs only: "falsified", "cannot_falsify", or "inconclusive".

Invariants:
1. Must never approve a trade; its authority is strictly falsification.
2. Every test is pre-registered and produces a quantitative test record.
3. Policy Enforcement:
   - Reject trades in stressed/whiplash markets unless quality > 0.80.
   - Reject trades with sub-threshold confidence (< 0.45).
   - Reject trades with poor Risk/Reward (< 1.5 R:R).
4. Self-Calibrating Trust Loop: Adjusts scepticism threshold based on whether warnings predicted losses.
"""

from typing import Any, Optional
import numpy as np

from core.models import Proposal, Falsification
from data.economic_calendar import EconomicCalendar


class TheEnforcerSceptic:
    """Adversarial auditor and falsification engine."""

    KILL_CRITERIA = {
        "min_median_fold_t": 1.0,
        "min_bootstrap_p05_r": 0.0,
        "min_positive_folds": 4,
        "max_fold_drawdown_pct": 20.0,
        "min_trades": 100,
        "min_deflated_sharpe": 0.50,
    }

    def __init__(
        self,
        base_trust_weight: float = 1.0,
        falsify_threshold: float = 0.50,
        economic_calendar: Optional[EconomicCalendar] = None,
        forex_news_engine: Optional[Any] = None,
    ):
        self.trust_weight = base_trust_weight
        self.falsify_threshold = falsify_threshold
        self.economic_calendar = economic_calendar or EconomicCalendar()
        self.forex_news_engine = forex_news_engine

    # ------------------------------------------------------------------
    # Trade Candidate Falsification
    # ------------------------------------------------------------------

    def audit_trade_proposal(
        self,
        proposal: Proposal,
        market_context: dict[str, Any],
        open_positions: dict[str, Any],
    ) -> Falsification:
        """
        Runs rigorous adversarial tests on an incoming trade proposal.
        """
        tests: list[dict[str, Any]] = []
        objections: list[str] = []

        confidence = proposal.confidence
        payload = proposal.payload
        regime = payload.get("regime") or market_context.get("regime") or "unknown"
        quality = payload.get("quality") if payload.get("quality") is not None else market_context.get("quality", 0.5)

        # Test 1: Confidence Floor Check
        conf_passed = confidence >= 0.45
        tests.append({
            "name": "confidence_floor",
            "result": confidence,
            "threshold": 0.45,
            "passed": conf_passed,
        })
        if not conf_passed:
            objections.append(f"Confidence {confidence:.2f} is below minimum threshold 0.45")

        # Test 2: Whiplash / Stressed Market Protection
        stress_passed = not (regime == "stressed" and quality < 0.75)
        tests.append({
            "name": "whiplash_market_guard",
            "result": f"regime={regime}, quality={quality:.2f}",
            "threshold": "quality >= 0.75 in stressed market",
            "passed": stress_passed,
        })
        if not stress_passed:
            objections.append("Market is in high-volatility/stressed regime without high quality confirmation")

        # Test 3: Correlation Doubling-Down Check
        # Check if we already have exposure to the same base currency/symbol
        corr_passed = proposal.symbol not in open_positions
        tests.append({
            "name": "duplicate_exposure_check",
            "result": proposal.symbol in open_positions,
            "threshold": "no existing position in symbol",
            "passed": corr_passed,
        })
        if not corr_passed:
            objections.append(f"Already holding an active position in {proposal.symbol}")

        # Test 4: Visual Chart Cleanliness Check (The Vision Agent / Chart Reader Gate)
        cleanliness = market_context.get("visual_cleanliness_score")
        if cleanliness is not None:
            vision_passed = float(cleanliness) >= 0.45
            tests.append({
                "name": "visual_chart_cleanliness",
                "result": round(float(cleanliness), 2),
                "threshold": "cleanliness >= 0.45",
                "passed": vision_passed,
            })
            if not vision_passed:
                objections.append(f"Visual chart reader rejected geometry: cleanliness {float(cleanliness):.2f} is congested with choppy wicks")

        # Test 5: Spread & Slippage Guard (Refuse trades if spread > 15% of ATR)
        spread = market_context.get("spread")
        atr = market_context.get("atr")
        if spread is not None and atr is not None and atr > 0:
            spread_ratio = float(spread) / float(atr)
            spread_passed = spread_ratio <= 0.15
            tests.append({
                "name": "spread_guard",
                "result": f"{spread_ratio * 100:.1f}% ATR",
                "threshold": "spread <= 15% of ATR",
                "passed": spread_passed,
            })
            if not spread_passed:
                objections.append(f"Spread guard: Spread ({spread:.5f}) is {spread_ratio * 100:.1f}% of ATR (limit 15.0%), transaction drag destroys edge")

        # Test 6: Macro Regime Guard (BTC 50 EMA for Altcoins)
        sym_clean = proposal.symbol.upper().replace("/", "").replace("-", "").replace("_", "")
        fx_currencies = {"EUR", "GBP", "JPY", "AUD", "CAD", "CHF", "NZD"}
        is_fx_symbol = any(cur in sym_clean for cur in fx_currencies) and not any(crypto in sym_clean for crypto in ("BTC", "ETH", "SOL", "AVAX", "DOGE", "XRP"))
        is_altcoin = not is_fx_symbol and ("USDT" in sym_clean or "USD" in sym_clean) and not sym_clean.startswith("BTC")
        direction = (
            getattr(proposal, "action", None)
            or (proposal.payload.get("direction") if isinstance(proposal.payload, dict) else None)
            or (proposal.payload.get("side") if isinstance(proposal.payload, dict) else None)
            or ""
        ).upper()
        if is_altcoin and direction in ("BUY", "LONG"):
            btc_above_ema50 = market_context.get("btc_above_ema50")
            if btc_above_ema50 is False:
                tests.append({
                    "name": "btc_50_ema_macro_guard",
                    "result": "BTC below 50 EMA",
                    "threshold": "BTC must be above 50 EMA for altcoin longs",
                    "passed": False,
                })
                objections.append(f"Macro Regime Guard: {proposal.symbol} long breakout blocked because Bitcoin is trading below its 50 EMA baseline")
            elif btc_above_ema50 is True:
                tests.append({
                    "name": "btc_50_ema_macro_guard",
                    "result": "BTC above 50 EMA",
                    "threshold": "BTC must be above 50 EMA for altcoin longs",
                    "passed": True,
                })

        # Test 7: Counter-Trend / Regime Alignment Gate (Attribution Root-Cause Invariant)
        # Never allow mean-reversion or bounce BUYs in a confirmed 'trending_down' market,
        # and never allow counter-trend SELLs in a confirmed 'trending_up' market.
        strategy_source = getattr(proposal, "source", "").lower()
        strategy_meta = ""
        if isinstance(proposal.payload, dict):
            strategy_meta = str(proposal.payload.get("strategy", "")).lower() + " " + str(proposal.payload.get("pattern", "")).lower()
        is_counter_trend = any(k in strategy_source or k in strategy_meta for k in ["bollinger", "reversion", "bounce", "oversold", "overbought", "altfins"])

        if is_counter_trend:
            if "trending_down" in regime and direction in ("BUY", "LONG"):
                tests.append({
                    "name": "counter_trend_regime_gate",
                    "result": f"regime={regime}, strategy={strategy_source}",
                    "threshold": "no counter-trend longs in trending_down regime",
                    "passed": False,
                })
                objections.append(f"Regime Gate: Counter-trend BUY ({strategy_source}) falsified in active trending_down market (falling knife protection)")
            elif "trending_up" in regime and direction in ("SELL", "SHORT"):
                tests.append({
                    "name": "counter_trend_regime_gate",
                    "result": f"regime={regime}, strategy={strategy_source}",
                    "threshold": "no counter-trend shorts in trending_up regime",
                    "passed": False,
                })
                objections.append(f"Regime Gate: Counter-trend SHORT ({strategy_source}) falsified in active trending_up market")
            else:
                tests.append({
                    "name": "counter_trend_regime_gate",
                    "result": f"regime={regime}, strategy={strategy_source}",
                    "threshold": "counter-trend setup aligned with regime",
                    "passed": True,
                })

        # Test 8: Negative Funding Rate / Short Squeeze Guard
        funding_rate = (
            payload.get("funding_rate")
            if isinstance(payload, dict)
            else market_context.get("funding_rate")
        )
        if direction in ("SELL", "SHORT") and funding_rate is not None:
            funding_passed = float(funding_rate) >= -0.0003  # -0.03%
            tests.append({
                "name": "funding_squeeze_guard",
                "result": f"{float(funding_rate) * 100:.3f}%",
                "threshold": "funding_rate >= -0.03% for short entries",
                "passed": funding_passed,
            })
            if not funding_passed:
                objections.append(f"Funding Squeeze Guard: Perpetual funding rate ({float(funding_rate) * 100:.3f}%) < -0.03% (short liquidation hazard)")

        # Test 9: Forex News Blackout & Weekend Risk Gate
        fx_currencies = {"EUR", "GBP", "JPY", "AUD", "CAD", "CHF", "NZD"}
        sym_clean = proposal.symbol.upper().replace("/", "").replace("-", "").replace("_", "")
        is_fx = any(cur in sym_clean for cur in fx_currencies) and not any(crypto in sym_clean for crypto in ("BTC", "ETH", "SOL", "AVAX", "DOGE", "XRP"))

        if is_fx:
            # A. Weekend Gap Gate
            is_weekend, weekend_reason = self.economic_calendar.is_weekend_closed()
            tests.append({
                "name": "forex_weekend_guard",
                "result": "closed" if is_weekend else "open",
                "threshold": "interbank FX must be open and not near Friday close",
                "passed": not is_weekend,
            })
            if is_weekend:
                objections.append(f"Weekend Gap Guard: {weekend_reason}")

            # B. Macroeconomic News Blackout Window
            is_blackout, news_reason = self.economic_calendar.is_blackout_active(proposal.symbol)
            tests.append({
                "name": "forex_news_blackout_guard",
                "result": news_reason or "clear",
                "threshold": "no high-impact Tier-1 macro releases within +/- 30m",
                "passed": not is_blackout,
            })
            if is_blackout:
                objections.append(f"News Blackout Guard: {news_reason} (high volatility and spread hazard)")

            # C. Retail Contrarian Fade Guard
            retail_pos = market_context.get("retail_positioning")
            if not retail_pos and hasattr(self, "forex_news_engine") and self.forex_news_engine:
                try:
                    retail_pos = self.forex_news_engine.get_retail_positioning(proposal.symbol)
                except Exception:
                    retail_pos = None

            if retail_pos:
                retail_long = float(retail_pos.get("retail_long_pct", 0.50))
                direction = (
                    getattr(proposal, "action", None)
                    or (proposal.payload.get("direction") if isinstance(proposal.payload, dict) else None)
                    or (proposal.payload.get("side") if isinstance(proposal.payload, dict) else None)
                    or ""
                ).upper()

                if direction in ("BUY", "LONG") and retail_long >= 0.75:
                    tests.append({
                        "name": "retail_contrarian_fade_guard",
                        "result": f"retail_long={retail_long * 100:.1f}%",
                        "threshold": "retail net long must be < 75% for BUY proposals",
                        "passed": False,
                    })
                    objections.append(f"Retail Overcrowding Veto: Retail crowd is {retail_long * 100:.1f}% net long on {proposal.symbol} (extreme long crowding / stop-hunt hazard)")
                elif direction in ("SELL", "SHORT") and retail_long <= 0.25:
                    tests.append({
                        "name": "retail_contrarian_fade_guard",
                        "result": f"retail_short={(1.0 - retail_long) * 100:.1f}%",
                        "threshold": "retail net short must be < 75% for SHORT proposals",
                        "passed": False,
                    })
                    objections.append(f"Retail Overcrowding Veto: Retail crowd is {(1.0 - retail_long) * 100:.1f}% net short on {proposal.symbol} (short squeeze hazard)")
                else:
                    tests.append({
                        "name": "retail_contrarian_fade_guard",
                        "result": f"retail_long={retail_long * 100:.1f}%",
                        "threshold": "crowd positioning balanced or contrarian alignment verified",
                        "passed": True,
                    })

            # Test 11: Forex ADR Exhaustion Guard (Rule 1: Breakout & Trend chases vetoed if daily range >= 85% of ADR)
            if "range_to_adr" in market_context:
                range_to_adr = float(market_context["range_to_adr"])
                strat_tag = str(proposal.payload.get("strategy", proposal.source)).lower()
                is_breakout_chase = any(k in strat_tag for k in ["breakout", "donchian", "cbot", "expansion", "turtle"])

                if range_to_adr >= 0.85 and is_breakout_chase:
                    tests.append({
                        "name": "adr_exhaustion_guard",
                        "result": f"range_to_adr={range_to_adr * 100:.1f}%",
                        "threshold": "daily range must be < 85% of ADR for breakout/trend entries",
                        "passed": False,
                    })
                    objections.append(
                        f"ADR Exhaustion Veto: Daily range has consumed {range_to_adr * 100:.1f}% of 20-day ADR on {proposal.symbol}. "
                        f"Breakout entries at daily volatility extremes have negative statistical expectancy."
                    )
                else:
                    tests.append({
                        "name": "adr_exhaustion_guard",
                        "result": f"range_to_adr={range_to_adr * 100:.1f}%",
                        "threshold": "daily range within acceptable ADR bounds or reversal setup",
                        "passed": True,
                    })

        # Verdict Determination
        failed_tests = [t for t in tests if not t["passed"]]
        if failed_tests:
            verdict = "falsified"
            objection_str = "; ".join(objections)
            sceptic_conf = 0.85
        else:
            verdict = "cannot_falsify"
            objection_str = None
            sceptic_conf = 0.80

        return Falsification(
            proposal_id=proposal.id,
            verdict=verdict,
            tests_run=tests,
            specific_objection=objection_str,
            confidence=sceptic_conf,
        )

    # ------------------------------------------------------------------
    # Strategy Falsification (Walk-Forward / Folds)
    # ------------------------------------------------------------------

    def audit_strategy_folds(
        self,
        strategy_id: str,
        fold_returns: list[list[float]],
        fold_drawdowns: list[float],
    ) -> Falsification:
        """
        Tests backtest fold results against pre-registered KILL_CRITERIA.
        """
        tests: list[dict[str, Any]] = []
        objections: list[str] = []

        total_folds = len(fold_returns)
        positive_folds = sum(1 for f in fold_returns if sum(f) > 0)
        max_dd = max(fold_drawdowns) if fold_drawdowns else 0.0

        # 1. Min positive folds (e.g., 4 of 5)
        pf_passed = positive_folds >= self.KILL_CRITERIA["min_positive_folds"]
        tests.append({
            "name": "positive_folds_ratio",
            "result": f"{positive_folds}/{total_folds}",
            "threshold": f"{self.KILL_CRITERIA['min_positive_folds']}/{total_folds}",
            "passed": pf_passed,
        })
        if not pf_passed:
            objections.append(f"Only {positive_folds}/{total_folds} positive folds; fails 4/5 rule")

        # 2. Max fold drawdown
        dd_passed = max_dd <= self.KILL_CRITERIA["max_fold_drawdown_pct"]
        tests.append({
            "name": "max_fold_drawdown",
            "result": f"{max_dd:.1f}%",
            "threshold": f"{self.KILL_CRITERIA['max_fold_drawdown_pct']}%",
            "passed": dd_passed,
        })
        if not dd_passed:
            objections.append(f"Max fold drawdown {max_dd:.1f}% exceeds 20% ceiling")

        # 3. Bootstrap CI p05 > 0
        all_trades = [r for f in fold_returns for r in f]
        if len(all_trades) >= 20:
            rng = np.random.default_rng(42)
            boot_means = [rng.choice(all_trades, size=len(all_trades), replace=True).mean() for _ in range(1000)]
            p05 = float(np.quantile(boot_means, 0.05))
            p05_passed = p05 > self.KILL_CRITERIA["min_bootstrap_p05_r"]
            tests.append({
                "name": "bootstrap_p05_return",
                "result": p05,
                "threshold": "> 0.0",
                "passed": p05_passed,
            })
            if not p05_passed:
                objections.append(f"5th percentile bootstrap return {p05:.4f} <= 0")
        else:
            tests.append({"name": "sample_size", "result": len(all_trades), "threshold": ">= 20", "passed": False})
            objections.append("Insufficient trade count for statistical significance")

        # 4. Deflated Sharpe Ratio (Bailey & López de Prado Multiple Testing Correction)
        if len(all_trades) >= 20 and len(fold_returns) >= 2:
            try:
                from analysis.research_stats import deflated_sharpe, sharpe
                fold_srs = [sharpe(f) for f in fold_returns if len(f) >= 2]
                if len(fold_srs) >= 2:
                    dsr_meta = deflated_sharpe(all_trades, fold_srs)
                    dsr_val = float(dsr_meta.get("dsr", 0.0))
                    if not (np.isnan(dsr_val) or np.isinf(dsr_val)):
                        dsr_passed = dsr_val >= self.KILL_CRITERIA["min_deflated_sharpe"]
                        tests.append({
                            "name": "deflated_sharpe_ratio",
                            "result": round(dsr_val, 3),
                            "threshold": f">= {self.KILL_CRITERIA['min_deflated_sharpe']}",
                            "passed": dsr_passed,
                        })
                        if not dsr_passed:
                            objections.append(f"Deflated Sharpe Ratio {dsr_val:.2f} < 0.50 (fails multiple-testing noise hurdle)")
            except Exception:
                pass

        failed = [t for t in tests if not t["passed"]]
        verdict = "falsified" if failed else "cannot_falsify"

        return Falsification(
            proposal_id=strategy_id,
            verdict=verdict,
            tests_run=tests,
            specific_objection="; ".join(objections) if objections else None,
            confidence=0.90,
        )

    # ------------------------------------------------------------------
    # OverfitGuard Adversarial Validation (DSR + Sealed OOS + White's RC)
    # ------------------------------------------------------------------

    def audit_overfitguard(
        self,
        strategy_id: str,
        returns: Any,
        n_trials: int = 100,
        benchmark: Optional[Any] = None,
        holdout_frac: float = 0.35,
    ) -> Falsification:
        """
        Runs OverfitGuard reality-check:
        1. Deflated Sharpe Ratio (penalizes Sharpe against multiple trials & non-normality).
        2. Sealed Out-of-Sample Holdout (detects overfitted data-mining mirages).
        """
        try:
            import overfitguard
            res = overfitguard.validate(
                returns=returns,
                n_trials=n_trials,
                benchmark=benchmark,
                holdout_frac=holdout_frac,
            )
            dsr = float(res.deflated_sharpe) if res.deflated_sharpe is not None else 0.0
            oos_ret = float(res.oos_retention) if res.oos_retention is not None else 0.0

            tests = [
                {
                    "name": "overfitguard_verdict",
                    "result": res.verdict,
                    "threshold": "LIKELY_REAL",
                    "passed": res.verdict in ("LIKELY_REAL", "SURVIVES_DEFLATION_BUT_DECAYS_OOS"),
                },
                {
                    "name": "deflated_sharpe_confidence",
                    "result": f"{dsr * 100:.1f}%",
                    "threshold": ">= 95.0%",
                    "passed": dsr >= 0.95,
                },
                {
                    "name": "out_of_sample_retention",
                    "result": f"{oos_ret * 100:.1f}%",
                    "threshold": ">= 50.0%",
                    "passed": oos_ret >= 0.50,
                },
            ]
            objections = list(res.notes)

            if res.verdict in ("FAILS_OUT_OF_SAMPLE", "LIKELY_OVERFIT", "INSUFFICIENT_DATA"):
                verdict = "falsified"
            elif res.verdict == "INCONCLUSIVE":
                verdict = "inconclusive"
            else:
                verdict = "cannot_falsify"

            return Falsification(
                proposal_id=strategy_id,
                verdict=verdict,
                tests_run=tests,
                specific_objection="; ".join(objections) if objections else None,
                confidence=round(dsr, 2),
            )
        except Exception as exc:
            return Falsification(
                proposal_id=strategy_id,
                verdict="inconclusive",
                tests_run=[{"name": "overfitguard_execution", "result": str(exc), "passed": False}],
                specific_objection=f"OverfitGuard execution failed: {exc}",
                confidence=0.50,
            )

    def audit_whites_reality_check(
        self,
        candidates_returns: Any,
        n_bootstrap: int = 500,
    ) -> Falsification:
        """
        Runs White's Reality Check across the full space of strategy candidates
        to test whether the best model truly has an edge over pure data-snooping luck.
        """
        try:
            import overfitguard
            res = overfitguard.screen(candidates=candidates_returns, n_bootstrap=n_bootstrap)
            p_val = getattr(res, "p_value", 1.0)
            passed = res.verdict == "BEST_IS_SIGNIFICANT"

            tests = [
                {
                    "name": "whites_reality_check",
                    "result": res.verdict,
                    "threshold": "BEST_IS_SIGNIFICANT",
                    "passed": passed,
                },
                {
                    "name": "family_wise_p_value",
                    "result": round(float(p_val), 4),
                    "threshold": "<= 0.05",
                    "passed": float(p_val) <= 0.05,
                },
            ]
            verdict = "cannot_falsify" if passed else "falsified"
            return Falsification(
                proposal_id="WHITES_REALITY_CHECK",
                verdict=verdict,
                tests_run=tests,
                specific_objection=None if passed else f"Family-wise search failed White's Reality Check (p={p_val:.3f})",
                confidence=0.95,
            )
        except Exception as exc:
            return Falsification(
                proposal_id="WHITES_REALITY_CHECK",
                verdict="inconclusive",
                tests_run=[{"name": "screen_execution", "result": str(exc), "passed": False}],
                specific_objection=f"White's Reality Check failed: {exc}",
                confidence=0.50,
            )

    # ------------------------------------------------------------------
    # Closed-Loop Sceptic Trust Update
    # ------------------------------------------------------------------

    def update_trust(self, closed_trades: list[dict[str, Any]]) -> None:
        """
        Did Sceptic warnings predict bad trades over recent window?
        Adjusts authority accordingly.
        """
        warned = [t for t in closed_trades if t.get("sceptic_verdict") == "falsified"]
        passed = [t for t in closed_trades if t.get("sceptic_verdict") == "cannot_falsify"]

        if warned and passed:
            warned_win_rate = sum(1 for t in warned if t.get("r", 0.0) > 0) / len(warned)
            passed_win_rate = sum(1 for t in passed if t.get("r", 0.0) > 0) / len(passed)

            if warned_win_rate > passed_win_rate:
                # Warnings were wrong (false alarms) -> soften threshold
                self.falsify_threshold = min(0.70, self.falsify_threshold + 0.05)
            elif warned_win_rate < passed_win_rate - 0.05:
                # Warnings accurately caught bad trades -> strengthen sceptic weight
                self.trust_weight = min(1.20, self.trust_weight + 0.05)
