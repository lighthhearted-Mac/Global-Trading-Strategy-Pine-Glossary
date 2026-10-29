# Family TR: Trend Following & Momentum

**Total Strategies in Family:** 18  
**Pine Script v5 Implementations:** 12  

## Strategies Overview

| ID | Strategy Name | Alternative Names | Has Pine Code |
|---|---|---|:---:|
| **TR-01** | [Donchian Channel Breakout](#tr-01--donchian_channel_breakout) | 唐奇安通道突破 · Прорыв канала Дончиана | ✅ Pine v5 |
| **TR-02** | [Turtle Trading System (S1/S2)](#tr-02--turtle_trading_system_s1s2) | 海龟交易法则 · Система «Черепах» | ✅ Pine v5 |
| **TR-03** | [Dual Moving Average Crossover (Golden Cross)](#tr-03--dual_moving_average_crossover_golden_cross) | 双均线金叉死叉 · Пересечение скользящих средних | ✅ Pine v5 |
| **TR-04** | [Granville Eight Rules of Moving Averages](#tr-04--granville_eight_rules_of_moving_averages) | 格兰维尔八大法则 · Восемь правил Гранвиля | 📖 Logic-only |
| **TR-05** | [MACD Trend and Histogram System](#tr-05--macd_trend_and_histogram_system) | MACD趋势+柱状图系统 · Система по MACD | ✅ Pine v5 |
| **TR-06** | [Parabolic SAR Flip System](#tr-06--parabolic_sar_flip_system) | 抛物线SAR系统 · Система по Параболику SAR | ✅ Pine v5 |
| **TR-07** | [ADX/DMI Trend Filter System](#tr-07--adxdmi_trend_filter_system) | ADX/DMI趋势过滤系统 · Система на ADX/DMI | 📖 Logic-only |
| **TR-08** | [SuperTrend](#tr-08--supertrend) | 超级趋势 · Супертренд | ✅ Pine v5 |
| **TR-09** | [UT Bot Alerts (ATR Trailing Stop on Close)](#tr-09--ut_bot_alerts_atr_trailing_stop_on_close) | UT Bot · ATR трейлинг-стоп | ✅ Pine v5 |
| **TR-10** | [Chandelier Exit](#tr-10--chandelier_exit) | 吊灯止损 · Chandelier-выход | ✅ Pine v5 |
| **TR-11** | [Ichimoku Kinko Hyo](#tr-11--ichimoku_kinko_hyo) | 一目均衡表 · 一目均衡表 (Ишимоку) | ✅ Pine v5 |
| **TR-12** | [Kaufman Adaptive Moving Average (KAMA)](#tr-12--kaufman_adaptive_moving_average_kama) | 卡玛自适应均线 · Адаптивная средняя Кауфмана | ✅ Pine v5 |
| **TR-13** | [VIDYA (Variable Index Dynamic Average)](#tr-13--vidya_variable_index_dynamic_average) | VIDYA可变动指数平均 · VIDYA | 📖 Logic-only |
| **TR-14** | [FRAMA (Fractal Adaptive Moving Average)](#tr-14--frama_fractal_adaptive_moving_average) | 分形自适应均线 · FRAMA | 📖 Logic-only |
| **TR-15** | [Guppy Multiple Moving Averages (GMMA)](#tr-15--guppy_multiple_moving_averages_gmma) | 顾比复合移动平均线 · GMMA Ганна Гаппи | ✅ Pine v5 |
| **TR-16** | [Heikin-Ashi Trend Flip](#tr-16--heikin_ashi_trend_flip) | 平均K线趋势翻转 · Торговля по Хейкин-Аши | ✅ Pine v5 |
| **TR-17** | [Time-Series Momentum (TSMOM)](#tr-17--time_series_momentum_tsmom) | 时间序列动量 · Моментум по времени | 📖 Logic-only |
| **TR-18** | [CANSLIM Momentum / Leading-Stock Playbook](#tr-18--canslim_momentum_leading_stock_playbook) | 欧奈尔CANSLIM选股法 · CANSLIM | 📖 Logic-only |

---

### TR-01 · Donchian Channel Breakout
*唐奇安通道突破 · Прорыв канала Дончиана*

- **Origin & Lineage:** Richard Donchian, US commodity research columns, late 1940s-1960s; popularized as the 4-week rule.
- **Core Hypothesis:** Buy when price closes above the highest high of the prior N bars and sell when it closes below the lowest low, letting the channel itself define trend participation. The channel doubles as the trailing exit on a shorter counter-channel. It is the direct ancestor of the Turtle system and of most later channel-breakout robots.
- **Execution Rules:** Enter long on close above the 20-bar (prior, offset by 1) high; exit on close below the 10-bar low; short mirrored.
- **Key Parameters:** Entry channel 20 (55 for slow systems); exit channel 10 (20); works best on continuous futures and trending FX pairs.
- **Duplicates Eliminated:** Turtle S1/S2; CN 海龟策略 templates (JoinQuant, myquant.cn); RU «Пробой канала» robots; vn.py TurtleSignalStrategy.

**Pine Script Reference Implementation:** [`tr-01_donchian_channel_breakout.pine`](tr-01_donchian_channel_breakout.pine)

```pinescript
//@version=5
strategy("Donchian 20-10 Breakout", overlay=true,
default_qty_type=strategy.percent_of_equity, default_qty_value=100)
nIn  = input.int(20, "Entry channel")
nOut = input.int(10, "Exit channel")
hi   = ta.highest(high, nIn)[1]
lo   = ta.lowest(low, nIn)[1]
xHi  = ta.highest(high, nOut)[1]
xLo  = ta.lowest(low, nOut)[1]
if strategy.position_size == 0 and close > hi
strategy.entry("L", strategy.long)
if strategy.position_size > 0 and close < xLo
strategy.close("L", comment="Exit channel")
if strategy.position_size == 0 and close < lo
strategy.entry("S", strategy.short)
if strategy.position_size < 0 and close > xHi
strategy.close("S", comment="Exit channel")
plot(hi, "Entry High", color=color.teal)
plot(lo, "Entry Low", color=color.red)
```

---

### TR-02 · Turtle Trading System (S1/S2)
*海龟交易法则 · Система «Черепах»*

- **Origin & Lineage:** Richard Dennis & William Eckhardt experiment, 1983-1988; full rules leaked online in 2003 and archived widely (Way of the Turtle, 2007).
- **Core Hypothesis:** A complete trend-following stack: Donchian entries (System 1 at 20 days, System 2 at 55 days), volatility-normalized unit sizing via ATR ('N'), 0.5N pyramiding up to 4 units, a 2N stop per unit, and channel exits. Its lasting contribution is sizing by volatility rather than conviction. Most later trend robots are Turtles with renamed parameters.
- **Execution Rules:** Unit = 1% of equity / ATR(20). Add a unit each +0.5N; stop the whole position at 2N from last fill; exit longs on a 10-day (S1) or 20-day (S2) low.
- **Key Parameters:** N period 20; unit risk 1%; max 4 units; exits 10/20 days.
- **Duplicates Eliminated:** 海龟交易法则 implementations on JoinQuant/BigQuant/vn.py (TurtleSignalStrategy); RU «Система Черепах» on Si/RTS futures; original Turtle Rules PDF archive.

**Pine Script Reference Implementation:** [`tr-02_turtle_trading_system_s1s2.pine`](tr-02_turtle_trading_system_s1s2.pine)

```pinescript
//@version=5
strategy("Turtle S2 Condensed (55/20, 2N stop)", overlay=true, pyramiding=4)
nLen    = input.int(20, "N length (ATR)")
riskPct = input.float(1.0, "Equity risk per unit, %", step=0.25)
N       = ta.atr(nLen)
entryHi = ta.highest(high, 55)[1]
exitLo  = ta.lowest(low, 20)[1]
var float lastFill = na
longSig = strategy.position_size == 0 and close > entryHi
addSig  = strategy.position_size > 0 and not na(lastFill) and close > lastFill + 0.5 * N and strategy.opentrades < 4
if longSig or addSig
strategy.entry("U" + str.tostring(strategy.opentrades + 1), strategy.long,
qty=(strategy.equity * riskPct / 100) / N)
lastFill := close
if strategy.position_size > 0 and ((not na(lastFill) and close < lastFill - 2 * N) or close < exitLo)
strategy.close_all(comment="2N stop or 20-day low")
lastFill := na
```

---

### TR-03 · Dual Moving Average Crossover (Golden Cross)
*双均线金叉死叉 · Пересечение скользящих средних*

- **Origin & Lineage:** Attributed to Granville-era US practice; every retail platform ships it as the default example strategy.
- **Core Hypothesis:** Go long when a faster MA crosses above a slower MA and exit (or reverse) on the opposite cross. It is the 'Hello World' of quant trading — literally the default demo on JoinQuant — and remains a useful baseline to benchmark any trend model against. Its chronic weakness is whipsaw when the two averages are close in length.
- **Execution Rules:** Long on EMA(50) crossing above EMA(200) (or 5/20 on Chinese platforms); reverse or stop on the cross under; optional ATR trailing stop instead of reversal.
- **Key Parameters:** Common pairs: 50/200 swing, 5/20 or 5/10 intraday; ATR stop 3x14.
- **Duplicates Eliminated:** CN 双均线策略 (JoinQuant/myquant default demo, DoubleMaStrategy in vn.py); RU «Пересечение SMA 50/200»; MQL5 CodeBase MA-cross EAs.

**Pine Script Reference Implementation:** [`tr-03_dual_moving_average_crossover_golden_cross.pine`](tr-03_dual_moving_average_crossover_golden_cross.pine)

```pinescript
//@version=5
strategy("Dual MA Cross + ATR Stop", overlay=true)
fastLen = input.int(50, "Fast MA")
slowLen = input.int(200, "Slow MA")
atrMult = input.float(3.0, "Stop ATR multiple")
fast = ta.ema(close, fastLen)
slow = ta.ema(close, slowLen)
if ta.crossover(fast, slow)
strategy.entry("L", strategy.long)
if ta.crossunder(fast, slow)
strategy.entry("S", strategy.short)
if strategy.position_size > 0
strategy.exit("LX", from_entry="L", stop=close - atrMult * ta.atr(14))
if strategy.position_size < 0
strategy.exit("SX", from_entry="S", stop=close + atrMult * ta.atr(14))
plot(fast, "Fast EMA", color=color.teal)
plot(slow, "Slow EMA", color=color.orange)
```

---

### TR-04 · Granville Eight Rules of Moving Averages
*格兰维尔八大法则 · Восемь правил Гранвиля*

- **Origin & Lineage:** Joseph Granville, 1960s US newsletters; formalized into scored strategies on JoinQuant (双均线-格兰维 strategy).
- **Core Hypothesis:** Rather than a single cross signal, Granville codified eight MA relationships: four buys (cross up, pullback to rising MA, break-then-reclaim, divergence away from a falling MA) and four sells (mirror). Chinese community strategies score all eight conditions into a 0-100 ranking and trade the highest-scoring names. It is an early example of signal confluence scoring now common in factor models.
- **Execution Rules:** Score MA alignment, price-vs-MA breakout, volume confirmation; buy top-ranked names when score exceeds threshold; sell on bearish rule triggers, fixed take-profit, or trailing stop from peak.
- **Key Parameters:** Typical CN implementation: MA 5/10/20/60; volume ratio filter; 20% take-profit; 10% trailing stop.
- **Duplicates Eliminated:** JoinQuant 双均线-格兰维交易 strategy; CN 移动平均线战法 variants; RU «Правила Гранвиля» tutorials (no separate robot).

---

### TR-05 · MACD Trend and Histogram System
*MACD趋势+柱状图系统 · Система по MACD*

- **Origin & Lineage:** Gerald Appel, 1970s (MACD); histogram by Thomas Aspray, 1986.
- **Core Hypothesis:** Trade the MACD line versus its signal line, filtered by the zero line so signals are only taken in the direction of the underlying momentum regime. The histogram's slope adds early warning of momentum loss before the actual cross. It remains one of the most-ported indicators on TradingView, MQL5, and Chinese platforms.
- **Execution Rules:** Long on MACD(12,26,9) crossing above signal while above zero; short mirrored; exit on opposite cross or histogram divergence.
- **Key Parameters:** 12/26/9 standard; CN variants add 背离 (divergence) detection on the histogram.
- **Duplicates Eliminated:** MACD+EMA combos in MQL5 CodeBase; CN MACD背离战法; vn.py MACD demo strategies.

**Pine Script Reference Implementation:** [`tr-05_macd_trend_and_histogram_system.pine`](tr-05_macd_trend_and_histogram_system.pine)

```pinescript
//@version=5
strategy("MACD Zero-Line Trend System", overlay=false)
[macdLine, sigLine, hist] = ta.macd(close, 12, 26, 9)
if ta.crossover(macdLine, sigLine) and macdLine > 0
strategy.entry("L", strategy.long)
if ta.crossunder(macdLine, sigLine) and macdLine < 0
strategy.entry("S", strategy.short)
plot(macdLine, "MACD", color=color.teal)
plot(sigLine, "Signal", color=color.orange)
plot(hist, "Histogram", style=plot.style_columns,
color=hist >= 0 ? color.new(color.teal, 40) : color.new(color.red, 40))
hline(0)
```

---

### TR-06 · Parabolic SAR Flip System
*抛物线SAR系统 · Система по Параболику SAR*

- **Origin & Lineage:** J. Welles Wilder, New Concepts in Technical Trading Systems, 1978.
- **Core Hypothesis:** A perpetual-in-the-market stop-and-reverse system: dots trail price with an accelerating factor, and every stop hit flips the position. Wilder designed it for commodity trends; modern usage adds a filter (e.g., only long above a 200 EMA) because SAR bleeds badly in ranges. It survives everywhere as a trailing-stop visual.
- **Execution Rules:** Long while close is above SAR, flip short when close crosses below; acceleration 0.02 per new extreme, capped at 0.2.
- **Key Parameters:** AF start 0.02 / increment 0.02 / max 0.2.
- **Duplicates Eliminated:** PSAR+EMA200+MACD signal packs (multiple GitHub repos); CN SAR跟踪策略; RU «Параболик» robots.

**Pine Script Reference Implementation:** [`tr-06_parabolic_sar_flip_system.pine`](tr-06_parabolic_sar_flip_system.pine)

```pinescript
//@version=5
strategy("Parabolic SAR Flip", overlay=true)
start = input.float(0.02, "Start")
inc   = input.float(0.02, "Increment")
maxv  = input.float(0.2, "Max")
sar = ta.sar(start, inc, maxv)
if close > sar and strategy.position_size <= 0
strategy.entry("L", strategy.long)
if close < sar and strategy.position_size >= 0
strategy.entry("S", strategy.short)
plot(sar, "SAR", style=plot.style_circles,
color=strategy.position_size >= 0 ? color.teal : color.red)
```

---

### TR-07 · ADX/DMI Trend Filter System
*ADX/DMI趋势过滤系统 · Система на ADX/DMI*

- **Origin & Lineage:** J. Welles Wilder, 1978; refined by numerous TASC articles.
- **Core Hypothesis:** Use +DI/-DI crossovers for direction and ADX as a regime gate: only take DI signals while ADX is rising above ~20-25, which separates trending from chopping conditions. As a standalone it underperforms its filters' reputation, but as an overlay it is attached to half of the breakout systems in this glossary. Chinese CTA templates and Smart-Lab robots both use it almost identically.
- **Execution Rules:** Long when +DI crosses above -DI with ADX > 20 and rising; exit on reverse cross or ADX rolling over from a high.
- **Key Parameters:** DMI 14; ADX threshold 20-25; optional exit at ADX peak.
- **Duplicates Eliminated:** ADX gates inside CN CTA templates (文华/TB); RU «ADX-фильтр» modules; generic MT4 ADX EAs.

---

### TR-08 · SuperTrend
*超级趋势 · Супертренд*

- **Origin & Lineage:** Olivier Seban (France), circa 2009; hundreds of open Pine ports.
- **Core Hypothesis:** An ATR band flipped around price: the level trails beneath uptrends and above downtrends by factor x ATR, and crossing it flips the position. It is conceptually Wilder's vol-stop with a cleaner flip mechanic, which is why it replaced SAR in most modern retail systems. Its exposure is near-binary, so it is usually paired with a higher-timeframe filter.
- **Execution Rules:** Long while price is above the SuperTrend line (direction -1), short while below; flips on close through the line.
- **Key Parameters:** Factor 3, ATR 10 (classic); factor 2-4, ATR 7-14 in the wild.
- **Duplicates Eliminated:** CN 超级趋势 (JoinQuant/文华); RU «Супертренд» TradingView scripts; countless 'ST + filter' hybrids on MQL5.

**Pine Script Reference Implementation:** [`tr-08_supertrend.pine`](tr-08_supertrend.pine)

```pinescript
//@version=5
strategy("SuperTrend Flip", overlay=true)
factor = input.float(3.0, "Factor")
atrLen = input.int(10, "ATR Length")
[st, dir] = ta.supertrend(factor, atrLen)
if dir < 0
strategy.entry("L", strategy.long)
if dir > 0
strategy.entry("S", strategy.short)
plot(dir < 0 ? st : na, "ST Up", color=color.teal, style=plot.style_linebr)
plot(dir > 0 ? st : na, "ST Down", color=color.red, style=plot.style_linebr)
```

---

### TR-09 · UT Bot Alerts (ATR Trailing Stop on Close)
*UT Bot · ATR трейлинг-стоп*

- **Origin & Lineage:** Yo_adriiiiaan on TradingView (2020), popularized by QuantNomad videos; ATR trailing-stop lineage from 2010s forex forums.
- **Core Hypothesis:** A recursive ATR trailing stop computed on closes: the stop only ratchets in the trend direction and flips when close crosses it, producing sparse buy/sell alerts. Its popularity comes from clean visualization and alert-driven automation rather than novelty — it is mathematically inside the SuperTrend/Chandelier family. Widely cloned with EMA, HTF, or session filters bolted on.
- **Execution Rules:** Trail = close -/+ key x ATR(period), ratcheting only; long when close crosses above the down-trail, exit/short on cross under the up-trail.
- **Key Parameters:** Key (sensitivity) 2 (1-3 typical); ATR period 10 (or 1 in aggressive clones).
- **Duplicates Eliminated:** Original 'ATR Trailing Stops' scripts (R	thomson bands, 2018); RU 'Универсальный трейлинг' packs; UT Bot + EMA 200 variants (QuantNomad).

**Pine Script Reference Implementation:** [`tr-09_ut_bot_alerts_atr_trailing_stop_on_close.pine`](tr-09_ut_bot_alerts_atr_trailing_stop_on_close.pine)

```pinescript
//@version=5
strategy("UT Bot-Style ATR Trailing Stop", overlay=true)
keyA   = input.float(2.0, "Sensitivity")
atrLen = input.int(10, "ATR Length")
nLoss  = keyA * ta.atr(atrLen)
var float up = na
var float dn = na
up := close > nz(up[1], close) and close[1] > nz(up[1], close) ?
math.max(nz(up[1]), close - nLoss) : close - nLoss
dn := close < nz(dn[1], close) and close[1] < nz(dn[1], close) ?
math.min(nz(dn[1]), close + nLoss) : close + nLoss
if ta.crossover(close, dn)
strategy.entry("L", strategy.long)
if ta.crossunder(close, up)
strategy.entry("S", strategy.short)
plot(ta.crossover(close, dn) ? dn : na, "Buy", style=plot.style_circles, color=color.teal, linewidth=3)
plot(ta.crossunder(close, up) ? up : na, "Sell", style=plot.style_circles, color=color.red, linewidth=3)
```

---

### TR-10 · Chandelier Exit
*吊灯止损 · Chandelier-выход*

- **Origin & Lineage:** Chuck LeBeau, 1990s (Systems & Exchanges seminars; popularized via TASC).
- **Core Hypothesis:** Trail a stop at the highest high since entry minus a multiple of ATR, hanging from the 'chandelier' rather than from entry price. As a standalone system it rides trends with a volatility-scaled ratchet and re-enters when the trend state flips. It is the professional-grade ancestor of most modern trailing-stop scripts including UT Bot and SuperTrend variants.
- **Execution Rules:** Long stop = highest high(22) - 3 x ATR(22); flip trend when the stop is breached; short mirrored.
- **Key Parameters:** Lookback 22; multiple 3.0 (2.5-4.0).
- **Duplicates Eliminated:** ATR Trailing Stops (Wilders-based); 'QQE trailing' variants; CN 吊灯止损 modules in CTA templates.

**Pine Script Reference Implementation:** [`tr-10_chandelier_exit.pine`](tr-10_chandelier_exit.pine)

```pinescript
//@version=5
strategy("Chandelier Exit Trend Rider", overlay=true)
nLen = input.int(22, "Lookback")
mult = input.float(3.0, "ATR Multiple")
longStop  = ta.highest(high, nLen) - mult * ta.atr(nLen)
shortStop = ta.lowest(low, nLen) + mult * ta.atr(nLen)
var float trail = na
var int   trend = 1
trend := close > nz(trail[1], shortStop) ? 1 :
close < nz(trail[1], longStop) ? -1 : nz(trend[1], 1)
trail := trend == 1 ? math.max(longStop, nz(trail[1], longStop)) :
math.min(shortStop, nz(trail[1], shortStop))
if trend == 1 and nz(trend[1]) == -1
strategy.entry("L", strategy.long)
if trend == -1 and nz(trend[1]) == 1
strategy.entry("S", strategy.short)
plot(trend == 1 ? trail : na, "Long trail", color=color.teal, style=plot.style_linebr)
plot(trend == -1 ? trail : na, "Short trail", color=color.red, style=plot.style_linebr)
```

---

### TR-11 · Ichimoku Kinko Hyo
*一目均衡表 · 一目均衡表 (Ишимоку)*

- **Origin & Lineage:** Goichi Hosoda, Japan, developed 1930s-1960s, published 1969.
- **Core Hypothesis:** A five-part system — conversion and base lines (Donchian-style midpoints), a leading span computed from them, a 52-period span, and a displaced cloud — that encodes trend, momentum, support/resistance, and forward projection in one overlay. Trading rules combine cloud position, Kijun as the trend referee, and TK crosses. It has dedicated practitioner schools in Japan, China (一目均衡表 communities), and Russia, where 'Ишимоку' became a retail cult in the 2000s.
- **Execution Rules:** Long when price is above the cloud, Tenkan > Kijun, and Chikou is clear of price; Kijun bounces or TK crosses with cloud alignment trigger entries; exit on TK cross against or Kijun break.
- **Key Parameters:** 9/26/52 with 26-bar displacement (some modern markets use 20/60/120).
- **Duplicates Eliminated:** CN 一目均衡表 strategy packs; RU Ишимоку school variants (see RU-10); MT4 Ichimoku EAs.

**Pine Script Reference Implementation:** [`tr-11_ichimoku_kinko_hyo.pine`](tr-11_ichimoku_kinko_hyo.pine)

```pinescript
//@version=5
strategy("Ichimoku Kinko Hyo", overlay=true)
donchian(len) => math.avg(ta.highest(high, len), ta.lowest(low, len))
tenkan = donchian(9)
kijun  = donchian(26)
spanA  = math.avg(tenkan, kijun)
spanB  = donchian(52)
cloudHi = math.max(spanA[26], spanB[26])
cloudLo = math.min(spanA[26], spanB[26])
longCond  = close > kijun and close > cloudHi and tenkan > kijun
shortCond = close < kijun and close < cloudLo and tenkan < kijun
if longCond
strategy.entry("L", strategy.long)
if shortCond
strategy.entry("S", strategy.short)
plot(tenkan, "Tenkan", color=color.teal)
plot(kijun, "Kijun", color=color.red)
plot(spanA, "Span A", color=color.new(color.teal, 60), offset=26)
plot(spanB, "Span B", color=color.new(color.red, 60), offset=26)
```

---

### TR-12 · Kaufman Adaptive Moving Average (KAMA)
*卡玛自适应均线 · Адаптивная средняя Кауфмана*

- **Origin & Lineage:** Perry Kaufman, Smarter Trading, 1998.
- **Core Hypothesis:** KAMA scales its own smoothing constant by an Efficiency Ratio: when price travels cleanly (high ER) it hugs price like a fast EMA, and in noise (low ER) it flattens like a long SMA. This makes it a single-line trend filter that self-throttles in ranges. Traders either trade close-vs-KAMA crosses or use KAMA slope as the regime gate for other entries.
- **Execution Rules:** Long on close crossing above KAMA with rising slope; exit on cross under or slope flattening; short mirrored.
- **Key Parameters:** Window 10, fast 2, slow 30 (canonical); CN CTA uses 10/2/30 on commodity futures.
- **Duplicates Eliminated:** KAMA modules in CN CTA kits (文华/TB); RU «АМА Кауфмана» robots; KAMA+filter packs on MQL5.

**Pine Script Reference Implementation:** [`tr-12_kaufman_adaptive_moving_average_kama.pine`](tr-12_kaufman_adaptive_moving_average_kama.pine)

```pinescript
//@version=5
strategy("Kaufman Adaptive MA Trend", overlay=true)
len   = input.int(10, "Efficiency window")
fastE = input.int(2, "Fast smoothing")
slowE = input.int(30, "Slow smoothing")
chg = math.abs(close - close[len])
vol = math.sum(math.abs(ta.change(close)), len)
er  = chg / math.max(vol, syminfo.mintick)
sc  = math.pow(er * (2.0 / (fastE + 1) - 2.0 / (slowE + 1)) + 2.0 / (slowE + 1), 2)
var float kama = na
kama := na(kama[1]) ? close : kama[1] + sc * (close - kama[1])
if ta.crossover(close, kama)
strategy.entry("L", strategy.long)
if ta.crossunder(close, kama)
strategy.entry("S", strategy.short)
plot(kama, "KAMA", color=color.teal)
```

---

### TR-13 · VIDYA (Variable Index Dynamic Average)
*VIDYA可变动指数平均 · VIDYA*

- **Origin & Lineage:** Tushar Chande, 1992 (Technical Analysis of Stocks & Commodities).
- **Core Hypothesis:** VIDYA multiplies the EMA increment by the absolute momentum of a CMO, so the average speeds up in directional markets and stalls in noise — an alternative adaptive-MA solution to KAMA with different lag structure. It is usually used as the trend line inside breakout or pullback systems rather than as a cross system itself.
- **Execution Rules:** Treat VIDYA like an adaptive EMA in a dual-MA or pullback system; slope direction acts as the regime filter.
- **Key Parameters:** Length 9-20 with CMO(9) scaling is typical.
- **Duplicates Eliminated:** VIDYA in MetaStock/AmiBroker libraries (the 1990s archive era); MT4 VIDYA indicators; RU VIDYA forks.

---

### TR-14 · FRAMA (Fractal Adaptive Moving Average)
*分形自适应均线 · FRAMA*

- **Origin & Lineage:** John Ehlers, 2005 (TASC; fractal dimension work with Ric Way).
- **Core Hypothesis:** FRAMA computes a fractal dimension from half-window high/low geometry and maps it into an adaptive exponential weighting: smooth trends drive dimension toward 1 (fast MA), choppy ranges toward 2 (very slow MA). It is the most theoretically grounded of the adaptive-MA trio (KAMA, VIDYA, FRAMA) and behaves best on swing timeframes.
- **Execution Rules:** Use as a single-line trend filter; trade price-vs-FRAMA crosses with slope confirmation, or gate other systems with FRAMA slope.
- **Key Parameters:** Base length 16 (windows of len/2); alpha clamped [0.01, 1.0].
- **Duplicates Eliminated:** FRAMA ports in TASC Traders' Tips archive; MT4/MT5 FRAMA; CN 分形均线 experiments.

---

### TR-15 · Guppy Multiple Moving Averages (GMMA)
*顾比复合移动平均线 · GMMA Ганна Гаппи*

- **Origin & Lineage:** Daryl Guppy (Australia), Trading Tactics, 1990s; huge uptake in Chinese retail materials (顾比均线).
- **Core Hypothesis:** Twelve EMAs (3-15 and 30-60) split into a short-term 'traders' group and long-term 'investors' group; the geometry between the groups — compression, expansion, and crossover of the ribbons — reads consensus and disagreement. Trades are taken on group compression followed by expansion in the trend direction. It is a ribbon visualization of trend stability rather than a mechanical signal, which is why most implementations remain indicator-only.
- **Execution Rules:** Long when the fast ribbon crosses above and the slow ribbon expands with both sloping up; exit when ribbons compress and interpenetrate.
- **Key Parameters:** Fast 3/5/8/10/12/15; slow 30/35/40/45/50/60.
- **Duplicates Eliminated:** CN 顾比均线 templates (通达信/同花顺 formulas); RU «Вееры Ганна/Гаппи» ribbon packs.

**Pine Script Reference Implementation:** [`tr-15_guppy_multiple_moving_averages_gmma.pine`](tr-15_guppy_multiple_moving_averages_gmma.pine)

```pinescript
//@version=5
indicator("Guppy Multiple Moving Averages (GMMA)", overlay=true)
plot(ta.ema(close, 3),  "F3",  color=color.new(color.teal, 0))
plot(ta.ema(close, 5),  "F5",  color=color.new(color.teal, 20))
plot(ta.ema(close, 8),  "F8",  color=color.new(color.teal, 30))
plot(ta.ema(close, 10), "F10", color=color.new(color.teal, 40))
plot(ta.ema(close, 12), "F12", color=color.new(color.teal, 50))
plot(ta.ema(close, 15), "F15", color=color.new(color.teal, 60))
plot(ta.ema(close, 30), "S30", color=color.new(color.red, 0))
plot(ta.ema(close, 35), "S35", color=color.new(color.red, 20))
plot(ta.ema(close, 40), "S40", color=color.new(color.red, 30))
plot(ta.ema(close, 45), "S45", color=color.new(color.red, 40))
plot(ta.ema(close, 50), "S50", color=color.new(color.red, 50))
plot(ta.ema(close, 60), "S60", color=color.new(color.red, 60))
```

---

### TR-16 · Heikin-Ashi Trend Flip
*平均K线趋势翻转 · Торговля по Хейкин-Аши*

- **Origin & Lineage:** Munehisa Homma's candle lineage; Heikin-Ashi formalized for modern charts by Dan Valcu (2004, 'Using Heikin-Ashi technique').
- **Core Hypothesis:** Heikin-Ashi averages open/close into pseudo-candles whose bodies shrink in chop and stretch in trends; a run of same-color HA candles with full bodies is a high-contrast trend state. Systems flip long/short after N consecutive colored bodies with a minimum body size, or simply exit on the first opposite-colored candle. It is best treated as a regime filter because HA values are recursive and repaint the 'real' OHLC.
- **Execution Rules:** Long after 2 consecutive up HA bodies of at least 0.5 ATR; flip/exit on the mirror condition.
- **Key Parameters:** Run length 2-3; body filter 0.5 x ATR(14).
- **Duplicates Eliminated:** HA smoothing packs (every platform); CN Heikin-Ashi策略; RU «Хейкин Аши» scalping variants.

**Pine Script Reference Implementation:** [`tr-16_heikin_ashi_trend_flip.pine`](tr-16_heikin_ashi_trend_flip.pine)

```pinescript
//@version=5
strategy("Heikin-Ashi Trend Flip", overlay=true)
nRun = input.int(2, "Consecutive HA bars")
atrF = input.float(0.5, "Min body as ATR fraction")
var float haO = na
var float haC = na
haO := na(haO[1]) ? (open + close) / 2 : (haO[1] + haC[1]) / 2
haC := (open + high + low + close) / 4
body  = haC - haO
upRun = nz(ta.barssince(body <= 0), 999)
dnRun = nz(ta.barssince(body >= 0), 999)
bigEnough = math.abs(body) > atrF * ta.atr(14)
if upRun == nRun and bigEnough and strategy.position_size <= 0
strategy.entry("L", strategy.long)
if dnRun == nRun and bigEnough and strategy.position_size >= 0
strategy.entry("S", strategy.short)
```

---

### TR-17 · Time-Series Momentum (TSMOM)
*时间序列动量 · Моментум по времени*

- **Origin & Lineage:** Moskowitz, Ooi & Pedersen, Journal of Financial Economics, 2012 (AQR lineage).
- **Core Hypothesis:** Go long an asset if its own return over the past k months (commonly 12) is positive, short if negative, sized inversely to volatility. The paper documented that this simple sign rule monetizes the autocorrelation institutional CTAs create, across 58 instruments over decades. It is the academic formalization of what Donchian/Turtle systems do mechanically, and the backbone of most CTA replication products.
- **Execution Rules:** Sign of trailing 12-month return decides direction; position = target vol / realized vol; rebalance monthly.
- **Key Parameters:** Lookback 1-12 months; vol target 10-20% annualized.
- **Duplicates Eliminated:** Cross-sectional momentum (ST-04); CTA trend replication funds; CN 商品CTA趋势 replication research.

---

### TR-18 · CANSLIM Momentum / Leading-Stock Playbook
*欧奈尔CANSLIM选股法 · CANSLIM*

- **Origin & Lineage:** William O'Neil, How to Make Money in Stocks (1988; Investor's Business Daily methodology).
- **Core Hypothesis:** A fundamentals-plus-technique momentum system: buy stocks meeting Current earnings, Annual growth, New product/price highs, Supply/demand, Leaders, Institutional sponsorship, and Market direction, entered chiefly on cup-with-handle or flat-base breakouts in strong uptrends. Exits are hard rules: cut at 7-8% below entry, take profits into climactic runs. It is the direct ancestor of Qullamägi-style EP momentum (see BK-03 relatives) and of A-share 龙头战法 (CN-04) logic.
- **Execution Rules:** Screen by earnings/price leadership; buy base breakouts above pivot with volume surge; stop 7-8%; pyramiding only while the advance stays orderly.
- **Key Parameters:** Relative strength top percentile; volume >= 1.5x average on breakout; bases 3-7 weeks.
- **Duplicates Eliminated:** IBD-style screeners; CN 龙头战法 (structurally similar); RU «рост на лидерах» screeners.

---
