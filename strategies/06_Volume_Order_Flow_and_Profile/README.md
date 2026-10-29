# Family VO: Volume, Order Flow & Market Profile

**Total Strategies in Family:** 12  
**Pine Script v5 Implementations:** 2  

## Strategies Overview

| ID | Strategy Name | Alternative Names | Has Pine Code |
|---|---|---|:---:|
| **VO-01** | [Volume Spread Analysis (VSA)](#vo-01--volume_spread_analysis_vsa) | 量价分析法 · Объёмно-спредовый анализ (VSA) | 📖 Logic-only |
| **VO-02** | [On-Balance Volume Divergence](#vo-02--on_balance_volume_divergence) | 能量潮背离 · Дивергенция OBV | ✅ Pine v5 |
| **VO-03** | [Chaikin Money Flow / Accumulation-Distribution Line](#vo-03--chaikin_money_flow_accumulation_distribution_line) | 蔡金资金流 · Линия A/D и CMF | 📖 Logic-only |
| **VO-04** | [Money Flow Index](#vo-04--money_flow_index) | 资金流量指数 · Индекс денежного потока | 📖 Logic-only |
| **VO-05** | [Volume Profile Nodes (HVN/LVN/POC)](#vo-05--volume_profile_nodes_hvnlvnpoc) | 成交量分布节点 · Объёмный профиль (POC/HVN/LVN) | 📖 Logic-only |
| **VO-06** | [Market Profile TPO (Steidlmayer)](#vo-06--market_profile_tpo_steidlmayer) | 市场轮廓TPO · Маркет-профиль (TPO) | 📖 Logic-only |
| **VO-07** | [VWAP Deviation Bands (Execution-Grade)](#vo-07--vwap_deviation_bands_execution_grade) | VWAP偏差通道 · Полосы VWAP | ✅ Pine v5 |
| **VO-08** | [Anchored VWAP (AVWAP)](#vo-08--anchored_vwap_avwap) | 锚定VWAP · Якорный VWAP | 📖 Logic-only |
| **VO-09** | [Cumulative Delta Divergence (CVD)](#vo-09--cumulative_delta_divergence_cvd) | 累计成交量差背离 · Кумулятивная дельта (CVD) | 📖 Logic-only |
| **VO-10** | [Klinger Volume Oscillator](#vo-10--klinger_volume_oscillator) | 克林格成交量振荡器 · Осциллятор Клингера | 📖 Logic-only |
| **VO-11** | [Ease of Movement](#vo-11--ease_of_movement) | 简易波动指标 · Индекс лёгкости движения | 📖 Logic-only |
| **VO-12** | [Volume-Weighted Momentum Breakout](#vo-12--volume_weighted_momentum_breakout) | 量价动量突破 · Объёмно-взвешенный пробой | 📖 Logic-only |

---

### VO-01 · Volume Spread Analysis (VSA)
*量价分析法 · Объёмно-спредовый анализ (VSA)*

- **Origin & Lineage:** Tom Williams (ex-Wyckoff syndicate trader), Master the Markets (2003); software lineage TradeGuider; direct descent from PA-01/02.
- **Core Hypothesis:** VSA codifies Wyckoff reading into named bar patterns: 'no supply' (down bar, narrow spread, low volume at range lows — selling dried up), 'no demand' (up bar, narrow spread, low volume at highs), 'stopping volume' (climactic down bar absorbed), and 'effort vs result' anomalies. Systems trade the named setups with trend context. It is the single most-exported volume methodology to Russian and Chinese retail communities.
- **Execution Rules:** Long on 'no supply' after a downtrend with subsequent strength confirmation; short on 'no demand' after an up-leg; confirm with next-bar follow-through.
- **Key Parameters:** Spread percentile and volume relative to 20-50 bar averages; trend context filter.
- **Duplicates Eliminated:** VSA scripts (dozens of packs); CN 量价分析 school; RU VSA-сообщество (Smart-Lab's volume tradition); Wyckoff bar-reading (PA-02).

---

### VO-02 · On-Balance Volume Divergence
*能量潮背离 · Дивергенция OBV*

- **Origin & Lineage:** Joe Granville, 1963 (New Key to Stock Market Profits).
- **Core Hypothesis:** OBV accumulates signed volume; when price makes new highs/lows without OBV confirming, the move lacks participation and is prone to reversal — Granville's original 'OBV vs price' divergence. As a system it is a confirmation layer: trend entries require OBV agreement, and OBV non-confirmation flags exits. Granville's later salesmanship outran his statistics, but the mechanism survives in modern flow measures.
- **Execution Rules:** Compare 20-bar linreg slopes of price and OBV; divergence flags reversal candidates; confluence confirms trend entries.
- **Key Parameters:** Slope window 20; divergence persistence 3 bars.
- **Duplicates Eliminated:** OBV in every platform; CN 能量潮战法; RU OBV-роботы; CMF/ADL cousins (MR-15).

**Pine Script Reference Implementation:** [`vo-02_on_balance_volume_divergence.pine`](vo-02_on_balance_volume_divergence.pine)

```pinescript
//@version=5
indicator("OBV Divergence Helper", overlay=false)
obv = ta.obv
obvSlope = ta.linreg(obv, 20, 0) - ta.linreg(obv, 20, 1)
priceSlope = ta.linreg(close, 20, 0) - ta.linreg(close, 20, 1)
bullDiv = priceSlope < 0 and obvSlope > 0
bearDiv = priceSlope > 0 and obvSlope < 0
plot(obv, "OBV", color=color.teal)
plotshape(bullDiv, "Bull div", shape.circle, location.bottom, color=color.teal, size=size.tiny)
plotshape(bearDiv, "Bear div", shape.circle, location.top, color=color.red, size=size.tiny)
```

---

### VO-03 · Chaikin Money Flow / Accumulation-Distribution Line
*蔡金资金流 · Линия A/D и CMF*

- **Origin & Lineage:** Marc Chaikin, 1966-1980s (building on Granville OBV and Joe Joseph's work).
- **Core Hypothesis:** The A/D line weights each bar's volume by where close sits in its range (close-line location = buying pressure), and CMF normalizes it over 20 bars into a +/- oscillator. Sustained positive CMF during flat price flags accumulation — the classic 'smart money is buying the dip' read. It is a location-weighted OBV and inherits the same confirmation role.
- **Execution Rules:** Long when CMF > +0.25 with price basing; exit when CMF crosses down through zero after a run; divergence use as VO-02.
- **Key Parameters:** CMF 20-21; thresholds 0.25 / -0.25.
- **Duplicates Eliminated:** ADL/CMF packs; CN CMF资金流策略; RU CMF-роботы.

---

### VO-04 · Money Flow Index
*资金流量指数 · Индекс денежного потока*

- **Origin & Lineage:** Avinash 'Avi' Quong & Mehran Soudack, TASC August 1989 (a volume-weighted RSI).
- **Core Hypothesis:** MFI multiplies typical price by volume into 'money flow', then applies RSI math to positive vs negative flow days — producing an RSI-shaped oscillator that requires participation for extremes to register. MFI extremes with price non-confirmation are the volume-flavored divergence signal. As a fade system it mirrors MR-15's usage.
- **Execution Rules:** Long on MFI < 20 in uptrend regime; exit MFI > 50; divergence reading as primary use.
- **Key Parameters:** Length 14; bands 20/80.
- **Duplicates Eliminated:** MFI everywhere; CN MFI资金策略; RU MFI-скрипты.

---

### VO-05 · Volume Profile Nodes (HVN/LVN/POC)
*成交量分布节点 · Объёмный профиль (POC/HVN/LVN)*

- **Origin & Lineage:** Market Profile descendant; volume-profile software (2000s: MarketDelta, Sierra) then Pine ports.
- **Core Hypothesis:** Histogram traded volume by price level; the Point of Control (heaviest node) acts as magnet and fair value, High-Volume Nodes as support/resistance shelf, and Low-Volume Nodes as vacuum zones price traverses quickly. Systems trade POC bounces in balance and LVN traversals toward the next node. Pine implementations estimate profiles from bar ranges — an approximation noted in code comments.
- **Execution Rules:** Long at HVN support under POC in balance; target the next HVN; break of POC with acceptance flips the balance area.
- **Key Parameters:** Profile window 50-200 bars; bin count 24-100; acceptance = 2+ closes beyond.
- **Duplicates Eliminated:** Volume profile packs (LuxAlgo, multiple); CN 成交量分布策略; RU объёмный профиль community.

---

### VO-06 · Market Profile TPO (Steidlmayer)
*市场轮廓TPO · Маркет-профиль (TPO)*

- **Origin & Lineage:** J. Peter Steidlmayer, CBOT, 1984 (with the CBOT's Market Profile concept letter).
- **Core Hypothesis:** TPO counts time-at-price in 30-minute brackets, defining value areas, one-timeelling rotations, and open types (open-drive, open-rejection, open-test). Steidlmayer's insight — the market's auction finds fair value where time accumulates — created a complete auction-theory framework. The systematic edges (value-area fades, initiative vs responsive opens) require session-TPO construction that Pine approximates poorly, so it remains mostly logic-only here.
- **Execution Rules:** Fade edges of the prior day's value area on responsive opens; join initiative moves that accept outside value.
- **Key Parameters:** TPO period 30 min; value area 70% of TPO; open-type classification.
- **Duplicates Eliminated:** TPO chart packs; RU аукционная теория followers; CN 市场轮廓 study groups.

---

### VO-07 · VWAP Deviation Bands (Execution-Grade)
*VWAP偏差通道 · Полосы VWAP*

- **Origin & Lineage:** Institutional execution analytics; popularized by VWAP-band scripts and Brian Shannon's teaching.
- **Core Hypothesis:** Session VWAP with standard-deviation bands turns the execution benchmark into a regime map: price above VWAP is a buy-the-dip day, below is sell-the-rip, band-3 extremes in balance are reversion candidates. Unlike MR-12 (pure fade), the band system's core rule is trade WITH the VWAP side and use bands for entry timing. It is the most-used institutional overlay on intraday desks.
- **Execution Rules:** Long dips to VWAP or -1 sigma while price holds above VWAP; fade -2/-3 sigma only in balance regimes; exit at VWAP cross against.
- **Key Parameters:** Session VWAP; bands 1/2/3 sigma of (close - VWAP); regime by first-hour VWAP side.
- **Duplicates Eliminated:** VWAP band packs; CN VWAP通道; RU VWAP-стратегии; anchored-VWAP variants (VO-08).

**Pine Script Reference Implementation:** [`vo-07_vwap_deviation_bands_execution_grade.pine`](vo-07_vwap_deviation_bands_execution_grade.pine)

```pinescript
//@version=5
indicator("Session VWAP + Deviation Bands", overlay=true)
b1 = input.float(1.0, "Band 1 (stdev)")
b2 = input.float(2.0, "Band 2 (stdev)")
v = ta.vwap(hlc3)
dev = ta.stdev(close - v, 50)
plot(v, "VWAP", color=color.orange)
plot(v + b1 * dev, "+1", color=color.new(color.teal, 40))
plot(v - b1 * dev, "-1", color=color.new(color.teal, 40))
plot(v + b2 * dev, "+2", color=color.new(color.red, 40))
plot(v - b2 * dev, "-2", color=color.new(color.red, 40))
```

---

### VO-08 · Anchored VWAP (AVWAP)
*锚定VWAP · Якорный VWAP*

- **Origin & Lineage:** Brian Shannon, Maximum Trading Gains with Anchored VWAP (2020) — the formalization of a desk-era tool.
- **Core Hypothesis:** VWAP anchored not to the session but to a meaningful event (earnings gap, swing high/low, news) traces the average participation price since that event;AVWAPs from major pivots act as institutional memory levels that price respects or breaks meaningfully. Systems trade AVWAP bounces in trends and acceptance-through-AVWAP as regime shifts.
- **Execution Rules:** Anchor at event bars (user-defined or automated pivots); long retests of rising AVWAP in trend; exit on 2-bar acceptance through AVWAP against the trade.
- **Key Parameters:** Anchor events; confluence of 2+ AVWAPs strengthens the level.
- **Duplicates Eliminated:** AVWAP packs (Shannon-affiliated and clones); CN 锚定VWAP; RU якорный VWAP.

---

### VO-09 · Cumulative Delta Divergence (CVD)
*累计成交量差背离 · Кумулятивная дельта (CVD)*

- **Origin & Lineage:** Footprint/order-flow software (2000s: MarketDelta, NinjaTrader Order Flow) — Pine approximates from bar microstructure.
- **Core Hypothesis:** Delta = aggressive buys minus aggressive sells (proxied in Pine by close-position-in-range heuristics); cumulative delta tracks net aggression. Divergences — price new high without delta confirmation — flag absorption by passive sellers, the modern footprint version of Wyckoff effort-vs-result. True tick-level CVD is unavailable in Pine, so implementations document the approximation honestly.
- **Execution Rules:** Long on bullish CVD divergence at support (price low, delta higher low); confirm with structure; exit on delta flip.
- **Key Parameters:** Delta proxy: (close - low - (high - close)) / range x volume; divergence window 20-50 bars.
- **Duplicates Eliminated:** CVD packs; CN 订单流/德尔塔 scripts; RU дельта-анализ (footprint communities).

---

### VO-10 · Klinger Volume Oscillator
*克林格成交量振荡器 · Осциллятор Клингера*

- **Origin & Lineage:** Stephen Klinger, 1977 (publication in 1980s TASC-era materials).
- **Core Hypothesis:** KVO compares two EMAs of a 'volume force' (trend direction x volume x range position) to detect long-term accumulation/distribution turning points; signal-line crosses with divergence flag major reversals. It aims to catch the force behind trends before price confirms. Mostly used as confirmation context in hybrid systems.
- **Execution Rules:** Long on KVO crossing signal from below while price makes marginal lows (accumulation divergence); exit on signal re-cross.
- **Key Parameters:** 34/55 EMAs of volume force; signal 13.
- **Duplicates Eliminated:** KVO packs; CN KVO指标; RU Klinger robots.

---

### VO-11 · Ease of Movement
*简易波动指标 · Индекс лёгкости движения*

- **Origin & Lineage:** Richard Arms, 1970s (Arms also of TRIN fame).
- **Core Hypothesis:** EMV scales the mid-price change per bar by the inverse of volume per range unit — price traveling far on light volume scores high 'ease', implying an uncontested move. Arms' auction logic reads ease as sustainability. It is a niche confirmation oscillator today, surviving in scan stacks rather than as a standalone system.
- **Execution Rules:** Trend confirmation: EMV > 0 sustains longs in trend systems; negative cross flags fading drive.
- **Key Parameters:** Length 14; smoothed variant common.
- **Duplicates Eliminated:** EMV in classic libraries; CN EMV模板.

---

### VO-12 · Volume-Weighted Momentum Breakout
*量价动量突破 · Объёмно-взвешенный пробой*

- **Origin & Lineage:** Formalization of 放量突破 across CN platforms and OBV-breakout research in western scan communities.
- **Core Hypothesis:** A consolidated form of BK-08: enter breakouts only when a composite of volume surge, OBV slope, and CMF agrees — requiring the flow triad to confirm the price break. This reduces false breaks materially at the cost of later entries, and is the typical 'volume-confirmed breakout' template in Chinese factor workbooks.
- **Execution Rules:** Long on N-bar high with volume > k x avg, OBV slope > 0, CMF > 0; stop under breakout bar low.
- **Key Parameters:** N 20-60; k 1.5-2; flow gates as above.
- **Duplicates Eliminated:** BK-08; VO-02/03 combos; RU «пробой с потоком» scripts.

---
