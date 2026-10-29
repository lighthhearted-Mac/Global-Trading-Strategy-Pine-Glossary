# Family RX: Risk, Sizing & Execution Models

**Total Strategies in Family:** 7  
**Pine Script v5 Implementations:** 2  

## Strategies Overview

| ID | Strategy Name | Alternative Names | Has Pine Code |
|---|---|---|:---:|
| **RX-01** | [Fixed Fractional / Percent-Risk Sizing](#rx-01--fixed_fractional_percent_risk_sizing) | 固定比例风险仓位 · Фикс-фракционное позиционирование | 📖 Logic-only |
| **RX-02** | [Kelly & Half-Kelly Criterion](#rx-02--kelly_half_kelly_criterion) | 凯利公式与半凯利 · Критерий Келли | ✅ Pine v5 |
| **RX-03** | [Volatility-Targeted Sizing (ATR Units)](#rx-03--volatility_targeted_sizing_atr_units) | 波动率目标仓位 · Волатильно-таргетированный размер | 📖 Logic-only |
| **RX-04** | [Portfolio Heat & Correlation Limits](#rx-04--portfolio_heat_correlation_limits) | 组合热度与相关性限制 · Портфельный «нагрев» | 📖 Logic-only |
| **RX-05** | [Breakeven Ratchet & Scale-Out Exits](#rx-05--breakeven_ratchet_scale_out_exits) | 保本推进与分批止盈 · Безубыток и частичная фиксация | ✅ Pine v5 |
| **RX-06** | [Time Stops & Opportunity-Cost Exits](#rx-06--time_stops_opportunity_cost_exits) | 时间止损 · Временной стоп | 📖 Logic-only |
| **RX-07** | [Execution Algorithms (TWAP / VWAP / POV) & Slippage Budgets](#rx-07--execution_algorithms_twap_vwap_pov_slippage_budgets) | 算法交易与滑点预算 · Алго-исполнение | 📖 Logic-only |

---

### RX-01 · Fixed Fractional / Percent-Risk Sizing
*固定比例风险仓位 · Фикс-фракционное позиционирование*

- **Origin & Lineage:** Ralph Vince, Portfolio Management Formulas (1990); universal practice since.
- **Core Hypothesis:** Size every trade so that the stop distance equals a fixed fraction of equity (0.5-2%): losses scale down in drawdowns and up in recoveries, giving geometric growth bounded by the risk fraction. It is the professional default and the direct generalization of the Turtle unit. The subtleties are volatility-of-volatility and gap risk beyond the stop.
- **Execution Rules:** Quantity = (equity x risk%) / (entry - stop); recompute per trade; cap gaps with position limits.
- **Key Parameters:** Risk 0.5-2%; correlation-aware portfolio caps.
- **Duplicates Eliminated:** TR-02 Turtle units (the volatility-normalized ancestor); every platform's default sizing.

---

### RX-02 · Kelly & Half-Kelly Criterion
*凯利公式与半凯利 · Критерий Келли*

- **Origin & Lineage:** John Kelly, Bell System Technical Journal 1956; Thorp's 1960s-70s market applications.
- **Core Hypothesis:** Kelly sizing f* = p - q/b maximizes long-run logarithmic growth; full Kelly is uninvestable in practice (variance brutal, edge estimates wrong), so practitioners use half or quarter Kelly. The formula's real lesson is that sizing and edge are inseparable — overbetting turns any positive-expectancy system into ruin. Implemented here as a Pine helper for educational sizing.
- **Execution Rules:** Estimate win rate and win/loss ratio; size fraction = k x Kelly with k = 0.25-0.5; re-estimate on rolling trade history.
- **Key Parameters:** Rolling sample 30-100 trades; k fraction; caps by volatility budget.
- **Duplicates Eliminated:** RX-01 (the practical constrained form); prop-firm sizing policies.

**Pine Script Reference Implementation:** [`rx-02_kelly_half_kelly_criterion.pine`](rx-02_kelly_half_kelly_criterion.pine)

```pinescript
//@version=5
indicator("Kelly Sizing Helper", overlay=false)
winRate = input.float(55.0, "Win rate %")
avgWin  = input.float(1.8, "Average win (R)")
avgLoss = input.float(1.0, "Average loss (R)")
kelly(p, b) => p - (1 - p) / b
f = kelly(winRate / 100, avgWin / avgLoss)
plot(f * 100, "Kelly %", color=f > 0 ? color.teal : color.red)
hline(0)
```

---

### RX-03 · Volatility-Targeted Sizing (ATR Units)
*波动率目标仓位 · Волатильно-таргетированный размер*

- **Origin & Lineage:** Turtle 'N' doctrine (TR-02); CTA standard practice; risk-parity (ST-17) single-asset form.
- **Core Hypothesis:** Scale positions inversely to recent volatility so each trade contributes equal risk regardless of the instrument's storminess — the quiet insight that lets one system trade rebar, crude, and equities coherently. Combined with a portfolio vol target it is the standard CTA architecture. Its failure mode is the vol spike that hits after the signal but before the resize.
- **Execution Rules:** Position = target risk / ATR; portfolio vol target scales total exposure; adjust at vol-shift thresholds, not every bar.
- **Key Parameters:** ATR window 14-20; per-trade risk 0.5-1%; portfolio target 10-15% annualized.
- **Duplicates Eliminated:** TR-02/TR-17 (the parents); ST-17 (portfolio level).

---

### RX-04 · Portfolio Heat & Correlation Limits
*组合热度与相关性限制 · Портфельный «нагрев»*

- **Origin & Lineage:** Prop/CTA risk management canon (1990s+); documented in CTA risk literature.
- **Core Hypothesis:** Heat = total open risk (sum of each position's stop-distance loss) as a fraction of equity; capping heat (e.g., 6%) and per-correlation-cluster heat (e.g., 3%) is what prevents five 'good trades' in the same factor from becoming one giant trade. Cluster-aware limits require mapping positions to common factors — the discipline that separates professionals from account blowups.
- **Execution Rules:** Sum open risk; block new entries above heat caps; cluster positions by factor/correlation and cap per cluster.
- **Key Parameters:** Total heat 4-8%; cluster heat 2-3%; correlation threshold 0.6+.
- **Duplicates Eliminated:** RX-01/03 (per-trade forms); ST-17 (allocation form).

---

### RX-05 · Breakeven Ratchet & Scale-Out Exits
*保本推进与分批止盈 · Безубыток и частичная фиксация*

- **Origin & Lineage:** Universal trader practice; formalized in exit-engineering literature (LeBeau lineage).
- **Core Hypothesis:** Two exit upgrades that dominate expectancy: moving the stop to breakeven at a profit threshold (converting trades to free options at the cost of some win rate), and scaling out at fixed R multiples (banking base + letting a runner work). Their interaction with trend systems is the classic tension — ratchets cut winners early. Implemented as a reusable Pine exit shell.
- **Execution Rules:** At +kR, stop to entry; scale out fractions at 1R/2R/3R or by ATR bands; trail the remainder.
- **Key Parameters:** k 0.8-1.5R; scale fractions 50/25/25; trail on remainder.
- **Duplicates Eliminated:** TR-10 trailing stops (the pure trail); GR-03 pyramids' exit side.

**Pine Script Reference Implementation:** [`rx-05_breakeven_ratchet_scale_out_exits.pine`](rx-05_breakeven_ratchet_scale_out_exits.pine)

```pinescript
//@version=5
strategy("Breakeven Ratchet Exit Shell", overlay=true)
rMult  = input.float(1.0, "BE at (R)")
atrMult = input.float(2.0, "Initial stop ATR")
atr = ta.atr(14)
if strategy.position_size == 0
strategy.entry("L", strategy.long)
var float stopPx = na
if strategy.position_size > 0
if na(stopPx)
stopPx := strategy.position_avg_price - atrMult * atr
gainR = (high - strategy.position_avg_price) / (atrMult * atr)
if gainR >= rMult
stopPx := math.max(stopPx, strategy.position_avg_price)
strategy.exit("LX", from_entry="L", stop=stopPx)
if strategy.position_size == 0
stopPx := na
```

---

### RX-06 · Time Stops & Opportunity-Cost Exits
*时间止损 · Временной стоп*

- **Origin & Lineage:** Prop-desk doctrine ('dead money is negative money'); quantified in TASC-era exit studies.
- **Core Hypothesis:** If a trade has not moved favorably within N bars, its premise is stale: exit and recycle capital into live setups. Backtests consistently show time stops improve capital efficiency even when they slightly reduce average win, because the opportunity cost of parked capital compounds. The parameter is regime-sensitive — swing trades need days, scalps need minutes.
- **Execution Rules:** Exit if unrealized P&L below a threshold after N bars (or if no new high/low within N bars); re-entry rules unchanged.
- **Key Parameters:** N by style (3-10 bars intraday, 5-20 days swing); dead-money threshold.
- **Duplicates Eliminated:** CN-02 board time-stop; BK-01 session-flat rule (time stop by clock).

---

### RX-07 · Execution Algorithms (TWAP / VWAP / POV) & Slippage Budgets
*算法交易与滑点预算 · Алго-исполнение*

- **Origin & Lineage:** Institutional execution research (Bertsimas-Lo 1998; Almgren-Chriss 2000); retail access via broker APIs.
- **Core Hypothesis:** Large orders are strategies too: TWAP slices time, VWAP tracks volume curve, POV participates at a market-share rate — each trading off market impact against timing risk. The retail-relevant lesson is the slippage budget: every strategy entry in this glossary must reserve costs (spread + impact + fees) that often decide viability more than the signal itself. Quantifying them is the last mile between backtest and P&L.
- **Execution Rules:** Slice parent orders per the chosen curve; randomize child sizes; measure realized slippage vs benchmark; feed the measurement back into strategy viability.
- **Key Parameters:** Participation 5-20%; impact model by ADV; cost ledger per strategy.
- **Duplicates Eliminated:** VO-07/08 (VWAP as signal — same benchmark, different job); RU-13/CR-08 (latency-bound execution domains).

---
