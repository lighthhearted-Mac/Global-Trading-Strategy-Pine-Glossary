# Family CR: Crypto-Native Systems (Perp & DEX)

**Total Strategies in Family:** 11  
**Pine Script v5 Implementations:** 0  

## Strategies Overview

| ID | Strategy Name | Alternative Names | Has Pine Code |
|---|---|---|:---:|
| **CR-01** | [Funding-Rate Arbitrage (Delta-Neutral Carry)](#cr-01--funding_rate_arbitrage_delta_neutral_carry) | 资金费率套利 · Арбитраж фандинга | 📖 Logic-only |
| **CR-02** | [Cash-and-Carry / Futures Basis Trade](#cr-02--cash_and_carry_futures_basis_trade) | 期现基差套利 · Кэш-энд-керри | 📖 Logic-only |
| **CR-03** | [Liquidation-Cascade Fade](#cr-03--liquidation_cascade_fade) | 爆仓瀑布反打 · Фейд каскада ликвидаций | 📖 Logic-only |
| **CR-04** | [Open-Interest Regime Model (OI + Price Matrix)](#cr-04--open_interest_regime_model_oi_price_matrix) | 持仓量状态模型 · Режимная модель OI | 📖 Logic-only |
| **CR-05** | [On-Chain Whale & Flow Following](#cr-05--on_chain_whale_flow_following) | 链上巨鲸跟踪 · Следование за китами | 📖 Logic-only |
| **CR-06** | [BTC Dominance / Altcoin Rotation](#cr-06--btc_dominance_altcoin_rotation) | BTC占比与山寨轮动 · Ротация BTC-альты | 📖 Logic-only |
| **CR-07** | [Crypto Volatility Breakout (Donchian + Funding Filter)](#cr-07--crypto_volatility_breakout_donchian_funding_filter) | 加密波动突破 · Крипто-пробой | 📖 Logic-only |
| **CR-08** | [Triangular Arbitrage](#cr-08--triangular_arbitrage) | 三角套利 · Треугольный арбитраж | 📖 Logic-only |
| **CR-09** | [DeFi Concentrated Liquidity Market-Making](#cr-09--defi_concentrated_liquidity_market_making) | DeFi做市策略 · DeFi ММ (Uniswap v3) | 📖 Logic-only |
| **CR-10** | [MEV Extraction (Sandwich / Backrun) — Documented, Not Endorsed](#cr-10--mev_extraction_sandwich_backrun_documented_not_endorsed) | MEV抢跑与三明治攻击 | 📖 Logic-only |
| **CR-11** | [Cross-Exchange Latency Arbitrage](#cr-11--cross_exchange_latency_arbitrage) | 跨所延迟套利 · Межбиржевой арбитраж | 📖 Logic-only |

---

### CR-01 · Funding-Rate Arbitrage (Delta-Neutral Carry)
*资金费率套利 · Арбитраж фандинга*

- **Origin & Lineage:** Perpetual futures funding design (BitMEX, 2016); exchange research notes and CN/RU crypto-bot communities (2019+).
- **Core Hypothesis:** Perps pay funding to anchor to spot: longs pay shorts when funding is positive. Holding spot long plus perp short harvests the funding while staying delta-neutral — the dominant structural carry of the 2020-2024 cycles, with double-digit annualized rates at bull peaks. Risk is funding flip, margin spirals, and exchange credit; executions exist as exchange-native 'funding arb' bots on CN and RU-facing venues alike.
- **Execution Rules:** Buy spot, short equal perp notional; collect funding while positive; close when funding turns negative after costs; ladder across venues.
- **Key Parameters:** Funding threshold > 2 x fees per period; margin buffer 3-5x; venue diversification.
- **Duplicates Eliminated:** ST-06 carry (the general form); CR-02 (dated-futures version).

---

### CR-02 · Cash-and-Carry / Futures Basis Trade
*期现基差套利 · Кэш-энд-керри*

- **Origin & Lineage:** Classical arbitrage (RU-06's ancestor) reborn on CME/derivatives bases (2017+); documented in every post-2020 crypto research note.
- **Core Hypothesis:** When quarterly futures trade at a premium to spot (bull markets routinely 10-30% annualized), short the future, long spot, and hold to convergence — the premium is the return. It is the oldest arb in finance on the newest market, and its 2020-2021 magnitudes made it a flagship institutional crypto product. Same risk profile as CR-01 with dated convergence instead of indefinite funding.
- **Execution Rules:** Long spot / short dated future when annualized basis > threshold; hold to expiry or unwind at normalization; roll if the term structure stays steep.
- **Key Parameters:** Basis threshold 8-15% annualized; margin buffer; expiry calendar.
- **Duplicates Eliminated:** CR-01 (perp version); ST-16 (commodity roll analog); CN-25 (CN index-futures version).

---

### CR-03 · Liquidation-Cascade Fade
*爆仓瀑布反打 · Фейд каскада ликвидаций*

- **Origin & Lineage:** Exchange data transparency (2019+); CN/RU crypto-Twitter communities; quantified by crypto research blogs.
- **Core Hypothesis:** Cascading liquidations drive price far past fair value within minutes — wicks of hundreds of dollars on BTC — because forced market orders exhaust the book; fading the cascade once liquidation flow exhausts (wick reversal, OI flush) targets the snap-back. Entry discipline is everything: only after OI/liquidation measures peak, never during. It is Wyckoff spring logic on an exchange-enforced timescale.
- **Execution Rules:** Detect abnormal wick + liquidation-volume spike + OI drop; enter reversal on the first reclaim bar; tight stop beyond wick; quick target at pre-cascade level.
- **Key Parameters:** Wick > 2-3 ATR; liquidation percentile > 99th; holding minutes-to-hours.
- **Duplicates Eliminated:** PA-01 spring (mechanism); VO-09 delta flush (informational cousin).

---

### CR-04 · Open-Interest Regime Model (OI + Price Matrix)
*持仓量状态模型 · Режимная модель OI*

- **Origin & Lineage:** Derivatives-data platforms (Coinglass-era); CN/RU crypto communities' regime dashboards.
- **Core Hypothesis:** The OI x price quadrant classifies market state: OI up + price up = new longs (trend fuel), OI up + price down = new shorts, OI down + move = deleveraging (weak move), OI flat = range. Systems trade with new-position trends and fade deleveraging moves. It is the crypto analog of volume confirmation (VO family) built on a cleaner dataset.
- **Execution Rules:** Classify each bar into the OI-price quadrant; trade continuation in OI-building moves; fade post-flush moves as OI rebuilds.
- **Key Parameters:** OI change thresholds vs ATR; quadrant persistence; funding context.
- **Duplicates Eliminated:** VO-12 volume-confirmed breakout (tradfi analog); CR-03 (event special case).

---

### CR-05 · On-Chain Whale & Flow Following
*链上巨鲸跟踪 · Следование за китами*

- **Origin & Lineage:** On-chain analytics platforms (Glassnode, Nansen era, 2019+); CN/RU crypto research communities.
- **Core Hypothesis:** Blockchain transparency exposes large-wallet behavior: exchange inflows (sell pressure), outflows (accumulation), stablecoin minting (dry powder), and smart-money wallet mimicry. Systems convert flow signals into regime gates or entry triggers — e.g., exchange net-outflow streaks precede supply squeezes. Data quality and interpretation lag are the binding caveats; attribution of wallets is probabilistic.
- **Execution Rules:** Track net exchange flows and whale-wallet cohorts; accumulate on outflow streaks + price basing; de-risk on inflow spikes with price strength.
- **Key Parameters:** Flow thresholds vs circulating supply; cohort definitions; confirmation lag 1-7 days.
- **Duplicates Eliminated:** CN-07/08 (flow-copy logic in tradfi clothes); VO order-flow family.

---

### CR-06 · BTC Dominance / Altcoin Rotation
*BTC占比与山寨轮动 · Ротация BTC-альты*

- **Origin & Lineage:** Crypto cycle literature (2017/2021 cycles); CN/RU altcoin communities.
- **Core Hypothesis:** Capital rotates through the crypto stack in cycles: BTC leads, then large alts, then speculative small caps, visible in BTC dominance charts; rotation systems shift weights along the dominance cycle and de-risk at blow-off signs. The edge is cycle timing, and its failure mode is staying late in the speculation phase. Implementations range from manual dashboards to automated dominance-momentum switches.
- **Execution Rules:** Track BTC dominance momentum; rotate BTC -> large alts -> small caps as dominance falls; reverse or go stable as dominance turns up sharply.
- **Key Parameters:** Dominance windows 30-90 days; rotation thresholds; blow-off detection (funding, volume).
- **Duplicates Eliminated:** CN-11 cap rotation (tradfi analog); TR-17 momentum machinery.

---

### CR-07 · Crypto Volatility Breakout (Donchian + Funding Filter)
*加密波动突破 · Крипто-пробой*

- **Origin & Lineage:** Adaptation of TR-01/02 to 24/7 crypto (2017+ bot era); CN grid-vs-trend debates popularized the filter set.
- **Core Hypothesis:** Crypto trends hard; Donchian/ATR breakouts with a funding-regime filter (only long when funding is not extremely positive, avoiding crowded longs) capture major moves while avoiding the worst blow-off entries. Sizing is vol-normalized with wide stops because daily ATR can exceed 5-10%. It is the crypto workhorse trend shell.
- **Execution Rules:** Long on N-day high break when funding below crowd threshold; stop k x ATR; trail on opposite N/2-day low; short mirrored with funding context flipped.
- **Key Parameters:** N 20-55; funding cap (e.g., < 0.05%/8h for longs); stop 2-4 ATR.
- **Duplicates Eliminated:** TR-01/TR-02 (parents); SE-09 (session overlays); RU/CN crypto-bot presets.

---

### CR-08 · Triangular Arbitrage
*三角套利 · Треугольный арбитраж*

- **Origin & Lineage:** FX desk-era technique; cryptoized 2017+ (high-frequency bots; CN/RU arbitrage communities).
- **Core Hypothesis:** Exploit inconsistencies across three-leg cycles (BTC/USDT, ETH/USDT, ETH/BTC) where implied cross rates diverge beyond fees; profits are tick-scale and vanish with latency, making this an HFT-adjacent game of infrastructure rather than strategy. Documented because it is the canonical answer to 'can retail arb crypto?' — usually no, at speed.
- **Execution Rules:** Monitor implied cross vs quoted; execute all three legs atomically when edge > 3x fees; cancel on leg failure.
- **Key Parameters:** Edge threshold; execution latency < 50 ms realistically; fee tier optimization.
- **Duplicates Eliminated:** CR-11 (cross-venue variant); RU-13 (latency-bound scalping lessons).

---

### CR-09 · DeFi Concentrated Liquidity Market-Making
*DeFi做市策略 · DeFi ММ (Uniswap v3)*

- **Origin & Lineage:** Uniswap v3 whitepaper (2021); DeFi research and CN/RU DeFi communities.
- **Core Hypothesis:** Concentrated-liquidity positions earn fees proportional to capital efficiency within a chosen range; the strategy is choosing ranges around expected mean-reversion zones, managing inventory drift (impermanent loss is rebalancing), and compounding fees. It is market-making with a public, non-custodial venue — and its risk profile (inventory + range exit) is classic MM risk in new clothes.
- **Execution Rules:** Provide liquidity in a range around fair value; re-center on drift; widen ranges in high-vol regimes; compound fees.
- **Key Parameters:** Range width vs ATR; rebalance drift threshold; fee tier selection; gas budget.
- **Duplicates Eliminated:** GR-01 grid (the AMM is a grid at heart); VO order-flow family (inventory logic).

---

### CR-10 · MEV Extraction (Sandwich / Backrun) — Documented, Not Endorsed
*MEV抢跑与三明治攻击*

- **Origin & Lineage:** Flash Boys 2.0 paper (Daian et al., 2019); MEV research (Flashbots era).
- **Core Hypothesis:** Public mempools let bots see pending swaps and extract value by front/back-running them, an estimated billion-dollar category; the strategy is pure latency-plus-auction economics, and the countermeasure evolution (private RPCs, batch auctions, MEV-boost) is one of the great market-structure stories of the decade. Listed for completeness with the explicit note that it is adversarial extraction, increasingly disintermediated by protocol design.
- **Execution Rules:** Detection of profitable pending transactions; bundle bidding via MEV infrastructure; economics capped by priority-auction competition.
- **Key Parameters:** Bid competitiveness; bundle profitability floor; infra costs.
- **Duplicates Eliminated:** CR-08 (latency family); regulatory grey-zone literature.

---

### CR-11 · Cross-Exchange Latency Arbitrage
*跨所延迟套利 · Межбиржевой арбитраж*

- **Origin & Lineage:** 2017+ crypto fragmentation era; CN (pre-ban) and RU arbitrage communities extensively documented it.
- **Core Hypothesis:** Price discovery leads on the deepest venue (Binance/CME); lagging venues drift a few basis points behind, and fast bots synchronize by buying the lag and hedging the lead. Withdrawal/transfer risk and fee tiers decide viability; the modern edge is mostly dead at retail latency. It completes the arbitrage subset of this family and marks the boundary where strategy ends and infrastructure begins.
- **Execution Rules:** Lead venue defines fair price; trade laggards when divergence > 2 x costs; hedge or transfer inventory; risk = transfer/counterparty.
- **Key Parameters:** Divergence threshold; inventory rebalancing cadence; venue credit risk.
- **Duplicates Eliminated:** CR-08 (same-latency family); CN-era '搬砖' (brick-moving) practice — the CN name for exactly this trade.

---
