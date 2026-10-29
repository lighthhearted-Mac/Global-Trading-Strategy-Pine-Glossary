# Family CN: China-Specific Systems (A-Share & CN Futures)

**Total Strategies in Family:** 26  
**Pine Script v5 Implementations:** 4  

## Strategies Overview

| ID | Strategy Name | Alternative Names | Has Pine Code |
|---|---|---|:---:|
| **CN-01** | [Chan Theory (缠论): Fractals, Pens, Pivots & Three Buy/Sell Points](#cn-01--chan_theory_fractals_pens_pivots_three_buysell_points) | 缠论：分型、笔、中枢与三类买卖点 | ✅ Pine v5 |
| **CN-02** | [Limit-Up Board Tactics (打板：首板/连板/接力)](#cn-02--limit_up_board_tactics) | 涨停板战法 | ✅ Pine v5 |
| **CN-03** | [Limit-Up Pullback Re-entry (涨停回马枪)](#cn-03--limit_up_pullback_re_entry) | 涨停回马枪 | ✅ Pine v5 |
| **CN-04** | [Dragon-Head Leading-Stock Tactics (龙头战法)](#cn-04--dragon_head_leading_stock_tactics) | 龙头战法 | 📖 Logic-only |
| **CN-05** | [Sentiment Cycle Model (情绪周期)](#cn-05--sentiment_cycle_model) | 情绪周期：冰点→发酵→高潮→退潮 | 📖 Logic-only |
| **CN-06** | [Chip Distribution (筹码分布 / CYQ)](#cn-06--chip_distribution_cyq) | 筹码分布与SCR指标 | 📖 Logic-only |
| **CN-07** | [Dragon-Tiger List Following (龙虎榜跟随)](#cn-07--dragon_tiger_list_following) | 龙虎榜策略 | 📖 Logic-only |
| **CN-08** | [Northbound Capital Following (北向资金跟随)](#cn-08--northbound_capital_following) | 北向资金策略 | 📖 Logic-only |
| **CN-09** | [Margin Balance Sentiment (融资融券情绪)](#cn-09--margin_balance_sentiment) | 两融情绪策略 | 📖 Logic-only |
| **CN-10** | [Double-Low Convertible Bonds (双低可转债)](#cn-10--double_low_convertible_bonds) | 双低转债策略 | 📖 Logic-only |
| **CN-11** | [Large/Small-Cap Rotation (大小盘轮动)](#cn-11--largesmall_cap_rotation) | 大小盘轮动策略 | 📖 Logic-only |
| **CN-12** | [Sector Rotation (行业轮动)](#cn-12--sector_rotation) | 行业轮动策略 | 📖 Logic-only |
| **CN-13** | [Index Enhancement (指数增强)](#cn-13--index_enhancement) | 指数增强策略 | 📖 Logic-only |
| **CN-14** | [Alpha Strategy with Index-Futures Hedge (阿尔法策略)](#cn-14--alpha_strategy_with_index_futures_hedge) | 阿尔法策略 | 📖 Logic-only |
| **CN-15** | [Multi-Factor Stock Selection (多因子选股)](#cn-15--multi_factor_stock_selection) | 多因子选股策略 | 📖 Logic-only |
| **CN-16** | [MA Convergence Breakout (均线粘合突破)](#cn-16--ma_convergence_breakout) | 均线粘合突破战法 | ✅ Pine v5 |
| **CN-17** | [N-Structure Tactics (N字战法)](#cn-17--n_structure_tactics_n) | N字战法 | 📖 Logic-only |
| **CN-18** | [Rising Pullback System (上升回档)](#cn-18--rising_pullback_system) | 上升回档模式 | 📖 Logic-only |
| **CN-19** | [Main-Force Accumulation Tracking (主力吸筹跟踪)](#cn-19--main_force_accumulation_tracking) | 主力吸筹战法 | 📖 Logic-only |
| **CN-20** | [Swing Band System (波段操作 / 波段王)](#cn-20--swing_band_system) | 波段王 | 📖 Logic-only |
| **CN-21** | [Intraday T+0 Around Base Position (底仓做T)](#cn-21--intraday_t0_around_base_position_t) | 底仓做T策略 | 📖 Logic-only |
| **CN-22** | [Call-Auction & Tail-Session Tactics (集合竞价/尾盘战法)](#cn-22--call_auction_tail_session_tactics) | 集合竞价与尾盘战法 | 📖 Logic-only |
| **CN-23** | [Calendar Spread Arbitrage (跨期套利)](#cn-23--calendar_spread_arbitrage) | 跨期套利 | 📖 Logic-only |
| **CN-24** | [Cross-Commodity Spreads (跨品种套利)](#cn-24--cross_commodity_spreads) | 跨品种套利 | 📖 Logic-only |
| **CN-25** | [Futures-Cash Basis Arbitrage (期现套利)](#cn-25--futures_cash_basis_arbitrage) | 期现套利与ETF套利 | 📖 Logic-only |
| **CN-26** | [Valuation-Band Rotation (估值分位轮动)](#cn-26--valuation_band_rotation) | 估值分位轮动策略 | 📖 Logic-only |

---

### CN-01 · Chan Theory (缠论): Fractals, Pens, Pivots & Three Buy/Sell Points
*缠论：分型、笔、中枢与三类买卖点*

- **Origin & Lineage:** The blogger 缠中说禅 (Chan Zhongshuo Chan), serial essays 2006-2008 (教你炒股票 series).
- **Core Hypothesis:** Chan theory builds a strictly nested structure: K-lines merge (处理包含), top/bottom fractals (分型) chain into pens (笔), pens into segments (线段), and the overlap of three consecutive sub-moves defines a pivot zone (中枢). Trades are the three buy points: first buy at the pivot's trend-exhaustion divergence, second on the failed retest low, third on the pullback that holds above the pivot after breakout. Its rigor and completeness made it China's dominant native TA framework, now industrialized in open source.
- **Execution Rules:** Build fractal/pen/segment structure; locate 中枢 [ZG, ZD]; buy-3 when price breaks above ZG then pulls back holding above ZG; mirror for sell-3; MACD divergence confirms buy-1/sell-1.
- **Key Parameters:** Pen thresholds (5+ bars); pivot overlap rule; level nesting 1m/5m/30m/daily (多级别联立).
- **Duplicates Eliminated:** czsc (waditu/czsc — 200+ signal functions, Rust core); chanlun-pro (gaoxiaojun) with JoinQuant/Broker adapters; 缠论 indicator packs on 通达信; no western equivalent (pivot-breakout SMC is a loose cousin).

**Pine Script Reference Implementation:** [`cn-01_chan_theory_fractals_pens_pivots_three_buysell_points.pine`](cn-01_chan_theory_fractals_pens_pivots_three_buysell_points.pine)

```pinescript
//@version=5
strategy("Chanlun-style Pivot (Zhongshu) Breakout", overlay=true)
segLen = input.int(10, "Segment window")
atr = ta.atr(14)
// Overlap of three consecutive segment ranges approximates the zhongshu
hi1 = ta.highest(high, segLen)
lo1 = ta.lowest(low, segLen)
hi2 = ta.highest(high, segLen)[segLen]
lo2 = ta.lowest(low, segLen)[segLen]
hi3 = ta.highest(high, segLen)[2 * segLen]
lo3 = ta.lowest(low, segLen)[2 * segLen]
zg = math.min(hi1, math.min(hi2, hi3))
zd = math.max(lo1, math.max(lo2, lo3))
hasPivot = zg > zd
var bool broke = false
if hasPivot and close > zg
broke := true
thirdBuy  = broke and low > zg and close > open
thirdSell = not hasPivot or close < zd
if thirdBuy and strategy.position_size <= 0
strategy.entry("L", strategy.long)
if thirdSell and strategy.position_size > 0
strategy.close("L", comment="Pivot invalidated")
plot(zg, "ZG (pivot top)", color=color.teal)
plot(zd, "ZD (pivot bottom)", color=color.red)
```

---

### CN-02 · Limit-Up Board Tactics (打板：首板/连板/接力)
*涨停板战法*

- **Origin & Lineage:** 宁波涨停板敢死队 (Ningbo 'death squad') era, early 2000s; codified in 淘股吧/游资 literature.
- **Core Hypothesis:** The 10% daily limit creates a queue-auction: a stock sealing the limit signals one-sided demand that cannot clear until the next day, and 连板 (consecutive limit streaks) mark the momentum lifecycle of speculative cycles. 打板 buys the seal itself or the next day's open on strength; 首板/连板 classifications and 情绪周期 (CN-05) govern which day of the cycle is tradeable. This is the purest momentum strategy extant anywhere — and the most dependent on exchange microstructure.
- **Execution Rules:** Detect limit-close (close == limit price); enter next open if sentiment regime supports continuation; exit on a non-limit close, failure to seal intraday, or time stop.
- **Key Parameters:** Limit 10% (main board) / 20% (ChiNext/STAR); sentiment gates (前日连板高度, 跌停家数); no short side (A-share constraint).
- **Duplicates Eliminated:** Every A-share 打板 screener (同花顺/通达信 formulas); BigQuant limit-up factors; not replicable on unlimited markets (the limit IS the edge).

**Pine Script Reference Implementation:** [`cn-02_limit_up_board_tactics.pine`](cn-02_limit_up_board_tactics.pine)

```pinescript
//@version=5
strategy("Limit-Up Board Continuation (打板, generalized)", overlay=true)
limitPct = input.float(10.0, "Daily limit %")
tol = input.float(0.002, "Price tolerance")
lim = close[1] * (1 + limitPct / 100)
limitUp = close >= lim * (1 - tol) and close == high
firstBoard = limitUp and not limitUp[1]
if firstBoard
strategy.entry("L", strategy.long, comment="Next-open continuation")
if strategy.position_size > 0 and not limitUp
strategy.close("L", comment="No follow-through")
if strategy.position_size > 0 and nz(ta.barssince(firstBoard)) > 3
strategy.close("L", comment="Time stop")
```

---

### CN-03 · Limit-Up Pullback Re-entry (涨停回马枪)
*涨停回马枪*

- **Origin & Lineage:** A-share swing community (2010s WeChat 战法 literature); also a standard TDX formula.
- **Core Hypothesis:** After a limit-up marks institutional arrival, the stock typically digests for days; the trade buys the controlled pullback to the 10/20-day MA while the limit-up's volume signature stays constructive, targeting the retest of the spike high. It converts the emotional limit-up event into a measured swing entry, and is among the most-shared CN formulas.
- **Execution Rules:** A limit-up within the last 5-8 bars; pullback touches MA(10/20) with shrinking volume; long on a bullish reclaim bar; stop under pullback low.
- **Key Parameters:** Lookback 5-8; MA 10/20; volume contraction < 0.7 x spike-day volume.
- **Duplicates Eliminated:** 回踩战法 variants; 强势股回调买入 templates; TDX 回马枪 formulas (same pattern).

**Pine Script Reference Implementation:** [`cn-03_limit_up_pullback_re_entry.pine`](cn-03_limit_up_pullback_re_entry.pine)

```pinescript
//@version=5
strategy("Limit-Up Pullback Re-entry (回马枪)", overlay=true)
limitPct = input.float(10.0, "Daily limit %")
lookback = input.int(6, "Recent limit-up within N bars")
maLen = input.int(20, "Pullback MA")
lim = close[1] * (1 + limitPct / 100)
limitUp = close >= lim * 0.998 and close == high
recentBoard = nz(ta.barssince(limitUp)) <= lookback
ma = ta.sma(close, maLen)
pullback = recentBoard and low <= ma and close > ma and volume < ta.sma(volume, 5)
if pullback and strategy.position_size == 0
strategy.entry("L", strategy.long)
atr = ta.atr(14)
if strategy.position_size > 0 and close < strategy.position_avg_price - 2 * atr
strategy.close("L", comment="Stop")
```

---

### CN-04 · Dragon-Head Leading-Stock Tactics (龙头战法)
*龙头战法*

- **Origin & Lineage:** 游资 (hot-money) tradition, 淘股吧 era; popularized by traders like 炒股养家 (public posts, 2010s).
- **Core Hypothesis:** Within a speculative theme, the dragon head (leading stock) absorbs the majority of capital attention and keeps rising while followers die first; the strategy identifies the theme's first limit-up stock with sector resonance, buys its continuation or its first strong pullback, and rides until 龙头首阴 (the leader's first big bearish candle) or sentiment top. It is CANSLIM's leadership principle (TR-18) weaponized on limit-up mechanics with an explicit sentiment lifecycle.
- **Execution Rules:** Identify theme + first/strongest limit-up with sector breadth; enter continuation boards or first MA pullback; exit on leader's first bearish engulfing or sentiment peak signals (CN-05).
- **Key Parameters:** Sector resonance >= 3 limit-ups; leader relative strength top 1%; exit discipline on 首阴.
- **Duplicates Eliminated:** CANSLIM (TR-18) structural cousin; CN 主升浪战法; 打板 (CN-02) entry mechanics.

---

### CN-05 · Sentiment Cycle Model (情绪周期)
*情绪周期：冰点→发酵→高潮→退潮*

- **Origin & Lineage:** 游资 community synthesis (2010s; 炒股养家, 淘县 school).
- **Core Hypothesis:** A-share speculation moves through observable phases — 冰点 (freeze: limit-up count collapses), 发酵 (fermentation: leaders emerge), 高潮 (climax: broad limit-up waves, high 连板 heights), 退潮 (ebb: leaders fail, 跌停 clusters) — measured by daily limit-up/limit-down counts, board heights, and 炸板率 (failed seals). The model is a market-regime gate: 打板/接力 strategies trade only in fermentation-climax phases and stand down in ebb. It is sentiment quantification with a uniquely CN data basis.
- **Execution Rules:** Compute daily limit-up count, max board height, failed-seal rate; classify phase; enable aggressive tactics only in fermentation/climax; flip to defensive in ebb/freeze.
- **Key Parameters:** Thresholds on counts/heights (e.g., climax: 100+ limit-ups, height >= 5); phase persistence filters.
- **Duplicates Eliminated:** 连板高度 monitoring dashboards; BigQuant sentiment factors; no direct western analog (closest: breadth-thrust regime models).

---

### CN-06 · Chip Distribution (筹码分布 / CYQ)
*筹码分布与SCR指标*

- **Origin & Lineage:** 陈浩 (Chen Hao) & 天狼50 school, 2000s; implemented in 指南针/通达信 indicators.
- **Core Hypothesis:** A cost-basis distribution estimated from historical volume assuming round-trip decay: each price level holds the shares believed to be held there, forming peaks at congestion and valleys at fast moves. Reads: 筹码单峰密集 (single-peak concentration) precedes breakouts, 主力低位吸筹 shows mass migrating to lows, and 获利盘比例 (profit-holder ratio) drives resistance. It is a uniquely CN institutional-psychology lens on volume.
- **Execution Rules:** Estimate the chip distribution (triangular decay over ~60-120 bars); trade breakouts from single-peak zones or profit-ratio thresholds (e.g., sell when 90%+ in profit into resistance).
- **Key Parameters:** Decay factor ~0.5-0.8 per turnover; estimation window 60-250 bars.
- **Duplicates Eliminated:** CYQ/SCR indicator clones; 筹码峰 formulas in TDX; volume-profile (VO-05) is the western statistical cousin.

---

### CN-07 · Dragon-Tiger List Following (龙虎榜跟随)
*龙虎榜策略*

- **Origin & Lineage:** SSE/SZSE disclosure rules (2010s formalization); 集思录/淘股吧 tracking communities.
- **Core Hypothesis:** Exchanges disclose daily the top broker-branch flows behind abnormal moves; famous 游资 seats have trackable styles, so strategies follow disclosed net-buyers of specific seats into the next session (or fade notorious sellers). It is flow-copy trading with an official data source — a transparency artifact unique to A-shares.
- **Execution Rules:** Nightly, parse 龙虎榜 disclosures; if known-strong seats net-buy heavily, enter next open with limit-up-cycle regime gate (CN-05); exit per 打板 rules.
- **Key Parameters:** Seat whitelist/blacklist; position sizing by seat conviction; next-open entry discipline.
- **Duplicates Eliminated:** 席位跟踪 dashboards (问财/开盘啦); not portable without disclosure data.

---

### CN-08 · Northbound Capital Following (北向资金跟随)
*北向资金策略*

- **Origin & Lineage:** Stock Connect launch (2014/2016); HKEX daily flow disclosure; CN quant community adoption.
- **Core Hypothesis:** Northbound (HK->mainland) flows were visible daily and acquired a 'smart money' halo; strategies follow sustained northbound net-buying per stock or rotate into the most-bought constituents. Academic evidence on the flow's alpha is mixed, and the 2024 disclosure-frequency cut (daily to quarterly for holdings) degraded most implementations — an instructive archive lesson in data-regime risk.
- **Execution Rules:** Track daily northbound net flow by stock; enter sustained multi-day accumulation names with trend filter; exit on flow reversal or target.
- **Key Parameters:** Flow threshold vs free float; persistence 3-5 days; regime filter.
- **Duplicates Eliminated:** 北向资金实时 tracking tools (pre-2024); 外资流入 strategies on JoinQuant/BigQuant.

---

### CN-09 · Margin Balance Sentiment (融资融券情绪)
*两融情绪策略*

- **Origin & Lineage:** Margin trading pilot 2010; CNKI/HSE-style academic studies and platform factors.
- **Core Hypothesis:** Margin financing balance (融资余额) proxies leveraged retail bullishness; rising balances with flat price flag hidden demand, while falling balances in rallies warn of weak conviction. Systematic uses include leverage-sentiment regime gates for rotation strategies and per-stock margin-buy screening. It is the CN analog of US margin-debt sentiment studies.
- **Execution Rules:** Gate rotation strategies by aggregate 融资余额 trend; screen stocks with rising margin balance + price base; exit when balance rolls over.
- **Key Parameters:** Balance percentile windows 20-60 days; index-level regime gates.
- **Duplicates Eliminated:** 两融数据 factor studies (华泰金工 reports); platform sentiment factors.

---

### CN-10 · Double-Low Convertible Bonds (双低可转债)
*双低转债策略*

- **Origin & Lineage:** 集思录 community canon (2014+); 小散/掌村 bloggers' formalization.
- **Core Hypothesis:** CB double-low = price + conversion premium x 100; the lowest double-low bonds combine bond-floor protection with equity optionality, and rotating monthly into the cheapest decile historically compounded at equity-like rates with far smaller drawdowns. Add-ons include 强赎 (forced redemption) avoidance and 下修 (reset) event anticipation. It is China's most distinctive quant-retail success story — a genuinely unique instrument-driven strategy.
- **Execution Rules:** Rank all CBs by price + 100 x conversion premium; hold the bottom N equal-weighted; rebalance monthly; exclude bonds near forced-redemption triggers.
- **Key Parameters:** N 5-20; rebalance weekly/monthly; filters: size, rating, redemption distance.
- **Duplicates Eliminated:** 集思录轮动 dashboards; 双低 variants (低价/低溢价 separable); CB wheel strategies.

---

### CN-11 · Large/Small-Cap Rotation (大小盘轮动)
*大小盘轮动策略*

- **Origin & Lineage:** Academic and 券商金工 research (2010s); JoinQuant/BigQuant template staple.
- **Core Hypothesis:** Relative momentum (or valuation spread) between CSI 300 and CSI 500/1000 governs which cap bucket leads multi-month cycles; the rotation form holds the leading index (or its ETF) with monthly rebalance, optionally gated by volatility or M2/credit regime. The 2016-2017 and 2013 cycles are the canonical case studies.
- **Execution Rules:** Compute 3-12 month relative strength (or PE/PB spread percentile) 300 vs 500/1000; hold the winner's ETF; rebalance monthly with hysteresis.
- **Key Parameters:** Lookback 3-6 months; hysteresis band 5-10%; vol gate optional.
- **Duplicates Eliminated:** 行业轮动 (CN-12) at sector scale; global size-factor rotation (ST-04/05).

---

### CN-12 · Sector Rotation (行业轮动)
*行业轮动策略*

- **Origin & Lineage:** JoinQuant's ten canonical strategies list; 券商金工 sector-momentum reports (华泰/国盛).
- **Core Hypothesis:** Rank SW/CITIC industry indices by multi-window momentum (or by fundamental momentum: earnings revision + price), rotate into the top 3-5 industries monthly. CN implementations add policy-sentiment overlays because sector moves are policy-driven. The mechanism is standard cross-sectional momentum (ST-04) applied to industry indices.
- **Execution Rules:** Rank industries by 3+6 month momentum; hold top k ETFs; monthly rebalance; optional drawdown stop.
- **Key Parameters:** Momentum windows 3/6/12; k 3-5; transaction-cost aware rebalance.
- **Duplicates Eliminated:** ST-04 cross-sectional momentum (same mechanism); US sector-rotation literature.

---

### CN-13 · Index Enhancement (指数增强)
*指数增强策略*

- **Origin & Lineage:** CN quant-fund industry practice (2010s); JoinQuant template #7.
- **Core Hypothesis:** Track a benchmark (CSI 300/500) while adding tilts — multi-factor stock selection, T+0 intraday enhancement on the base position (CN-21), and allocation timing — to beat the index by a few percent annually. It is not one algorithm but a framework: benchmark replication + alpha overlays. Listed here because CN platforms treat it as a canonical strategy class.
- **Execution Rules:** Hold index-tilted portfolio (factor tilts, see ST entries); harvest intraday enhancement via 做T; hedge tail with index futures when allowed.
- **Key Parameters:** Tracking-error budget 2-5%; factor tilt weights; hedge ratio.
- **Duplicates Eliminated:** ST-08/09 factor overlays; global 'index-plus' products.

---

### CN-14 · Alpha Strategy with Index-Futures Hedge (阿尔法策略)
*阿尔法策略*

- **Origin & Lineage:** JoinQuant's canonical ten (myquant docs); 2010-2015 IF-era golden age.
- **Core Hypothesis:** Long a stock basket selected to beat the index, short the corresponding index future (IF/IC/IM), isolating pure alpha from market beta. The strategy's Chinese golden age ended with the 2015 futures restrictions (discounts, position limits), after which the basis cost ate much of the alpha — a documented lesson in regulatory risk. Still taught as the fundamental market-neutral template.
- **Execution Rules:** Construct positive-alpha basket (multi-factor, CN-15); short equivalent index futures; roll contracts; manage basis risk.
- **Key Parameters:** Basket beta targeting; hedge ratio 0.8-1.0; roll calendar.
- **Duplicates Eliminated:** ST statistical arb at index level; global 130/30 and market-neutral funds.

---

### CN-15 · Multi-Factor Stock Selection (多因子选股)
*多因子选股策略*

- **Origin & Lineage:** JoinQuant canonical ten; 华泰金工/国盛金工 factor research series; WorldQuant BRAIN CN community.
- **Core Hypothesis:** Score stocks by combined factors (value, growth, quality, momentum, liquidity, reversal) with industry/size neutralization, hold the top decile with periodic rebalance. The CN twist: reversal and small-cap factors historically dominated, and Barra-style CN risk models are public via 券商 reports. It is the industrial backbone of CN quant equity.
- **Execution Rules:** Compute factor z-scores with winsorization/neutralization; composite score; hold top N monthly; rebalance with cost control.
- **Key Parameters:** Factor set per Barra-CN; weighting IC-weighted or equal; rebalance monthly.
- **Duplicates Eliminated:** ST-04..ST-11 factor entries (the global canon of the same idea); WorldQuant 101 Alphas (ST-10).

---

### CN-16 · MA Convergence Breakout (均线粘合突破)
*均线粘合突破战法*

- **Origin & Lineage:** CN platform-era 战法 (TDX/同花顺 formula canon).
- **Core Hypothesis:** When 5/10/20/60-day MAs converge within a few percent of each other, trend disagreement has collapsed — energy coiled; the first close above the bundle with volume marks the release. It is a moving-average-systems' answer to the squeeze (MR-05) and behaves like a base-breakout with self-drawn boundaries.
- **Execution Rules:** Detect MA bundle spread < 3% of price; long on close above the highest MA with volume > 1.5x; stop under bundle mid.
- **Key Parameters:** MA set 5/10/20/60; spread threshold 2-4%; volume 1.5x.
- **Duplicates Eliminated:** BK-09 box breakout (same coiling mechanism); CN 平台突破 with MA flavor.

**Pine Script Reference Implementation:** [`cn-16_ma_convergence_breakout.pine`](cn-16_ma_convergence_breakout.pine)

```pinescript
//@version=5
strategy("MA Convergence Breakout (均线粘合突破)", overlay=true)
ma1 = ta.sma(close, 5)
ma2 = ta.sma(close, 10)
ma3 = ta.sma(close, 20)
ma4 = ta.sma(close, 60)
hiMa = math.max(ma1, math.max(ma2, math.max(ma3, ma4)))
loMa = math.min(ma1, math.min(ma2, math.min(ma3, ma4)))
spread = (hiMa - loMa) / close
glued = spread < 0.03
if glued and close > hiMa and volume > 1.5 * ta.sma(volume, 20)
strategy.entry("L", strategy.long)
atr = ta.atr(14)
if strategy.position_size > 0 and close < strategy.position_avg_price - 2 * atr
strategy.close("L", comment="Stop")
```

---

### CN-17 · N-Structure Tactics (N字战法)
*N字战法*

- **Origin & Lineage:** CN swing community canon (波段 literature, 2010s).
- **Core Hypothesis:** An N is the minimal trend unit — up-move, retracement holding above the prior low, then new high — and consecutive qualified Ns define the trend's health. The trade buys the breakout of the retracement's start-level after a qualifying retrace, with stops under the N's low. It is essentially a measured swing-continuation grammar, the CN retail mirror of Brooks' H1 logic (PA-05).
- **Execution Rules:** Detect impulse, retrace (0.38-0.618 or MA touch), trigger on close above retrace start; stop under retrace low; project next N.
- **Key Parameters:** Retrace bounds 0.38-0.618; volume contraction on retrace.
- **Duplicates Eliminated:** PA-05 Brooks H1/H2; flag patterns; 缠论笔结构 (CN-01) at coarser granularity.

---

### CN-18 · Rising Pullback System (上升回档)
*上升回档模式*

- **Origin & Lineage:** 经传软件 (JingChuan) teaching system; CN retail platform canon.
- **Core Hypothesis:** In an uptrend defined by a proprietary combination (e.g., 智能交易线 smart line + 操盘线), buy the pullback that touches the rising guide line with a reversal candle, sell into strength at the upper channel. The software packaged wave-riding into a two-line discipline that millions of CN retail users learned. Mechanically it is a Keltner-ish pullback (MR-04) with CN branding.
- **Execution Rules:** Trend = price above rising guide MA; buy on pullback touch + reversal; exit at upper band or trend-line break.
- **Key Parameters:** Guide MA 10-20; channel width 1.5-2 ATR.
- **Duplicates Eliminated:** MR-04 Keltner pullback; CN 波段王 (CN-20) overlap.

---

### CN-19 · Main-Force Accumulation Tracking (主力吸筹跟踪)
*主力吸筹战法*

- **Origin & Lineage:** 庄股-era analysis tradition (1990s-2000s); indicator canon (主力进出/吸筹 formulas).
- **Core Hypothesis:** Institutional accumulation leaves signatures: price resists falling on bad days, volume creeps up without price progress, large-order net inflows persist — reads formalized into CN indicators (主力吸筹, 大单净量). Systems screen for the signature cluster and position ahead of the markup phase. It is Wyckoff accumulation (PA-01) translated into CN order-flow proxies.
- **Execution Rules:** Screen: large-order net inflow positive N days + price flat/down + volatility contraction; enter on breakout of accumulation range.
- **Key Parameters:** Large-order threshold (10万+ tickets proxy); persistence 5-10 days.
- **Duplicates Eliminated:** PA-01/PA-02 Wyckoff; VO-03 CMF accumulation reads; CN-06 chip distribution confirmation.

---

### CN-20 · Swing Band System (波段操作 / 波段王)
*波段王*

- **Origin & Lineage:** CN retail platform canon (波段王 named systems across TDX-era software).
- **Core Hypothesis:** A two-line channel system: hold longs while price rides above a rising guide line inside the upper half of a 20/60 band, exit into the upper extreme, re-enter at mid-band pullbacks. It packages swing trading into visual band discipline for non-technical users. The mechanism is envelope-based swing riding (MR-04/BK-13 duality applied to swings).
- **Execution Rules:** Long from mid-band pullback while guide line rises; exit at upper band extreme or guide-line break.
- **Key Parameters:** Bands 20/60 (or 10/30 intraday); guide EMA 10.
- **Duplicates Eliminated:** MR-04/BK-13 Keltner forms; CN-18 rising pullback (same anatomy).

---

### CN-21 · Intraday T+0 Around Base Position (底仓做T)
*底仓做T策略*

- **Origin & Lineage:** A-share T+1 workaround culture; JoinQuant/uqer enhancement templates.
- **Core Hypothesis:** Holding a base position, each day the trader sells a portion on intraday strength and rebuys on weakness (or buys dips and sells into strength), ending flat-to-base daily — manufacturing T+0 economics inside a T+1 regime. Systematic forms trigger on VWAP deviation bands (VO-07) or opening-range logic with hard same-day round-trip discipline. It is the standard 'enhancement' overlay of CN-13.
- **Execution Rules:** Base position held; intraday: sell k% into +2 sigma strength or buy into -2 sigma weakness; restore base by close.
- **Key Parameters:** k 10-30% of base; sigma bands; skip on limit-up/down days.
- **Duplicates Eliminated:** VO-07/SE-08 intraday shells; CN-13 enhancement module.

---

### CN-22 · Call-Auction & Tail-Session Tactics (集合竞价/尾盘战法)
*集合竞价与尾盘战法*

- **Origin & Lineage:** A-share session microstructure practice; 打板 ecosystem components.
- **Core Hypothesis:** The 09:15-09:25 call auction reveals overnight order intent (竞价异动), and the 14:30-15:00 tail session reveals institutional commitment because T+1 sellers have finished — strategies read auction imbalance for gap plays and buy 尾盘 strength for next-day continuation, the classic 尾盘买入法. Both exploit session-boundary information asymmetry unique to CN trading hours.
- **Execution Rules:** Auction form: enter open on auction volume surge + gap in sentiment regime (CN-05 gate); tail form: buy last-30-min strength with closing push, exit next open/first strength.
- **Key Parameters:** Auction volume multiple; 尾盘 window 14:30-15:00; next-day exit discipline.
- **Duplicates Eliminated:** SE-03 open-momentum logic; CN-02 continuation boards.

---

### CN-23 · Calendar Spread Arbitrage (跨期套利)
*跨期套利*

- **Origin & Lineage:** JoinQuant canonical ten (myquant docs); CN futures desk practice (IF/IC era 2010s).
- **Core Hypothesis:** Trade the spread between contract months of the same underlying: the near-far spread mean-reverts around a cost-of-carry band, so fades at band extremes harvest mispricing while directional traders use spread momentum as a regime signal. Rebar/rebar and IF/IF spreads are the classic CN teaching cases. Pure statistical arbitrage at single-asset-family scale.
- **Execution Rules:** Model carry band; fade spread beyond +/-k sigma; hold to mean or carry rationalization; roll awareness.
- **Key Parameters:** Sigma 1.5-2.5; lookback 20-60 days; liquidity per leg.
- **Duplicates Eliminated:** ST-01/02 stat-arb machinery; CN-24/25 sibling arb forms.

---

### CN-24 · Cross-Commodity Spreads (跨品种套利)
*跨品种套利*

- **Origin & Lineage:** CN futures tradition (油粕比, 螺纹-热卷, 豆油-棕榈 pairs); myquant templates.
- **Core Hypothesis:** Related commodities keep process-driven ratios (soybean meal/soybean oil crush spread; rebar/hot-rolled coil mill spread); trade ratio deviations toward fundamental anchors with hedge sizing by beta. CN commodity desks treat these as the canonical 'industrial logic' arb — the spread's mean is explainable, not just historical.
- **Execution Rules:** Compute ratio (or dollar-neutral spread); trade beyond k-sigma with fundamental checkpoint (process margins extreme); exit at mean or margin reversion.
- **Key Parameters:** Ratio z-score window 60-120; hedge ratio by beta; margin-extreme confirmation.
- **Duplicates Eliminated:** ST-01 pairs (statistical form); RU Brent-Urals (RU-12) — same construct, different commodities.

---

### CN-25 · Futures-Cash Basis Arbitrage (期现套利)
*期现套利与ETF套利*

- **Origin & Lineage:** IF/IC launch 2010; ETF creation-basket arb practice; myquant templates.
- **Core Hypothesis:** When index futures premium exceeds carry + costs, short the future and buy the cash basket (ETF); the convergence at expiry locks the premium. Reverse-cash arbitrage was long blocked by shorting constraints, making CN basis arb structurally one-sided — a regulatory artifact documented in every CN derivatives textbook. The 2015 restrictions' discounts made the reverse trade briefly viable for hedged funds.
- **Execution Rules:** Monitor basis vs fair carry; execute basket-vs-future when premium > threshold; hold to convergence or unwind at reversion.
- **Key Parameters:** Threshold = carry + 2x costs; basket replication error; roll rules.
- **Duplicates Eliminated:** ST-16 roll yield (related mechanics); global index-arb literature.

---

### CN-26 · Valuation-Band Rotation (估值分位轮动)
*估值分位轮动策略*

- **Origin & Lineage:** 果仁网/且慢-era strategy canon; E大长赢体系 style percentile practice.
- **Core Hypothesis:** Rotate between equity and bond/cash using the index's historical PE/PB percentile: buy equities under the 30th percentile, scale out above the 70th, hold otherwise. It is the CN retail answer to valuation-timing research, popularized through ETF portfolios because it requires no individual-stock skill. The edge is cyclical patience, not prediction — and it is the most-used 'smart beta' discipline among CN long-term retail investors.
- **Execution Rules:** Compute 10-year PE/PB percentile of target index; scale equity weight in bands (e.g., 0-30%: full; 30-70%: half; 70-100%: defensive); rebalance quarterly.
- **Key Parameters:** Percentile windows 5-10 years; band thresholds; bond/cash leg choice.
- **Duplicates Eliminated:** CN-11 rotation (momentum flavor); global value-timing research; GR-04 smart DCA anchors.

---
