# Family SE: Session, Time & Calendar Edges

**Total Strategies in Family:** 9  
**Pine Script v5 Implementations:** 1  

## Strategies Overview

| ID | Strategy Name | Alternative Names | Has Pine Code |
|---|---|---|:---:|
| **SE-01** | [Asia Range Sweep & London Reversal](#se-01--asia_range_sweep_london_reversal) | 亚洲区间扫荡 · Съём азиатского диапазона | 📖 Logic-only |
| **SE-02** | [London Breakout («Лондонский взрыв»)](#se-02--london_breakout) | 伦敦突破 · Лондонский взрыв | ✅ Pine v5 |
| **SE-03** | [NY Open Momentum (10:00 Rule)](#se-03--ny_open_momentum_1000_rule) | 纽约开盘动量 · Моментум открытия Нью-Йорка | 📖 Logic-only |
| **SE-04** | [Overnight vs Intraday Edge (Tug of War)](#se-04--overnight_vs_intraday_edge_tug_of_war) | 隔夜与日内收益差 · Овернайт-эффект | 📖 Logic-only |
| **SE-05** | [Turn-of-Month / Turn-of-Quarter Effect](#se-05--turn_of_month_turn_of_quarter_effect) | 月末效应 · Эффект конца месяца | 📖 Logic-only |
| **SE-06** | [Sell in May / Halloween Indicator](#se-06--sell_in_may_halloween_indicator) | 五月卖出效应 · Эффект 'Продавай в мае' | 📖 Logic-only |
| **SE-07** | [Pre-FOMC Announcement Drift](#se-07--pre_fomc_announcement_drift) | 美联储议息前漂移 · Пре-FOMC дрифт | 📖 Logic-only |
| **SE-08** | [Hour-of-Day Volatility Breakout](#se-08--hour_of_day_volatility_breakout) | 时段波动突破 · Внутричасовой пробой | 📖 Logic-only |
| **SE-09** | [Crypto Weekend & Funding Window Effects](#se-09--crypto_weekend_funding_window_effects) | 加密周末与资金费率窗口 · Крипто-сезонность | 📖 Logic-only |

---

### SE-01 · Asia Range Sweep & London Reversal
*亚洲区间扫荡 · Съём азиатского диапазона*

- **Origin & Lineage:** Forex session-structure practice (1990s-2000s desks); formalized in ICT materials (PA-09).
- **Core Hypothesis:** The Asian session builds a tight range of resting liquidity; London's first hours typically sweep one side of it before the real move — the sweep is entry fuel, not trend. Systems fade the sweep back through the range or trade the post-sweep continuation with the range midpoint as the discriminator. The mechanism is pure stop-cluster engineering on session boundaries.
- **Execution Rules:** Mark Asia range (00:00-07:00 UTC); on London open, fade a sweep of the range edge that fails within 2 bars; target range mid/other edge.
- **Key Parameters:** Asia window 00:00-07:00 UTC; failure window 15-30 min; midpoint discriminator.
- **Duplicates Eliminated:** ICT Judas swing (PA-09); RU «съём лоув/хай Азии» scripts; CN 亚盘区间策略.

---

### SE-02 · London Breakout («Лондонский взрыв»)
*伦敦突破 · Лондонский взрыв*

- **Origin & Lineage:** Classic forex strategy codified in Russian forums (2000s) and British prop-desk practice; one of the most-robotized session systems.
- **Core Hypothesis:** The Asia range defines the day's expected expansion; trade the break of its edges during the London window with stop at the opposite edge and target of one range height. Its Russian nickname 'London explosion' reflects its 2000s-era popularity on RU forex portals, and it remains the reference session-breakout template. Higher failure rates on quiet Mondays and news Fridays are standard caveats.
- **Execution Rules:** Range = Asia session high/low; enter on first close outside during 07:00-10:00 UTC; stop at range midpoint, target 1x range.
- **Key Parameters:** Asia 00:00-07:00; trade 07:00-10:00 UTC; TP/SL = 1x/0.5x range.
- **Duplicates Eliminated:** RU «Пробой утреннего флэта» (RU-09, same mechanism on MOEX hours); CN 伦敦突破; every MT4 London-bot.

**Pine Script Reference Implementation:** [`se-02_london_breakout.pine`](se-02_london_breakout.pine)

```pinescript
//@version=5
strategy("London Breakout (Asia Range)", overlay=true)
asiaSess = input.session("0000-0700", "Asia range")
tz       = input.string("UTC", "Timezone")
inAsia  = not na(time(timeframe.period, asiaSess, tz))
var float aHi = na
var float aLo = na
if inAsia
aHi := na(aHi) ? high : math.max(aHi, high)
aLo := na(aLo) ? low  : math.min(aLo, low)
var bool tradedToday = false
newDay = ta.change(time("D")) != 0
if newDay
tradedToday := false
canTrade = not inAsia and not tradedToday and not na(aHi)
if canTrade and close > aHi
strategy.entry("L", strategy.long)
tradedToday := true
if canTrade and close < aLo
strategy.entry("S", strategy.short)
tradedToday := true
rng = aHi - aLo
if strategy.position_size > 0
strategy.exit("LX", from_entry="L", stop=aLo, limit=aHi + rng)
if strategy.position_size < 0
strategy.exit("SX", from_entry="S", stop=aHi, limit=aLo - rng)
plot(inAsia ? aHi : na, "Asia High", color=color.teal, style=plot.style_linebr)
plot(inAsia ? aLo : na, "Asia Low", color=color.red, style=plot.style_linebr)
```

---

### SE-03 · NY Open Momentum (10:00 Rule)
*纽约开盘动量 · Моментум открытия Нью-Йорка*

- **Origin & Lineage:** US equity intraday desk lore (1990s-2000s); quantified in the overnight/intraday literature (Lou-Polk-Skouras, 2019).
- **Core Hypothesis:** The first 90 minutes of NY hours carry disproportionate volume and price discovery; the direction established by 10:00 with confirmation holds disproportionately often to the close. The systematic form enters with the 10:00 direction when the open range and VWAP side agree. On reversal days the failure itself is informative — hence the strict invalidation rules.
- **Execution Rules:** At 10:00 ET, take the direction of the open range side if price and VWAP agree; stop at open range mid; exit 15:45 ET.
- **Key Parameters:** Open range 09:30-10:00; VWAP confluence; time-stop EOD.
- **Duplicates Eliminated:** IB/ORB variants (BK-01); CN 美股开盘策略; RU «Нью-Йорк открытие» bots.

---

### SE-04 · Overnight vs Intraday Edge (Tug of War)
*隔夜与日内收益差 · Овернайт-эффект*

- **Origin & Lineage:** Lou, Polk & Skouras, 'A Tug of War: Overnight Versus Intraday Expected Returns', JFE 2019.
- **Core Hypothesis:** US equity returns have accrued almost entirely overnight for decades while intraday returns favor momentum names — a structural split linked to who trades when (retail vs institutional windows). The systematic form holds positions only overnight in night-favoring names and only intraday in day-favoring ones. Pine can express the timing shell, though multi-asset ranking needs a screener.
- **Execution Rules:** Classify asset by historical overnight vs intraday mean dominance; hold overnight-only for night-winners (buy close, sell open), intraday-only for day-winners.
- **Key Parameters:** Estimation window 1-3 years; rebalance monthly; borrow/fee awareness essential.
- **Duplicates Eliminated:** Buy-the-close-sell-the-open papers; CN 隔夜效应研究; RU овернайт-стратегии on SPB panel.

---

### SE-05 · Turn-of-Month / Turn-of-Quarter Effect
*月末效应 · Эффект конца месяца*

- **Origin & Lineage:** Ariel (1987), Lakonishok & Smidt (1988) documentation; institutional cash-flow timing as the driver.
- **Core Hypothesis:** Equity returns concentrate in the last trading day(s) and first 3-4 days of the month, attributed to institutional funding cycles, 401k/pension inflows, and index rebalancing. The systematic form is long-only across the turn-of-month window and flat or hedged otherwise. It is among the most persistent calendar anomalies documented across markets.
- **Execution Rules:** Enter long at T-1 of month end; exit at T+3; optionally hedge (index short) outside the window.
- **Key Parameters:** Window T-1..T+3; skip months with major scheduled shocks (per user risk policy).
- **Duplicates Eliminated:** TOQ/TOY variants; CN 月末效应研究; RU месячные окна стратегии.

---

### SE-06 · Sell in May / Halloween Indicator
*五月卖出效应 · Эффект 'Продавай в мае'*

- **Origin & Lineage:** Bouman & Jacobsen, 'The Halloween Indicator, Sell in May and Go Away', American Economic Review 2002.
- **Core Hypothesis:** November-April historically outperforms May-October across many markets for decades; Bouman-Jacobsen verified the effect in 37 countries and tied it loosely to vacation-liquidity seasons. As a system it is a binary annual regime gate — hold risk assets November-April, rotate to defensives or cash otherwise. Best treated as a tilt, not a standalone edge.
- **Execution Rules:** Long risk assets Nov 1 - Apr 30; rotate to cash/bonds/defensive sectors May-Oct.
- **Key Parameters:** Hemisphere-adjusted variant; combine with momentum for robustness.
- **Duplicates Eliminated:** Seasonal rotation ETF strategies; CN 五穷六绝七翻身 folklore systematized; RU сезонность studies.

---

### SE-07 · Pre-FOMC Announcement Drift
*美联储议息前漂移 · Пре-FOMC дрифт*

- **Origin & Lineage:** Lucca & Moench, NY Fed Staff Report 2011 / Journal of Finance 2015.
- **Core Hypothesis:** US equities exhibit a large, statistically robust drift upward in the hours before scheduled FOMC announcements — documented since 1980 across 100+ meetings — interpreted as pre-announcement risk-premium compensation. The systematic form is long the index from the morning of announcement day (or 2 hours pre-release) and flat after the release. One of the cleanest central-bank calendar effects ever documented.
- **Execution Rules:** Long SPX/ES from 10:00-14:00 ET window before the 14:00 statement; exit at release or shortly after; skip unscheduled/emergency meetings.
- **Key Parameters:** FOMC calendar; entry window per the paper; skip days with concurrent major data.
- **Duplicates Eliminated:** ECB/pre-announcement drift follow-up studies; CN 美联储会议策略; RU пред-FOMC стратегии.

---

### SE-08 · Hour-of-Day Volatility Breakout
*时段波动突破 · Внутричасовой пробой*

- **Origin & Lineage:** Intraday seasonality of volume/volatility (Admati-Pfleiderer 1988; Wood-McInish-Ord 1985).
- **Core Hypothesis:** Volatility clusters at session open/close and lunch lulls elsewhere; systems trade breakouts only during high-energy windows (first/last 90 minutes) and trade range-fades during the midday lull. The insight is that the same breakout signal has different expectancy by clock hour, so the calendar acts as a signal multiplier.
- **Execution Rules:** Enable breakout logic in 09:30-11:00 and 14:30-16:00 windows; switch to band-fade logic 11:30-14:00.
- **Key Parameters:** Hour buckets per market; window tuning by ATR percentile.
- **Duplicates Eliminated:** Session-filter modules in CN/RU robots; ICT kill zones (PA-09) overlap.

---

### SE-09 · Crypto Weekend & Funding Window Effects
*加密周末与资金费率窗口 · Крипто-сезонность*

- **Origin & Lineage:** Crypto market-structure research (2019+ exchange papers; funding-settlement timing on perpetuals).
- **Core Hypothesis:** Crypto exhibits weekend liquidity holes, Sunday-gap behavior, and volatility bursts around perpetual funding settlements every 8 hours; systems harvest the predictable windows: fade weekend illiquidity extremes before Monday re-liquidity, or trade funding-settlement micro-drift. The effects decay as market structure matures — a documented feature of young markets.
- **Execution Rules:** Fade weekend range extremes toward the weekend VWAP with tight targets; avoid holding majors through Monday open gaps; optional funding-window scalps.
- **Key Parameters:** Weekend window Sat 00:00 - Mon 00:00 UTC; funding times 00/08/16 UTC; slippage-aware sizing.
- **Duplicates Eliminated:** Funding-window bots; CN 周末行情策略; RU крипто-сезонность notes.

---
