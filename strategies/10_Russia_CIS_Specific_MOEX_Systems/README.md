# Family RU: Russia/CIS-Specific Systems (MOEX & Si)

**Total Strategies in Family:** 16  
**Pine Script v5 Implementations:** 2  

## Strategies Overview

| ID | Strategy Name | Alternative Names | Has Pine Code |
|---|---|---|:---:|
| **RU-01** | [Elder's Triple Screen](#ru-01--elders_triple_screen) | Система «Три экрана» Элдера | ✅ Pine v5 |
| **RU-02** | [Ilan Family (RSI + CCI Martingale Advisors)](#ru-02--ilan_family_rsi_cci_martingale_advisors) | Советники «Илан» (RSI+CCI мартингейл) | ✅ Pine v5 |
| **RU-03** | [Sniper Method («Снайпер», Дмитриев / Байнов)](#ru-03--sniper_method) | Стратегия «Снайпер» | 📖 Logic-only |
| **RU-04** | [Elder SafeZone Stops & Elder Ray](#ru-04--elder_safezone_stops_elder_ray) | SafeZone-стопы и Elder Ray | 📖 Logic-only |
| **RU-05** | [Order-Book (Стакан) Scalping on MOEX Futures](#ru-05--order_book_scalping_on_moex_futures) | Стаканный скальпинг (фьючерсы МосБиржи) | 📖 Logic-only |
| **RU-06** | [Synthetic Bond Arbitrage («SyntheticBondsArbitrage»)](#ru-06--synthetic_bond_arbitrage_syntheticbondsarbitrage) | Синтетические облигации (арбитраж) | 📖 Logic-only |
| **RU-07** | [Dividend-Gap Trading (Дивидендный гэп)](#ru-07--dividend_gap_trading) | Стратегия дивидендного гэпа | 📖 Logic-only |
| **RU-08** | [Pairs Trading on MOEX Equities](#ru-08--pairs_trading_on_moex_equities) | Парный трейдинг на акциях МосБиржи | 📖 Logic-only |
| **RU-09** | [Morning Flat Breakout («Пробой утреннего флэта»)](#ru-09--morning_flat_breakout) | Пробой утреннего флэта | 📖 Logic-only |
| **RU-10** | [Russian Ichimoku Schools (Ишимоку-школы)](#ru-10--russian_ichimoku_schools) | Ишимоку: русские школы системы | 📖 Logic-only |
| **RU-11** | [Automated Fibonacci Level Robots](#ru-11--automated_fibonacci_level_robots) | Роботы по уровням Фибоначчи | 📖 Logic-only |
| **RU-12** | [Brent-Urals & Calendar Spread Trading (TSLab)](#ru-12--brent_urals_calendar_spread_trading_tslab) | Спред Брент-Юралс и календарные спреды | 📖 Logic-only |
| **RU-13** | [Book + Tape Hybrid (Стакан + Лента) Automation](#ru-13--book_tape_hybrid_automation) | Связка «стакан + лента» | 📖 Logic-only |
| **RU-14** | [Smart-Lab Community Trend Robots (Si/RTS)](#ru-14--smart_lab_community_trend_robots_sirts) | Трендовые роботы сообщества Smart-Lab | 📖 Logic-only |
| **RU-15** | [T-Bank Community Auto-Strategies (Tinkoff API era)](#ru-15--t_bank_community_auto_strategies_tinkoff_api_era) | Стратегии сообщества Т-Банк (Tinkoff API) | 📖 Logic-only |
| **RU-16** | [Academic Quant Lineage (ВШЭ / МФТИ factor studies)](#ru-16--academic_quant_lineage_factor_studies) | Академический квант-трек (ВШЭ, МФТИ) | 📖 Logic-only |

---

### RU-01 · Elder's Triple Screen
*Система «Три экрана» Элдера*

- **Origin & Lineage:** Alexander Elder (b. Leningrad), 1985 articles; Trading for a Living (1993).
- **Core Hypothesis:** Three timeframes in a fixed hierarchy: the weekly chart sets trend (screen 1), the daily oscillator times pullbacks against it (screen 2), and intraday triggers the entry (screen 3) — never fight the higher tide, buy the dip with the tide. Elder, a Russian-born New York psychiatrist, gave retail trading its most teachable multi-timeframe discipline, and no system is more universally cited in RU-language education.
- **Execution Rules:** Weekly trend up (EMA-26 rising) + weekly oscillator oversold + daily tick up: long; weekly trailing stop at 2 x ATR(13); short mirrored.
- **Key Parameters:** Weekly EMA 26; weekly stochastic 14; daily force index/RSI-2 trigger; stop 2 x ATR(13).
- **Duplicates Eliminated:** Countless RU/EN course versions; HTF-filter trend-pullback hybrids globally; SafeZone stops are Elder's exit companion (RU-04).

**Pine Script Reference Implementation:** [`ru-01_elders_triple_screen.pine`](ru-01_elders_triple_screen.pine)

```pinescript
//@version=5
strategy("Elder Triple Screen", overlay=true)
wkUp = request.security(syminfo.tickerid, "W",
ta.ema(close, 26) > ta.ema(close, 26)[1], lookahead=barmerge.lookahead_off)
wkStoch = request.security(syminfo.tickerid, "W",
ta.stoch(close, high, low, 14), lookahead=barmerge.lookahead_off)
dailyTrigger = ta.rsi(close, 2)
atr = ta.atr(13)
buySetup  = wkUp and wkStoch < 30 and dailyTrigger > nz(dailyTrigger[1]) and close > open
sellSetup = not wkUp and wkStoch > 70 and dailyTrigger < nz(dailyTrigger[1]) and close < open
if buySetup
strategy.entry("L", strategy.long)
if sellSetup
strategy.entry("S", strategy.short)
if strategy.position_size > 0
strategy.exit("LX", from_entry="L", stop=strategy.position_avg_price - 2 * atr)
if strategy.position_size < 0
strategy.exit("SX", from_entry="S", stop=strategy.position_avg_price + 2 * atr)
if strategy.position_size > 0 and wkStoch > 70
strategy.close("L", comment="Weekly OB")
if strategy.position_size < 0 and wkStoch < 30
strategy.close("S", comment="Weekly OS")
```

---

### RU-02 · Ilan Family (RSI + CCI Martingale Advisors)
*Советники «Илан» (RSI+CCI мартингейл)*

- **Origin & Lineage:** MT4-era RU forex forums (~2008-2010); Ilan 1.6 Dynamic the canonical build; Ilan 2.0 documented on MQL5 (RSI + CCI oscillators); 'Apocalypse' a known modification.
- **Core Hypothesis:** The most famous RU-language advisor lineage: enter on oscillator oversold (RSI + CCI confluence), then pyramid with multiplied lots at fixed adverse spacing until the basket recovers — GR-02's martingale geometry wrapped in an oscillator trigger. Its ubiquity made it the archetype teachers use to explain why martingales die, and its surviving forks all add equity stops. Documented as the RU contribution to retail automation history.
- **Execution Rules:** Long when RSI < buy level and CCI < -100; add size^k at each N-ATR adverse step (max steps); basket take-profit at breakeven + margin; hard equity stop.
- **Key Parameters:** RSI 14/30-level, CCI 14/-100; step ~30-50 pips original; multiplier 1.4-2.0; max 6-8 steps.
- **Duplicates Eliminated:** GR-02 martingale (the mechanism); 'Apocalypse' and every Ilan fork; CN 扛单 systems (same geometry).

**Pine Script Reference Implementation:** [`ru-02_ilan_family_rsi_cci_martingale_advisors.pine`](ru-02_ilan_family_rsi_cci_martingale_advisors.pine)

```pinescript
//@version=5
strategy("Ilan-style RSI+CCI Martingale (RISK DEMO)", overlay=false, pyramiding=8)
rsiL = input.int(14, "RSI length")
cciL = input.int(14, "CCI length")
buyLv = input.float(30, "RSI buy level")
stepAtr = input.float(1.0, "Spacing (ATR)")
sizeMult = input.float(1.4, "Lot multiplier")
r = ta.rsi(close, rsiL)
c = ta.cci(close, cciL)
atr = ta.atr(14)
if strategy.position_size == 0 and r < buyLv and c < -100
strategy.entry("I1", strategy.long, qty=1)
if strategy.position_size > 0 and close <= strategy.position_avg_price - stepAtr * atr and strategy.opentrades < 8
strategy.entry("I" + str.tostring(strategy.opentrades + 1), strategy.long,
qty=math.pow(sizeMult, strategy.opentrades))
if strategy.position_size > 0 and close >= strategy.position_avg_price + 0.3 * atr
strategy.close_all(comment="Basket TP")
```

---

### RU-03 · Sniper Method («Снайпер», Дмитриев / Байнов)
*Стратегия «Снайпер»*

- **Origin & Lineage:** Pavel Dmitriev, on the basis of Pyotr Baynov's «Мясо» system; RU forex portals (2010s).
- **Core Hypothesis:** A level-only scalping method (no indicators, no news): identify 'total' impulse levels on higher timeframes (M15/H1 relative to the M1/M5 working chart), then trade precise break or bounce of those levels with strict SL/TP arithmetic. Its branding emphasizes single-shot precision — one planned entry per level with predefined risk. It represents the RU school of level-geometry scalping, cousins of western supply/demand (PA-07) but with codified level hierarchy.
- **Execution Rules:** Mark impulse levels from higher-TF swings; on the working TF trade the touch: bounce form enters at the level with stop behind it, break form waits for a close-through with retest entry.
- **Key Parameters:** Level TF hierarchy M1/M5 working vs M15/H1 reference; stop beyond level; TP 1-2x stop.
- **Duplicates Eliminated:** PA-07 supply/demand zones; «Мясо» (parent system); RU Sniper X derivatives.

---

### RU-04 · Elder SafeZone Stops & Elder Ray
*SafeZone-стопы и Elder Ray*

- **Origin & Lineage:** Alexander Elder, Come Into My Trading Room (2002).
- **Core Hypothesis:** SafeZone computes stops from the average of recent adverse excursions multiplied by a coefficient, so stops sit just beyond normal noise rather than at arbitrary percentages; Elder Ray decomposes price into buying/selling power relative to a 13-day EMA to visualize bull/bear strength. Together they are Elder's answer to exit engineering, and RU/EN course materials treat them as a package with Triple Screen.
- **Execution Rules:** Stop = highest recent adverse-move average x coefficient (2.0-2.7) below price in longs, ratcheting; use Elder Ray extremes as exit confluence.
- **Key Parameters:** Lookback 10-22; coefficient 2.0-2.7; Elder Ray EMA 13.
- **Duplicates Eliminated:** Chandelier exit (TR-10) — same adaptive-stop family; ATR-trail systems.

---

### RU-05 · Order-Book (Стакан) Scalping on MOEX Futures
*Стаканный скальпинг (фьючерсы МосБиржи)*

- **Origin & Lineage:** MOEX derivatives market culture (2000s+); Smart-Lab scalping threads; proprietary desk lineage.
- **Core Hypothesis:** Si/RTS/Br futures scalpers read the DOM (стакан): large resting bids/offers, their pulls, and aggressive prints crossing the spread signal short-term direction; manual scalpers fade spoofed walls and join genuine absorption, while semi-automatic 'стакан+lenta' (book+tape) hybrids automate the read. It is the RU native order-flow school — footprint trading at the source rather than through proxies.
- **Execution Rules:** Read ladder: fade large one-sided walls that fail to trade; join sweeps that lift multiple levels; exit within seconds-to-minutes on tape slowdown.
- **Key Parameters:** DOM depth 5-20 levels; print-rate thresholds; latency budget < 10 ms for automation.
- **Duplicates Eliminated:** VO-09 CVD (Pine proxy of the same information); HFT spoofing-detection literature.

---

### RU-06 · Synthetic Bond Arbitrage («SyntheticBondsArbitrage»)
*Синтетические облигации (арбитраж)*

- **Origin & Lineage:** Smart-Lab.ru community (lectures and the SyntheticBondsArbitrage robot, 2010s-2020s).
- **Core Hypothesis:** Construct a 'synthetic bond' from a futures position plus a money-market leg (or from OFZ vs futures basis), harvesting the difference between implied financing in the futures basis and the actual deposit/REPO rate. Smart-Lab's robot lineage automates the roll-calendar and basis-monitoring logic. It is the MOEX version of the global cash-and-carry trade (CR-02's ancestor) adapted to Russian rate mechanics.
- **Execution Rules:** Monitor futures basis vs fair carry; long bond/short future (or reverse) when basis deviates beyond costs; roll calendar-aware.
- **Key Parameters:** Cost threshold; REPO rate benchmark; roll dates; margin efficiency.
- **Duplicates Eliminated:** ST-16 roll-yield; CR-02 cash-and-carry; RU-12 spread family.

---

### RU-07 · Dividend-Gap Trading (Дивидендный гэп)
*Стратегия дивидендного гэпа*

- **Origin & Lineage:** MOEX practice (2000s+); T-Bank/Smart-Lab community canon — a genuinely RU-specific institutional artifact.
- **Core Hypothesis:** MOEX equities drop by the declared dividend on the registry-close date, and the gap's refill speed varies with dividend yield, market phase, and tax regime: high-yield blue chips refill fastest. Classic plays: (a) 'cut the coupon' — hold through the gap only when taxes/fees make the dividend worthwhile; (b) gap-refill — buy the gap down, target the refill over days-to-weeks; (c) post-gap drift trades on refill statistics. The strategy's statistics are published annually in RU media because the pattern is structural to the exchange.
- **Execution Rules:** Build the registry calendar; measure gap size vs ATR; buy refill candidates (high yield, uptrend, index-heavy) at the gap open; target full or 50% refill; stop beyond 1.5x gap.
- **Key Parameters:** Yield screen > 6-8%; refill window 2-30 sessions; tax-aware holding period.
- **Duplicates Eliminated:** BK-10 gap playbook (general form); CN 分红除权 practices (structurally similar, different regime).

---

### RU-08 · Pairs Trading on MOEX Equities
*Парный трейдинг на акциях МосБиржи*

- **Origin & Lineage:** Gatev et al. (ST-01) mechanics adapted by the RU quant community (2010s Smart-Lab/TSLab threads).
- **Core Hypothesis:** Cointegration pairs of sector twins (Сбербанк ordinary vs preferred, Лукойл/Роснефть, Norilsk/Rusal proxies) with spread z-score entries; the RU specifics are fat-tailed event risk (sanctions, dividends) and ordinary-vs-preferred (ао-ап) pairs whose spread embeds governance discount. TSLab/StockSharp implementations handle the two-leg execution and hedge rebalancing.
- **Execution Rules:** Estimate hedge ratio (rolling OLS/Kalman); enter at z +/- 2; exit z = 0; hard stop z = 3.5 or fundamentals-break veto.
- **Key Parameters:** Estimation 250-500 days; z windows 20-60; event-veto list.
- **Duplicates Eliminated:** ST-01/ST-03 (the general mechanism); CN-24 cross-commodity analog.

---

### RU-09 · Morning Flat Breakout («Пробой утреннего флэта»)
*Пробой утреннего флэта*

- **Origin & Lineage:** RU forex/QUIK-era intraday canon (2000s); MOEX-hours adaptation of the London breakout.
- **Core Hypothesis:** The first hour of MOEX cash-equity trading (10:00-11:00 MSK) typically builds a flat; its break with momentum frequently drives the first leg of the day. The robotized form trades stop orders at the flat edges with tight invalidation. It is SE-02's mechanism on Moscow hours, kept as a separate entry because the community treats it as a distinct canon with its own statistics.
- **Execution Rules:** Range = 10:00-11:00 MSK extremes; enter on break during 11:00-14:00; stop at range midpoint; target 1-1.5x range.
- **Key Parameters:** Range window 60 min; skip news days; volume confirmation optional.
- **Duplicates Eliminated:** SE-02 London breakout (same mechanism); BK-01 ORB (session-open family).

---

### RU-10 · Russian Ichimoku Schools (Ишимоку-школы)
*Ишимоку: русские школы системы*

- **Origin & Lineage:** RU Ichimoku course tradition (2000s+, translators of Hosoda; dedicated RU portals).
- **Core Hypothesis:** The RU community institutionalized Ichimoku with its own conventions: mandatory chikou-span clearance rules, 'three pillars' trend grading by cloud color and Kijun slope, and conservative 'signal only when price is beyond BOTH spans' filters. The system traded is TR-11's, but the RU school's added discipline layers (entry only after cloud exit + pullback to Kijun) deserve separate documentation as the canonical CIS variant.
- **Execution Rules:** Trade only with cloud bias; entry on Kijun pullback with Tenkan cross; stop beyond the cloud edge; add on Chikou clearance confirmation.
- **Key Parameters:** 9/26/52 standard; RU schools often 120-period displacement variants on MOEX dailies.
- **Duplicates Eliminated:** TR-11 Ichimoku (the parent); RU/UA course forks.

---

### RU-11 · Automated Fibonacci Level Robots
*Роботы по уровням Фибоначчи*

- **Origin & Lineage:** MT4-era RU automation (2000s-2010s); MQL5 CodeBase corpus.
- **Core Hypothesis:** Automatically anchor Fibonacci retracements to the last significant zigzag swing and post limit orders at 38.2/50/61.8 with stops beyond 78.6 — the mechanization of the single most-taught manual tool in RU technical courses. Variants add trend filters (only trade retracements in trend direction) and cluster confluence with round numbers (PA-16).
- **Execution Rules:** Detect swing (zigzag); place limit grid at ratios; cancel on invalidation; trail after 61.8 retrace resumes the trend.
- **Key Parameters:** Zigzag 3-8%; ratio set; confluence tolerance 0.1 ATR.
- **Duplicates Eliminated:** GR-05 Fibonacci grid (the averaging form); RU-03 Sniper (level-logic cousin).

---

### RU-12 · Brent-Urals & Calendar Spread Trading (TSLab)
*Спред Брент-Юралс и календарные спреды*

- **Origin & Lineage:** TSLab/StockSharp community (2010s+); MOEX commodity-desk practice.
- **Core Hypothesis:** Trade structural spreads: Brent-Urals quality differential around its geopolitical band, and same-instrument calendar spreads around fair carry. The RU educational corpus treats spread trading as the 'calm' alternative to directional futures, with TSLab's visual builder as the standard implementation environment. Sizing is beta-hedged to the lead leg.
- **Execution Rules:** Model the spread band (carry for calendars, quality/logistics for Brent-Urals); fade band extremes; exit at mean or band rationalization.
- **Key Parameters:** Band lookback 60-250 days; hedge ratio; roll-calendar handling.
- **Duplicates Eliminated:** CN-24 cross-commodity spreads; ST-01/02 stat-arb; RU-06 synthetic bonds (rate-spread cousin).

---

### RU-13 · Book + Tape Hybrid (Стакан + Лента) Automation
*Связка «стакан + лента»*

- **Origin & Lineage:** QUIK Lua / StockSharp community scripts (2010s+); semi-HFT retail practice.
- **Core Hypothesis:** Automate the classic scalper's read: combine DOM imbalance (стакан) with trade-tape aggression (лента) — large prints at ask with thinning offers signal continuation; the bot posts immediate-or-cancel entries with hard tick stops. Latency, not signal, is the binding constraint, which caps its viability for retail — a fact the community documents candidly. Included as the RU-native bridge between manual scalping and HFT.
- **Execution Rules:** Compute DOM imbalance + tape aggression score; enter IOC on confluence; exit on tape reversal or tick stop.
- **Key Parameters:** Imbalance thresholds; tick stop 3-10 ticks; max holding seconds.
- **Duplicates Eliminated:** RU-05 (manual form); VO-09 (Pine proxy); HFT microstructure literature.

---

### RU-14 · Smart-Lab Community Trend Robots (Si/RTS)
*Трендовые роботы сообщества Smart-Lab*

- **Origin & Lineage:** Smart-Lab.ru blog corpus (2010s+); public robot threads and lecture series.
- **Core Hypothesis:** The community's workhorse trend systems on MOEX futures: Donchian/MA-channel entries with ATR stops and Si/RTS-specific filters (session windows, spread-point vol normalization, squeeze-of-the-day gates). Their published equity curves, parameter walks, and failure post-mortems form an unusually honest public archive. Representative rather than a single recipe — the family's contribution is the documentation culture itself.
- **Execution Rules:** Channel/MA trend entry; ATR stop; session filter (day session only); volatility-normalized sizing.
- **Key Parameters:** Entry 20-55 bars; ATR 2-3 x stop; per-contract risk caps.
- **Duplicates Eliminated:** TR-01/TR-02 (mechanism parents); RU-09 (session variant).

---

### RU-15 · T-Bank Community Auto-Strategies (Tinkoff API era)
*Стратегии сообщества Т-Банк (Tinkoff API)*

- **Origin & Lineage:** Tinkoff Investments open API (2018+); RU retail-bot community (github/ecosystem).
- **Core Hypothesis:** The open-broker API spawned a generation of retail bots: scheduled DCA with dip-boosts, threshold rebalancing, dividend-calendar loaders, and simple MA regime switches — all sharing the constraint of T+1 settlement and no shorting on the standard account. The family matters as the modern RU retail baseline, analogous to the US 'robo-advisor plus API' wave.
- **Execution Rules:** Regime gate (price vs 200-day MA) for contributions; DCA tranches; rebalance bands; dividend-date awareness.
- **Key Parameters:** Contribution schedule; regime MA 200; rebalance threshold 10-20%.
- **Duplicates Eliminated:** GR-04 DCA; GR-07 rebalancing (mechanisms); RU-07 dividend calendar integration.

---

### RU-16 · Academic Quant Lineage (ВШЭ / МФТИ factor studies)
*Академический квант-трек (ВШЭ, МФТИ)*

- **Origin & Lineage:** HSE/MIPT quant programs and preprints (2010s+); RU brokerage research desks.
- **Core Hypothesis:** The RU academic track replicates global factor zoo results on MOEX data: momentum's weakness, value's persistence, liquidity premia, and low-vol anomalies under sanctions-era market structure. Practical output is factor-screens and rotation models distributed via brokerage research. Included because 'thinktank and database' coverage of the RU space centers on this lineage rather than on retail blogs.
- **Execution Rules:** Replicate factor definitions (Fama-French/Barra analogs) on MOEX universe; rank by factor score; test with transaction costs and illiquidity caps.
- **Key Parameters:** Factor windows per paper; universe filters (free float, liquidity).
- **Duplicates Eliminated:** ST-04..ST-11 (the global canon it replicates); CN-15 (the CN counterpart lineage).

---
