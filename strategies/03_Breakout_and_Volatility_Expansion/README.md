# Family BK: Breakout & Volatility Expansion

**Total Strategies in Family:** 13  
**Pine Script v5 Implementations:** 3  

## Strategies Overview

| ID | Strategy Name | Alternative Names | Has Pine Code |
|---|---|---|:---:|
| **BK-01** | [Opening Range Breakout (ORB)](#bk-01--opening_range_breakout_orb) | 开盘区间突破 · Пробой диапазона открытия | ✅ Pine v5 |
| **BK-02** | [Narrow Range 7 / Inside Day Patterns](#bk-02--narrow_range_7_inside_day_patterns) | 窄幅整理形态 · Внутренний день / узкий диапазон | 📖 Logic-only |
| **BK-03** | [Volatility Contraction Pattern (VCP)](#bk-03--volatility_contraction_pattern_vcp) | 波动收缩形态 · Модель сжатия волатильности | ✅ Pine v5 |
| **BK-04** | [Darvas Box](#bk-04--darvas_box) | 达瓦斯箱体 · Ящик Дарваса | 📖 Logic-only |
| **BK-05** | [Bill Williams Alligator + Fractals](#bk-05--bill_williams_alligator_fractals) | 比尔·威廉姆斯鳄鱼线+分形 · Аллигатор и фракталы Вильямса | ✅ Pine v5 |
| **BK-06** | [Awesome Oscillator / Accelerator System](#bk-06--awesome_oscillator_accelerator_system) | 神奇震荡指标系统 · Система по AO/AC | 📖 Logic-only |
| **BK-07** | [Aroon Breakout](#bk-07--aroon_breakout) | 阿隆指标突破 · Система по Aroon | 📖 Logic-only |
| **BK-08** | [Range Breakout with Volume Surge (放量突破)](#bk-08--range_breakout_with_volume_surge) | 放量突破平台 · Пробой флэта с объёмом | 📖 Logic-only |
| **BK-09** | [Consolidation Box Breakout](#bk-09--consolidation_box_breakout) | 平台整理突破 · Пробой боковика | 📖 Logic-only |
| **BK-10** | [Gap Playbook (Fade / Continue)](#bk-10--gap_playbook_fade_continue) | 跳空缺口策略 · Стратегии гэпов | 📖 Logic-only |
| **BK-11** | [Squeeze Pro / Multi-Threshold Squeeze](#bk-11--squeeze_pro_multi_threshold_squeeze) | 多档挤压指标 · Squeeze Pro | 📖 Logic-only |
| **BK-12** | [High-of-Day Break & Retest](#bk-12--high_of_day_break_retest) | 日内新高突破回踩 · Пробой максимума дня с ретестом | 📖 Logic-only |
| **BK-13** | [Volatility Expansion Breakout (Keltner/ATR form)](#bk-13--volatility_expansion_breakout_keltneratr_form) | 波动扩张突破 · Пробой расширения волатильности | 📖 Logic-only |

---

### BK-01 · Opening Range Breakout (ORB)
*开盘区间突破 · Пробой диапазона открытия*

- **Origin & Lineage:** Toby Crabel, Day Trading with Short Term Price Patterns and Opening Range Breakout (1990).
- **Core Hypothesis:** Define the high/low of the first 5-30 minutes and trade stops outside that range; the opening range encodes overnight information being repriced by the day's first liquidity wave. Crabel's statistical work on gap behavior underlies dozens of modern ORB variants, including the 2020s 'ORB-5' revival in US equities. Failure handling (re-entry, midpoint stops) matters more than the entry itself.
- **Execution Rules:** After the range closes, long on close above OR-high (stop on OR-low), short mirrored; flatten by session end.
- **Key Parameters:** Range 5/15/30 minutes; stop at opposite edge or midpoint; skip inside days by volume filter.
- **Duplicates Eliminated:** CN 开盘区间突破 (股票/股指); RU «Пробой открытия» intraday robots; ICT opening-range variants (cross PA-09).

**Pine Script Reference Implementation:** [`bk-01_opening_range_breakout_orb.pine`](bk-01_opening_range_breakout_orb.pine)

```pinescript
//@version=5
strategy("Opening Range Breakout (ORB)", overlay=true)
sess  = input.session("0930-0945", "Opening range session")
tz    = input.string("America/New_York", "Timezone")
inOR  = not na(time(timeframe.period, sess, tz))
var float orHi = na
var float orLo = na
newDay = ta.change(time("D")) != 0
if newDay
orHi := na
orLo := na
if inOR
orHi := na(orHi) ? high : math.max(orHi, high)
orLo := na(orLo) ? low  : math.min(orLo, low)
if not inOR and not na(orHi) and strategy.position_size == 0
if close > orHi
strategy.entry("L", strategy.long)
if close < orLo
strategy.entry("S", strategy.short)
if strategy.position_size > 0
strategy.exit("LX", from_entry="L", stop=orLo)
if strategy.position_size < 0
strategy.exit("SX", from_entry="S", stop=orHi)
if newDay
strategy.close_all(comment="Session reset")
plot(inOR ? orHi : na, "OR High", color=color.teal, style=plot.style_linebr)
plot(inOR ? orLo : na, "OR Low", color=color.red, style=plot.style_linebr)
```

---

### BK-02 · Narrow Range 7 / Inside Day Patterns
*窄幅整理形态 · Внутренний день / узкий диапазон*

- **Origin & Lineage:** Toby Crabel (1990), building on 1970s floor-trader NR7 lore.
- **Core Hypothesis:** A day whose range is the narrowest of the last 7 (NR7), or an inside day fully engulfed by the prior bar, marks volatility contraction that statistically precedes expansion; trade the break of the contraction bar in either direction. Crabel's book remains the quantitative foundation of all 'compression day' trading. Modern VCP (BK-03) is the multi-stage generalization.
- **Execution Rules:** Next day, buy a stop above the NR7/inside-day high, sell a stop below its low; cancel the unfilled side after the first fill.
- **Key Parameters:** NR7 (or NR4); ORB-style stops; ATR-scaled targets.
- **Duplicates Eliminated:** CN 窄幅整理突破; RU 'узкий диапазон' scripts; ID/NR4 variants.

---

### BK-03 · Volatility Contraction Pattern (VCP)
*波动收缩形态 · Модель сжатия волатильности*

- **Origin & Lineage:** Mark Minervini (2010s workshops/books); crowdsourced into Pine scanners.
- **Core Hypothesis:** Successive pullbacks within a base each get shallower (volume dries up in parallel) until a breakout with restored volume; the geometry is a volume-price handshake that supply is exhausted. The Pine form is a scan: decreasing range-depth stages plus a 10/50-bar volume dry-up, then a breakout trigger. It is the swing-trading descendant of Crabel's NR logic and O'Neil's base counts.
- **Execution Rules:** Detect 2-4 stages of contraction (depth_n < depth_n-1); arm on volume dry-up; enter on close above contraction high with volume > 1.5x 50-bar average.
- **Key Parameters:** Base 50-65 bars; 3 stages typical; volume surge 1.5-2x.
- **Duplicates Eliminated:** Minervini scan packs; Qullamägi EP/gap momentum (cousin); CN 强势股缩量整理突破.

**Pine Script Reference Implementation:** [`bk-03_volatility_contraction_pattern_vcp.pine`](bk-03_volatility_contraction_pattern_vcp.pine)

```pinescript
//@version=5
indicator("VCP Contraction Scan", overlay=true)
lookback = input.int(60, "Base lookback")
stages   = input.int(3, "Contraction stages")
seg = int(lookback / stages)
depth(k) => (ta.highest(high, k) - ta.lowest(low, k)) / ta.lowest(low, k) * 100
d1 = depth(seg)
d2 = depth(seg * 2)
d3 = depth(seg * 3)
contracting = d1 < d2 and d2 < d3
dryUp = ta.sma(volume, 10) < 0.6 * ta.sma(volume, 50)
breakout = close > ta.highest(high, seg)[1] and volume > 1.5 * ta.sma(volume, 50)
plotshape(contracting and dryUp, "Contraction + dry-up", shape.circle,
location.belowbar, color=color.orange, size=size.tiny)
plotshape(breakout and contracting[1], "Breakout", shape.triangleup,
location.belowbar, color=color.teal, size=size.small)
```

---

### BK-04 · Darvas Box
*达瓦斯箱体 · Ящик Дарваса*

- **Origin & Lineage:** Nicolas Darvas, 1959 Barron's articles; How I Made $2,000,000 in the Stock Market (1960).
- **Core Hypothesis:** After three consecutive higher highs form a 'box top' and a failing pullback forms the box bottom, buy the breakout of the top and trail the stop under the most recent box bottom; each new consolidation draws a new box. It is trend following on a dancer's travel schedule — Darvas famously ran it by telegram from nightclubs. Mechanically it is a swing-anchored Donchian with human box-drawing rules.
- **Execution Rules:** Box from 3-day top / bottom definition; enter on close above box top; stop under box bottom; pyramid into new boxes.
- **Key Parameters:** 3-day box (classic); volume confirmation optional; stop = last box bottom.
- **Duplicates Eliminated:** CN 箱体突破; RU «Метод Дарваса»; box-drawing scripts across all platforms.

---

### BK-05 · Bill Williams Alligator + Fractals
*比尔·威廉姆斯鳄鱼线+分形 · Аллигатор и фракталы Вильямса*

- **Origin & Lineage:** Bill Williams, Trading Chaos (1995) and New Trading Dimensions (1998).
- **Core Hypothesis:** Three smoothed MAs (13/8/5 of the median price, displaced forward) form the Alligator: when the lines fan out in order the 'alligator is eating' and fractal breakouts may be traded in that direction; when they interweave, sleep and stand aside. Up/down fractals (5-bar extremes) supply entry triggers. No system better symbolizes the 1990s-2000s retail era — and none has a larger Russian following.
- **Execution Rules:** Long when the Alligator is aligned up and close breaks the most recent up-fractal; short mirrored; exit on Alligator interweave or opposite fractal.
- **Key Parameters:** SMMA 13/8/5 with 8/5/3 forward displacement; fractal 5-bar pivots.
- **Duplicates Eliminated:** RU «Аллигатор Вильямса» robots (enormous MQL4/5 corpus); CN 鳄鱼线战法; Awesome/AC oscillator combos (BK-06).

**Pine Script Reference Implementation:** [`bk-05_bill_williams_alligator_fractals.pine`](bk-05_bill_williams_alligator_fractals.pine)

```pinescript
//@version=5
strategy("Alligator + Fractal Breakout", overlay=true)
jaw   = ta.rma(hl2, 13)
teeth = ta.rma(hl2, 8)
lip   = ta.rma(hl2, 5)
alignedUp = lip > teeth and teeth > jaw
alignedDn = lip < teeth and teeth < jaw
upFr = ta.pivothigh(high, 2, 2)
dnFr = ta.pivotlow(low, 2, 2)
var float lastUpFr = na
var float lastDnFr = na
if not na(upFr)
lastUpFr := upFr
if not na(dnFr)
lastDnFr := dnFr
if alignedUp and not na(lastUpFr) and close > lastUpFr and strategy.position_size <= 0
strategy.entry("L", strategy.long)
if alignedDn and not na(lastDnFr) and close < lastDnFr and strategy.position_size >= 0
strategy.entry("S", strategy.short)
plot(jaw, "Jaw", color=color.blue, offset=8)
plot(teeth, "Teeth", color=color.red, offset=5)
plot(lip, "Lip", color=color.green, offset=3)
```

---

### BK-06 · Awesome Oscillator / Accelerator System
*神奇震荡指标系统 · Система по AO/AC*

- **Origin & Lineage:** Bill Williams, New Trading Dimensions (1998).
- **Core Hypothesis:** The Awesome Oscillator (SMA(34) - SMA(5) of median price) signals via 'saucer' patterns, twin peaks, and zero-line crosses; the Accelerator adds momentum-of-momentum. Used with the Alligator it filters entries to trend direction. Mechanically it is a slow-fast MA spread oscillator — a MACD cousin — which is why standalone AO systems mostly duplicate MACD logic under new vocabulary.
- **Execution Rules:** Long on AO saucer-above-zero or zero-line cross up, in Alligator-up regime; short mirrored.
- **Key Parameters:** AO 34/5; AC 5; Alligator filter optional.
- **Duplicates Eliminated:** RU «Система Билла Вильямса» full-suite robots; CN AO/AC战法; MACD-equivalent logic (cross TR-05).

---

### BK-07 · Aroon Breakout
*阿隆指标突破 · Система по Aroon*

- **Origin & Lineage:** Tushar Chande, 1995 (TASC September 1995).
- **Core Hypothesis:** Aroon Up/Down measure bars since the recent 25-bar high/low; crossovers near the top of their range flag fresh trend leadership. As a breakout proxy it is slower than Donchian but immune to close-versus-intrabar ambiguity. It sees periodic revivals in scan-oriented communities but rarely stands alone in production.
- **Execution Rules:** Long when Aroon-Up crosses above Aroon-Down above 70; exit on reverse cross or drop below 50.
- **Key Parameters:** Period 25 (14 in fast variants).
- **Duplicates Eliminated:** Aroon cross robots on MQL5; CN 阿隆指标 templates.

---

### BK-08 · Range Breakout with Volume Surge (放量突破)
*放量突破平台 · Пробой флэта с объёмом*

- **Origin & Lineage:** Universal TA; formalized in CN platform templates (通达信/同花顺 放量突破 formulas) and JoinQuant volume-confirm strategies.
- **Core Hypothesis:** Breakouts validated by abnormal volume fail less: the entry demands both a new N-bar high and volume above k times its moving average, tying the break to real participation. Chinese retail materials treat this as the canonical platform-breakout (平台突破) filter, and it is the volume layer that most western breakout systems add informally.
- **Execution Rules:** Long on close above N-bar high with volume > k x SMA(volume,20); stop under the range low; trail after 1R.
- **Key Parameters:** N 20-60; k 1.5-2.5; range depth filter optional.
- **Duplicates Eliminated:** BK-09 consolidation breakout; RU «пробой с объёмом»; OBV/CMF breakout hybrids.

---

### BK-09 · Consolidation Box Breakout
*平台整理突破 · Пробой боковика*

- **Origin & Lineage:** Classic swing methodology; CN platform-era formalization (平台突破战法).
- **Core Hypothesis:** Identify a sideways box of at least N bars with contracting range, then trade the close outside the box with volume confirmation. Unlike Darvas (BK-04) it does not require the prior uptrend geometry, so it is the generic form used on any instrument. The statistical justification is identical to NR7: compression precedes expansion.
- **Execution Rules:** Box = highest/lowest over N bars with range < x% of price; long on close above box high + volume filter; stop at box midpoint.
- **Key Parameters:** N 15-40; max box height 5-10%; volume 1.5x.
- **Duplicates Eliminated:** CN 平台突破/整理突破; RU «пробой консолидации»; Darvas and NR7 (same mechanism).

---

### BK-10 · Gap Playbook (Fade / Continue)
*跳空缺口策略 · Стратегии гэпов*

- **Origin & Lineage:** Crabel's gap statistics (1990); institutionalized in US equities; MOEX dividend-gap practice (RU-07) is a special case.
- **Core Hypothesis:** Classify opening gaps by size against ATR and by cause: small technical gaps in trend direction tend to continue, while large exhaustion gaps into resistance tend to fill. The systematic form trades the first 15-30 minutes' failure or confirmation of the gap. Full-measure and runaway gaps are excluded from fading.
- **Execution Rules:** Fade: short gap-ups > 0.5 ATR into resistance after a weak first hour; continue: enter with the gap when the open drives further within 15 minutes.
- **Key Parameters:** Gap size 0.25-1.0 ATR buckets; confirmation window 15-30 min; stop beyond gap extreme.
- **Duplicates Eliminated:** CN 缺口回补策略; RU гэп-роботы; ORB gap variants (cross BK-01).

---

### BK-11 · Squeeze Pro / Multi-Threshold Squeeze
*多档挤压指标 · Squeeze Pro*

- **Origin & Lineage:** LuxAlgo (2020-2023 open library), extending TTM Squeeze (MR-05).
- **Core Hypothesis:** Grades compression into low/mid/high squeeze levels by comparing Bollinger-to-Keltner distance against historical thresholds, giving a severity ladder rather than a binary flag. Traders arm alerts at high squeeze and trade the release. Functionally it is TTM Squeeze with a calibrated intensity scale — kept as a distinct entry because its release logic differs.
- **Execution Rules:** Alert on high-squeeze; enter on squeeze release in the direction of the momentum histogram; scale position by squeeze grade.
- **Key Parameters:** BB/KC as TTM; percentile thresholds 0.5/1.0/1.5 sigma of band separation.
- **Duplicates Eliminated:** TTM Squeeze (MR-05) as the parent; LazyBear Hi-Lo squeezes; CN 多档收口实验性 scripts.

---

### BK-12 · High-of-Day Break & Retest
*日内新高突破回踩 · Пробой максимума дня с ретестом*

- **Origin & Lineage:** Intraday momentum practice (2000s prop desks); formalized in community scripts.
- **Core Hypothesis:** When price takes out the morning's high after consolidation, enter on the retest of that broken level rather than the break itself, cutting the false-break rate at the cost of missing runners. The retest requirement is the key differentiator from raw ORB-style momentum. Often combined with VWAP-relative position filters.
- **Execution Rules:** Long on pullback touching the broken HOD with a bullish reversal bar; stop under retest low; target 1.5-2R or EOD.
- **Key Parameters:** HOD window from open; retest tolerance 0.1-0.2 ATR; VWAP filter.
- **Duplicates Eliminated:** CN 日内新高策略; RU intraday HOD scripts; IB opening-drive variants.

---

### BK-13 · Volatility Expansion Breakout (Keltner/ATR form)
*波动扩张突破 · Пробой расширения волатильности*

- **Origin & Lineage:** Chester Keltner's envelope re-cast as a breakout by Linda Raschke and vn.py's KingKeltner template.
- **Core Hypothesis:** Instead of fading the Keltner envelope (MR-04), trade stops outside it: close beyond EMA(20) + 2 x ATR(10) signals expansion worth following. This is the CTA workhorse form — the vn.py KingKeltnerStrategy is exactly this on Chinese futures. It pairs naturally with ADX gates to avoid trendless expansion noise.
- **Execution Rules:** Long on close above upper band; exit on close back inside the channel or a trailing 3 x ATR stop; short mirrored.
- **Key Parameters:** EMA 20, ATR 10, multiple 2-2.5; optional ADX > 20 gate.
- **Duplicates Eliminated:** vn.py KingKeltnerStrategy; CN 肯特纳突破 CTA templates; RU канальные пробойные роботы.

---
