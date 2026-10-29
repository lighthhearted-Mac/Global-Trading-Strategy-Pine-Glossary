# Family MR: Mean Reversion & Oscillators

**Total Strategies in Family:** 15  
**Pine Script v5 Implementations:** 7  

## Strategies Overview

| ID | Strategy Name | Alternative Names | Has Pine Code |
|---|---|---|:---:|
| **MR-01** | [Connors RSI(2) Pullback](#mr-01--connors_rsi2_pullback) | 康纳斯RSI(2)回调 · Система RSI(2) Коннорса | ✅ Pine v5 |
| **MR-02** | [Bollinger Band Reversion (%B Fade)](#mr-02--bollinger_band_reversion_b_fade) | 布林带回归 · Отскок от границ Боллинджера | ✅ Pine v5 |
| **MR-03** | [Double 7s / 3-Day High-Low Pullback](#mr-03--double_7s_3_day_high_low_pullback) | 双七策略 · Система 'двойная семёрка' | 📖 Logic-only |
| **MR-04** | [Keltner Channel Pullback](#mr-04--keltner_channel_pullback) | 肯特纳通道回调 · Откат по каналам Кельтнера | 📖 Logic-only |
| **MR-05** | [TTM Squeeze / Squeeze Momentum](#mr-05--ttm_squeeze_squeeze_momentum) | 布林-KC挤压 · Сжатие Боллинджера и Кельтнера | ✅ Pine v5 |
| **MR-06** | [QQE (Qualitative Quantitative Estimation)](#mr-06--qqe_qualitative_quantitative_estimation) | QQE指标系统 · QQE-система | ✅ Pine v5 |
| **MR-07** | [WaveTrend Oscillator](#mr-07--wavetrend_oscillator) | 波形震荡器 · Волновой осциллятор WaveTrend | ✅ Pine v5 |
| **MR-08** | [Fisher Transform Reversal](#mr-08--fisher_transform_reversal) | 费雪变换反转 · Преобразование Фишера | ✅ Pine v5 |
| **MR-09** | [RSI Regular Divergence System](#mr-09--rsi_regular_divergence_system) | RSI背离系统 · Дивергенции по RSI | ✅ Pine v5 |
| **MR-10** | [Stochastic Oversold System](#mr-10--stochastic_oversold_system) | 随机指标超卖系统 · Система по стохастику | 📖 Logic-only |
| **MR-11** | [Pivot Point Reversion](#mr-11--pivot_point_reversion) | 枢轴点回归 · Торговля от пивотов | 📖 Logic-only |
| **MR-12** | [Intraday VWAP Mean Reversion](#mr-12--intraday_vwap_mean_reversion) | VWAP日内均值回归 · Возврат к VWAP | 📖 Logic-only |
| **MR-13** | [Z-Score Spread Reversion](#mr-13--z_score_spread_reversion) | Z分数价差回归 · Z-score возврат спреда | 📖 Logic-only |
| **MR-14** | [Williams %R Fade](#mr-14--williams_r_fade) | 威廉指标回归 · Уильямс %R | 📖 Logic-only |
| **MR-15** | [Money-Flow Reversion (CMF/MFI)](#mr-15--money_flow_reversion_cmfmfi) | 资金流回归 · Возврат по денежному потоку | 📖 Logic-only |

---

### MR-01 · Connors RSI(2) Pullback
*康纳斯RSI(2)回调 · Система RSI(2) Коннорса*

- **Origin & Lineage:** Laurence Connors, Short Term Trading Strategies That Work (2009) and Connors Research papers.
- **Core Hypothesis:** Buy short-term panic inside an uptrend: RSI(2) under 10 while price is above its 200-day average, exit into the snap-back near RSI 55-65 or the 5-day MA. The edge is heavily documented on US equities and ETFs and degrades on assets with fat left tails. It is the archetype of 'buy the dip, sell the rip' mechanical scalping.
- **Execution Rules:** Long when trend filter true and RSI(2) < buy level; exit when RSI(2) > exit level or close > SMA(5); short mirror below the 200-day MA.
- **Key Parameters:** RSI 2 (3-5 variants); buy <10, exit >60; 200-MA regime filter.
- **Duplicates Eliminated:** RSI(3)/RSI(4) variants; CN 短线超卖反弹 templates; RU 'RSI отскок' MT4 robots.

**Pine Script Reference Implementation:** [`mr-01_connors_rsi2_pullback.pine`](mr-01_connors_rsi2_pullback.pine)

```pinescript
//@version=5
strategy("RSI(2) Pullback (Connors-style)", overlay=true)
rsiLen = input.int(2, "RSI length")
buyLv  = input.int(10, "Buy below")
sellLv = input.int(60, "Exit above")
trendOk = close > ta.sma(close, 200)
r = ta.rsi(close, rsiLen)
if trendOk and r < buyLv
strategy.entry("L", strategy.long)
if strategy.position_size > 0 and (r > sellLv or close > ta.sma(close, 5))
strategy.close("L", comment="Snap-back exit")
```

---

### MR-02 · Bollinger Band Reversion (%B Fade)
*布林带回归 · Отскок от границ Боллинджера*

- **Origin & Lineage:** John Bollinger, 1980s (Bollinger on Bollinger Bands, 2001).
- **Core Hypothesis:** Price outside a 2-sigma band is statistically stretched; fade back to the mean basis, ideally only in the direction of the higher-timeframe trend. Bollinger himself warns that walking the band is a trend signal, so serious implementations add a trend gate or a squeeze precondition. It is one of the two or three most universal retail strategies on earth.
- **Execution Rules:** Long when trend-up and close pierces the lower band, exit at the middle band; short mirrored; optional RSI confluence.
- **Key Parameters:** Length 20, deviations 2.0; exit at SMA(20); RSI(14) < 30 confluence.
- **Duplicates Eliminated:** CN 布林带下轨抄底 (ETF/股票); RU «торговля от границ Боллинджера»; Bollinger %B factor research.

**Pine Script Reference Implementation:** [`mr-02_bollinger_band_reversion_b_fade.pine`](mr-02_bollinger_band_reversion_b_fade.pine)

```pinescript
//@version=5
strategy("Bollinger Band Reversion", overlay=true)
len  = input.int(20, "Length")
mult = input.float(2.0, "StdDev")
basis = ta.sma(close, len)
dev   = mult * ta.stdev(close, len)
lower = basis - dev
trendUp = close > ta.sma(close, 200)
if trendUp and close < lower
strategy.entry("L", strategy.long)
if strategy.position_size > 0 and close >= basis
strategy.close("L", comment="Mean reversion")
```

---

### MR-03 · Double 7s / 3-Day High-Low Pullback
*双七策略 · Система 'двойная семёрка'*

- **Origin & Lineage:** Laurence Connors & Cesar Alvarez, Connors Research (2010s).
- **Core Hypothesis:** An extremely simple pullback quantification: buy when close is at its lowest of the last 7 days but the market is above its 200-day MA, exit at the highest close of the last 7 days. Variants substitute 3-day windows or add a cumulative RS filter. It demonstrates how small the mean-reversion edge can be while still being systematic.
- **Execution Rules:** Long on 7-day-low close above SMA(200); exit on 7-day-high close; time-stop optional.
- **Key Parameters:** Window 7 (3-day variant); 200-MA filter; position ~equally weighted across a basket.
- **Duplicates Eliminated:** 3-Day High/Low; 'TFSE' Connors variants; CN 七日新低反弹 scripts.

---

### MR-04 · Keltner Channel Pullback
*肯特纳通道回调 · Откат по каналам Кельтнера*

- **Origin & Lineage:** Chester Keltner, 1960 (10-day MA of typical price); modern ATR version by Linda Raschke, 1990s.
- **Core Hypothesis:** Raschke's modernization sets the channel at EMA(20) +/- 1.5-2 x ATR(10); mean-reversion traders fade the outer band back to the EMA, while trend traders use the opposite (KingKeltner breakout in vn.py). The same envelope therefore hosts two opposite philosophies depending on whether the trend filter is inside or outside the system. This entry covers the fade form; the breakout form is BK-13.
- **Execution Rules:** Long when close < lower Keltner band in an uptrend regime; exit at the EMA basis or opposite band.
- **Key Parameters:** EMA 20; ATR 10; multiple 1.5-2.0.
- **Duplicates Eliminated:** vn.py KingKeltnerStrategy (breakout form, cross-ref BK-13); CN 肯特纳通道 scripts; RU каналы Кельтнера.

---

### MR-05 · TTM Squeeze / Squeeze Momentum
*布林-KC挤压 · Сжатие Боллинджера и Кельтнера*

- **Origin & Lineage:** John Carter, Mastering the Trade (2005); LazyBear's open Pine port (2014) made it a TradingView staple.
- **Core Hypothesis:** When Bollinger Bands fit entirely inside Keltner Channels, volatility has compressed to a coiled state; the script fires when the squeeze releases, in the direction of a linreg momentum histogram measured against the midpoint of the range. It is a volatility-contraction breakout disguised as an oscillator and is among the most-cloned scripts on TradingView.
- **Execution Rules:** Arm during squeeze-on; enter on squeeze fire with histogram positive (long) or negative (short); trail via histogram color flips or ATR stop.
- **Key Parameters:** BB 20/2.0; KC 20/1.5; momentum linreg 20.
- **Duplicates Eliminated:** Squeeze Momentum Indicator [LazyBear]; Squeeze Pro (LuxAlgo, cross-ref BK-11); CN 布林收口战法; RU «сжатие волатильности» scripts.

**Pine Script Reference Implementation:** [`mr-05_ttm_squeeze_squeeze_momentum.pine`](mr-05_ttm_squeeze_squeeze_momentum.pine)

```pinescript
//@version=5
strategy("TTM Squeeze", overlay=false)
lenBB = input.int(20, "BB length")
multBB = input.float(2.0, "BB mult")
lenKC = input.int(20, "KC length")
multKC = input.float(1.5, "KC mult")
basis = ta.sma(close, lenBB)
dev   = multBB * ta.stdev(close, lenBB)
bbU   = basis + dev
bbL   = basis - dev
ma    = ta.ema(close, lenKC)
rng   = ta.atr(lenKC)
kcU   = ma + multKC * rng
kcL   = ma - multKC * rng
squeezeOn = bbU < kcU and bbL > kcL
mom = ta.linreg(close - math.avg(math.avg(ta.highest(high, lenKC),
ta.lowest(low, lenKC)), ta.sma(close, lenKC)), lenKC, 0)
fired = squeezeOn[1] and not squeezeOn
if fired and mom > 0
strategy.entry("L", strategy.long)
if fired and mom < 0
strategy.entry("S", strategy.short)
plot(mom, "Momentum", style=plot.style_histogram,
color=mom >= 0 ? color.teal : color.red)
hline(0)
bgcolor(squeezeOn ? color.new(color.orange, 80) : na)
```

---

### MR-06 · QQE (Qualitative Quantitative Estimation)
*QQE指标系统 · QQE-система*

- **Origin & Lineage:** MT4 forex community (2000s); famous 'QQE mod' by Glaz on TradingView (2014+); MT4 port by Mihkel00.
- **Core Hypothesis:** QQE smooths RSI with a short EMA and wraps it in a Wilder-style ATR-of-the-RSI trailing band, so signals are RSI crosses of a volatility-adjusted trail rather than raw oversold touches. The construction gives RSI trend-following behavior with far fewer whipsaws. It is beloved in forex and gold scalping communities in both Russian and Chinese forums.
- **Execution Rules:** Long when the smoothed RSI crosses above its lower ATR trail; short on the cross under the upper trail; optional 50-line regime filter.
- **Key Parameters:** RSI 14, smoothing 5, Wilder 14, factor 4.238 (classic mod settings).
- **Duplicates Eliminated:** QQE MOD (Glaz, Mihkel00 ports); RU QQE-форекс советники; CN QQE+MACD hybrids.

**Pine Script Reference Implementation:** [`mr-06_qqe_qualitative_quantitative_estimation.pine`](mr-06_qqe_qualitative_quantitative_estimation.pine)

```pinescript
//@version=5
strategy("QQE (RSI + RSI-ATR Trailing)", overlay=false)
rsiLen  = input.int(14, "RSI length")
smLen   = input.int(5, "RSI smoothing")
wildLen = input.int(14, "Wilder length")
sf      = input.float(4.238, "ATR factor")
rsi   = ta.rsi(close, rsiLen)
rsiMa = ta.ema(rsi, smLen)
dar   = ta.ema(ta.rma(math.abs(rsiMa - nz(rsiMa[1], rsiMa)), wildLen), 2 * wildLen - 1)
band  = sf * dar
var float trailUp = na
var float trailDn = na
trailUp := nz(rsiMa[1], rsiMa) > nz(trailUp[1], 0) and rsiMa > nz(trailUp[1], 0) ?
math.max(nz(trailUp[1]), rsiMa - band) : rsiMa - band
trailDn := nz(rsiMa[1], rsiMa) < nz(trailDn[1], 100) and rsiMa < nz(trailDn[1], 100) ?
math.min(nz(trailDn[1]), rsiMa + band) : rsiMa + band
if ta.crossover(rsiMa, trailDn)
strategy.entry("L", strategy.long)
if ta.crossunder(rsiMa, trailUp)
strategy.entry("S", strategy.short)
plot(rsiMa, "RSI MA", color=color.teal)
plot(trailUp, "Fast trail", color=color.new(color.red, 30))
plot(trailDn, "Slow trail", color=color.new(color.teal, 30))
hline(50)
```

---

### MR-07 · WaveTrend Oscillator
*波形震荡器 · Волновой осциллятор WaveTrend*

- **Origin & Lineage:** Ported from TradeStation/MetaTrader origins by LazyBear (2014) — 'The Perfectionist' lineage; exact original author unknown.
- **Core Hypothesis:** WaveTrend measures the typical price's distance from its own EMA, normalized by 0.015 x an EMA of absolute deviation, then double-smoothed — producing a very smooth cycle oscillator with distinctive overbought/oversold plateaus. Trades fire on WT1/WT2 crosses at extremes. It is one of the top-installed community oscillators ever and the standard confirmation layer in crypto scalping dashboards.
- **Execution Rules:** Long on WT1 crossing above WT2 below the oversold band; short on the cross under above overbought; exit near the zero line.
- **Key Parameters:** Channel length 10, average 21, bands +/-53; signal SMA 4.
- **Duplicates Eliminated:** WaveTrend [WT] (LazyBear); SJ WaveTrend and dozens of forks; CN WT+VWAP scalping dashboards; RU WaveTrend forks on MQL5.

**Pine Script Reference Implementation:** [`mr-07_wavetrend_oscillator.pine`](mr-07_wavetrend_oscillator.pine)

```pinescript
//@version=5
strategy("WaveTrend Oscillator Cross", overlay=false)
chLen  = input.int(10, "Channel length")
avgLen = input.int(21, "Average length")
obLv   = input.float(53, "Overbought")
osLv   = input.float(-53, "Oversold")
ap  = hlc3
esa = ta.ema(ap, chLen)
d   = ta.ema(math.abs(ap - esa), chLen)
ci  = (ap - esa) / (0.015 * math.max(d, syminfo.mintick))
wt1 = ta.ema(ci, avgLen)
wt2 = ta.sma(wt1, 4)
if ta.crossover(wt1, wt2) and wt1 < osLv
strategy.entry("L", strategy.long)
if ta.crossunder(wt1, wt2) and wt1 > obLv
strategy.entry("S", strategy.short)
plot(wt1, "WT1", color=color.teal)
plot(wt2, "WT2", color=color.red)
hline(obLv)
hline(osLv)
hline(0)
```

---

### MR-08 · Fisher Transform Reversal
*费雪变换反转 · Преобразование Фишера*

- **Origin & Lineage:** John Ehlers, 'Using the Fisher Transform', TASC November 2002.
- **Core Hypothesis:** The Fisher transform maps any bounded oscillator (here a normalized price position in its range) through a logit-like function that sharpens turning points: ordinary swings become nearly Gaussian-peaked, so crossings of the transformed line with its 1-bar lag mark reversals unusually cleanly. Ehlers designed it to make cycle turning points unambiguous for mechanical exits.
- **Execution Rules:** Long on Fisher crossing above its previous value while negative; short on the cross under while positive; exit on opposite signal or zero-line pass.
- **Key Parameters:** Length 9; clamps the normalized value to +/-0.999.
- **Duplicates Eliminated:** Fisher in Ehlers' book suite (Cybernetic Analysis, 2002); MT4/MT5 Fisher; CN 费雪指标 scripts.

**Pine Script Reference Implementation:** [`mr-08_fisher_transform_reversal.pine`](mr-08_fisher_transform_reversal.pine)

```pinescript
//@version=5
strategy("Ehlers Fisher Transform", overlay=false)
len = input.int(9, "Length")
hh  = ta.highest(high, len)
ll  = ta.lowest(low, len)
rng = math.max(hh - ll, syminfo.mintick)
var float val = 0.0
var float fish = 0.0
val  := 0.33 * 2.0 * ((close - ll) / rng - 0.5) + 0.67 * nz(val[1])
val  := math.max(math.min(val, 0.999), -0.999)
fish := 0.5 * math.log((1 + val) / (1 - val)) + 0.5 * nz(fish[1])
if ta.crossover(fish, nz(fish[1])) and fish < 0
strategy.entry("L", strategy.long)
if ta.crossunder(fish, nz(fish[1])) and fish > 0
strategy.entry("S", strategy.short)
plot(fish, "Fisher", color=color.teal)
plot(nz(fish[1]), "Trigger", color=color.red)
hline(0)
```

---

### MR-09 · RSI Regular Divergence System
*RSI背离系统 · Дивергенции по RSI*

- **Origin & Lineage:** Classic manual TA (Wilder's RSI, 1978) mechanized via pivot detection in the Pine community (2010s).
- **Core Hypothesis:** A regular bullish divergence forms when price prints a lower low while RSI prints a higher low — selling exhaustion. Mechanical detection compares the last two RSI pivot lows and the price lows between them, then enters on confirmation. Divergence systems look brilliant on annotated screenshots and are much noisier in backtests, so implementations always add trend and volatility filters.
- **Execution Rules:** Detect RSI pivot lows (5/5); long when a new lower price low pairs with a higher RSI low, above a 200-MA; exit on RSI failing above 70.
- **Key Parameters:** Pivot left/right 5; RSI 14; divergence lookback ~60 bars.
- **Duplicates Eliminated:** Hidden divergence variants; CN MACD/RSI背离战法; RU 'дивергенция' robots on MQL5.

**Pine Script Reference Implementation:** [`mr-09_rsi_regular_divergence_system.pine`](mr-09_rsi_regular_divergence_system.pine)

```pinescript
//@version=5
strategy("RSI Regular Divergence", overlay=false)
rsiLen = input.int(14, "RSI")
lbL = input.int(5, "Pivot left")
lbR = input.int(5, "Pivot right")
rsi = ta.rsi(close, rsiLen)
pl  = ta.pivotlow(rsi, lbL, lbR)
var float lastPL = na
var float prevPL = na
var float lastPLPrice = na
var float prevPLPrice = na
if not na(pl)
prevPL      := lastPL
prevPLPrice := lastPLPrice
lastPL      := pl
lastPLPrice := low[lbR]
bullDiv = not na(prevPL) and lastPL > prevPL and lastPLPrice < prevPLPrice
if bullDiv and close > ta.sma(close, 200)
strategy.entry("L", strategy.long)
if strategy.position_size > 0 and ta.crossunder(rsi, 70)
strategy.close("L", comment="RSI roll")
plot(rsi, "RSI", color=color.teal)
hline(30)
hline(70)
```

---

### MR-10 · Stochastic Oversold System
*随机指标超卖系统 · Система по стохастику*

- **Origin & Lineage:** George Lane, 1950s-1980s (stochastic oscillator).
- **Core Hypothesis:** Fade %K/%D extremes toward the middle of the range, classically demanding a cross out of the 20/80 zones as confirmation rather than entry at the extreme itself. Lane's original framing tied the indicator to cycle troughs; modern use adds trend filters because raw stochastic fades bleed in trends. It remains the default oscillator in Russian and Chinese retail platforms.
- **Execution Rules:** Long when %K crosses above %D from below 20; exit at 50 or 80; short mirrored.
- **Key Parameters:** 14/3/3 classic; CN 9/3/3 intraday variants.
- **Duplicates Eliminated:** RU «Стохастик + RSI» комбо-роботы; CN KDJ战法 (the CN KDJ is a stochastic variant); MT4 stochastic packs.

---

### MR-11 · Pivot Point Reversion
*枢轴点回归 · Торговля от пивотов*

- **Origin & Lineage:** Floor-trader pivots, pre-digital Chicago pits; codified in 1990s day-trading literature (Crabel, Pesavento).
- **Core Hypothesis:** Compute R1/S1 pivots from the prior session's high/low/close and fade touches back toward the central pivot when the day is range-bound. The system is a session-anchored mean reversion with unusually clean institutional logic — everyone watches the same levels. It requires an intraday trend filter (e.g., yesterday's close vs today's open) to avoid fading real trend days.
- **Execution Rules:** Long at S1 if open > prior close (gap-up bias); exit at PP or R1; short mirrored; skip on wide-gap trend days.
- **Key Parameters:** Classic pivot formulas; skip threshold for gaps > 0.5 x ATR.
- **Duplicates Eliminated:** CN 分时均线/枢轴 strategies; RU 'пивот-уровни' robots; every MT4 pivot indicator pack.

---

### MR-12 · Intraday VWAP Mean Reversion
*VWAP日内均值回归 · Возврат к VWAP*

- **Origin & Lineage:** Institutional execution benchmark turned retail signal (1990s-2000s); Pine ta.vwap session form.
- **Core Hypothesis:** VWAP is the day's institutional cost basis; when price stretches multiple standard deviations away, mean-reversion traders fade back toward it, exploiting the same pull that execution algos exert. Implementations typically require the deviation to be volatility-normalized and avoid fading on breakout days (strong trend + news). The companion breakout use of VWAP belongs to VO-07/08.
- **Execution Rules:** Long when close < VWAP - 2 x rolling stdev of (close - VWAP) with no gap-news regime; exit at VWAP; short mirrored.
- **Key Parameters:** Deviation window 20-50 bars; bands at 1-2 sigma; hard time-stop by session end.
- **Duplicates Eliminated:** CN 分时VWAP回归; RU «откат к VWAP» скрипты; every VWAP-bands pack on TradingView.

---

### MR-13 · Z-Score Spread Reversion
*Z分数价差回归 · Z-score возврат спреда*

- **Origin & Lineage:** Academic stat-arb (Gatev et al. 1999; Avellaneda & Lee 2010) adapted to single-asset z-scores.
- **Core Hypothesis:** Standardize a price, spread, or indicator as a rolling z-score and trade crossings of +/-2 back toward zero, with sizing scaled by the z magnitude. On a pair spread it is pairs trading (ST-01); on a single asset's deviation from its own anchor (MA, VWAP, ratio to a lead) it is the general form of every band fade in this family. The z formulation is what makes threshold tuning transferable across assets.
- **Execution Rules:** Enter at z beyond +/-2 in the direction of reversion; exit at z = 0; hard stop at z = +/-3.5 (assumption break).
- **Key Parameters:** Lookback 20-60 for the mean/sigma; half-life check via Ornstein-Uhlenbeck fit.
- **Duplicates Eliminated:** RU «Z-score роботы»; CN 标准化偏离策略; Pairs-trading single-leg approximations.

---

### MR-14 · Williams %R Fade
*威廉指标回归 · Уильямс %R*

- **Origin & Lineage:** Larry Williams, 1966-1973 (the %R oscillator).
- **Core Hypothesis:** A normalized stochastic that reads where close sits inside the recent high-low range; classic use fades readings beyond -80/-20 back toward the midrange. Williams himself is better known for volatility-breakout systems (C-Degree, OOPS), so the fade form is the community's usage rather than the author's own trading. It shares all the standard oscillator-fade caveats.
- **Execution Rules:** Long when %R crosses up through -80; exit at -50 or -20; short mirrored.
- **Key Parameters:** 14-period standard; session-filtered intraday variants.
- **Duplicates Eliminated:** RU %R-роботы; CN 威廉指标战法; bundled in every platform's default indicator set.

---

### MR-15 · Money-Flow Reversion (CMF/MFI)
*资金流回归 · Возврат по денежному потоку*

- **Origin & Lineage:** Chaikin Money Flow / Accumulation-Distribution (Marc Chaikin, 1966-1980s); Money Flow Index (Quong & Soudack, 1989).
- **Core Hypothesis:** Volume-weighted oscillators score whether closing strength coincides with volume; readings at extremes with price not confirming signal absorption or climactic transfer. Mean-reversion implementations fade CMF/MFI extremes toward zero with a price-trend filter, treating the volume dimension as the edge over plain RSI fades.
- **Execution Rules:** Long when MFI(14) < 20 with price above its 200-MA; exit when MFI > 50; CMF variant uses +/-0.25 bands.
- **Key Parameters:** MFI 14; CMF 20-21; regime filter 200-MA.
- **Duplicates Eliminated:** CN 资金流指标策略; RU «денежный поток» индикаторные системы; OBV-family hybrids (cross VO-02).

---
