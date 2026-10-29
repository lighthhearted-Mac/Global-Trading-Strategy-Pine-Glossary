# Family GR: Grid, Martingale & Averaging Systems

**Total Strategies in Family:** 7  
**Pine Script v5 Implementations:** 2  

## Strategies Overview

| ID | Strategy Name | Alternative Names | Has Pine Code |
|---|---|---|:---:|
| **GR-01** | [Classic Spot Grid Bot](#gr-01--classic_spot_grid_bot) | 网格交易机器人 · Сеточный робот | ✅ Pine v5 |
| **GR-02** | [Martingale / Averaging-Down Systems](#gr-02--martingale_averaging_down_systems) | 马丁格尔加仓 · Мартингейл / усреднение | ✅ Pine v5 |
| **GR-03** | [Anti-Martingale Pyramiding](#gr-03--anti_martingale_pyramiding) | 反马丁加仓 · Анти-мартингейл | 📖 Logic-only |
| **GR-04** | [DCA & Smart DCA Bots](#gr-04--dca_smart_dca_bots) | 定投与智能定投机器人 · DCA-боты | 📖 Logic-only |
| **GR-05** | [Fibonacci Grid](#gr-05--fibonacci_grid) | 斐波那契网格 · Фибо-сетка | 📖 Logic-only |
| **GR-06** | [ATR-Adaptive Grid](#gr-06--atr_adaptive_grid) | ATR自适应网格 · Адаптивная сетка по ATR | 📖 Logic-only |
| **GR-07** | [Portfolio Rebalancing Bot](#gr-07--portfolio_rebalancing_bot) | 组合再平衡机器人 · Ребаланс-боты | 📖 Logic-only |

---

### GR-01 · Classic Spot Grid Bot
*网格交易机器人 · Сеточный робот*

- **Origin & Lineage:** Manual grid trading since the 1970s US commodity floors; industrialized by crypto exchange bot marketplaces (2019+), JoinQuant/myquant templates, and 3Commas/Pionex products.
- **Core Hypothesis:** Lay N limit buys below and sells above a base price at fixed percentage steps; every filled buy is paired with a sell one step higher, harvesting oscillation regardless of direction. Profit per cycle = step x quantity, risk = full inventory in a sustained trend against the ladder. Variants differ in step definition (fixed %, ATR, Fib levels) and range-reset logic.
- **Execution Rules:** Base position at start; buy each grid down, re-sell each filled rung one grid up; reset the grid when price exits the configured range.
- **Key Parameters:** Grid count 10-100; step 0.5-2% (crypto), 0.2-0.5% (majors); order size = capital / grid count.
- **Duplicates Eliminated:** CN 网格交易 (myquant/JoinQuant templates, E大网格体系); RU «сеточные роботы» (Binance/Bybit RU marketplaces); every Pionex/3Commas preset.

**Pine Script Reference Implementation:** [`gr-01_classic_spot_grid_bot.pine`](gr-01_classic_spot_grid_bot.pine)

```pinescript
//@version=5
strategy("Spot Grid Bot (Ladder)", overlay=true, pyramiding=30)
gridCount = input.int(10, "Grid levels")
stepPct   = input.float(1.0, "Grid step, %")
qtyPct    = input.float(10.0, "Order size, % of equity")
var float lastBuy = na
qty() => (strategy.equity * qtyPct / 100) / close
if strategy.position_size == 0
strategy.entry("G0", strategy.long, qty=qty())
strategy.exit("TP0", from_entry="G0", limit=close * (1 + stepPct / 100))
lastBuy := close
if strategy.position_size > 0 and not na(lastBuy) and close <= lastBuy * (1 - stepPct / 100) and strategy.opentrades < gridCount
id = "G" + str.tostring(strategy.opentrades)
strategy.entry(id, strategy.long, qty=qty())
strategy.exit("TP" + str.tostring(strategy.opentrades), from_entry=id, limit=close * (1 + stepPct / 100))
lastBuy := close
```

---

### GR-02 · Martingale / Averaging-Down Systems
*马丁格尔加仓 · Мартингейл / усреднение*

- **Origin & Lineage:** 18th-century French casino theory; industrialized by MT4-era advisors — most famously the Ilan family (RU-02) — and every forex 'recovery' EA.
- **Core Hypothesis:** Double (or multiply) size at fixed adverse intervals so the basket's breakeven converges toward current price; the win rate is very high until a sustained trend vaporizes the account. The modern trade-off versions (Ilan's RSI+CCI gating, ATR spacing, equity stop) merely delay the tail. Documented here because it remains one of the most-sold strategy families in RU and CN retail markets — with the explicit warning that its risk-adjusted profile is negative without a hard equity stop.
- **Execution Rules:** Initial position; add size^k at each N-ATR adverse step; exit the basket at breakeven + spread; HARD equity stop at max drawdown.
- **Key Parameters:** Multiplier 1.5-2.5; step 0.5-1.5 ATR; max steps 6-10; equity stop mandatory.
- **Duplicates Eliminated:** Ilan 1.6/2.0 & Apocalypse (RU-02); CN 马丁/扛单 systems; every 'recovery zone' EA on MQL5 market.

**Pine Script Reference Implementation:** [`gr-02_martingale_averaging_down_systems.pine`](gr-02_martingale_averaging_down_systems.pine)

```pinescript
//@version=5
strategy("ATR Martingale Averager (RISK DEMO)", overlay=true, pyramiding=10)
mult    = input.float(2.0, "Size multiplier")
stepAtr = input.float(1.0, "Add every N ATR")
atr = ta.atr(14)
if strategy.position_size == 0
strategy.entry("M1", strategy.long, qty=1)
if strategy.position_size > 0 and close <= strategy.position_avg_price - stepAtr * atr
strategy.entry("M" + str.tostring(strategy.opentrades + 1), strategy.long,
qty=math.pow(mult, strategy.opentrades))
if strategy.position_size > 0 and close >= strategy.position_avg_price + 0.25 * atr
strategy.close_all(comment="Basket recovery")
```

---

### GR-03 · Anti-Martingale Pyramiding
*反马丁加仓 · Анти-мартингейл*

- **Origin & Lineage:** Turtle doctrine (TR-02); formal risk literature favoring pyramiding into winners.
- **Core Hypothesis:** The mirror of GR-02: add to winners at fixed favorable intervals with unit sizing constant or declining, so risk concentrates behind the trend rather than behind hope. Drawdown geometry is bounded while upside compounds — the mathematically sound side of the averaging debate. Turtles added 0.5N units; equity-curve variants gate adds on system performance.
- **Execution Rules:** Add a unit each +0.5N-1R advance up to a cap; trail stops on the whole stack at 2N from the last fill.
- **Key Parameters:** Add interval 0.5N-1R; unit cap 3-4; stack trailing stop.
- **Duplicates Eliminated:** Turtle pyramiding (TR-02); trend-add modules in CN CTA kits; RU «доливка по тренду» practice.

---

### GR-04 · DCA & Smart DCA Bots
*定投与智能定投机器人 · DCA-боты*

- **Origin & Lineage:** Dollar-cost averaging canon (Graham-era); bot-marketplace industrialization (2019+); CN 定投 practice (E大长赢体系) and RU T-Bank auto-invest.
- **Core Hypothesis:** Scheduled buys regardless of price, optionally with valuation gates ('smart' variants buy more when price is below a moving anchor or index percentile). The edge is behavioral discipline plus volatility harvesting on the cost basis, not timing. Smart variants (valuation-triggered, dip-multiplied) blur into GR-01 grid logic at the margins.
- **Execution Rules:** Buy fixed amounts on schedule; smart variants scale the tranche by (anchor / price) or z-score below fair value; rebalance or take-profit rules vary.
- **Key Parameters:** Frequency weekly/monthly; valuation multiplier 1-3x; take-profit band 20-50% (CN 定投止盈 convention).
- **Duplicates Eliminated:** CN 基金定投+止盈体系; RU T-Bank auto-invest strategies; 3Commas DCA presets.

---

### GR-05 · Fibonacci Grid
*斐波那契网格 · Фибо-сетка*

- **Origin & Lineage:** Fibonacci retracement practice merged with grid automation (MT4 era); popular in RU forex communities.
- **Core Hypothesis:** Anchor a Fibonacci retracement on the last impulse and place grid orders at the classic ratios (38.2/50/61.8/78.6), trading reversals at each level toward the impulse origin or breakouts beyond 100%. It converts a discretionary drawing tool into an automatic ladder. The edge is crowd-level self-fulfillment at famous ratios, which decays in fast markets.
- **Execution Rules:** Anchor pivots define the retracement; buy limits at 38.2/50/61.8 with stops beyond 78.6; targets at 0% then extensions.
- **Key Parameters:** Impulse pivot selection (zigzag 3-8%); ratio set; per-level sizing.
- **Duplicates Eliminated:** RU «сетка по Фибо» robots; CN 斐波那契网格 experiments; MT4 Fibo-grid EAs.

---

### GR-06 · ATR-Adaptive Grid
*ATR自适应网格 · Адаптивная сетка по ATR*

- **Origin & Lineage:** Grid-bot engineering iteration (2020s crypto bot marketplaces; CN grid research notes).
- **Core Hypothesis:** Replace the fixed percentage step with k x ATR so grid density self-adjusts to volatility: wide grids in storms (fewer, cheaper fills), tight grids in calm. Range bounds can follow Bollinger/Keltner envelopes, making the grid a volatility-adaptive oscillator harvester. This is the most robust of the grid family because it prices risk in the same units as the market's own motion.
- **Execution Rules:** Step = k x ATR(14) recomputed at reset; range = EMA +/- m x ATR; reset grid when price exits the envelope.
- **Key Parameters:** k 0.5-1.5; m 2-3; reset on envelope break.
- **Duplicates Eliminated:** Volatility-grid presets in bot marketplaces; CN 自适应网格研究; RU адаптивные сетки.

---

### GR-07 · Portfolio Rebalancing Bot
*组合再平衡机器人 · Ребаланс-боты*

- **Origin & Lineage:** Shannon's Demon (Claude Shannon & Thomas Cover, 1970s lectures) as the theory; BitUniverse 'Grid Trading Battle' era (2019) as the retail phenomenon.
- **Core Hypothesis:** Hold fixed value weights across assets; periodic or threshold rebalancing systematically sells winners and buys losers, harvesting the volatility of the pair (Shannon's demon: an unlevered volatile pair grows wealth under rebalance alone). The 2019-2021 BitUniverse rebalance battles made it a retail staple in CN and RU crypto circles. Its edge equals pair volatility minus rebalance costs.
- **Execution Rules:** Rebalance to target weights when any weight drifts beyond a threshold or on a schedule; cash leg optional as the stable asset.
- **Key Parameters:** Threshold 5-20% absolute drift; rebalance fee-awareness; asset pair volatility screen.
- **Duplicates Eliminated:** Shannon's demon writeups; BitUniverse battles; CN 定投再平衡 hybrids; RU ребалансировка боты.

---
