# Family ST: Statistical, Factor & Arbitrage Systems

**Total Strategies in Family:** 18  
**Pine Script v5 Implementations:** 1  

## Strategies Overview

| ID | Strategy Name | Alternative Names | Has Pine Code |
|---|---|---|:---:|
| **ST-01** | [Pairs Trading (Distance Method)](#st-01--pairs_trading_distance_method) | 配对交易 · Парный трейдинг | 📖 Logic-only |
| **ST-02** | [Statistical Arbitrage (Avellaneda-Lee)](#st-02--statistical_arbitrage_avellaneda_lee) | 统计套利 · Стат-арб Авellaneda | 📖 Logic-only |
| **ST-03** | [Kalman-Filter Hedge Ratio (Dynamic Pairs)](#st-03--kalman_filter_hedge_ratio_dynamic_pairs) | 卡尔曼滤波对冲比率 · Фильтр Калмана в парах | 📖 Logic-only |
| **ST-04** | [Cross-Sectional Momentum (Jegadeesh-Titman)](#st-04--cross_sectional_momentum_jegadeesh_titman) | 横截面动量因子 · Кросс-секционный моментум | 📖 Logic-only |
| **ST-05** | [Value Factor (HML) & Value-Momentum Combination](#st-05--value_factor_hml_value_momentum_combination) | 价值因子与价值动量组合 · Фактор стоимости | 📖 Logic-only |
| **ST-06** | [FX Carry Trade](#st-06--fx_carry_trade) | 利差交易 · Керри-трейд | 📖 Logic-only |
| **ST-07** | [Low-Volatility Anomaly](#st-07--low_volatility_anomaly) | 低波动异象 · Аномалия низкой волатильности | 📖 Logic-only |
| **ST-08** | [Betting Against Beta (BAB)](#st-08--betting_against_beta_bab) | 贝塔对冲因子 · Betting Against Beta | 📖 Logic-only |
| **ST-09** | [Quality / Profitability Factor (QMJ)](#st-09--quality_profitability_factor_qmj) | 质量因子 · Фактор качества | 📖 Logic-only |
| **ST-10** | [WorldQuant 101 Formulaic Alphas](#st-10--worldquant_101_formulaic_alphas) | WorldQuant 101 Alpha库 | ✅ Pine v5 |
| **ST-11** | [The Factor Zoo & Multiple-Testing Corrections](#st-11--the_factor_zoo_multiple_testing_corrections) | 因子动物园与多重检验校正 · Факторный зоопарк | 📖 Logic-only |
| **ST-12** | [COT Positioning Strategies](#st-12--cot_positioning_strategies) | CFTC持仓报告策略 · Стратегии по COT | 📖 Logic-only |
| **ST-13** | [Dispersion Trading (Index vs Constituents)](#st-13--dispersion_trading_index_vs_constituents) | 离散度交易 · Дисперсионный трейдинг | 📖 Logic-only |
| **ST-14** | [Volatility Risk Premium Harvesting](#st-14--volatility_risk_premium_harvesting) | 波动率风险溢价收割 · Сбор премии за волатильность | 📖 Logic-only |
| **ST-15** | [Gamma Scalping (Long-Gamma Rebalancing)](#st-15--gamma_scalping_long_gamma_rebalancing) | Гамма-скальпинг | 📖 Logic-only |
| **ST-16** | [Commodity Roll Yield / Contango Harvest](#st-16--commodity_roll_yield_contango_harvest) | 商品展期收益 · Ролл-доходность | 📖 Logic-only |
| **ST-17** | [Risk Parity & Volatility Targeting](#st-17--risk_parity_volatility_targeting) | 风险平价与波动率目标 · Паритет риска | 📖 Logic-only |
| **ST-18** | [Commodity Seasonality](#st-18--commodity_seasonality) | 商品季节性策略 · Сезонность сырья | 📖 Logic-only |

---

### ST-01 · Pairs Trading (Distance Method)
*配对交易 · Парный трейдинг*

- **Origin & Lineage:** Gatev, Goetzmann & Rouwenhorst, working paper 1999 / RFS 2006.
- **Core Hypothesis:** Find historically co-moving pairs, trade their normalized spread at +/-2 sigma, exit at convergence — market-neutral by construction. The paper's 1962-1996 US data showed mid-single-digit annual Sharpe-healthy returns; later replication shows decayed but persistent edges, concentrated in less-efficient markets. It is the parent of every stat-arb simplification including CN-24 and RU-08.
- **Execution Rules:** Form pairs on 12-month normalized distance; trade beyond 2 sigma; exit at zero crossing or 6-month time stop; stop-loss at 3+ sigma.
- **Key Parameters:** Formation 12 months; trading 6 months; sigma bands 2.0/0; universe liquidity filter.
- **Duplicates Eliminated:** RU-08 MOEX pairs; CN-24 commodity spreads; RU «парный трейдинг» community (mechanism identical).

---

### ST-02 · Statistical Arbitrage (Avellaneda-Lee)
*统计套利 · Стат-арб Авellaneda*

- **Origin & Lineage:** Marco Avellaneda & Jeong-Hyun Lee, 'Statistical Arbitrage in the US Equities Market', Quantitative Finance 2010.
- **Core Hypothesis:** Decompose stock returns into a statistical risk model (PCA factors) plus residual; trade mean-reversion of residual idiosyncratic returns whose speed-of-mean-reversion (Ornstein-Uhlenbeck) is fast enough to clear costs. The paper formalized how much of the classic pairs edge lives in the residual, and provided the OU half-life screen that practitioners still use as the go/no-go gate.
- **Execution Rules:** Estimate factor model; compute residual OU parameters; trade residuals with half-life < 20 days at +/-2 sigma; exit at mean.
- **Key Parameters:** PCA 10-15 factors; half-life cap 15-25 days; band 1.5-2.5 sigma.
- **Duplicates Eliminated:** ST-01 (simplified ancestor); institutional stat-desk literature.

---

### ST-03 · Kalman-Filter Hedge Ratio (Dynamic Pairs)
*卡尔曼滤波对冲比率 · Фильтр Калмана в парах*

- **Origin & Lineage:** Signal-processing adaptation popularized in quant blogs (2010s, e.g., QuantStart lineage).
- **Core Hypothesis:** Instead of a static OLS hedge ratio, a Kalman filter treats the ratio as a hidden state evolving with noise, adapting intra-sample as the relationship drifts — materially reducing spread blowups from ratio drift. The filter's innovation variance doubles as a regime alarm. It is the standard upgrade path for ST-01 implementations.
- **Execution Rules:** State = [alpha, beta] evolving as random walk; observation = pair prices; enter on standardized innovation bands; exit at mean.
- **Key Parameters:** Process noise 1e-5..1e-3; observation noise from residuals; band 2 sigma of innovation.
- **Duplicates Eliminated:** ST-01/02 implementations; RU Kalman-пары threads.

---

### ST-04 · Cross-Sectional Momentum (Jegadeesh-Titman)
*横截面动量因子 · Кросс-секционный моментум*

- **Origin & Lineage:** Narasimhan Jegadeesh & Sheridan Titman, Journal of Finance 1993.
- **Core Hypothesis:** Rank stocks by trailing 3-12 month returns, long the top decile short the bottom, skip the most recent month; winners outperform for 3-12 months. The most replicated anomaly in finance, present in nearly every market studied (with the notable CN exception where reversal historically dominated). It powers CN-12 sector rotation and TR-17's time-series cousin.
- **Execution Rules:** Rank by 12-1 month return; long top decile (or quintile), monthly rebalance; optional industry/size neutralization.
- **Key Parameters:** Lookback 3-12 months; skip 1 month; decile portfolios.
- **Duplicates Eliminated:** CN-12/CN-15 (CN implementations); TR-17 TSMOM (time-series form); RU-16 (MOEX replication).

---

### ST-05 · Value Factor (HML) & Value-Momentum Combination
*价值因子与价值动量组合 · Фактор стоимости*

- **Origin & Lineage:** Fama & French 1992/1993; Asness, Moskowitz & Pedersen 'Value and Momentum Everywhere', JF 2013.
- **Core Hypothesis:** Long cheap (book/price, earnings/price) short expensive within industries; Asness et al. showed value and momentum are negatively correlated across every asset class, making their 50/50 combination the classic diversification machine. The CN twist is that value worked better than momentum historically on A-shares, driving CN-26's valuation-band popularity.
- **Execution Rules:** Rank by composite value metrics; long cheap decile (optionally short rich); rebalance annually/quarterly; combine with momentum 50/50.
- **Key Parameters:** B/M or E/B ranks; industry-neutral form; rebalance 1-12 months.
- **Duplicates Eliminated:** CN-26 (valuation timing); ST-09 quality-value hybrids; global smart-beta products.

---

### ST-06 · FX Carry Trade
*利差交易 · Керри-трейд*

- **Origin & Lineage:** Documented since the 1990s (BIS literature); Koijen, Moskowitz, Pedersen & Vrugt 'Carry', JFE 2018 formalized it everywhere.
- **Core Hypothesis:** Borrow low-yield currencies to buy high-yield ones, harvesting the forward-premium mispricing; returns are negatively skewed — years of grinding gains punctuated by violent unwinds. Systematic forms diversify across G10 pairs and add vol/regime filters. Carry also appears inside commodities and equities (roll yield, ST-16), making it the second universal factor.
- **Execution Rules:** Rank G10 by interest differential; long top, short bottom, vol-targeted; crash filter (momentum/vol gates) optional.
- **Key Parameters:** 3-month differentials; vol target 10%; pair diversification.
- **Duplicates Eliminated:** CR-01 crypto funding carry (the perp analog); ST-16 commodity carry.

---

### ST-07 · Low-Volatility Anomaly
*低波动异象 · Аномалия низкой волатильности*

- **Origin & Lineage:** Baker, Bradley & Wurgler, 'Benchmarks as Limits to Arbitrage', JFQA 2011 (building on Ang et al. 2006).
- **Core Hypothesis:** Low-beta/low-volatility stocks deliver higher risk-adjusted returns than the market — attributed to leverage constraints and benchmark-chasing incentives. Systematic forms long the lowest-vol quintile (optionally hedged), or tilt portfolios toward min-variance constructions. The anomaly is institutional-proof because it cannot be levered easily by benchmarked managers.
- **Execution Rules:** Rank by trailing 12-month vol; long bottom quintile; rebalance monthly/quarterly; optionally short the high-vol tail.
- **Key Parameters:** Vol window 1-3 years; quintiles; quality screens to avoid value traps.
- **Duplicates Eliminated:** ST-08 BAB (leverage-neutrality framing); min-variance portfolios; RU-16 replication.

---

### ST-08 · Betting Against Beta (BAB)
*贝塔对冲因子 · Betting Against Beta*

- **Origin & Lineage:** Andrea Frazzini & Lasse Pedersen, 'Betting Against Beta', JFE 2014 (AQR).
- **Core Hypothesis:** Lever the low-beta half of stocks to beta-1, short the levered high-beta half to beta-1 — a market-neutral bet that high-beta assets underperform risk-adjusted. The construction isolates the anomaly that low-vol research described, with funding costs made explicit. It became the institutional vehicle for the constraint-based explanation of the low-vol puzzle.
- **Execution Rules:** Compute betas; construct two beta-1 portfolios; long-levered-low-beta minus short-levered-high-beta; rebalance with borrow-cost awareness.
- **Key Parameters:** Beta window 1-5 years; leverage via futures/financing; quarterly rebalance.
- **Duplicates Eliminated:** ST-07 (the unlevered view); global smart-beta funds.

---

### ST-09 · Quality / Profitability Factor (QMJ)
*质量因子 · Фактор качества*

- **Origin & Lineage:** Robert Novy-Marx, 'The Other Side of Value: The Gross Profitability Premium', JFE 2013; Asness-Frazzini-Pedersen QMJ.
- **Core Hypothesis:** Profitable firms (gross profit/assets) outperform regardless of valuation; QMJ blends profitability, growth, and safety into the institutional quality factor. It anchors the quality-minus-junk framing used across CN 券商 factor reports and global fund marketing alike. As a system: long quality decile, optionally short junk, or use quality as a screen over other strategies.
- **Execution Rules:** Rank by gross profitability (and growth/safety in QMJ); long top decile; annual rebalance; combine with value for the classic quality-value pairing.
- **Key Parameters:** GP/A primary; industry neutralization; rebalance 1-4 quarters.
- **Duplicates Eliminated:** ST-05 (value pairing); Piotroski F-Score screens (cousin); CN-15 factor suite.

---

### ST-10 · WorldQuant 101 Formulaic Alphas
*WorldQuant 101 Alpha库*

- **Origin & Lineage:** Zura Kakushadze, '101 Formulaic Alphas', arXiv:1601.00991 (2015); SSRN 2701346.
- **Core Hypothesis:** One hundred one explicit alpha formulas (ranks, time-series operators, price-volume constructs) that are simultaneously specification and code — published precisely to seed the crowd. The archive became the de-facto syllabus for CN quant education (DolphinDB implementations, WorldQuant BRAIN platform community) and the template for expression-based alpha mining. Individual alphas are weak; the corpus teaches construction grammar.
- **Execution Rules:** Example Alpha#1: rank(Ts_ArgMax(signedPower(returns < 0 ? stddev(returns,20) : close, 2), 5)) - 0.5 — long when the recent max of the conditional quantity happened early (positive alpha proxy).
- **Key Parameters:** Per-alpha windows (5-20 days); cross-sectional rank requires a universe screener — single-symbol Pine proxies are documented as approximations.
- **Duplicates Eliminated:** CN-15 (the CN platform implementations); BRAIN community alphas; DolphinDB 101-alpha ports.

**Pine Script Reference Implementation:** [`st-10_worldquant_101_formulaic_alphas.pine`](st-10_worldquant_101_formulaic_alphas.pine)

```pinescript
//@version=5
indicator("WorldQuant Alpha #1 (single-symbol proxy)", overlay=false)
ret = ta.roc(close, 1) / 100
sd = ta.stdev(ret, 20)
src = ret < 0 ? sd : close
// Ts_ArgMax over 5 bars of src^2: highestbars returns negative offset
argIdx = ta.highestbars(math.pow(src, 2), 5)
rankProxy = -argIdx / 5.0
alpha = rankProxy - 0.5
plot(alpha, "Alpha #1 proxy", color=alpha > 0 ? color.teal : color.red)
hline(0)
```

---

### ST-11 · The Factor Zoo & Multiple-Testing Corrections
*因子动物园与多重检验校正 · Факторный зоопарк*

- **Origin & Lineage:** Harvey, Liu & Zhu, '...and the Cross-Section of Expected Returns', RFS 2016 (316 published factors); Green, Hand & Zhang 2017 (103 characteristics).
- **Core Hypothesis:** Hundreds of published return-predictors are catalogued, but multiple testing means a t-stat of 2.0 is meaningless at this scale — Harvey et al. recommend 3.0+ hurdles and document that most post-publication alpha decays. The 'factor' is thus itself a meta-strategy: demand higher bars, weight economic rationale, and expect decay. Every serious factor effort (CN-15, RU-16, BRAIN) now cites this work as hygiene.
- **Execution Rules:** Screen candidate factors by t > 3.0, out-of-sample persistence, and economic mechanism; monitor post-publication decay; penalize correlated duplicates.
- **Key Parameters:** t-hurdle 3.0; Bonferroni/BHA corrections; decay monitoring.
- **Duplicates Eliminated:** ST-04..10 (the zoo's residents); CN-15/RU-16 (regional replications).

---

### ST-12 · COT Positioning Strategies
*CFTC持仓报告策略 · Стратегии по COT*

- **Origin & Lineage:** CFTC Commitments of Traders reports (1962+ public data); Stephen Briese's commercialization (1990s); academic tests mixed.
- **Core Hypothesis:** Weekly positioning of commercials vs large specs encodes hedger conviction: extremes in speculator net-long (percentile-based) historically precede corrective phases in commodities. Systems fade positioning extremes or use them as filters for trend entries. Signal quality is regime-dependent and slow — it is a context factor more than a timing system.
- **Execution Rules:** Compute net-position percentiles (26-week window); fade spec extremes > 90th/< 10th percentile with trend confirmation.
- **Key Parameters:** Percentile windows; report lag handling (Tuesday data, Friday release).
- **Duplicates Eliminated:** Positioning analytics vendors; RU «отчёты COT» study groups; crypto COT-era analogs (BTC futures).

---

### ST-13 · Dispersion Trading (Index vs Constituents)
*离散度交易 · Дисперсионный трейдинг*

- **Origin & Lineage:** European options-desk practice (late 1990s); academic formalization 2000s.
- **Core Hypothesis:** Index implied volatility systematically exceeds the average of constituent vols (correlation premium); short index options and long a basket of constituent options harvests the premium when realized correlation disappoints. It is correlation trading — the payout depends on realized vs implied correlation, not direction. Executable via variance swaps in modern markets.
- **Execution Rules:** Short index straddles/variants; long constituent straddles in vol-weighted amounts; delta-hedge; unwind at correlation normalization.
- **Key Parameters:** Basket size 20-50 names; correlation window 60-250 days; vega neutrality.
- **Duplicates Eliminated:** VRP (ST-14) at index level; dispersion desks' literature.

---

### ST-14 · Volatility Risk Premium Harvesting
*波动率风险溢价收割 · Сбор премии за волатильность*

- **Origin & Lineage:** Documented across 1990s-2000s academic literature (Carr & Wu 2009 formalization); VIX-futures products industrialized it.
- **Core Hypothesis:** Implied vol systematically exceeds subsequent realized vol — sellers of insurance collect the premium; systematic short-vol (short VIX futures, put-selling with hedges) harvests it while carrying crash exposure. The February 2018 'Volmageddon' demonstrated the tail: levered short-vol ETPs died in a day. Modern implementations size by VRP estimate and cap leverage structurally.
- **Execution Rules:** Estimate VRP = implied - realized forecast; short vol when VRP > threshold with defined-risk structures; de-risk before events and after vol spikes.
- **Key Parameters:** VRP estimate windows; defined-risk structures only; leverage caps.
- **Duplicates Eliminated:** ST-13 (correlation cousin); SE-07 (event-calendar de-risking).

---

### ST-15 · Gamma Scalping (Long-Gamma Rebalancing)
*Гамма-скальпинг*

- **Origin & Lineage:** Options-desk canon (1980s+); formalized in dynamic-hedging literature (Taleb 1997).
- **Core Hypothesis:** Own options and delta-hedge continuously: each rebalance sells high/buys low, converting realized volatility into P&L at the cost of theta; profitable exactly when realized vol exceeds implied. It is the long side of ST-14 and the mechanism through which dealer hedging propagates volatility (the 2018/2024 vol events). Not Pine-implementable (needs options chain), so logic-only.
- **Execution Rules:** Long straddle/strangle; hedge delta to neutral at threshold crossings; monitor gamma-P&L vs theta bleed.
- **Key Parameters:** Hedge threshold 0.1-0.2 delta; expiry choice by expected event calendar; position vega budget.
- **Duplicates Eliminated:** ST-14 (the short side); dealer-flow research notes.

---

### ST-16 · Commodity Roll Yield / Contango Harvest
*商品展期收益 · Ролл-доходность*

- **Origin & Lineage:** Gorton & Rouwenhorst, 'Facts and Fantasies about Commodity Futures', JF 2006; ETF-era lessons (2006-2015).
- **Core Hypothesis:** Futures curve shape (contango/backwardation) systematically transfers wealth between contract holders; long-in-backwardation/short-in-contango baskets harvest roll yield as a systematic return stream independent of spot direction. The 2000s commodity-ETF era's UIPath-style losses in contango (UNG) are the cautionary archive. It is carry (ST-06) in commodity form.
- **Execution Rules:** Rank commodity futures by roll yield (near-far spread annualized); long the most backwardated, short the most contangoed; roll monthly.
- **Key Parameters:** Roll yield window; basket diversification 10+ commodities; contract liquidity filter.
- **Duplicates Eliminated:** ST-06 carry; RU-06 synthetic bonds (financing-rate analog); CN-25 basis arb.

---

### ST-17 · Risk Parity & Volatility Targeting
*风险平价与波动率目标 · Паритет риска*

- **Origin & Lineage:** Bridgewater's All Weather (1990s, Ray Dalio); Qian (2005) formalization; academic treatment 2010s.
- **Core Hypothesis:** Allocate so each asset class contributes equal risk rather than equal capital, leveraging the low-vol assets (bonds) to match equity risk; volatility targeting then scales total exposure inversely to realized vol. The 2022 bond-equity joint selloff exposed the regime-dependence of the correlations underneath. It is portfolio construction rather than signal — but it is the standard shell for factor portfolios.
- **Execution Rules:** Estimate covariance; solve equal-risk-contribution weights; leverage to target vol; rebalance quarterly or on drift.
- **Key Parameters:** Target vol 8-12%; lookback 1-3 years; leverage/financing costs.
- **Duplicates Eliminated:** ST-07/08 (risk-based tilts); GR-07 rebalancing (the retail cousin).

---

### ST-18 · Commodity Seasonality
*商品季节性策略 · Сезонность сырья*

- **Origin & Lineage:** Decades of CTA practice; academic seasoning via seasonality papers (2000s-2010s).
- **Core Hypothesis:** Physical cycles (planting/harvest, heating season, OPEC logistics) create repeatable monthly drift patterns per commodity — e.g., heating oil strength into winter, gasoline into driving season. Systems long the statistically favorable months per contract with position sizing by pattern stability. The edges are small but persist because the physical driver persists.
- **Execution Rules:** Compute per-contract monthly return history; long months with stable positive historical drift; size by consistency score.
- **Key Parameters:** History 15-30 years; consistency thresholds; roll handling.
- **Duplicates Eliminated:** SE-05/06 (equity seasonality); RU grain-market seasonal notes; CN 农产品季节性 studies.

---
