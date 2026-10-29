# Appendix B & C: Source Inventories, Conventions & Disclaimer


## Appendix B — Source and Archive Inventory

Sources are grouped by type. Domain-level references are given as top-level domains because deep links rot; all were live during the October 2026 survey window.
Table 3. Source inventory by category
Category
Representative sources
Primary contribution
Archives & historical collections
Original Turtle Rules PDFs and Way of the Turtle (2003-2007 archive); Wyckoff Stock Market Institute course materials; Gartley (1935), Darvas (1960), Wilder (1978), Crabel (1990) early editions; TASC Traders' Tips archive (technical.traders.com)
Pre-internet canon: Donchian, Turtle, Wyckoff, Gartley, ORB, Wilder's indicator suite
Academic databases
SSRN (papers.ssrn.com); arXiv q-fin (101 Formulaic Alphas: arXiv:1601.00991); NBER (w20592, Harvey-Liu-Zhu); RFS/JF/JFE journals; Federal Reserve staff reports (Lucca-Moench pre-FOMC); CNKI 知网 / Wanfang; HSE/MIPT preprints
Factor zoo, momentum/carry/value literature, multiple-testing corrections, calendar anomalies
Global communities & script libraries
TradingView (tradingview.com/scripts, 100k+ publications); LuxAlgo Library; PineCoders; MQL5.com CodeBase (MetaQuotes, RU-rooted); ForexFactory; forex-station; NexusFi/Elite Trader; QuantConnect forums; GitHub strategy collections (PineTS, script bundles)
UT Bot, QQE mod, WaveTrend, SMC/LuxAlgo Squeeze Pro, TTM Squeeze ports, MT4-era EA corpus
China platforms & blogs
JoinQuant 聚宽; myquant 掘金; BigQuant; Uqer 优矿; vn.py; czsc (waditu/czsc); chanlun-pro; Jisilu 集思录; Xueqiu 雪球; Taoguba 淘股吧; Guorn 果仁网; Zhihu/CSDN quant columns; Huatai 华泰 / Guosheng 国盛 quant-research series; WorldQuant BRAIN CN community
Chan theory industrialization, limit-up ecosystem, double-low convertibles, rotation and factor templates, ten canonical strategies canon
Russia/CIS platforms & blogs
Smart-Lab.ru (largest CIS trader community); TSLab (tslab.ru); StockSharp (stocksharp.com); QUIK Lua community (quik.ru); T-Bank/Tinkoff Investments community; MOEX education (moex.com); Finam publications; Gerchik journal; LiteFinance/InstaForex knowledge bases; MQL5 RU blogs
Ilan advisor lineage, Sniper method, dividend-gap canon, synthetic-bond arb, DOM-scalping school, Smart-Lab robot archive
Think tanks & institutional research
BIS papers; Federal Reserve Board/NY Fed staff reports; WorldQuant (BRAIN platform); AQR publications; CFTC COT data; exchange research (BitMEX/OKX/Glassnode/CoinMetrics notes); CBOT Market Profile letters (Steidlmayer)
Carry/momentum formalization, pre-FOMC drift, funding-rate and on-chain research, auction-theory canon

## Appendix C — Pine Conventions, Statistics, and Disclaimer

All Pine listings follow one convention set: Pine Script v5; inputs exposed for every canonical parameter; strategy() for systems with entry/exit rules, indicator() for measurement tools; no request.security beyond documented higher-timeframe filters; and no repainting constructs (signals use closed-bar data; higher-timeframe calls use lookahead_off). Comments inside the code note where an implementation is a condensed or approximated form of the original mechanism — for example the single-symbol proxy of WorldQuant Alpha #1 (ST-10), whose true form requires a cross-sectional universe, or the bar-microstructure delta proxy (VO-09), which approximates tick-level CVD. Code blocks shade their background and use a monospace face at reduced size; they are meant to be read, copied into TradingView, and re-tuned, not trusted blind.
Table 4. Glossary statistics by family
Family
Entries
Pine implementations
A — Trend Following & Momentum (TR)
18
12
B — Mean Reversion & Oscillator Systems (MR)
15
7
C — Breakout & Volatility Expansion (BK)
13
3
D — Price Action, Patterns & Smart Money (PA)
16
4
E — Indicator Hybrids & Cycle Tools (IH)
14
3
F — Volume, Order Flow & Market Profile (VO)
12
2
G — Session, Time & Calendar Edges (SE)
9
1
H — Grid, Martingale & Averaging Systems (GR)
7
2
I — China-Specific Systems (A-Share & CN Futures) (CN)
26
4
J — Russia/CIS-Specific Systems (RU)
16
2
K — Statistical, Factor & Arbitrage Systems (ST)
18
1
L — Crypto-Native Systems (CR)
11
0
M — Machine Learning & AI Systems (ML)
7
0
N — Risk, Sizing & Execution (RX)
7
2
Total
189
43
Disclaimer. This document is a research compilation, not investment advice. Historical documentation of a strategy is not evidence of profitability; most published edges decay after publication, several documented families (martingale averaging, unhedged short-volatility) carry structurally negative tail profiles, and regional systems depend on market microstructure that can change by regulation overnight — as the 2015 CN index-futures restrictions and the 2024 northbound-disclosure cut demonstrated. All code is reference-grade and untested against live data feeds. Verify every system through the evaluation discipline of ML-07 before committing capital, and size according to the risk family (RX) rather than conviction.