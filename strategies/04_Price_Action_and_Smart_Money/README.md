# Family PA: Price Action & Smart Money

**Total Strategies in Family:** 16  
**Pine Script v5 Implementations:** 4  

## Strategies Overview

| ID | Strategy Name | Alternative Names | Has Pine Code |
|---|---|---|:---:|
| **PA-01** | [Wyckoff Accumulation/Distribution & Spring (V-Hook)](#pa-01--wyckoff_accumulationdistribution_spring_v_hook) | 威科夫吸筹与弹簧效应 · Метод Вайкоффа | ✅ Pine v5 |
| **PA-02** | [Effort vs Result / Composite Operator Reading](#pa-02--effort_vs_result_composite_operator_reading) | 量价背离的威科夫读法 · Соотнесение усилия и результата | 📖 Logic-only |
| **PA-03** | [Pin Bar / Hammer Rejection](#pa-03--pin_bar_hammer_rejection) | 长影线反转 · Пинбар | 📖 Logic-only |
| **PA-04** | [Engulfing & Inside-Bar Momentum Patterns](#pa-04--engulfing_inside_bar_momentum_patterns) | 吞没与内包形态 · Паттерны поглощения и внутреннего бара | ✅ Pine v5 |
| **PA-05** | [Al Brooks Bar-by-Bar Price Action](#pa-05--al_brooks_bar_by_bar_price_action) | 布鲁克斯逐K线价格行为 · Прайс-экшн по Бруксу | 📖 Logic-only |
| **PA-06** | [Fakey / False-Breakout Inside-Bar](#pa-06--fakey_false_breakout_inside_bar) | 假突破内包形态 · Фейки (ложный пробой) | 📖 Logic-only |
| **PA-07** | [Supply & Demand Zones (Set-and-Forget)](#pa-07--supply_demand_zones_set_and_forget) | 供需区域策略 · Зоны спроса и предложения | ✅ Pine v5 |
| **PA-08** | [Smart Money Concepts (BOS / CHoCH / Order Blocks / FVG)](#pa-08--smart_money_concepts_bos_choch_order_blocks_fvg) | 聪明钱结构交易 · Умные деньги (SMC) | ✅ Pine v5 |
| **PA-09** | [ICT Kill Zones, Silver Bullet & Time-Based Liquidity](#pa-09--ict_kill_zones_silver_bullet_time_based_liquidity) | ICT时区流动性策略 · ICT Килл-зоны | 📖 Logic-only |
| **PA-10** | [Turtle Soup / Fake Breakout Fade](#pa-10--turtle_soup_fake_breakout_fade) | 海龟汤反向策略 · Контрпробой 'Turtle Soup' | 📖 Logic-only |
| **PA-11** | [Harmonic Patterns (Gartley / Bat / Butterfly / AB=CD)](#pa-11--harmonic_patterns_gartley_bat_butterfly_abcd) | 谐波形态 · Гармонические паттерны | 📖 Logic-only |
| **PA-12** | [Elliott Wave (Mechanized Approaches)](#pa-12--elliott_wave_mechanized_approaches) | 艾略特波浪（机械化） · Волны Эллиотта | 📖 Logic-only |
| **PA-13** | [Wolfe Waves](#pa-13--wolfe_waves) | 沃尔夫波浪 · Волны Вольфа | 📖 Logic-only |
| **PA-14** | [Classical Reversal Patterns Automated (Double Top, H&S)](#pa-14--classical_reversal_patterns_automated_double_top_hs) | 经典反转形态自动化 · Автоматизация классических паттернов | 📖 Logic-only |
| **PA-15** | [Trendline & Channel Break Automation](#pa-15--trendline_channel_break_automation) | 趋势线突破自动化 · Автопробой трендовых линий | 📖 Logic-only |
| **PA-16** | [Round Numbers / Psychological Levels](#pa-16--round_numbers_psychological_levels) | 整数关口 · Круглые уровни | 📖 Logic-only |

---

### PA-01 · Wyckoff Accumulation/Distribution & Spring (V-Hook)
*威科夫吸筹与弹簧效应 · Метод Вайкоффа*

- **Origin & Lineage:** Richard D. Wyckoff, Stock Market Institute course materials (1931-1934); schematics formalized later by Bob Evans.
- **Core Hypothesis:** Markets accumulate in ranges where the composite operator absorbs supply; the spring is the deliberate shakeout below the range that sweeps resting stops before markup — the upthrust mirrors it in distribution. The mechanical form trades a defined range: sweep beyond the low by up to ~1 ATR on a volume spike, then reclaim of the range low, with stops outside the sweep. Every liquidity-sweep method in this glossary is downstream of this idea.
- **Execution Rules:** Define a 20-40 bar range; long on a low piercing range-low by <= 1 ATR that closes back inside with volume > 1.5x average; stop below sweep low; targets at range high then measured move.
- **Key Parameters:** Range lookback 20-40; depth cap 1.0-1.2 ATR; volume multiple 1.5-2.5; phase filters optional.
- **Duplicates Eliminated:** Wyckoff [theUltimator5] schematic indicator; CN 威科夫吸筹 materials; RU Вайкофф course translations; Linda Raschke's Turtle Soup (PA-10) is the fade-cousin; this workspace's V-Hook agent is a direct implementation.

**Pine Script Reference Implementation:** [`pa-01_wyckoff_accumulationdistribution_spring_v_hook.pine`](pa-01_wyckoff_accumulationdistribution_spring_v_hook.pine)

```pinescript
//@version=5
strategy("Wyckoff Spring / Upthrust (V-Hook)", overlay=true)
rangeLen = input.int(30, "Range lookback")
depthMax = input.float(1.0, "Max sweep depth (ATR)")
volMult  = input.float(1.5, "Volume multiple")
rngHi = ta.highest(high, rangeLen)[1]
rngLo = ta.lowest(low, rangeLen)[1]
atr   = ta.atr(14)
flat    = (rngHi - rngLo) / rngLo < 0.15
swept   = low < rngLo and rngLo - low <= depthMax * atr and close > rngLo
upthrust = flat and high > rngHi and high - rngHi <= depthMax * atr and close < rngHi
volSpike = volume > volMult * ta.sma(volume, 20)
spring = flat and swept and volSpike
if spring
strategy.entry("L", strategy.long)
if upthrust and volSpike
strategy.entry("S", strategy.short)
if strategy.position_size > 0 and close < rngLo - 2 * atr
strategy.close("L", comment="Failed spring")
if strategy.position_size < 0 and close > rngHi + 2 * atr
strategy.close("S", comment="Failed upthrust")
plot(rngHi, "Range high", color=color.new(color.teal, 40))
plot(rngLo, "Range low", color=color.new(color.red, 40))
```

---

### PA-02 · Effort vs Result / Composite Operator Reading
*量价背离的威科夫读法 · Соотнесение усилия и результата*

- **Origin & Lineage:** Wyckoff course lineage; teaching tradition via Bob Evans' 'effort vs result' papers.
- **Core Hypothesis:** Compare the effort (spread and volume of a bar or swing) with the result (price progress): big effort with no progress signals absorption by the other side, small effort with large progress signals a vacuum of opposing orders. These are the diagnostic sentences of Wyckoff analysis; mechanically they appear as volume-spread anomalies that gate other entries rather than standalone signals.
- **Execution Rules:** Flag bars in the top decile of volume with bottom-quartile progress; use as entry/exit confluence for PA-01 or VO-01 systems.
- **Key Parameters:** Volume percentile 90; progress normalized by ATR.
- **Duplicates Eliminated:** VSA (VO-01) is the formalized descendant; CN 量价背离 reading; RU «усилие-результат» school.

---

### PA-03 · Pin Bar / Hammer Rejection
*长影线反转 · Пинбар*

- **Origin & Lineage:** Candlestick lineage (Homma, 18th c.; Nison's 1991 westernization); 'pin bar' term popularized by Martin Cole and Nial Fuller (2000s).
- **Core Hypothesis:** A long-tailed bar whose close sits near the opposite extreme shows a one-sided auction that was rejected; trading the close beyond the bar's nose in the rejection direction captures the failure of the sweep. The pattern is a single-bar Wyckoff spring and is the most-taught retail setup in Russian and English-language price-action schools alike.
- **Execution Rules:** Long when a lower-wick >= 2x body bar closes in the upper third after a downswing; enter above its high; stop below the wick.
- **Key Parameters:** Tail/body ratio 2:1; trend context filter (EMA 50/200); 1-2R targets.
- **Duplicates Eliminated:** RU «пинбар» schools (every RU PA course); CN 长下影/锤子线战法; hammer/shooting-star mechanical scripts.

---

### PA-04 · Engulfing & Inside-Bar Momentum Patterns
*吞没与内包形态 · Паттерны поглощения и внутреннего бара*

- **Origin & Lineage:** Japanese candlestick canon; Steve Nison, Japanese Candlestick Charting Techniques (1991).
- **Core Hypothesis:** An engulfing bar completesly absorbs the prior bar's body, marking a decisive swing of control; the inside bar marks compression that resolves in the direction of the break. Both are the atomic units from which larger setups (fakey, ORB, Wyckoff) are assembled, and they backtest best with a trend filter and volume confirmation rather than standalone.
- **Execution Rules:** Long on bullish engulfing above EMA(50); stop 1.5 ATR; optional inside-bar break continuation entry.
- **Key Parameters:** Body-based definition (wicks excluded); trend filter EMA 50/200.
- **Duplicates Eliminated:** MT4 engulfing EAs; CN 阳包阴战法; RU «поглощение» robots.

**Pine Script Reference Implementation:** [`pa-04_engulfing_inside_bar_momentum_patterns.pine`](pa-04_engulfing_inside_bar_momentum_patterns.pine)

```pinescript
//@version=5
strategy("Engulfing with Trend Filter", overlay=true)
bodyUp = close > open and close[1] < open[1] and close >= open[1] and open <= close[1]
bodyDn = close < open and close[1] > open[1] and close <= open[1] and open >= close[1]
upTrend = close > ta.ema(close, 50)
dnTrend = close < ta.ema(close, 50)
atr = ta.atr(14)
if bodyUp and upTrend
strategy.entry("L", strategy.long)
if bodyDn and dnTrend
strategy.entry("S", strategy.short)
if strategy.position_size > 0 and close < strategy.position_avg_price - 1.5 * atr
strategy.close("L", comment="Stop")
if strategy.position_size < 0 and close > strategy.position_avg_price + 1.5 * atr
strategy.close("S", comment="Stop")
```

---

### PA-05 · Al Brooks Bar-by-Bar Price Action
*布鲁克斯逐K线价格行为 · Прайс-экшн по Бруксу*

- **Origin & Lineage:** Al Brooks, Reading Price Charts Bar by Bar (2009) and the Brooks Trading Course (2011+).
- **Core Hypothesis:** A complete grammar of 5-minute charts: every bar is a setup candidate, with high-1/low-1 to high-4/low-4 counted entries in pullbacks, second-entry doctrine, measured-move targets, and always-in direction. It is the most internally consistent retail price-action system ever published, though its full context-dependence resists complete mechanization; partial Pine ports implement the counted entries and always-in flip.
- **Execution Rules:** In a bull trend, buy the first pullback to the EMA-20 that forms a bull bar (H1); re-enter on H2/H3 after failed attempts; always-in flips on strong reversal bars.
- **Key Parameters:** EMA 20 anchor; 5-minute or daily charts; scalper's entry/exit or swing variant.
- **Duplicates Eliminated:** Brooks-method scan scripts; RU «бар-за баром» translations; second-entry fan implementations.

---

### PA-06 · Fakey / False-Breakout Inside-Bar
*假突破内包形态 · Фейки (ложный пробой)*

- **Origin & Lineage:** Popularized by Nial Fuller's price-action courses (2000s); mechanism identical to Wyckoff's upthrust-after-pullback.
- **Core Hypothesis:** An inside bar followed by a false break of the mother bar that closes back inside creates a two-sided liquidity trap: breakout traders are trapped and their stops fuel the reversal. Trading the close back through the mother-bar edge turns the trap into an entry with a naturally tight stop behind the false extreme.
- **Execution Rules:** Detect inside bar; on a false break beyond the mother bar that closes back inside, enter the reversal; stop beyond the false extreme.
- **Key Parameters:** Mother bar 1-3 bars; breakout tolerance 1-2 ticks; trend filter recommended.
- **Duplicates Eliminated:** Turtle Soup (PA-10); stop-run/'spoofy' scripts; RU «ложный пробой» scripts.

---

### PA-07 · Supply & Demand Zones (Set-and-Forget)
*供需区域策略 · Зоны спроса и предложения*

- **Origin & Lineage:** Sam Seiden (2000s webinars, 'supply and demand' rebranding of S/R); hundreds of open Pine implementations.
- **Core Hypothesis:** A strong one-way move leaving a small consolidation ('base') defines a zone where institutional orders rested; price's first return to the zone is traded for a continuation, on the theory that unfilled institutional interest remains. The mechanical core is a rally-base-rally or drop-base-drop detector plus a retest trigger. It is the retail-popular cousin of order-block logic (PA-08).
- **Execution Rules:** Detect base (low-range bars) followed by impulse > 1.5 ATR; mark zone as base high/low; enter on first retest; stop beyond zone.
- **Key Parameters:** Base 1-5 bars; impulse 1.5-2 ATR; zone validity 1-3 touches.
- **Duplicates Eliminated:** Order block overlaps (PA-08); CN 供需区域 scripts; RU «зоны спроса/предложения» packs.

**Pine Script Reference Implementation:** [`pa-07_supply_demand_zones_set_and_forget.pine`](pa-07_supply_demand_zones_set_and_forget.pine)

```pinescript
//@version=5
strategy("Supply-Demand Zone Retest", overlay=true)
impulse  = input.float(1.5, "Impulse ATR multiple")
baseBars = input.int(3, "Base bars")
atr = ta.atr(14)
baseFlat = math.abs(ta.highest(high, baseBars) - ta.lowest(low, baseBars)) < atr
bullBase = baseFlat[1] and close - close[baseBars] > impulse * atr
bearBase = baseFlat[1] and close[baseBars] - close > impulse * atr
var float dzTop = na
var float dzBot = na
var float szTop = na
var float szBot = na
if bullBase
dzTop := ta.highest(high, baseBars)[1]
dzBot := ta.lowest(low, baseBars)[1]
if bearBase
szTop := ta.highest(high, baseBars)[1]
szBot := ta.lowest(low, baseBars)[1]
demandRetest = not na(dzBot) and low <= dzTop and close > dzBot and strategy.position_size <= 0
supplyRetest = not na(szTop) and high >= szBot and close < szTop and strategy.position_size >= 0
if demandRetest
strategy.entry("L", strategy.long)
if supplyRetest
strategy.entry("S", strategy.short)
plot(dzTop, "Demand top", color=color.teal, style=plot.style_linebr)
plot(dzBot, "Demand bottom", color=color.teal, style=plot.style_linebr)
plot(szTop, "Supply top", color=color.red, style=plot.style_linebr)
plot(szBot, "Supply bottom", color=color.red, style=plot.style_linebr)
```

---

### PA-08 · Smart Money Concepts (BOS / CHoCH / Order Blocks / FVG)
*聪明钱结构交易 · Умные деньги (SMC)*

- **Origin & Lineage:** LuxAlgo 'Smart Money Concepts' open script (2021+, most-starred of its genre), systematizing ICT vocabulary (see PA-09).
- **Core Hypothesis:** SMC formalizes structure trading: a Break of Structure confirms trend continuation, a Change of Character flags reversal, order blocks mark the last opposing candle before an impulsive displacement (institutional footprint), and Fair Value Gaps are 3-bar imbalances expected to refill. The mechanical trade is: structure break defines bias, then a retrace into the order block or FVG is the entry. Its popularity makes it the defining retail framework of the 2020s.
- **Execution Rules:** Swing pivots define structure; on a bullish BOS mark the last bearish candle before displacement as the OB; long on first retrace into the OB while bias holds; CHoCH invalidates.
- **Key Parameters:** Swing length 5-15; displacement filter 1-1.5 ATR; OB expiry on full mitigation.
- **Duplicates Eliminated:** LuxAlgo SMC [ML] and dozens of forks; ICT order-block scripts; CN 主力结构 (SMART概念) scripts; RU SMC переводы — the framework is one concept despite hundreds of branded scripts.

**Pine Script Reference Implementation:** [`pa-08_smart_money_concepts_bos_choch_order_blocks_fvg.pine`](pa-08_smart_money_concepts_bos_choch_order_blocks_fvg.pine)

```pinescript
//@version=5
strategy("SMC: BOS + Order Block Retrace", overlay=true)
swingLen = input.int(10, "Swing length")
ph = ta.pivothigh(high, swingLen, swingLen)
pl = ta.pivotlow(low, swingLen, swingLen)
var float lastHigh = na
var float lastLow = na
var int bias = 0
var float obTop = na
var float obBot = na
if not na(ph)
lastHigh := ph
if not na(pl)
lastLow := pl
if not na(lastHigh) and close > lastHigh and nz(bias[1]) <= 0
bias := 1
obTop := lastHigh
obBot := ta.lowest(low, swingLen)
if not na(lastLow) and close < lastLow and nz(bias[1]) >= 0
bias := -1
obTop := ta.highest(high, swingLen)
obBot := lastLow
retraceLong  = bias == 1 and not na(obBot) and low <= obTop and close > obBot
retraceShort = bias == -1 and not na(obTop) and high >= obBot and close < obTop
if retraceLong
strategy.entry("L", strategy.long)
if retraceShort
strategy.entry("S", strategy.short)
plot(bias == 1 ? obTop : na, "Bull OB top", color=color.teal, style=plot.style_linebr)
plot(bias == 1 ? obBot : na, "Bull OB bottom", color=color.teal, style=plot.style_linebr)
plot(bias == -1 ? obTop : na, "Bear OB top", color=color.red, style=plot.style_linebr)
plot(bias == -1 ? obBot : na, "Bear OB bottom", color=color.red, style=plot.style_linebr)
```

---

### PA-09 · ICT Kill Zones, Silver Bullet & Time-Based Liquidity
*ICT时区流动性策略 · ICT Килл-зоны*

- **Origin & Lineage:** Michael J. Huddleston, 'The Inner Circle Trader' (2010s free/core courses; massive 2020s revival).
- **Core Hypothesis:** ICT maps institutional session rhythms: London and New York 'kill zones' carry the day's real liquidity events; the Silver Bullet is a 10:00-11:00 ET window where a specific FVG continuation setup repeats; Judas swings are early session fake moves that set up the true move. The edge claimed is time-conditional liquidity, making it a session family (SE) wearing price-action clothes.
- **Execution Rules:** During the defined window, enter on FVG/OB retrace in the direction of the session's initial sweep reversal; fixed R targets.
- **Key Parameters:** Kill zones 02:00-05:00 and 08:30-11:00 ET; Silver Bullet 10:00-11:00 ET; 2-6R targets.
- **Duplicates Eliminated:** ICT concepts scripts (dozens); PA-08 SMC (shared vocabulary); SE-01 Asia-range sweep (shared mechanism).

---

### PA-10 · Turtle Soup / Fake Breakout Fade
*海龟汤反向策略 · Контрпробой 'Turtle Soup'*

- **Origin & Lineage:** Linda Bradford Raschke & Larry Connors, Street Smarts (1995).
- **Core Hypothesis:** A deliberate anti-Donchian: when price breaks a 20-day high/low but fails to hold for one bar, fade the failure back into the range. Raschke's joke was that buying Donchian breakouts had become so popular that fading them fed on the crowd. It works best when the failure bar also sweeps an obvious stop cluster — the same auction logic as the Wyckoff spring in reverse time order.
- **Execution Rules:** Short when price takes out the 20-day high intraday but closes back below it; enter on the next bar, stop above the failure extreme, target the range mid.
- **Key Parameters:** 20-day extremes (or 55); one-bar failure rule; 50% range target.
- **Duplicates Eliminated:** Fakey (PA-06); 'stop hunt fade' scripts; CN 假突破反打.

---

### PA-11 · Harmonic Patterns (Gartley / Bat / Butterfly / AB=CD)
*谐波形态 · Гармонические паттерны*

- **Origin & Lineage:** H.M. Gartley, Profits in the Stock Market (1935); Fibonacci ratios and XABCD formalization by Larry Pesavento (1990s) and Scott Carney, The Harmonic Trader (1998).
- **Core Hypothesis:** Specific Fibonacci retracement/extension relationships between five swing points (X-A-B-C-D) define reversal geometries: the Gartley's B-point at 0.618 XA with D at 0.786, the Bat, the Butterfly's 1.27 XA extension, and the simpler AB=CD. Trades enter at the D completion with stops beyond the pattern's invalidation ratio. Mechanization requires robust pivot detection and ratio tolerance, which is why most implementations are indicators, not strategies.
- **Execution Rules:** Detect XABCD pivots; verify ratio windows (e.g., Gartley: B 0.618 +/- 0.05 XA, D 0.786 XA); enter at D, stop beyond X.
- **Key Parameters:** Ratio tolerance 0.03-0.06; pattern length 20-100 bars.
- **Duplicates Eliminated:** Pesavento vs Carney naming disputes (same patterns); RU «Гартли/летучая мышь» packs; CN 谐波形态 scripts.

---

### PA-12 · Elliott Wave (Mechanized Approaches)
*艾略特波浪（机械化） · Волны Эллиотта*

- **Origin & Lineage:** Ralph Nelson Elliott, The Wave Principle (1938); mechanization attempts since the 1980s software era.
- **Core Hypothesis:** Five-wave impulse and three-wave correction fractals, with wave 3 never the shortest and wave 4 not overlapping wave 1's territory. Fully automatic wave counting is famously ambiguous, so practical implementations use zigzag pivots with degree nesting to propose counts and trade the wave-4-to-5 continuation or the C-wave terminal. It endures as an analytical overlay more than a standalone strategy.
- **Execution Rules:** Zigzag pivots propose counts; long the pivot after a qualifying wave-4 low targeting wave-5 projection; invalidation on overlap.
- **Key Parameters:** Zigzag deviation 3-10%; Fibonacci projections 0.618/1.0/1.618 of wave 1.
- **Duplicates Eliminated:** RU Эллиотт-школы (large following); CN 波浪理论 automated drafts; every 'EW auto-count' indicator.

---

### PA-13 · Wolfe Waves
*沃尔夫波浪 · Волны Вольфа*

- **Origin & Lineage:** Brian and Bill Wolfe, early 1990s (published as a paid course; later widely redistributed).
- **Core Hypothesis:** A 5-point pattern where waves 1-4 bound an equilibrating channel and wave 5 overshoots a projected 'line' extension, targeting a natural-path reversal toward point 1-4 convergence. It is essentially a corrective wedge with a projected termination line, traded at the wave-5 extreme with a tight stop. Popularity concentrated in forex forums and RU/EN script libraries.
- **Execution Rules:** Detect 5 alternating pivots with 1-4 channel geometry; enter at wave-5 line touch; target the 1-4 ray.
- **Key Parameters:** Pivot detection zigzag 3-8%; target = 1-4 line projection.
- **Duplicates Eliminated:** Wolfe Wave scripts on MQL5/TradingView; RU «волны Вольфа» robots.

---

### PA-14 · Classical Reversal Patterns Automated (Double Top, H&S)
*经典反转形态自动化 · Автоматизация классических паттернов*

- **Origin & Lineage:** Schabacker (1932), Edwards & Magee (1948) — the archive canon; automation via pivot libraries.
- **Core Hypothesis:** Double tops/bottoms and head-and-shoulders are detected from swing pivots: two comparable extremes separated by a trough, or three extremes with a middle head, completed on a neckline break. Automated detection mainly serves as a scanner for discretionary traders; as mechanical entries they suffer from pattern-boundary ambiguity, so implementations tune pivot sensitivity heavily.
- **Execution Rules:** Detect pivots; H&S short on neckline break with stop above right shoulder; target = pattern height projected from the break.
- **Key Parameters:** Pivot strength 5-10; peak similarity tolerance 2-5%; neckline slope filter.
- **Duplicates Eliminated:** CN 双头双底/头肩顶 scripts; RU «голова-плечи» роботы; every platform's built-in pattern detection.

---

### PA-15 · Trendline & Channel Break Automation
*趋势线突破自动化 · Автопробой трендовых линий*

- **Origin & Lineage:** Manual TA since Dow; automated by linreg channels (Ehlers-era) and pivot-line fitting scripts.
- **Core Hypothesis:** Fit a line through at least two (ideally three) pivot highs/lows and trade closes beyond it, or trade the linear-regression channel's outer bands as dynamic trendlines. Automation exposes the subjectivity problem: touch tolerance and fit window dominate results. The linreg-channel form is the most reproducible and pairs with R-squared as a fit-quality gate.
- **Execution Rules:** Long on close above a downsloping line drawn through 2+ pivot lows, with rising R-squared; stop beyond the last pivot.
- **Key Parameters:** Fit window 50-150 bars; touch tolerance 0.2 ATR; R-squared > 0.6 gate.
- **Duplicates Eliminated:** RU «пробой трендовой» роботы; CN 趋势线突破 scripts; linreg channel packs.

---

### PA-16 · Round Numbers / Psychological Levels
*整数关口 · Круглые уровни*

- **Origin & Lineage:** Institutional limit-order clustering observations (1990s microstructure research); retail codification in forex communities.
- **Core Hypothesis:** Prices ending in zeros (and in CN/JPY contexts, fives) attract limit orders and stops, producing magnet-then-reject behavior; systematic approaches fade first touches of fresh round levels in ranges or use them as profit targets for momentum trades. Microstructure studies confirm clustering in FX and equities, making this one of the few patterns with clean academic support at the order-book level.
- **Execution Rules:** Define level = round(close, step); fade first touch when range regime; or place targets at the next level in trend regime.
- **Key Parameters:** Step = 1/2/10/100 by asset; first-touch-only rule; ATR distance filter.
- **Duplicates Eliminated:** CN 整数关口战法; RU «круглые цифры» robots; FX 'big figure' trading.

---
