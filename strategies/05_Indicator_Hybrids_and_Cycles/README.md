# Family IH: Indicator Hybrids & Cycles

**Total Strategies in Family:** 14  
**Pine Script v5 Implementations:** 3  

## Strategies Overview

| ID | Strategy Name | Alternative Names | Has Pine Code |
|---|---|---|:---:|
| **IH-01** | [MESA Adaptive MA (MAMA / FAMA)](#ih-01--mesa_adaptive_ma_mama_fama) | MESA自适应均线 · Адаптивная MESA | 📖 Logic-only |
| **IH-02** | [Instantaneous Trendline & Sine Wave](#ih-02--instantaneous_trendline_sine_wave) | 瞬时趋势线与正弦波 · Мгновенная линия тренда | 📖 Logic-only |
| **IH-03** | [Cyber Cycle](#ih-03--cyber_cycle) | 赛博周期 · Кибер-цикл | 📖 Logic-only |
| **IH-04** | [Ehlers SuperSmoother / Roofing Filter](#ih-04--ehlers_supersmoother_roofing_filter) | 超级平滑器 · Супер-сглаживатель | ✅ Pine v5 |
| **IH-05** | [Vortex Indicator](#ih-05--vortex_indicator) | 涡流指标 · Индикатор Вортекс | ✅ Pine v5 |
| **IH-06** | [True Strength Index (TSI)](#ih-06--true_strength_index_tsi) | 真实强度指数 · Индекс истинной силы | ✅ Pine v5 |
| **IH-07** | [Schaff Trend Cycle](#ih-07--schaff_trend_cycle) | 沙夫趋势循环 · Трендовый цикл Шаффа | 📖 Logic-only |
| **IH-08** | [Connors RSI (Composite)](#ih-08--connors_rsi_composite) | 康纳斯复合RSI · Композитный RSI Коннорса | 📖 Logic-only |
| **IH-09** | [Stochastic RSI](#ih-09--stochastic_rsi) | 随机RSI · Stochastic RSI | 📖 Logic-only |
| **IH-10** | [Commodity Channel Index Systems](#ih-10--commodity_channel_index_systems) | CCI顺势/回归系统 · Системы по CCI | 📖 Logic-only |
| **IH-11** | [Chande Momentum Oscillator](#ih-11--chande_momentum_oscillator) | 钱德动量摆动指标 · Осциллятор Чанде | 📖 Logic-only |
| **IH-12** | [Ultimate Oscillator](#ih-12--ultimate_oscillator) | 终极摆动指标 · Ультимативный осциллятор | 📖 Logic-only |
| **IH-13** | [Long-Cycle Momentum Composites (KST / Coppock)](#ih-13--long_cycle_momentum_composites_kst_coppock) | 长周期动量合成指标 · Долгосрочные осцилляторы | 📖 Logic-only |
| **IH-14** | [Detrended Price Oscillator & Cycle Projection](#ih-14--detrended_price_oscillator_cycle_projection) | 去趋势价格振荡器 · DPO и проекция циклов | 📖 Logic-only |

---

### IH-01 · MESA Adaptive MA (MAMA / FAMA)
*MESA自适应均线 · Адаптивная MESA*

- **Origin & Lineage:** John Ehlers, Rocket Science for Traders (2001); MESA trademark line.
- **Core Hypothesis:** A Hilbert-transform cycle measurement continuously retunes an EMA: when cycles are strong the MAMA tracks price closely, and the FAMA (MAMA of MAMA) trails as the signal line. Crosses of MAMA and FAMA generate signals that self-adjust to the dominant cycle length. It is the flagship of Ehlers' adaptive-filter program, though the full implementation is intricate enough that many ports approximate the phase calculation.
- **Execution Rules:** Long on MAMA crossing above FAMA; short mirrored; cycle period gate optional.
- **Key Parameters:** Fast limit 0.5, slow limit 0.05.
- **Duplicates Eliminated:** MAMA/FAMA ports (TradeStation->MT4->Pine); CN 自适应均线 experiments.

---

### IH-02 · Instantaneous Trendline & Sine Wave
*瞬时趋势线与正弦波 · Мгновенная линия тренда*

- **Origin & Lineage:** John Ehlers, Rocket Science for Traders (2001).
- **Core Hypothesis:** The Hilbert transform's dominant-cycle phase drives a sine wave that leads price into turns; when the phase line is clean, sine-vs-leadline crosses time reversals, and when the market is trending the tool itself says 'do not use me'. That self-aware regime flag is the sophisticated part: Ehlers explicitly gates the oscillator by trend detection. The instantaneous trendline (a phaser-corrected smoothing) is the companion trend measure.
- **Execution Rules:** Trade sine/leadline crosses only when the trend-mode flag is off; stand aside otherwise.
- **Key Parameters:** Standard Hilbert constants; smoothing length ~7 for the trendline.
- **Duplicates Eliminated:** Ehlers book-code ports; MT4/MT5 Hilbert suites.

---

### IH-03 · Cyber Cycle
*赛博周期 · Кибер-цикл*

- **Origin & Lineage:** John Ehlers, Cybernetic Analysis for Stocks and Futures (2004).
- **Core Hypothesis:** A two-pole high-pass filter that isolates the cycle component of price with minimal lag, then smooths it; crossovers with a trigger mark cycle turns. Ehlers positioned it as the clean cycle-extraction baseline against which more complex MESA work is judged. Its simplicity makes it one of the most-ported Ehlers tools.
- **Execution Rules:** Long on cycle crossing above trigger from a trough; short mirrored; skip signals when the trend component dominates.
- **Key Parameters:** Alpha ~0.07 smoothing; trigger 3-bar EMA.
- **Duplicates Eliminated:** Ports in the Ehlers TASC archive; CN 循环指标 experiments.

---

### IH-04 · Ehlers SuperSmoother / Roofing Filter
*超级平滑器 · Супер-сглаживатель*

- **Origin & Lineage:** John Ehlers, 'Predictive and Dedicated Indicators' (TASC 2013); roofing filter introduced with it.
- **Core Hypothesis:** The SuperSmoother is a two-pole Butterworth-style filter that removes aliasing noise far better than an EMA of equal length — Ehlers recommends it as the default replacement for every EMA in older systems. The roofing filter cascades a high-pass and SuperSmoother to feed clean data into cycle indicators. As a system it is a component, but its adoption fixed a generation of indicator quality.
- **Execution Rules:** Substitute SuperSmoother for EMA/SMA in any trend system; use roofing-filter output for cycle indicators.
- **Key Parameters:** Length 10 canonical; roofing bandpass 30-100 cycles.
- **Duplicates Eliminated:** SuperSmoother ports everywhere; CN 超平滑滤波 scripts.

**Pine Script Reference Implementation:** [`ih-04_ehlers_supersmoother_roofing_filter.pine`](ih-04_ehlers_supersmoother_roofing_filter.pine)

```pinescript
//@version=5
indicator("Ehlers SuperSmoother", overlay=true)
len = input.int(10, "Length")
price = hl2
a1 = math.exp(-1.414 * 3.14159 / len)
b1 = 2.0 * a1 * math.cos(1.414 * 3.14159 / len)
c2 = b1
c3 = -a1 * a1
c1 = 1.0 - c2 - c3
var float ss = na
ss := c1 * (price + nz(price[1])) / 2.0 + c2 * nz(ss[1]) + c3 * nz(ss[2])
plot(ss, "SuperSmoother", color=color.teal)
```

---

### IH-05 · Vortex Indicator
*涡流指标 · Индикатор Вортекс*

- **Origin & Lineage:** Etienne Botes & Douglas Siepman, TASC January 2010, inspired by Hans Hannula's vortex concept and water vortex dynamics.
- **Core Hypothesis:** VI+ sums upward true-motion (high to prior low) and VI- the downward mirror, each normalized by true range; VI+ crossing above VI- marks trend initiation, sustained separation marks trend health. It was explicitly designed to catch the start of trends faster than DMI while sharing its normalization philosophy. A compact, well-specified system that ports perfectly.
- **Execution Rules:** Long on VI+ crossing above VI-; exit on reverse cross or VI+ falling below 1.0 from a high.
- **Key Parameters:** Length 14 (21 on higher TFs).
- **Duplicates Eliminated:** Vortex packs on all platforms; CN 涡流指标; RU Вортекс robots.

**Pine Script Reference Implementation:** [`ih-05_vortex_indicator.pine`](ih-05_vortex_indicator.pine)

```pinescript
//@version=5
indicator("Vortex Indicator", overlay=false)
len = input.int(14, "Length")
vmPlus  = math.abs(high - nz(low[1]))
vmMinus = math.abs(low - nz(high[1]))
trSum = ta.sum(ta.tr(true), len)
vip = ta.sum(vmPlus, len) / trSum
vim = ta.sum(vmMinus, len) / trSum
plot(vip, "VI+", color=color.teal)
plot(vim, "VI-", color=color.red)
hline(1)
```

---

### IH-06 · True Strength Index (TSI)
*真实强度指数 · Индекс истинной силы*

- **Origin & Lineage:** William Blau, TASC 1991; Momentum, Direction and Divergence (1995).
- **Core Hypothesis:** TSI double-smooths momentum (25/13 classic) and normalizes by double-smoothed absolute momentum, yielding an oscillator bounded near +/-100 that tracks trend quality with unusually low noise. Blau's design philosophy — smooth first, then normalize — makes TSI excellent for divergence work and as a momentum-of-trend confirmation.
- **Execution Rules:** Long on TSI crossing its signal line below zero in an uptrend regime; exit at signal re-cross or overbought roll.
- **Key Parameters:** 25/13/7 classic; 13/7/5 faster variant.
- **Duplicates Eliminated:** TSI packs everywhere; CN TSI策略; RU TSI форекс-роботы.

**Pine Script Reference Implementation:** [`ih-06_true_strength_index_tsi.pine`](ih-06_true_strength_index_tsi.pine)

```pinescript
//@version=5
indicator("True Strength Index", overlay=false)
lenL = input.int(25, "Long length")
lenS = input.int(13, "Short length")
sigLen = input.int(13, "Signal length")
m = ta.mom(close, 1)
tsiVal = 100 * ta.ema(ta.ema(m, lenL), lenS) / ta.ema(ta.ema(math.abs(m), lenL), lenS)
sig = ta.ema(tsiVal, sigLen)
plot(tsiVal, "TSI", color=color.teal)
plot(sig, "Signal", color=color.red)
hline(0)
hline(25)
hline(-25)
```

---

### IH-07 · Schaff Trend Cycle
*沙夫趋势循环 · Трендовый цикл Шаффа*

- **Origin & Lineage:** Doug Schaff, 1999 (presented 2008; licensed to FXCM-era platforms).
- **Core Hypothesis:** A MACD output re-normalized through a stochastic of itself, cycling between 0-100 faster than MACD reacts: it behaves like a trend-aware oscillator whose 25/75 extremes mark pullback entries inside trends. Popular in forex and gold trading, especially in RU-language signal groups, as a MACD replacement with earlier turns.
- **Execution Rules:** Long on cycle crossing up from below 25 in a MACD-positive regime; short mirrored.
- **Key Parameters:** MACD 23/50/9, cycle 10; thresholds 25/75.
- **Duplicates Eliminated:** STC ports across MT4/MT5/Pine; CN STC experiments.

---

### IH-08 · Connors RSI (Composite)
*康纳斯复合RSI · Композитный RSI Коннорса*

- **Origin & Lineage:** Connors Research, 2012 (Larry Connors, Cesar Alvarez, Austin Lee).
- **Core Hypothesis:** A three-component composite: RSI(3) of price, streak-RSI (duration of consecutive up/down closes), and PercentRank of 1-day returns, averaged. It quantifies both stretch and abnormal one-day moves, producing sharper oversold readings than plain RSI for mean-reversion entries in the Connors program.
- **Execution Rules:** Long when composite < 15 with trend filter; exit on composite > 50-70; short mirrored.
- **Key Parameters:** RSI 3; streak RSI 2; PercentRank window 100.
- **Duplicates Eliminated:** CRSI packs; CN 复合RSI; RU CRSI-роботы.

---

### IH-09 · Stochastic RSI
*随机RSI · Stochastic RSI*

- **Origin & Lineage:** Tushar Chande & Stanley Kroll, The New Technical Trader (1994).
- **Core Hypothesis:** A stochastic applied to RSI rather than price, making the oscillator reach extremes far more often and earlier — useful for timing pullback entries inside established trends where raw RSI lags. It is the timing layer inside many trend-pullback hybrids and a default indicator on CN/RU platforms.
- **Execution Rules:** Long when stochRSI crosses up from < 20 while price is above the 200-MA; exit at 80+ cross down.
- **Key Parameters:** RSI 14; stochastic 14/3/3.
- **Duplicates Eliminated:** Everywhere; CN KDJ-of-RSI variants; RU stochRSI скальпинг packs.

---

### IH-10 · Commodity Channel Index Systems
*CCI顺势/回归系统 · Системы по CCI*

- **Origin & Lineage:** Donald Lambert, TASC October 1980.
- **Core Hypothesis:** CCI measures deviation of typical price from its SMA scaled by mean absolute deviation; Lambert's own framing was cyclical, but practice split it into a +/-100 breakout-trend system and a fade-at-extremes reversion system. The dual-personality is the reason it appears in both trend and reversion robots on CN and RU platforms.
- **Execution Rules:** Trend form: long on CCI > +100 (exit < -100); reversion form: fade CCI beyond +/-200 toward zero.
- **Key Parameters:** Length 20 (14 intraday); thresholds 100/200 by form.
- **Duplicates Eliminated:** CN CCI战法; RU CCI-советники; Woodie CCI variant (distinct calc, same idea).

---

### IH-11 · Chande Momentum Oscillator
*钱德动量摆动指标 · Осциллятор Чанде*

- **Origin & Lineage:** Tushar Chande, TASC March 1994 (also the VIDYA author).
- **Core Hypothesis:** CMO sums up-moves and down-moves over N bars into a -100/+100 momentum read with a fixed scale — a cleaner RSI alternative intended for overbought/oversold and trend-momentum readings. It powers Chande's own VIDYA adaptive average and appears as a momentum gate in hybrid systems.
- **Execution Rules:** Trend-momentum: long when CMO > 50 (with trend filter); fade form: CMO extremes beyond +/-50 toward the mid.
- **Key Parameters:** Length 9-14.
- **Duplicates Eliminated:** CMO in MetaStock-era libraries; CN CMO模板.

---

### IH-12 · Ultimate Oscillator
*终极摆动指标 · Ультимативный осциллятор*

- **Origin & Lineage:** Larry Williams, TASC 1985.
- **Core Hypothesis:** Blends buying-pressure averages over three weighted timeframes (7/14/28) to avoid the single-length trap; divergence between price and the composite is the primary signal. Williams designed it to catch accumulation/distribution phases that single-period oscillators miss, tying it loosely to his Wyckoff-influenced reading of markets.
- **Execution Rules:** Long on bullish divergence while UO < 30; exit at 50-70; short mirrored above 70.
- **Key Parameters:** 7/14/28 with 4/2/1 weights; bands 30/70.
- **Duplicates Eliminated:** UO packs; CN 终极指标; RU UO-роботы.

---

### IH-13 · Long-Cycle Momentum Composites (KST / Coppock)
*长周期动量合成指标 · Долгосрочные осцилляторы*

- **Origin & Lineage:** Coppock Curve: Edwin Coppock, Barron's 1962; KST: Martin Pring, 1990s.
- **Core Hypothesis:** Both aggregate multiple ROC lengths (Coppock: 14/11-month ROC smoothed by 10-month WMA; KST: four rate-of-change terms weighted) into slow momentum composites for monthly charts, designed around church-founding arithmetic in Coppock's case and cycle layering in Pring's. Signals are rare, zero-cross or turn-based, and act as regime context for shorter systems rather than standalone trades.
- **Execution Rules:** Long on curve turning up from below zero; exit on roll from above; use as regime gate.
- **Key Parameters:** Coppock 14/11/10 monthly; KST (10,15,20,30 ROC / 10,10,10,15 SMA).
- **Duplicates Eliminated:** Coppock screeners; RU «кривая Коппока» long-term followers.

---

### IH-14 · Detrended Price Oscillator & Cycle Projection
*去趋势价格振荡器 · DPO и проекция циклов*

- **Origin & Lineage:** 1980s cycle-analysis literature (Walter Bressert's work popularized the concept).
- **Core Hypothesis:** DPO shifts a displaced SMA to isolate the cycle component around a moving average, letting the analyst measure dominant cycle length and project the next trough/crest. Mechanically it feeds cycle-timed entries for oscillators (enter fades at projected troughs) rather than being traded on its own crossings. It is the practical bridge between Ehlers' DSP school and classic cycle-chart analysis.
- **Execution Rules:** Measure trough spacing on DPO; time mean-reversion entries near projected troughs; gate by cycle length stability.
- **Key Parameters:** DPO length 20-22 (period/2 + 1 displacement).
- **Duplicates Eliminated:** Bressert cycle tools; CN DPO周期模板; RU цикловый анализ.

---
