# Composer Atlas: Master Reference Document

**Version:** 1.83.2
**Status:** Active
**Last Updated:** 2026-10-31

This is the single authoritative reference for Composer Atlas. It consolidates product requirements, architecture, operational runbook, data schemas, API reference, roadmap, security posture, project tenets, FAQ, and documentation process.

---

## Table of Contents

**Part A; Product Requirements**
1. [Problem Statement](#1-problem-statement)
2. [Target Users](#2-target-users)
3. [Goals](#3-goals)
4. [Non-Goals](#4-non-goals)
5. [User Stories](#5-user-stories)
6. [Feature List](#6-feature-list)
7. [Constraints](#7-constraints)
8. [Assumptions](#8-assumptions)
9. [Success Criteria](#9-success-criteria)

**Part B; Technical & Operational Reference**
10. [Architecture & Technical Reference](#10-architecture--technical-reference)
11. [Operational Runbook](#11-operational-runbook)
12. [Strategy & Glossary Data Schemas](#12-strategy--glossary-data-schemas)
13. [Composer API Reference](#13-composer-api-reference)
14. [Roadmap](#14-roadmap)
15. [Security](#15-security)
16. [Tenets](#16-tenets)
17. [FAQ](#17-faq)
18. [Documentation Process](#18-documentation-process)
19. [Writing Style](#19-writing-style)

**Part C; Measurement, Practice & Record**
20. [Metrics](#20-metrics)
21. [Conventions](#21-conventions)
22. [Deprecation and Removal](#22-deprecation-and-removal)
23. [Working Practice](#23-working-practice)
24. [Documentation Versus Reality](#24-documentation-versus-reality)
25. [Risks and Open Questions](#25-risks-and-open-questions)
26. [Press Release](#26-press-release)
27. [Social Sharing Tags](#27-social-sharing-tags)
28. [Licensing](#28-licensing)
29. [Outstanding Work and Recommended Sequence](#29-outstanding-work-and-recommended-sequence)
30. [Brand Identity](#brand-identity)

**Two of the standard's named policies live inside other sections rather than
having one of their own, and are listed here so they can be found:** *Browser
Testing* and *Verification Environment* are both subsections of
[23. Working Practice](#23-working-practice), as "Browser Testing" and "How to
Verify a Change". They were written there before the standard named them, and
the standard's own rule is that an existing project arrangement beats an
imported default, so they stay where they are.

---

## Part A: Product Requirements

---

## 1. Problem Statement

Retail investors interested in rules-based, systematic investing lack a central, accessible resource that:

- Aggregates and explains Composer.trade strategies in plain language
- Bridges the gap between raw quant concepts and practical application
- Provides transparent breakdowns of strategy logic, not just backtest returns

There is no dedicated site for Composer.trade strategy discovery and education. Strategy authors share symphonies publicly on Composer, but the platform itself does not provide educational context about how the logic works or what signals are in play.

---

## 2. Target Users

**Primary; Composer.trade users**
Self-directed retail investors who already use Composer.trade. They want to understand strategies before cloning them, or want to see how other authors have approached a problem they are solving.

**Secondary; Systematic investing learners**
Intermediate traders learning RSI, momentum, VIX strategies, and leveraged ETF mechanics. They know what a moving average is but have not yet built a systematic strategy. Composer Atlas explains concepts in the context of real strategies.

**Tertiary; Quant-curious beginners**
Investors curious about algorithmic or rules-based investing who do not yet know the terminology. The glossary serves as their entry point; strategy pages show them real examples.

---

## 3. Goals

- Launch a public-facing site with 25 strategy pages and a concept glossary
- Require zero server infrastructure; run entirely in the browser via GitHub Pages
- Establish a scalable JSON-based strategy database that can grow to thousands of entries
- Educate users on the signals and logic behind each strategy, not just its returns
- Stay free and unmonetized: the only funding channel is voluntary reader donations via Buy Me a Coffee, reached through the Support link in the nav and footer. No ads, no premium tier, no paid content, and no user data collected or sold (decided 2026-08-15)

---

## 4. Non-Goals

- No user accounts or authentication
- No community features or comments
- No newsletter or email capture
- **No monetization beyond voluntary donations (decided 2026-08-15).** The site is funded solely by Buy Me a Coffee, linked via Support in the nav and footer. Explicitly ruled out: ads (including Google AdSense), a premium/paid strategy tier, paywalled content, affiliate or sponsored placement, and email/alert products
- **No user data collection.** No accounts, no email capture, no personal data stored, sold, or shared. Every tool runs client-side and nothing a visitor enters or uploads leaves their browser
- No manual metric update pipeline needed day-to-day: `scripts/update_metrics.py` runs daily via `.github/workflows/update-metrics.yml` and commits automatically; `scripts/update_metrics.py` can still be run manually for an immediate refresh
- No mobile app
- No light mode (dark mode only at MVP)

---

## 5. User Stories

**As a Composer.trade user,** I want to see a list of curated strategies with key metrics so that I can quickly compare options before deciding which to investigate further.

**As a Composer.trade user,** I want to read a plain-English explanation of how a strategy works so that I can understand the logic before cloning it.

**As a learner,** I want to click on a signal tag (e.g., "RSI") and read a dedicated page explaining what it is and how it is used in practice so that I can deepen my understanding while exploring strategies.

**As a learner,** I want to see which strategies use a specific concept (e.g., VIX tiers) so that I can find examples of that concept applied in real symphonies.

**As a visitor,** I want to click a single button to open a strategy directly on Composer.trade so that I can clone it without manually searching.

**As a curator,** I want a documented, repeatable process for adding a new strategy from a URL so that the site can grow without increasing per-entry effort.

**As a curator,** I want metrics to stay current without rebuilding the site so that visitors see accurate data after each market refresh.

---

## 6. Feature List

### MVP: Shipped (V1.0–V1.2.1)

**Strategy Library**
- Index page listing every **visible** curated strategy with key metrics at a glance (ARR, Max DD, Sharpe). 24 of the 36 entries in `data/strategies.json` are listed as of v1.41.0; the other 12 carry `hidden: true` (see the schema table and "Hiding a Strategy" below)
- Each strategy has a dedicated page with: name, description, tags, "Open in Composer" CTA, an AI Summary (Claude-authored analysis above How It Works), plain-English logic breakdown, signals used (cross-linked to glossary), risk profile, and full metrics table
- Strategy card titles are clickable links

**Concept Glossary**
- Index page listing every glossary concept. **Rebuilt as a grouped directory at v1.83.0**: four category groups with headings and counts, one row per concept, and a jump strip at the top, replacing 27 identical cards. **28 concepts as of 2026-10-19**
- Each concept has a dedicated page with: definition, how it works, in practice examples, limitations, formula (when applicable), and a "Building with..." essay section
- Concepts cross-link back to strategies that use them

**Data Layer**
- `data/strategies.json`: flat-file database of every curated strategy. **Count stated once, in the Strategy Library bullet above**, rather than repeated here
- `data/glossary.json`: flat-file database of every glossary concept. Count stated once, in the Concept Glossary bullet above
- Dual-mode loading: `window.STRATEGIES_DATA` / `window.GLOSSARY_DATA` globals for `file://` compatibility; `fetch()` fallback for HTTP
- `scripts/update_metrics.py`: reusable script to refresh all metrics and logic trees from the Composer API

**Navigation & Structure**
- Fixed top nav: About, Strategies, Database, Glossary, Azqato Invests, Support (v1.12.1 added "Azqato Invests" linking to `https://azqato.com/invests`; v1.10.2 previously included direct external links to Individual Stocks and Leveraged Strategies, now presented as a "More From Azqato" section on the About page instead)
- Mobile hamburger menu with drawer
- Breadcrumb navigation on all sub-pages
- Custom 404 page
- About page with disclaimer
- Footer with nav links, legal disclaimer, attribution

**Design**
- Dark mode design system (see docs/DESIGN.md)
- Mobile-responsive layout
- 🗺️ map emoji favicon and nav logo mark

**Deploy**
- GitHub Actions auto-deploy on push to `main`; rsync excludes internal docs and large files

### Shipped: Full Database Initiative (v1.12.0)

Separate from the 36 curated strategies, `data/database.json` holds the full raw
symphony database, originally seeded by an external Google Apps Script scrape (the
original 6,488-row scrape plus rows synced in from `data/storage.csv` over time).
The goal was to recreate that refresh pipeline on composeratlas.com itself against
the real Composer API, filter out non-strategy noise and duplicates, and build a
Leaderboard and Screener on top of the full database, all of which is now built,
refreshed, cleaned, and live.

**Went fully live v1.12.0:** the code (`database.html`, its CSS/JS, the full-database
scripts) had been live on `main`/composeratlas.com since v1.11.2, but the data files
were deliberately withheld until the full refresh and V1.14 noise-filtering pass
completed (see Section 14 Roadmap, V1.9's correction note, for the original
reasoning). As of v1.12.0, `data/database.json`/`.js`, `data/database_summary.json`/
`.js`, and `data/storage.csv` are committed and live. Final numbers at go-live:
**6,640 total entries**: 6,221 clean, 229 flagged `duplicate`, 88 `excluded`

> **Discrepancy (measured 2026-08-24).** The line above is the v1.11.23 figure and is kept as the
> historical record of that moment. Counted directly from `data/database.json` today the database
> holds **6,668 entries**, and the flag distribution is **6,473 unflagged, 69 `retry`, 94
> `caution`, 32 `excluded`, and 0 `duplicate`**. Two things moved: the weekly
> `refresh-full-database.yml` job has been adding rows and re-classifying failures ever since, and
> the `duplicate` population is now empty, which the v1.11.12 reset (flags cleared back to null so
> rows requeue) plus subsequent successful refreshes would produce. **6,655 entries carry a
> `sharpe_ratio`**, which is the Leaderboard's eligibility proxy (6,654 after the v1.25.2 dedupe).
>
> **`data/storage.csv` is larger than this, and is meant to be: 7,709 rows against 6,668 entries.**
> The two files hold different things. `storage.csv` is the long-term archive of every symphony URL
> ever seen, kept whether the symphony is alive or dead; `database.json` holds only the symphonies
> approved to appear on the site. Do not read the difference as a backlog or as drift. See
> "storage.csv Is Larger Than database.json, On Purpose" in Section 12.
>
> **How fast these move, measured rather than guessed.** The flag counts in the paragraph above were
> rewritten once during the day of 2026-08-24. The audit measured 6,324 unflagged, 248 `retry`, 81
> `caution` and 16 `excluded`; the weekly refresh job landed hours later and left 6,474 / 69 / 94 /
> 32. The total held at 6,669 and the `sharpe_ratio` count held at 6,655, so the churn is
> re-classification of failures, not new rows: the `retry` backlog drained by 179 as transient
> failures resolved, and the ones that did not resolve hardened into `caution` or `excluded`.
> **Treat every flag figure in this document as a reading with a date on it, not a property of the
> dataset.** The total and the eligibility count are the stable numbers.
>
> **The duplicate is gone as of v1.25.2.** The reading above was taken at 6,669 rows resolving to
> 6,668 distinct `symphony_id` values, one duplicate. `symphony_id` is now a stated invariant rather
> than an assumption: see "The Primary Key Invariant" in Section 12, enforced by
> `scripts/check_database_keys.py` as a deploy gate. The count is 6,668 and every id is distinct.
>
> `data/database_summary.json` held **6,665 rows against the full file's 6,669**, so the derived
> summary was four rows behind. `scripts/export_summary.py` had not been re-run since the last four
> additions. This was a real, if small, staleness bug rather than a documentation error: the site
> reads the summary, so those four symphonies were invisible on `database.html`.
>
> **Closed in v1.25.1 (2026-08-24).** The export was re-run and the summary now holds all 6,669 rows
> in the same order as `database.json`, with the `.js` twin verified to match the JSON exactly. The
> four that had been missing were "Pals Minor Spell of Summon Money (Core Logic)", "PP MAX TEC",
> "The Gold Miner (Original)" and "Extended Backtest Simplified Copy of [ChristMas] Test #1", all
> unflagged and valid, so nothing had filtered them out. `export_summary.py` was hardened in the same
> release: it derived its column list from `entries[0].keys()` alone, which would have silently
> dropped any field added to later entries without backfilling the first, and now takes the union of
> every entry's keys in first-seen order. Column order is unchanged.
(permanent API failures + name-pattern noise), 88 `caution` (Composer data warnings),
14 `retry` (transient, self-clearing).

- [x] `data/database.json` imported from the raw xlsx as the canonical JSON source (v1.9.0)
- [x] `scripts/import_full_database.py`: one-time, re-runnable xlsx → JSON importer (v1.9.0). **Deleted in v1.24.8**, along with `scripts/add_original_tag.py`. Both had done their one job: the bootstrap import happened once at v1.9.0 and `database.json` has been canonical ever since, and the `(Original)` renames, the `original` glossary entry and the four `original` tags are all sitting in the committed data. The importer was worse than merely unused, since its column layout had drifted from what `export_full_database_to_xlsx.py` writes, so running it against the current spreadsheet would have overwritten the live dataset with a mis-parsed import. Entries below and in `docs/PATCHNOTES.md` describing past work on either script are left as an accurate record of what happened at the time.
- [x] `scripts/refresh_full_database.py`: resumable, checkpointed API refresh script, mirrors `update_metrics.py` conventions (v1.9.0); automated weekly via `.github/workflows/refresh-full-database.yml` as of v1.12.0
- [x] `database.html` template: tabbed page (All Strategies / Leaderboard / Screener) (v1.9.0)
- [x] Target schema expansion: 17 new fields locked and captured (v1.9.1)
- [x] Filter panel (shared component for All Strategies; Screener has its own separate always-visible bucketed filter grid as of v1.11.15) (v1.10.x-v1.11.15)
- [x] Screener tab, full multi-view column switcher (v1.10.x, redesigned v1.11.15)
- [x] Leaderboard tab, 20-metric/1,000-point scoring model (v1.10.x), reweighted and S+ redefined per V1.17 (2026-07-13)
- [x] Performance Fix: columnar + float-rounded summary JSON, ~80% size reduction (v1.10.x)
- [x] Noise filtering (test ports, "Invest Copy"/duplicate clusters, WIP builds): implemented and run (V1.14, v1.11.22-23): permanent API failures and name-pattern noise flagged `excluded`, near-identical duplicates flagged `duplicate` via logic-tree structural comparison, all filterable via the Working/Broken/Duplicates/All toggle
- [x] Full-scale metric refresh: complete, all entries refreshed at least once; ongoing via the weekly automated workflow above
- [x] Data files pushed live (v1.12.0)

### Future Backlog (Post-MVP)

- Client-side search across strategies and glossary
- Tag-based filtering on strategy index
- Strategy comparison view (side-by-side metrics)
- Performance chart per strategy
- Expand strategy library toward 50+ entries
- Expand glossary with additional concepts
- Community strategy submission form
- Curator notes visible on strategy pages
- Related strategies section on each strategy page

---

## 7. Constraints

- Must run entirely in browser with no server infrastructure
- Must host on GitHub Pages
- Must use static JSON files as the data source
- Must be maintainable by a single developer
- No Node.js/npm dependencies at any stage (Python only for scripts)
- Zero operational cost at launch

---

## 8. Assumptions

- Composer.trade will remain available and symphony URLs will remain stable
- The Composer API backtest and score endpoints will continue to work without authentication
- GitHub Pages free tier is sufficient for the expected traffic at MVP scale
- A flat JSON file is sufficient for up to ~100 strategies without performance issues
- Backtested data from the Composer API is accurate enough to display as-is, with a last-updated date shown on each strategy page

---

## 9. Success Criteria

- 13 strategy pages live at launch with accurate metrics
- All 8 glossary concepts live at launch with full content
- Page load time under 2 seconds on desktop
- Zero server costs at launch
- At least 1 donation received in first 30 days (qualitative validation)
- Site works correctly by double-clicking HTML files locally (no server required)
- All internal links work on both GitHub Pages and `file://` protocol

---

## Part B: Technical & Operational Reference

---

## 10. Architecture & Technical Reference

### Overview

Composer Atlas is a fully static, browser-only application. There is no server, no API backend, no database service, and no authentication layer. All data is stored in flat JSON files and served via GitHub Pages. All page rendering is done in the browser via vanilla JavaScript, no build step is required.

### Tech Stack

| Layer | Choice | Rationale |
|---|---|---|
| HTML | Vanilla `.html` files | No build step; open in browser or serve with any static host |
| CSS | CSS custom properties | Design token system without requiring a preprocessor |
| JavaScript | Vanilla ES2020 | `fetch()` for data, DOM manipulation for rendering |
| Fonts | Google Fonts CDN | No local build needed |
| Hosting | GitHub Pages | Serves static files directly from repository root |
| CI/CD | GitHub Actions | rsync to `_site/`, upload artifact, deploy |
| Scripts | Python 3 (stdlib only) | Data refresh; no pip dependencies. All `.py` files must live in `scripts/` |

**V2 upgrade path:** Astro 5.x is the preferred migration target if the site grows beyond ~20 pages or content management complexity increases. The data schema, design system, and directory conventions are compatible with an Astro migration.

### Directory Structure

```
composer/
├── .github/
│   └── workflows/
│       ├── deploy.yml               # Five pre-deploy gates, then rsync → GitHub Pages (a MIRROR; Cloudflare is canonical)
│       ├── update-metrics.yml       # Daily 21:20 UTC: curated metrics + logic trees; script skips anything refreshed inside 7 days
│       ├── refresh-prices.yml       # Weekly, Friday. FIRST link in the chain: prices → database → out-of-sample
│       ├── refresh-full-database.yml # Weekly, Saturday. MIDDLE link
│       ├── refresh-oos.yml          # Weekly, Sunday. LAST link
│       └── refresh-rsi.yml          # 15:07 / 19:07 / 22:07 UTC, weekdays only
├── css/
│   └── main.css                 # Full design system: tokens, layout, components
├── data/
│   ├── strategies.json          # Curated strategy entries, source of truth. Count in Section 6
│   ├── strategies.js            # Same data as window.STRATEGIES_DATA, for file:// compat
│   ├── strategy_extras.json     # BUILD-TIME JOIN of strategies × database × k1, written by build_strategy_extras.py. strategies.html reads THIS, not the source files (v1.28.0)
│   ├── strategy_extras.js       # Same data as window.STRATEGY_EXTRAS_DATA, for file:// compat
│   ├── daily_returns.json       # Daily return series per visible strategy; unblocks worst month, VaR, CVaR, time in market, year-jackknife (V1.20 item 16)
│   ├── daily_returns.js         # Same data as window.DAILY_RETURNS_DATA, for file:// compat
│   ├── glossary.json            # Glossary concept entries, source of truth (was 8 at MVP). Count in Section 6
│   ├── glossary.js              # Same data as window.GLOSSARY_DATA, for file:// compat
│   ├── symphony_scores.json     # Full logic trees; AI analysis input only. Excluded from BOTH hosts (.assetsignore + deploy.yml)
│   ├── database.json            # Full community database. A BUILD INPUT, not a site asset: 19 MiB, excluded from both hosts, and no page fetches it (closed open question 2, v1.79.2)
│   ├── database.js              # Same data as window.DATABASE_DATA. Also excluded; nothing reads the global
│   ├── database_summary.json    # Columnar, float-rounded export of database.json. THIS is what database.html loads (v1.16)
│   ├── database_summary.js      # Same data as window.DATABASE_SUMMARY_DATA, for file:// compat (v1.16)
│   ├── oos.json                 # True out-of-sample statistics for the Leaderboard candidate set, keyed by symphony_id (V1.18)
│   ├── oos.js                   # Same data as window.OOS_DATA, for file:// compat
│   ├── overfit.json             # Population findings, the "par" curve the Overfit Score is read against, and a per-symphony index (V2.4)
│   ├── overfit.js               # Same data as window.OVERFIT_DATA, for file:// compat
│   ├── rsi.json                 # 10-day RSI (Wilder's smoothing) for the 20-ticker Frontrunner universe (V2.1)
│   ├── rsi.js                   # Same data as window.RSI_DATA, for file:// compat (V2.1)
│   ├── prices.json              # Full daily adjusted-close history (72 tickers from 2010) for the Signal Miner (v1.15.0)
│   ├── prices.js                # Same data as window.PRICES_DATA, for file:// compat (v1.15.0)
│   ├── ticker_inception.json    # Real first-trade date per ticker, so a backtest window can be judged against fund age rather than assumed
│   ├── ticker_inception.js      # Same data as window.TICKER_INCEPTION_DATA, for file:// compat
│   ├── k1.json                  # Master K-1 database: fund structure → tax form, per ticker (v1.27.0)
│   ├── k1.js                    # Same data as window.K1_DATA, for file:// compat (v1.27.0)
│   ├── k1_seed.txt              # Ticker candidate list refresh_k1.py reads with --seed; a request to check, not a claim (v1.27.0)
│   ├── storage.csv              # Append-only archive of EVERY symphony URL ever seen, alive or dead; deliberately larger than database.json (v1.10.1)
│   ├── AddSymphony.csv          # User-submitted URL inbox, single `url` column, manual-only (added 2026-07-15)
│   └── Full Database.xlsx       # Occasional export of the JSON for spreadsheet work. NOT in .assetsignore and therefore still served; see Section 24 row 2
├── js/
│   └── app.js                   # Shared utilities: format, nav, footer, render helpers, escapeHtml
├── scripts/                     # All Python scripts live here, never in the project root
│   ├── update_metrics.py        # Fetches backtest metrics + logic trees from the Composer API for the curated set
│   ├── refresh_full_database.py # Resumable, checkpointed API refresh for the community database (v1.9.0)
│   ├── refresh_prices.py        # Full Yahoo Finance daily-close history for the Signal Miner universe (v1.15.0)
│   ├── refresh_rsi.py           # Yahoo Finance daily bars → Wilder's RSI(10) (V2.1)
│   ├── refresh_oos.py           # True out-of-sample statistics for the Leaderboard candidates (V1.18)
│   ├── refresh_k1.py            # Reads each fund's Structure field, derives its tax form (v1.27.0)
│   ├── refresh_ticker_inception.py # Real first-trade date per ticker
│   ├── export_summary.py        # Derives database_summary.json/.js from database.json (v1.16); run after EVERY refresh
│   ├── export_full_database_to_xlsx.py # Local-only, occasional: regenerates the xlsx from the JSON (v1.9.4)
│   ├── build_strategy_extras.py # Joins the featured strategies to database.json and k1.json at build time (v1.28.0)
│   ├── build_overfit.py         # Derives data/overfit.json + twin for the Overfit Check page (V2.4)
│   ├── build_sitemap.py         # Regenerates sitemap.xml from the indexable pages + curated slugs (v1.25.1)
│   ├── check_html_js.py         # GATE 1: tokenizes every inline <script>; catches the v1.22.2 outage class
│   ├── check_composer_ladder.py # GATE 2: the emitted Composer tree satisfies the invariants Composer requires (v1.22.7)
│   ├── check_database_keys.py   # GATE 3: symphony_id unique, summary in sync, every symphony archived (v1.25.2)
│   ├── check_strategy_extras.py # GATE 4: the committed join matches a fresh one, both twins (v1.28.0)
│   ├── check_asset_sizes.py     # GATE 5: no served file exceeds Cloudflare's 25 MiB per-file limit (v1.43.2)
│   ├── check_prose_tokens.py    # GATE: a metric quoted in prose must be a {token}, never a typed figure
│   ├── check_risk_profiles.py   # ADVISORY by owner ruling: risk_profile is a string or a known-key object
│   ├── check_stat_drift.py      # ADVISORY by owner ruling: a hand-typed figure in prose that no longer matches live metrics
│   ├── check_daily_returns.py   # daily_returns.json is intact and agrees with the metrics table
│   ├── check_rank_claims.py     # Re-derives every library-wide rank claim in prose from live metrics
│   ├── check_signal_types.py    # The `signals` schema shape after V1.20 item 11; both fields degrade silently by design
│   ├── check_social_tags.py     # Open Graph and Twitter Card compliance. NOT a gate; open question 27, ruled manual
│   ├── check_live.py            # Lints what Cloudflare actually SERVES, rather than what git says was pushed
│   ├── analyze_leaderboard.py   # Manual only, never in CI. Re-derives every V1.18 number in this document
│   ├── measure_throughput.py    # Times Signal Miner Pass 1 from outside the browser
│   ├── run_harness.py           # Runs one of the Signal Miner headless-Edge harnesses (Edge, never Chrome)
│   ├── harness/                 # The harness drivers themselves, plus their own README
│   ├── dedupe_symphonies.py     # MANUAL ONLY, never in CI: flags near-identical name-cluster duplicates (V1.14)
│   ├── flag_name_noise.py       # MANUAL ONLY, never in CI: flags test ports and work-in-progress rows by name pattern (V1.14)
│   ├── purge_flagged_entries.py # Removes database.json entries by flag level
│   ├── sync_database_to_storage.py # Archives any database.json URL missing from storage.csv (v1.25.4)
│   ├── sync_storage_to_database.py # DANGEROUS: seeds storage.csv URLs into database.json. Run twice by mistake; see the runbook warning
│   ├── id_to_url.py             # Converts a symphony id to its canonical URL and back
│   ├── add_glossary.py          # One-time: added 9 glossary entries (v1.5.2), safe to re-run
│   ├── add_zoop.py              # One-time: added the zoop glossary entry + zoop tags (v1.5.3)
│   └── add_ai_summary.py        # Writes the ai_summary field on all strategies (v1.7.0), safe to re-run
├── index.html                   # Home page: pitch-led hero, explore cards, how-it-works. Reordered and the stats bar removed at v1.81.0
├── strategies.html              # Strategy listing + detail (?slug=X), single file
├── glossary.html                # Glossary listing + concept detail (?slug=X), single file. Listing rebuilt as a grouped directory at v1.83.0
├── database.html                # Full-database tabs: All Strategies / Leaderboard / Screener (v1.9.0)
├── rsi.html                     # Live RSI signals table, 20-ticker Frontrunner universe (V2.1)
├── rsi-backtest.html            # RSI Backtester, simple view (data/prices.json, client-side)
├── rsi-backtest-advanced.html   # RSI Backtester, advanced view; links both ways keep the settings
├── signal-miner.html            # Tool: client-side IF/THEN signal miner + backtester; nav Tools dropdown + footer + home (renamed from Signal Lab v1.16.6) (v1.15.2)
├── signal-lab.html              # Redirect stub → signal-miner.html (noindex); preserves old Signal Lab links (v1.16.6)
├── converter.html               # Tool: Symphony → JSON converter + logic tree; nav Tools dropdown + footer + homepage card (v1.16.3)
├── nodes.html                   # Tool: symphony URL → node count + breakdown by node type; nav Tools dropdown + footer + homepage card (v1.26.0)
├── k1.html                      # Tool: ticker → does it issue a Schedule K-1; local lookup over data/k1.json; nav Tools dropdown + footer + homepage card (v1.27.0)
├── overfit.html                 # Tool: paste a symphony → a 0-100 Overfit Score against the unedited-for-a-year population; nav Tools dropdown + footer (V2.4, v1.75.0, corrected v1.76.0)
├── etf-cloner.html              # Tool: ETF ticker or holdings file → a Composer symphony cloning the basket; footer + homepage card, intentionally NOT in nav (v1.16.0)
├── about.html                   # About page
├── 404.html                     # Custom 404 page
├── _wf-mockup.html              # Walk-forward validation mockup. GITIGNORED and local-only; the sole artifact describing V2.2 item B
├── favicon.svg                  # 🗺️ map emoji SVG favicon
├── robots.txt                   # Allows everything, advertises /sitemap.xml
├── sitemap.xml                  # Generated by scripts/build_sitemap.py; never hand-edited (v1.25.1)
├── README.md                    # General-reader front door. No install steps, by owner instruction 2026-08-24. Excluded from both hosts
├── LICENSE.md                   # All rights reserved, source-available. See Section 28
├── wrangler.jsonc               # Cloudflare Pages config. Sets assets.directory to ".", which is why .assetsignore exists
├── .assetsignore                # What Cloudflare does NOT serve. KEEP IN STEP with deploy.yml's rsync excludes; they do not read each other
├── .gitignore
└── docs/                        # PRD, DESIGN, PATCHNOTES. Excluded from both hosts
```

### CSS Custom Properties (Design Tokens)

All design tokens are defined as CSS variables in the `:root` block of `css/main.css`. **The values
are documented in `docs/DESIGN.md` and are deliberately not repeated here:** Section 2 holds the
colour palette with every step's measured contrast separation and the reasoning behind it, Section 3
the font stacks, Section 4 the layout tokens (`--nav-height`, `--page-px`, `--max-width`), and
Section 5 the radii. Between them they cover every token this section used to list.

> **This section carried a second copy of the palette, and that copy went two releases stale.** It
> still read `--color-bg: #0d0d0d` and `--color-pink: #ff4d8d` after v1.82.0 rebuilt the entire
> palette on a Visual Studio dark base, so the master reference described a site that had not existed
> for nineteen days. **Replaced with a pointer rather than re-synced, because re-syncing restores the
> same drift with a later start date.** It is also the third time this exact pair has disagreed:
> Section 24 row 12 registered `--color-disabled` as `#444444` here against `#c0c0c0` in the code on
> 2026-08-24. This is open question 20's rule applied to tokens rather than counts: state a fact in
> one place and cross-reference it everywhere else.

Dark mode is the only supported mode, and per Section 4 a light mode is a standing non-goal.

### Data Layer

**strategies.json and strategies.js**

- `data/strategies.json`: source of truth; JSON array of strategy objects
- `data/strategies.js`: assigns `window.STRATEGIES_DATA = [...]`; keeps data accessible on `file://` protocol

Both files must always be kept in sync. When editing `strategies.json`, make the identical change in `strategies.js`.

**glossary.json and glossary.js**

- `data/glossary.json`: source of truth; JSON array of concept objects
- `data/glossary.js`: assigns `window.GLOSSARY_DATA = [...]`

**Dual-mode loading (from `js/app.js`):**

```javascript
async function loadStrategies() {
  if (window.STRATEGIES_DATA) return window.STRATEGIES_DATA;
  const res = await fetch(`${BASE}/data/strategies.json`);
  if (!res.ok) throw new Error('Failed to load strategies.json');
  return res.json();
}
```

The same pattern applies to `loadGlossary()`. This ensures the site works in all three environments: double-click (`file://`), Python HTTP server, and GitHub Pages.

**Full database dataset:** `database.html` uses the identical pattern via its own inline `loadFullDatabase()` (not a shared `js/app.js` function, since this dataset is not part of the curated-library data layer). `data/database.js` assigns `window.DATABASE_DATA`; every script that writes `database.json` writes the `.js` twin in sync, same as `update_metrics.py` does for the curated set. A v1.9.0/v1.9.1 oversight shipped `database.html` with `fetch()`-only loading (no global fallback), which fails with "Failed to fetch" on `file://`; fixed in v1.9.2.

### BASE URL and `u()` Helper

```javascript
// On GitHub Pages (*.github.io) the first path segment is the repo name (e.g. /composer).
// On localhost or a custom domain the site is served at root, so BASE is empty.
const _seg = window.location.pathname.split('/')[1];
const BASE = (window.location.hostname.endsWith('.github.io') && _seg) ? '/' + _seg : '';

// All internal links use u() instead of BASE + path directly
function u(path) {
  if (window.location.protocol !== 'file:') return BASE + path;
  // On file://, all pages are at root depth, strip the leading slash
  // Maps '/' → 'index.html'; '/strategies.html?slug=X' → 'strategies.html?slug=X'
  const [pathPart, qs] = path.split('?');
  const rel = pathPart === '/' ? 'index.html' : pathPart.replace(/^\//, '');
  return rel + (qs ? '?' + qs : '');
}
```

Detects GitHub Pages by hostname (`*.github.io`) rather than matching the repo name, repo-rename-proof and works on any custom domain without changes.

### JS Utility Functions (js/app.js)

| Function | Signature | Purpose |
|---|---|---|
| `loadStrategies()` | `async () => object[]` | Returns strategy array from global or fetch |
| `loadGlossary()` | `async () => object[]` | Returns glossary array from global or fetch |
| `formatPct(n)` | `(float) => string` | `0.312` → `+31.20%`; always includes sign |
| `formatLargePct(n)` | `(float) => string` | For cumulative returns; rounds to nearest integer |
| `formatRatio(n)` | `(float) => string` | `1.43` → `"1.43"` (2 decimal places) |
| `formatDate(iso)` | `(string) => string` | `"2026-06-08"` → `"Jun 8, 2026"` |
| `formatBacktestDays(days)` | `(int) => string` | `551` → `"~2 yrs (551 trading days)"` |
| `colorClass(n)` | `(float) => string` | Returns `text-green`, `text-pink`, or `text-primary` |
| `tagClass(slug)` | `(string) => string` | Returns CSS class for tag pill styling |
| `tagLabel(slug)` | `(string) => string` | Returns display label for a tag slug |
| `renderTag(slug)` | `(string) => string` | Returns full `<a class="tag ...">` HTML |
| `badgeClass(category)` | `(string) => string` | Returns CSS class for category badge |
| `renderNav()` | `() => void` | Injects nav HTML into `#nav-root`; wires hamburger toggle |
| `renderFooter()` | `() => void` | Injects footer HTML into `#footer-root` |
| `renderBreadcrumb(id, crumbs)` | `(string, object[]) => void` | Renders breadcrumb nav into element by ID |
| `renderStrategyCard(s)` | `(object) => string` | Returns strategy card HTML |
| `renderConceptCard(concept, count)` | `(object, int) => string` | Returns glossary concept card HTML |
| `renderMetricsTable(s)` | `(object) => string` | Returns full metrics table HTML (grouped sections) |
| `renderStrategyListItem(s)` | `(object) => string` | Returns compact sidebar strategy row HTML |

### Page Routes

| URL (GitHub Pages) | File | Rendering |
|---|---|---|
| `/composer/` | `index.html` | Static marketing/landing page: hero, how-it-works, explore cards. **Reordered 2026-09-09 (v1.81.0) and the stats bar removed** |
| `/composer/strategies.html` | `strategies.html` | Listing view (no slug) |
| `/composer/strategies.html?tags=rsi,zoop` | `strategies.html` | Listing view pre-filtered to strategies carrying **all** the listed tags (AND). Written by the tag filter bar via `history.replaceState`, so filtered views are linkable (v1.17.0) |
| `/composer/strategies.html?slug=foo` | `strategies.html` | Detail view for `foo` |
| `/composer/glossary.html` | `glossary.html` | Listing view (no slug) |
| `/composer/glossary.html?slug=foo` | `glossary.html` | Detail view for `foo` |
| `/composer/database.html` | `database.html` | Tabs: All Strategies, Leaderboard (V1.13/V1.17 scoring), and Screener (bucket filters + 3 column views, plus Leaderboard Rank/Tier/Score columns and a tier filter as of v1.17.0). All three are built and live |
| `/composer/rsi.html` | `rsi.html` | Sortable RSI signals table (V2.1) |
| `/composer/rsi-backtest.html` | `rsi-backtest.html` | RSI Backtester, simple view: one Composer-rule table across levels with Sharpe; cascade (`?mode=cascade`) gets the same table across nearby setups, plus time in each fund |
| `/composer/rsi-backtest-advanced.html` | `rsi-backtest-advanced.html` | RSI Backtester, advanced view: verdict, Sharpe, equity curve, level-nudge and year-by-year tables; same URL parameters |
| `/composer/signal-miner.html` | `signal-miner.html` | Tool: IF/THEN signal miner + backtester, runs fully client-side. In the nav **Tools** dropdown, footer sitemap, and homepage Explore card; indexable. Renamed from "Signal Lab" at v1.16.6 (v1.15.2) |
| `/composer/signal-lab.html` | `signal-lab.html` | Redirect stub → `signal-miner.html` (preserves query string); `noindex`. Kept so old Signal Lab links do not break (v1.16.6) |
| `/composer/converter.html` | `converter.html` | Tool: Symphony → JSON converter + logic tree. Indexable; in the nav **Tools** dropdown, footer sitemap, and homepage Explore card (v1.16.3) |
| `/composer/nodes.html` | `nodes.html` | Tool: paste a symphony URL, get its node count and a breakdown by node type. Indexable; in the nav **Tools** dropdown, footer sitemap, and homepage Explore card (v1.26.0) |
| `/composer/k1.html` | `k1.html` | Tool: type a ticker, get whether it issues a Schedule K-1 or a 1099, plus the structure that decides it. Answers come from `data/k1.json`, shipped with the site, so the lookup is local and works offline. Indexable; in the nav **Tools** dropdown, footer sitemap, and homepage Explore card (v1.27.0) |
| `/composer/etf-cloner.html` | `etf-cloner.html` | Tool: ETF → Composer holdings-clone generator. Live top-holdings fetch by ticker + full-basket upload of an issuer CSV/xlsx. Indexable; in the footer sitemap + homepage Explore card, but intentionally **not** in the primary nav (v1.16.3) |
| `/composer/overfit.html` | `overfit.html` | Tool: paste a symphony and read a 0 to 100 **Overfit Score** against the population of 5,228 symphonies whose logic has gone a year unedited. Leads with the score as of v1.76.0. Indexable; in the nav **Tools** dropdown and the footer sitemap (V2.4 Tier 1, v1.75.0; substantially corrected v1.76.0; Tier 2 v1.77.0) |
| `/composer/about.html` | `about.html` | Static HTML |
| `/composer/404.html` | `404.html` | GitHub Pages error page |

**Listing/detail routing:** Each combined page checks `new URLSearchParams(window.location.search).get('slug')` on load. `null` → listing view; non-null → detail view for that slug.

**Tool pages:** `converter.html`, `signal-miner.html`, `nodes.html`, `k1.html`, `overfit.html`, and `etf-cloner.html` are standalone utilities that reuse `css/main.css` + `js/app.js` (so nav/footer render consistently). All are indexable. As of v1.16.3 the tools reachable from the primary nav (RSI Signals, Signal Miner, Converter, Nodes since v1.26.0, K1 Lookup since v1.27.0, and Overfit Check since v1.75.0) are grouped under a single **Tools** dropdown rather than sitting as separate top-level links; all of them also appear in the footer sitemap and homepage Explore grid. The ETF Cloner is lower-profile: it is live and indexable and appears in the footer sitemap + homepage Explore card, but at the user's request is intentionally held out of the primary nav (including the Tools dropdown). As of v1.15.4 no page carries a `noindex` robots meta.

**K1 Lookup data flow (v1.27.0):** the tool takes a ticker and answers whether holding it issues a
Schedule K-1 instead of a 1099. **The lookup is entirely local.** `k1.html` reads `data/k1.js`
(falling back to `fetch` of `data/k1.json`), matches the typed ticker against the object, and renders
the row. There is no network call at lookup time, which is why the answer is instant and why the page
works from `file://` and offline.

**The database is the primary path, and it is the only reviewed one.** etfdb.com sits behind
Cloudflare bot mitigation and sends no `access-control-allow-origin` header, so the page cannot read
it directly. `scripts/refresh_k1.py` fetches on a maintainer's machine and the site ships the
answers, which is why a hit is instant, works offline, and has been through a human.

**A live fallback covers a miss (v1.27.6).** Where a ticker is absent from the shipped database, the
browser fetches etfdb through `r.jina.ai`, a reader service that renders the page server-side and
**does** send CORS headers. It was chosen on measurement, not preference: `proxy.cors.sh` returns
Cloudflare's "Just a moment..." challenge, `codetabs` returns 522, `allorigins` times out,
`corsproxy.io` is paid-only, and `cors.lol` rate-limited on the first request. `r.jina.ai` returned
200 with usable content, and its extraction preserves both the `Structure` field and the capital
gains rates.

**A live answer is badged and never mistaken for a database answer.** It carries a `live, unverified`
chip, says in full that it was parsed in the browser just now from a third party's rendering and that
nobody has reviewed it, and runs the same structure-versus-rates corroboration, so a live row can
report its own disagreement.

**Two costs the owner accepted explicitly on 2026-08-27**, after both were put to them: each fallback
lookup sends the visitor's ticker to `r.jina.ai`, a third party, so a query leaves the browser in a
way nothing else on this site does; and the free tier is rate-limited and undocumented, so the
fallback can degrade without warning. The page reports a rate-limit as a rate-limit rather than as
"not found".

**The fallback cannot always answer, and must not guess when it cannot.** Some funds have no
`Structure` field on etfdb at all: `DRAM` (Roundhill Memory ETF) is the worked example. **The
capital gains rates are deliberately not used as a substitute signal.** `SOYB` and `TAGS` are
commodity pools that genuinely issue K-1s and publish `39.60%/20.00%`, the ordinary-rate signature,
so inferring "no K-1" from ordinary-looking rates would produce a confident wrong answer about
someone's taxes. The page says there is no answer instead.

**`FORMS` in `k1.html` duplicates `TAX_FORMS` in `scripts/refresh_k1.py`.** Two copies of one fact,
accepted because the alternative is shipping a data file to describe five strings. Change both in
the same commit.

**Clicking a ticker in the table looks it up (v1.27.6).** The cell is a real `?t=` link, so it can be copied, opened in a new tab and reached by keyboard; a plain click is intercepted and answered in place, and a modified click is left alone. The columns are **Ticker, K1, Name**.

**Three outcomes, deliberately distinguished.** A ticker in the database renders its verdict, its
structure, its tax form, both capital-gains rates and a link to verify by hand. A ticker recorded as
`not_found` says it is not an exchange-traded product on record. A ticker the database has never seen
says exactly that, **"not in this database yet, which is not the same as saying it has no K-1"**, and
offers the source link. The third case is the one worth getting right: silently answering "No" for an
unknown ticker would be a wrong answer about someone's taxes dressed as a confident one.

**The fund table below the lookup (reworked v1.27.2).** It lists **every** fund in the database,
not only the K-1 issuers, with three columns: Ticker, Name, K1. Three pills filter it (All, K-1,
No K-1) and a toggle collapses it. **It ships collapsed**, because it is 184 rows and the lookup box
is what the page is for; the table is reference material underneath it. Picking a filter while
collapsed expands the table, since a filter button that appears to do nothing is worse than an
unrequested expansion.

**Rows recorded as `not_found` are counted but never listed.** These are tickers that were checked and turned out to have no etfdb fund page, so there is no structure to read. The footnote states how many were excluded, so the number is not silently missing. **Individual stocks were removed from the database entirely at v1.27.5** and `data/k1_seed.txt` says they do not belong in it; the one row left is VBF, a closed-end fund rather than an ETF.

**All three columns sort (v1.27.4).** Clicking a header sorts by it; clicking the active header flips direction. A new column always starts ascending rather than inheriting a direction chosen for a different column. **Ticker is both the default sort and the tiebreak on every other column**, which makes the order total: two rows never swap places between renders of the same data. Sorting and filtering are independent, so a sort survives a filter change and vice versa.

**The filter, sort and collapsed state persist in `localStorage`** under
`composer-atlas.k1.view.v1`, matching the `composer-atlas.<page>.<thing>.<version>` key convention
`signal-miner.html` already uses. This is a per-viewer convenience, not user data: it never leaves
the browser, is never sent anywhere, and is never read back by anything but this page. **Every
access is wrapped**, because a private window or a browser set to block site data throws on the
accessor itself rather than returning empty, and the stored value is validated rather than trusted
so a stale or hand-edited entry cannot put the page into a state it has no button for. Under
`file://` the write throws and is swallowed, so the page works and simply forgets between visits.

**Nodes data flow (v1.26.0):** the tool takes a symphony URL, ID, or pasted JSON, walks the tree
from the `/score` endpoint, and counts nodes. It has no data file and no server component. **The
fetch is the hard part:** Composer's API answers the score request with HTTP 200 and **no
`access-control-allow-origin` header**, so a browser cannot read the response directly. The page
therefore tries four sources in order, direct first (so it starts working on its own the day
Composer adds the header), then the same three public relays the ETF Cloner uses (`proxy.cors.sh`,
allorigins, codetabs), and falls back to a link to the raw JSON plus a paste box if all four fail.
**Two of the three relays were returning 502/522 during the v1.26.0 build**, so the URL path
currently rests on `proxy.cors.sh` alone; the paste fallback is the reason that is survivable rather
than fatal. A relay that reaches Composer passes its status through, so a 404 is reported as "no
such symphony" rather than as a relay failure, since the two have completely different fixes.

**ETF Cloner data flow:** the tool has two independent input paths, both fully client-side. (1) **Live fetch by ticker**: reads a fund's top ~25 holdings from stockanalysis.com's SvelteKit `__data.json` route via a CORS relay (`proxy.cors.sh`, with allorigins/codetabs fallbacks), since issuer files and most holdings APIs are CORS-blocked or key-gated. (2) **Full-basket upload**: the user downloads the issuer's own holdings file (a top-level download, not a `fetch()`, so CORS never applies) and drops it in; CSV is parsed directly, and `.xlsx` is unzipped natively in the browser (`DecompressionStream('deflate-raw')` + `DOMParser`, no library) with a generic column-mapper that locates the Ticker/Weight/Name columns across issuer layouts. Both paths filter out non-company line items (cash, futures, collateral, pending dividends, currency, which can carry tickers that collide with real securities, e.g. cash "USD" vs. the USD ETF), normalize share-class tickers to Composer/Crescendo format (a trailing `.X`/`-X` class suffix becomes `/X`, e.g. `BRK.B`/`BRK-B` → `BRK/B`, in `cleanSym()`, since the dot/dash forms will not save or backtest on either platform, v1.16.7), renormalize weights across the remaining companies, and emit a Composer symphony (`root` → `wt-cash-specified` or `wt-cash-equal` → `asset` nodes). Nothing is uploaded anywhere; there is no server component and no committed data file for this tool.

### Navigation & Linking Model (v1.15.3)

Three link surfaces, each with a distinct, deliberate rule. When adding a new page, decide its placement against all three:

1. **Primary nav (`links` array in `renderNav`, `js/app.js`)**: *curated*, not exhaustive. Holds Home plus the main destinations, then the external CTAs (Azqato Invests, Support). As of v1.16.3, the tools (RSI Signals, Signal Miner, Converter, and since then Nodes, K1 Lookup and Overfit Check) are collapsed under a single **Tools** dropdown group, an item with a `children` array renders as a hover/click dropdown, to keep the top level short. Deliberately omits the lowest-profile utility (ETF Cloner) even from the Tools dropdown. Adding a page here is an editorial choice, not automatic.

2. **Footer (`renderFooter`, `js/app.js`)**: the **complete sitemap**. It must link *every* public-facing page on the site: Home and all internal pages (Strategies, Database, RSI, Signal Miner, Glossary, Converter, ETF Cloner, About), followed by external links (Support, Composer.trade). `404.html` is the only page excluded on principle (it is an error page, not a destination). When you add any public page, you **must** add it to the footer. As of v1.16.3 there is no exception, `etf-cloner.html` is now in the footer, closing the earlier temporary deferral.

3. **Homepage "Everything on this site" Explore grid (`index.html`)**: one card per **self-built tool or content section** we own. Concretely: a card for every *internal* footer link that is a tool/section we built, i.e. every internal footer link **except** Home (the page itself) and About (a static info page, not a tool). External links never get cards. Current set: Strategies, Database, RSI, Signal Miner, Glossary, Converter, ETF Cloner. The grid uses `.grid-3` (three columns; seven cards); update the count word in the section subhead ("Seven ways...") when it changes.

**Rule of thumb when shipping a new page:** always add it to the footer (rule 2); add an Explore card if it is a tool/section we built (rule 3); add it to the nav only if it is a primary destination (rule 1).

### GitHub Actions Deploy Pipeline

**This workflow publishes the GitHub Pages MIRROR, not the live site.** Cloudflare Pages builds
independently on the same push and is canonical. A red build here does not take the site down, and
a green one does not prove the site updated; `scripts/check_live.py` exists for the second half.

```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: pages
  cancel-in-progress: false

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Check inline JS syntax
        run: python3 scripts/check_html_js.py
      - name: Check the Composer export shape
        run: python3 scripts/check_composer_ladder.py
      - name: Check the database primary key and summary sync
        run: python3 scripts/check_database_keys.py
      - name: Check the strategy extras join
        run: python3 scripts/check_strategy_extras.py
      - name: Check served file sizes against Cloudflare's limit
        run: python3 scripts/check_asset_sizes.py

      - name: Setup Pages
        uses: actions/configure-pages@v5

      # KEEP THIS LIST IN STEP WITH .assetsignore. Two separate mechanisms for
      # one intent, and neither reads the other.
      - name: Build deploy folder
        run: |
          mkdir -p _site
          rsync -a \
            --exclude='.git' \
            --exclude='.github' \
            --exclude='_site' \
            --exclude='docs' \
            --exclude='scripts' \
            --exclude='data/symphony_scores.json' \
            --exclude='data/database.json' \
            --exclude='data/database.js' \
            --exclude='README.md' \
            --exclude='.gitignore' \
            . _site/

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: '_site'

      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

**The snippet above is abridged only in its comments.** `deploy.yml` carries a paragraph of reasoning
above most steps, explaining the specific incident each one exists to prevent. Read the file, not
this copy, before changing a step.

**Pre-deploy checks.** **Five** Python scripts gate the publish, added between v1.22.7 and v1.43.2.
They run before anything is built, so a failure leaves the previously deployed, working site
untouched. Every one of them exists because the failure it catches had already shipped, and because
each of those failures is invisible from outside: the page returns HTTP 200 and looks correct.

| # | Gate | Catches | Documented in |
|---|---|---|---|
| 1 | `check_html_js.py` | An inline `<script>` killed by a syntax error, on a page that still serves 200 with its static HTML intact (v1.22.2) | Below |
| 2 | `check_composer_ladder.py` | Miner output that is syntactically perfect and structurally wrong, so Composer rejects the import (v1.22.5) | Below |
| 3 | `check_database_keys.py` | A duplicate `symphony_id`, a `database_summary.json` out of step with `database.json`, or a symphony missing from `storage.csv`. The first shows one symphony twice everywhere; the second makes real symphonies invisible. Both have happened (v1.25.1, v1.25.2) | Section 12, "The Primary Key Invariant" |
| 4 | `check_strategy_extras.py` | A stale or half-committed `strategy_extras` join, which renders a correctly laid out strategy page with its new sections silently empty. Demands byte equality with **both** twins, so it also catches the `.json`/`.js` drift that gate 3 does not (v1.27.9 shipped exactly that) | Section 14, V1.20 |
| 5 | `check_asset_sizes.py` | Any served file past Cloudflare's 25 MiB per-file limit, which fails the **entire** deployment. That is how the site silently stopped updating on 2026-09-01 (v1.43.2) | Section 25, closed question 2 |

**Gate 5's honest limitation, recorded because it reverses the usual logic.** This workflow publishes
to GitHub Pages and is not the live path, so failing here cannot stop the Cloudflare build, which
runs independently on the same push. What the gate buys is a legible red X naming the offending file
and its size, instead of an opaque failure in a dashboard nobody watches.

**Three more checkers exist and deliberately do not gate**, by owner ruling on 2026-09-02:
`check_prose_tokens.py` gates metric tokens in authored prose, while `check_risk_profiles.py` and
`check_stat_drift.py` run, report, and cannot block. `check_social_tags.py` is manual by the ruling on
open question 27. See Section 14, V1.20 item 10b for the reasoning and the full gated/advisory table.

`scripts/check_html_js.py` tokenizes every inline `<script>` in the repo's HTML and rejects two things: a `'` or `"` string that runs past end of line, and unbalanced brackets. It exists because of the v1.22.2 outage, where an apostrophe inside `'Ignore BIL's Sortino...'` closed the string early, the stray quotes re-paired so brackets still balanced, and the entire inline script died. The page still served HTTP 200 with its static HTML intact, so nothing downstream could tell. There is no JS runtime in this toolchain, so `node --check` is not an option; this is the substitute. It understands line and block comments, template literals with nested `${...}`, and regex literals, the last being necessary because converter.html and etf-cloner.html both carry a JSON-highlighting regex holding unbalanced brackets and quotes. Run bare it checks every `*.html` in the repo root; `--self-test` runs 13 built-in cases, including the real outage string, and the full run executes them too so a checker that has stopped working cannot pass silently.

**Its one known blind spot, deliberately recorded as a passing self-test case:** an intruding quote whose strays all re-pair *before* end of line is invisible. `s = "he said "hi" to me";` is a genuine syntax error this tool calls clean. What made the outage catchable is that its re-pairing left a string running off the end of the line. Closing that gap needs a real JS parser.

`scripts/check_composer_ladder.py` covers the v1.22.5 class of bug, which is structurally wrong but syntactically perfect output. It holds a Python port of `buildComposerLadder` and walks the emitted tree asserting the invariant Composer requires: every `if` has exactly two children, every else holds exactly one thing, rungs nest in Calmar order with NaN last, each rung keeps its own target and conditions, and the deepest else is BIL. Because a port can drift from the JS it mirrors, and because the *original* port's failure was asserting the shape the builder produced rather than the shape Composer requires, it first runs a **source guard**: five regexes over `signal-miner.html` confirming the exporter still has the shape the port describes. Change the builder without updating the port and the guard fails by name. Verified by temporarily reverting the exporter to the flat shape and confirming the guard caught it.

### Performance Targets

| Metric | Target |
|---|---|
| Lighthouse Performance | 85+ |
| Lighthouse Accessibility | 90+ |
| Largest Contentful Paint (LCP) | < 2s (desktop) |
| Total page weight (home) | < 500KB uncompressed |
| JS shipped to client | < 15KB (app.js + page scripts) |

### Browser Support

Chrome 100+, Firefox 100+, Safari 15+, Edge 100+. No IE11. Requires: `fetch()`, `URLSearchParams`, CSS custom properties, `async/await`.

### Future Technical Considerations

| Feature | Approach |
|---|---|
| Client-side search | Fuse.js filter over loaded JSON |
| Tag filtering on index | Vanilla JS DOM filter |
| Performance charts | Chart.js or uPlot: loaded as a module script |
| Build system upgrade | Migrate to Astro 5.x |
| Analytics | **Cloudflare Web Analytics**, injected by the host at serve time on the canonical domain. Cookieless, collects no personal data and sets no client storage; adds about 359 bytes per page. Accepted by the owner, and settled: it is not to be re-raised as a privacy concern. Per Section 4 the site still collects no user data of its own |

> **Discrepancy (found 2026-08-24).** This row previously read "None currently. If ever added, it
> must be cookieless and collect no personal data (e.g. Plausible)". The requirement it stated was
> met, by a different product than the one it named: Cloudflare Pages injects its own Web Analytics
> beacon into every response on `composeratlas.com`, so the committed HTML has no analytics tag but
> the served HTML does. The row is corrected above rather than annotated, because the original text
> asserted an absence that is simply no longer true, and the policy it set is satisfied.

---

## 11. Operational Runbook

### Local Development Setup

**Prerequisites:** Python (any version), Git. No Node.js required.

**Option 1; Python HTTP server:**
```bash
python -m http.server 8000
# Site at http://localhost:8000/
```

**Option 2; Open directly:** Double-click any `.html` file. Site loads fully because `data/strategies.js` and `data/glossary.js` are loaded as script tags before `app.js`.

**Validate JSON before committing:**
```bash
python -c "import json; json.load(open('data/strategies.json')); print('Valid JSON')"
python -c "import json; json.load(open('data/glossary.json')); print('Valid JSON')"
```

---

### Adding a Strategy from a Composer URL (Streamlined: Preferred)

Provide a Composer.trade symphony URL to Claude Code and it automates the entire workflow.

**What you need to provide:**
- A Composer.trade symphony URL (any form: `/symphony/ID`, `/symphony/ID/factsheet`, `/symphony/ID/details`)
- Optional: preferred strategy name and slug (if omitted, Claude Code proposes them and asks for confirmation)

**What Claude Code does automatically:**
1. Extracts the symphony ID from the URL
2. Fetches backtest metrics via `POST /api/v0.1/symphonies/{id}/backtest` (no auth required)
3. Fetches the logic tree via `GET /api/v0.1/symphonies/{id}/score`
4. **Reads the ENTIRE logic tree, end to end, before writing any content** (see "Full-tree rule" below). Every branch, threshold, sort/select node and leaf allocation is traced, not sampled, to determine: primary trend gate, volatility routing, dip-buy conditions, cross-asset signals, correct canonical tags
5. Drafts all content fields per the "Content roles and factual bar" below: `description`, `ai_summary`, `how_it_works`, `signals`, `risk_profile`
6. Proposes name and slug; asks for confirmation before inserting
7. Inserts the complete entry into `data/strategies.json` and `data/strategies.js`
8. Adds the `ai_summary` to `scripts/add_ai_summary.py` under the new slug
9. Runs `python scripts/add_ai_summary.py` to write the summary into both data files. **Any performance figure in the summary is a token** (`{sharpe_ratio}`, `{max_drawdown_abs:0}`); see the Strategy JSON Schema section. The script is the canonical store, so a figure typed here as a literal survives every later refresh as a stale number.
10. Updates `docs/PATCHNOTES.md`

**Example usage:**
```
"Add this strategy: https://app.composer.trade/symphony/K8ql2SKFd4VDBemIstEr/factsheet
 Name: s90 50/40 maxDD (Half Low Catch), slug: s90-half-low-catch"
```

**Full-tree rule (curated strategies, mandatory from v1.38.x on).** For any curated strategy, the full logic tree MUST be read end to end before drafting or revising its page content. Do not characterize a strategy from the top few branches, the instrument list, or the name. Large trees are not truncated for curated work: if the `score` response is too large for one read, fetch and traverse it in parts until every node has been seen. The goal is that every factual statement on the page is verified against the specific tree, not generally plausible. (Truncation remains acceptable only for bulk, non-curated database analysis.)

**Content roles and factual bar.** The strategy page stacks three prose blocks, which must not repeat each other:
- **`description` (the Introduction, the lede):** 2 to 4 sentences. What it is, its provenance/positioning, the one-line core idea, and who it is for. No indicator-by-indicator mechanics, no metrics.
- **`ai_summary` (the analyst's read):** two paragraphs, interpretive not descriptive. Paragraph 1 = the single real bet the strategy is making once complexity is stripped away, its character, how to think about it. Paragraph 2 = an honest appraisal with the metrics and three to four caveats (regime dependence, drawdown reality, overfitting risk, window bias). References mechanics lightly; never re-lists the logic tree.
- **`how_it_works` (the mechanics):** the only home for the enumerated logic tree, indicators, thresholds and pools.

Every sentence across all blocks must clear this factual bar: **metrics** are written as tokens rather than typed, so they match the stored numbers by construction (`check_prose_tokens.py` gates this, and `check_stat_drift.py` remains as the advisory that catches a newly hand-typed figure); **mechanics** come only from the traced logic tree; **provenance** claims are limited to what `author_note` and the source symphony record support (named authors, name-match counts) with no invented edit histories, adoption stories, or motivations; **interpretation** is allowed only as clearly analytical framing ("best understood as a bet that..."), never asserted as historical fact.

**Known limitations:**
- Short backtests (<1 year) yield metrics sensitive to the covered market period; surfaced in `risk_profile` and `author_note`
- Always review drafted content and correct any characterizations that do not match the strategy's actual intent

---

### Hiding a Strategy

Set `"hidden": true` on the entry in **both** `data/strategies.json` and `data/strategies.js`
(or set it in the JSON and re-run `scripts/add_ai_summary.py`, which rewrites both), then re-run
`python scripts/build_sitemap.py` and update the Curated count in `index.html`.

**Hidden means unlisted, not deleted, and that distinction is the whole point.** The entry keeps
every field, so un-hiding is deleting one key. The detail page keeps rendering, because these slugs
have been live for months and carry inbound links: unlisting is reversible and a 404 is not.

**All filtering happens in `loadStrategies()` in `js/app.js`, deliberately.** That function is the
single choke point every listing path already went through, so a new grid, filter or count added
later cannot leak a hidden strategy by forgetting to filter. The detail renderer in
`strategies.html` calls `loadAllStrategies()` instead, which is the only caller that should.

**Hidden strategies are still refreshed.** `update_metrics.py` and `build_strategy_extras.py` both
operate on the full file, so a hidden entry's metrics stay current and it can be un-hidden without a
data catch-up. `check_strategy_extras.py` therefore still expects a join over all 36.

**Select by tag, not by slug pattern.** The first attempt at the v1.41.0 hide matched
`^zoops-.*-2026$` and silently found 11 of 12, because `zoops-2026-frontrunner` carries the year in
the middle of its slug. An assertion on the expected count caught it. Slugs are not a taxonomy.

---

### Adding a New Strategy (Manual)

Use when you prefer full control or the Composer API is unavailable.

**Step 1: Gather metrics.** Collect all required fields from Composer.trade. See the schema in Section 12.

**Step 2: Generate a slug.** Derive from the strategy name: lowercase, spaces → hyphens, remove special characters. Examples: "VIX Tier Rotator" → `vix-tier-rotator`. Do not change a slug after a strategy page is live, it breaks inbound links.

**Step 3: Update both data files.** Append to `data/strategies.json`, then make the identical addition to `data/strategies.js` (inside the `window.STRATEGIES_DATA = [...]` array).

```json
{
  "slug": "strategy-slug-here",
  "name": "Strategy Name Here",
  "symphony_url": "https://app.composer.trade/symphony/SYMPHONY_ID/details",
  "symphony_id": "SYMPHONY_ID",
  "annualized_rate_of_return": 0.000,
  "max_drawdown": -0.000,
  "cumulative_return": 0.000,
  "calmar_ratio": 0.00,
  "sharpe_ratio": 0.00,
  "standard_deviation": 0.000,
  "min": -0.000,
  "mean": 0.000,
  "median": 0.000,
  "max": 0.000,
  "trailing_one_month_return": 0.000,
  "trailing_three_month_return": 0.000,
  "trailing_one_year_return": 0.000,
  "backtest_days": 0,
  "description": "Plain-English description. 1-3 sentences. No HTML.",
  "tags": ["tag1", "tag2"],
  "last_updated": "YYYY-MM-DD",
  "ai_summary": ["AI analysis paragraph 1 (structure, assets, logic, why follow it).", "AI analysis paragraph 2 (metrics, backtest period, noteworthy characteristics)."],
  "how_it_works": ["Paragraph 1.", "Paragraph 2.", "Paragraph 3."],
  "signals": [
    { "name": "Signal Name", "tag": "related-tag", "description": "What this signal does." }
  ],
  "risk_profile": "Risk level and description."
}
```

**Step 4: Add the AI Summary to the script.** Open `scripts/add_ai_summary.py` and add an entry for the new slug to the `AI_SUMMARIES` dict. This is required: the script is the canonical store for all summaries, and if you skip this step, future runs of the script will warn and may overwrite or miss the new entry. See "Generating the AI Summary" in Section 11 for format and tone guidance.

```python
"strategy-slug-here": [
    "Paragraph 1: structure, assets, logic, and why someone would follow it.",
    "Paragraph 2: metrics, backtest period, and any noteworthy characteristics.",
],
```

Then run the script to write the summary into both data files:
```bash
python scripts/add_ai_summary.py
```

**Step 5: Verify tags.** Confirm every tag has a matching glossary entry. See the tag vocabulary in Section 12.

**Step 6: Test locally.**
```bash
python -m http.server 8000
# Navigate to http://localhost:8000/strategies.html?slug=strategy-slug-here
```

**Step 7: Update PATCHNOTES.md.** Add a versioned entry.

**Step 8: Commit and push.**
```bash
git add data/strategies.json data/strategies.js scripts/add_ai_summary.py docs/PATCHNOTES.md
git commit -m "feat: add [Strategy Name] strategy"
git push origin main
```

---

### Updating Metrics (Script)

`.github/workflows/update-metrics.yml` runs `scripts/update_metrics.py` automatically every day and commits any changes, then rebuilds `data/strategy_extras.json`/`.js` (v1.31.1, see Section 14 V1.20 item 1) because the script rewrites `strategies.json`, which that join reads. The script skips any strategy whose `last_updated` is under `STALE_AFTER_DAYS` (7) old, so most daily runs are a no-op except for retrying anything that failed on a previous run. No manual action is required for routine refreshes.

To force an immediate refresh (e.g. after a symphony logic change), run manually:

```bash
python scripts/update_metrics.py
```

This script:
1. Hits `POST /api/v0.1/symphonies/{id}/backtest` for all strategies not refreshed in the last 7 days → rewrites `data/strategies.json` and `data/strategies.js`
2. Hits `GET /api/v0.1/symphonies/{id}/score` for the same strategies → rewrites `data/symphony_scores.json`

No API key required. After a manual run:

```bash
git add data/strategies.json data/strategies.js data/symphony_scores.json
git commit -m "data: refresh metrics and symphony scores - YYYY-MM-DD"
git push origin main
```

**symphony_scores.json is for AI analysis only**: it is not served to the website. It contains the full EDN logic tree for each symphony, used to explain strategy logic in future conversations.

---

### The weekly data pipeline, and why it runs in this order

Three scheduled jobs feed each other, and since 2026-09-06 they run on three consecutive evenings in
dependency order. Each stage reads what the one before it wrote, so **moving any of the three means
checking the other two.** Each workflow file names its own position in the chain for exactly that
reason.

| Order | Workflow | Cron (UTC) | Pacific | Runtime | Writes | Read by |
|---|---|---|---|---|---|---|
| 1 | `refresh-prices.yml` | `7 2 * * 6` Sat 02:07 | Fri 7:07pm | ~90s | `data/prices.json` | Signal Miner, `refresh-oos.py` |
| 2 | `refresh-full-database.yml` | `7 1 * * 0` Sun 01:07 | Sat 6:07pm | 4.5-5 h | `database_summary.json` | the site, `refresh_oos.py` |
| 3 | `refresh-oos.yml` | `7 3 * * 1` Mon 03:07 | Sun 8:07pm | ~2.7 h | `data/oos.json` | the Leaderboard, `build_overfit.py` |

**Why prices go first.** The Friday close lands at 1pm Pacific, so a Friday evening run picks it up
the same day rather than waiting a night. Everything downstream is that much fresher.

**Why out-of-sample goes last.** It has two inputs and this slot is downstream of both. Its candidate
set is derived from the in-sample scores the full refresh writes, and its measurement window ends on
the last date in `prices.json`. **A third input was added in v1.76.0 and it is deliberately not a
scheduling constraint:** `data/strategies.json` exempts curated symphonies from the score cutoff, and
it is a hand-edited file with no job writing it, so it is current whenever the job runs. Under the schedule it briefly held on 2026-09-06 (OOS on Friday) that
window lagged about a week; in this order it lags two days.

**No two jobs overlap**, which matters because two of them are long API jobs against the same
unauthenticated host at the same 2-second throttle. Prices is short; the full refresh runs 01:07 to
about 06:07 UTC Sunday; out-of-sample runs 03:07 to about 05:50 UTC Monday. GitHub cron is UTC only
and does not follow daylight saving, so all three drift an hour earlier in Pacific terms each winter.
Nothing in the chain depends on the local hour.

**A caveat that applies to all three:** GitHub's scheduler is best-effort on public repositories.
Runs are frequently late and can be dropped entirely. Every job here checkpoints and resumes, so a
missed run costs freshness rather than data.

### Updating the Full Database (Script, Automated)

`.github/workflows/refresh-full-database.yml` (added v1.12.0) runs `scripts/refresh_full_database.py` automatically every **Sunday at 01:07 UTC** and commits any changes, plus regenerates and commits `data/database_summary.json`/`.js` (via `scripts/export_summary.py`) so the live site's actual data source stays in sync, plus rebuilds and commits `data/strategy_extras.json`/`.js` (via `scripts/build_strategy_extras.py`, added v1.31.1) because the refresh rewrites `database.json`, which that join reads. No manual action required for routine refreshes.

**This is a meaningfully heavier job than `update-metrics.yml`'s daily run.** `STALE_AFTER_DAYS` (7) matches this workflow's weekly cadence exactly, so essentially the entire ~6,600-row full database is "due" on every run, not just a handful of stragglers, at the proven-safe 2-second-per-call throttle (Section 13, Rate Limits), that's roughly 4.5–5 hours, close to GitHub's 6-hour job ceiling. The workflow's refresh step has its own 340-minute timeout with `continue-on-error: true`, and the summary-regeneration/commit steps run with `if: always()`, so if a run gets cut short, whatever `refresh_full_database.py` already checkpointed to disk (every 10 rows, per its own docstring) still gets committed rather than lost, the next Sunday's run picks up whatever's still stale via the normal staleness check. GitHub Actions minutes are unmetered for public repositories on GitHub-hosted runners, so the long weekly runtime has no cost implication.

`Full Database.xlsx` is deliberately **not** regenerated/committed by this workflow, it's documented as a local-only, occasional-use review artifact (see `scripts/export_full_database_to_xlsx.py`'s docstring), not part of the site's data pipeline, and not worth the binary-diff churn in git history on a weekly cadence. Regenerate it manually when wanted.

To force an immediate full-database refresh, either trigger the workflow manually (GitHub → Actions → "Refresh Full Database" → Run workflow) or run locally:

```bash
python scripts/refresh_full_database.py
python scripts/export_summary.py
git add data/database.json data/database.js data/database_summary.json data/database_summary.js
git commit -m "data: refresh full database - YYYY-MM-DD"
git push origin main
```

**Reminder, scope boundary:** this workflow runs `refresh_full_database.py` only. `scripts/flag_name_noise.py` and `scripts/dedupe_symphonies.py` (V1.14 Part A) remain manual-only and must never be added here or to any other scheduled/CI job, see "Name-Based Noise & De-Duplication" above for why.

---

### Submitting New Symphonies (`data/AddSymphony.csv`)

**Added 2026-07-15.** A single-column CSV (`url`, matching `storage.csv`'s existing format) where the user drops new Composer symphony URLs to submit for inclusion in the full database, outside of the original bulk-scrape/sync pipeline. Manual-only by design, same posture as `flag_name_noise.py`/`dedupe_symphonies.py`: this is never run automatically or from a scheduled workflow.

**Workflow, run only when the user explicitly asks (e.g. "check AddSymphony.csv"):**

1. Read every URL currently in `data/AddSymphony.csv`.
2. Check each one against `data/storage.csv` (the durable, deduped URL backup, one row per unique symphony ever seen) to filter out anything already present.
3. Append the surviving (genuinely new) URLs to `data/storage.csv`.
4. Add the same new URLs to `data/database.json` as new, unrefreshed entries, matching `scripts/sync_storage_to_database.py`'s row shape (every field null except `symphony_url`/`symphony_id`). **Do NOT actually run `scripts/sync_storage_to_database.py` for this**: see the warning immediately below. Add the specific new rows directly instead.
   - **⚠️ `storage.csv` is deliberately larger than `database.json`, by design, confirmed 2026-07-15:** `storage.csv` retains URLs for symphonies that were later **purged** from `database.json` (see "Purging Flagged Full-Database Entries" below, 1,004 permanently-404/422-broken rows were removed from `database.json` outright in v1.11.14, but their URLs were deliberately kept in `storage.csv` forever, per its own "never lose a URL once seen" design). Running `sync_storage_to_database.py` blindly does not distinguish "genuinely new URL" from "URL that was intentionally purged as dead", it will resurrect every purged dead entry as a new unrefreshed row. This actually happened: running it to process 10 new `AddSymphony.csv` URLs pulled in 1,055 stale/purged entries instead of 10. Reverted (nothing was committed) and redone by adding just the specific new rows directly. **If `sync_storage_to_database.py` is ever run for real, sanity-check the entry-count delta against the number of genuinely new URLs before proceeding to refresh/commit**: a large mismatch means purged entries are being resurrected.
5. Manually update the affected stats: run `scripts/refresh_full_database.py` (will pick up the new unrefreshed rows on its normal staleness check) or refresh just the new rows, then `scripts/export_summary.py` to regenerate `database_summary.json`/`.js`, then commit.
6. Clear `data/AddSymphony.csv` back to just its header row once processed, so it doesn't get re-processed on the next pass.

**The inbox can arrive id-keyed, not URL-keyed.** The 2026-09-01 batch was a `strategy_id` column of bare 20-character ids (with an instruction sentence sitting in row 1, not a real id), not the `url` column the section above assumes. `scripts/id_to_url.py` (added v1.39.1) is the reusable converter for this: `id_to_url()` builds the canonical `/details` URL that `storage.csv` expects, `url_to_id()` goes back, and it runs as a module or a CLI. Filter the inbox to valid 20-character ids first so a header/instruction row never becomes a malformed URL. Match each store on its own primary key while filtering (Section 14, The Primary Key Invariant): `symphony_id` for `database.json`, `url` for `storage.csv`.

**Second run (v1.39.1, 2026-09-01).** 6,358 valid ids in the inbox; 142 new to `storage.csv`, 147 new to `database.json`. Appended the 142 URLs to storage, seeded the 147 skeleton rows directly (not via `sync_storage_to_database.py`, per the warning above), then backtested **only those 147** rows and left the rest of the database alone. Result: 144 OK, 3 transient `retry`, 0 dead/`excluded`. Database 6,669 -> 6,816; storage 7,714 -> 7,856; `check_database_keys.py` passed. **On the refresh step, prefer a scoped refresh over step 5's first option whenever any existing rows are stale:** 155 existing rows were past the 7-day cutoff that day, so an unscoped `refresh_full_database.py` run would have swept them in too, violating the "new ids only" scope. The scoped run imported `post`/`apply_backtest_result`/`write_js` from `refresh_full_database.py` and iterated only the newly-seeded rows, reusing the canonical schema logic without triggering the staleness sweep.

**Third run (2026-10-07).** A single-id batch: `QH3TPPhXHg3cB9xhXUGF`, "Discover Slop". New to both
stores. Appended to `storage.csv`, seeded as a skeleton, scoped-refresh of that one id, 1 OK and 0
failures; database 6,816 -> 6,817, storage 7,856 -> 7,857. Mirror was a no-op, summary regenerated,
`check_database_keys.py` passed, inbox cleared back to its header. **The runbook below held with no
changes**, which is the point of having written it down: a one-row batch is the same five steps as a
147-row one, and the temptation on a single id is to hand-edit the JSON instead, which is how a row
ends up with a schema that does not match the other 6,816.

**Its metrics are extreme and that is not a data error.** ARR 3.33 with a Calmar of 20.08 over
**329 backtest days**. A sub-year backtest is exactly the regime the Overfit Detector exists to flag,
and the database stores what the API returned without editorialising. Nothing here promotes it to a
curated strategy, which is a separate workflow and a separate judgement.

**Before clearing the inbox, retry anything that never returned a backtest.** Step 6 destroys
the id list, so a row seeded but never successfully refreshed is easy to strand: it sits in
`database.json` as a skeleton with `flag: "retry"` and no `backtest_days`, and once the inbox is
cleared nothing points at it any more. It is recoverable (every id is in `storage.csv` forever, by
design) but nobody will think to look. Query the inbox ids for `backtest_days` in `(None, 0)` and
re-run those specific ids before clearing.

**Transient failures are worth retrying more than once.** On 2026-09-02, seven inbox ids had never
returned a backtest. A scoped re-run recovered **five of them**: they had failed on HTTP 500s that
were Composer's, not the symphonies'. Only two still failed, on repeated 500s across two attempts
20 seconds apart. A single failed call says nothing about whether a symphony is alive.

**500 is not 404.** A 5xx or 429 keeps `flag: "retry"`, because the symphony may be fine and the
server is not. Only 404 and 422 justify `flag: "excluded"`, which is the state that means the
symphony is genuinely gone. Do not promote a 500 to `excluded` to make a run look clean.

**Deliberately not automated:** matches the same reasoning already established for `flag_name_noise.py`/`dedupe_symphonies.py`: this touches `database.json` and should only ever run when explicitly invoked, never from a scheduled GitHub Actions job.

---

### Updating Metrics (Manual: Single Strategy)

1. Open `data/strategies.json` and `data/strategies.js`. Locate the entry by `slug`.
2. Update changed metric values. Set `last_updated` to today's date.
   - **Important:** `max_drawdown` is always stored as a negative number (e.g., `-0.432`, not `0.432`).
3. Validate JSON: `python -c "import json; json.load(open('data/strategies.json')); print('Valid JSON')"`
4. Commit: `git add data/strategies.json data/strategies.js && git commit -m "data: update metrics for [Strategy Name] - YYYY-MM-DD"`

---

### Adding a Glossary Entry

**Step 1: Add to both glossary files.**

Append a new entry to `data/glossary.json`, then make the identical addition to `data/glossary.js`.

```json
{
  "slug": "concept-slug",
  "name": "Concept Name",
  "category": "indicator",
  "description": "One-sentence description (under 160 characters).",
  "formula": "Optional formula string, or null",
  "related_tags": ["concept-slug"],
  "last_updated": "YYYY-MM-DD",
  "sections": [
    { "title": "Definition", "paragraphs": ["..."] },
    { "title": "How It Works", "paragraphs": ["..."] },
    { "title": "In Practice", "paragraphs": ["..."] },
    { "title": "Limitations", "paragraphs": ["..."] }
  ]
}
```

Valid `category` values: `"indicator"`, `"risk-metric"`, `"asset-class"`, `"strategy-concept"`

**Step 2: Tag related strategies.** Ensure relevant strategies in `data/strategies.json` include this concept's tag.

**Step 3: Test locally.**
```bash
python -m http.server 8000
# Navigate to http://localhost:8000/glossary.html?slug=concept-slug
```

**Step 4: Commit.**
```bash
git add data/glossary.json data/glossary.js data/strategies.json docs/PATCHNOTES.md
git commit -m "feat: add glossary entry for [Concept Name]"
git push origin main
```

---

### Removing a Strategy

1. Delete the entry from `data/strategies.json` and `data/strategies.js`.
2. Update `docs/PATCHNOTES.md` documenting the removal with a reason.
3. Commit:
```bash
git add data/strategies.json data/strategies.js docs/PATCHNOTES.md
git commit -m "remove: [Strategy Name] - [reason]"
git push origin main
```

---

### Regenerating the Sitemap

`scripts/build_sitemap.py` (added v1.25.1) writes `sitemap.xml` at the repository root. **Never hand-edit
`sitemap.xml`**; it is generated output and a manual change is lost on the next run.

```bash
python scripts/build_sitemap.py
```

**What it emits, and why nothing here is hardcoded:**

- **Every indexable top-level `.html` page**, discovered by globbing rather than from a list, so a new
  page appears in the sitemap without anyone remembering this script exists. Three exclusions:
  `404.html` (an error document, not a destination, the same principle that keeps it out of the
  footer sitemap in Section 6), any `_*.html` (local mockups and harness pages, gitignored and listed
  in `.assetsignore`), and any page carrying a `noindex` robots meta, currently only
  `signal-lab.html`.
- **One URL per curated strategy**, as `strategies.html?slug=<slug>`, read from `data/strategies.json`.
  These are genuinely distinct documents despite sharing one HTML file, because `strategies.html`
  sets a per-slug `<title>` and meta description at render time. The full community database is
  deliberately **not** enumerated this way: 6,669 query-string URLs of thin, near-identical rows is
  how a sitemap gets ignored.
- **`lastmod` only where it can be known.** Strategy URLs use each entry's own `last_updated` field;
  page URLs use the file's last commit date from `git log`. If git is unavailable or the file is
  untracked, the element is simply omitted. An absent `lastmod` is fine, a wrong one is worse than
  none.
- **No `changefreq` and no `priority`.** Google has stated it ignores both, and any value chosen for
  them is a guess.

**Run it after** adding or removing a page, after `scripts/update_metrics.py`, or after any change to
the curated set in `data/strategies.json`. Because page `lastmod` comes from git, regenerating
*after* the commit that changed a page gives a more accurate file than regenerating before it; this
is a minor inaccuracy, not a correctness problem, and is not worth a second commit on its own.

**Automated since v1.26.1.** `.github/workflows/update-metrics.yml` runs this script immediately
after `update_metrics.py` and commits `sitemap.xml` alongside the strategy data. That workflow is the
only one that writes `data/strategies.json`, so it is the only one whose output can staledate the 31
strategy `lastmod` values. Running by hand is still correct and still the right move after adding a
page, but forgetting no longer leaves the file wrong indefinitely: the next daily run repairs both
the strategy dates and the page dates.

> **`fetch-depth: 0` on that workflow's checkout is load-bearing, and removing it corrupts the
> sitemap silently.** Page `lastmod` comes from `git log -1 --format=%cs -- <path>`. On
> `actions/checkout`'s default shallow clone, the single fetched commit is grafted as the root, so
> git believes **every file in the tree was last modified in it**. The command does not fail and does
> not return empty; it returns *today's date, for every page, every day*. Measured on a real
> `--depth 1` clone of this repo at v1.26.1: all ten pages came back `2026-08-25`, against true dates
> ranging from `2026-06-22` to `2026-08-24`.
>
> That is the bad case, not the harmless one. `build_sitemap.py` omits `lastmod` when it cannot know
> the date, on the principle that an absent `lastmod` beats a wrong one, and a shallow checkout
> defeats that protection by handing it a date that is confidently wrong instead of missing. Every
> page would claim to have changed today, forever, which is precisely the signal `lastmod` exists to
> give and precisely the way to make a crawler stop trusting it. The cost of the fix is a full clone
> of a 122MB history on a daily job, weighed and accepted against publishing a daily lie.
>
> **This was written the other way round first**, predicting an empty result and a churning diff. It
> was only corrected because the shallow clone was actually made and the command actually run. Worth
> keeping as an instance of the repo's own rule: read the artifact, do not infer it.

**A deploy-time staleness gate was considered and declined at v1.26.1.** A fourth gate could
regenerate the sitemap in memory and fail the deploy if the committed file differed, which would
catch "added a page and forgot" at once rather than a day later. It was not built: it needs
`fetch-depth: 0` on `deploy.yml` too, slowing every deploy for a failure whose entire cost is one day
of a slightly stale `lastmod` on one page. The three existing gates all guard failures that are
silent *and* damaging; this one is neither.

**Only the canonical host gets a sitemap.** It points at `https://composeratlas.com`. The GitHub
Pages mirror is not given one on purpose, since it serves the same content and should not compete
with the canonical host for it.

---

### Refreshing the K-1 Database

`scripts/refresh_k1.py` (added v1.27.0) writes `data/k1.json` and `data/k1.js`, the database behind
`k1.html`. **Nothing automated runs it**, by choice: a fund's legal structure changes only when the
fund reorganises, so a daily or weekly job would spend thousands of requests to change nothing.

```bash
python scripts/refresh_k1.py                 # fetch anything missing or older than 180 days
python scripts/refresh_k1.py SOXL USO UVXY   # add or refresh specific tickers
python scripts/refresh_k1.py --seed          # add every ticker in data/k1_seed.txt first
python scripts/refresh_k1.py --all           # re-fetch every known ticker, ignoring staleness
python scripts/refresh_k1.py --inception-only # join inception dates only, fetch nothing
```

**`--inception-only` exists so refreshing dates cannot start an etfdb crawl by accident.** A bare
`python scripts/refresh_k1.py` refetches anything older than 180 days, so hanging the inception join
off the normal path would have meant that adding a date could touch 187 fund pages as a side effect.
The flag joins `data/ticker_inception.json` into `k1.json`, saves only if something changed, prints
the tickers still undated, and exits. It is idempotent: a second run reports 0.

**Adding tickers is the common case, and it is a two-file edit.** Put the new symbols in
`data/k1_seed.txt` (or pass them on the command line), run the script, then commit `data/k1.json`
**and** `data/k1.js` together. The `.js` twin is what the page reads over `file://`; committing one
without the other produces a page that works on the live site and silently shows stale data locally.

**It is slow on purpose.** One request at a time, 1.5 seconds apart, with a browser User-Agent
because the default urllib agent is refused. A full seed run of ~210 tickers takes roughly half an
hour. A checkpoint is written every 10 tickers, so an interrupted run keeps its progress and
re-running picks up where it stopped rather than starting over.

**Read the tail of the run, not just the exit code.** The script ends with two lists, and they mean
different things:

```
CONTESTED, etfdb's Distributes K1 flag disagrees with its own Structure field on 2: FOO, BAR
The page warns on these. Research each one and record the finding in OVERRIDES.
structure and tax rates disagree on 2: BAZ, QUX
Check those by hand before trusting them.
```

**The contested list is the one to act on first.** Those funds carry a warning on the live page
telling readers to go research the fund themselves, which is the right default and a poor permanent
state. Resolve one by reading the fund's own prospectus or annual report, or by checking whether its
issuer appears in EDGAR's register of 1940-Act funds, then record the finding in `OVERRIDES` in the
script. An override clears `contested`, so the page prints what was found instead of asking the
reader to find it again. **Do not resolve one by editing `data/k1.json`**: the next refresh silently
undoes it.

The rates list is the older, weaker signal: a non-empty one usually means the source page changed
shape rather than that a fund is misclassified.

**If a whole run comes back with unrecognised structures**, the parser's regexes no longer match the
page. `k1: null` renders as "unknown" rather than "no", so a broken run degrades to silence instead
of to wrong tax advice, but it still needs fixing rather than shipping.

**Run `python scripts/build_sitemap.py` only if you added a page**, not for a data refresh; `k1.html`
itself is already in the sitemap and a data change does not alter its `lastmod`.

### Purging Flagged Full-Database Entries

`scripts/purge_flagged_entries.py` (added v1.11.14) removes `data/database.json` entries by `flag` level, e.g. permanently-dead `excluded` (404/422) symphonies. Reusable for any future cleanse along the same lines, not a one-off script.

```bash
python scripts/purge_flagged_entries.py excluded
python scripts/purge_flagged_entries.py excluded retry caution   # multiple levels in one pass
```

**Safety invariant:** a purge candidate's `symphony_url` must already be present in `data/storage.csv` (the durable URL backup) before it's removed from `database.json`; the script aborts with no changes made if any candidate's URL is missing there, rather than silently losing the URL. Nothing is ever deleted outright, a purged row can always be re-promoted back into `database.json` later via `scripts/sync_storage_to_database.py`, unrefreshed.

Regenerates every downstream artifact in one run: `database.js`, `database_summary.json`/`.js` (via `scripts/export_summary.py`), and `Full Database.xlsx` (via `scripts/export_full_database_to_xlsx.py`: must not be open in Excel or this step fails with a `PermissionError`; close it and re-run that script by hand if so). Do not run while `scripts/refresh_full_database.py` is active in the background (same clobbering risk as other scripts that write `database.json`).

---

### Name-Based Noise & De-Duplication (V1.14 Part A)

Two scripts, run in sequence, implement the Part A policy (Section 14, V1.14 Part A):

```bash
python scripts/flag_name_noise.py       # run first
python scripts/dedupe_symphonies.py     # then this
python scripts/dedupe_symphonies.py 20  # optional LIMIT arg, for a small test run first
```

`scripts/flag_name_noise.py` (added v1.11.22) flags `TESTPORT #`/`[Work]`/`STILL BUILDING` non-strategy rows with `flag = "excluded"` (reuses the existing level rather than introducing a new one), no API calls. `scripts/dedupe_symphonies.py` (added v1.11.22) clusters the remaining clean (`flag == null`) rows by normalized name, confirms genuine duplicates via a logic-tree structural equality check (`GET /symphonies/{id}/score?score_version=v1`, one lightweight call per candidate row, falling back to metrics-tolerance comparison only if that fetch fails), and flags every loser in an identical group `flag = "duplicate"`: the keeper is chosen by longest `oos_date`, then earliest `symphony_id`. **Nothing is ever deleted by either script**: both only set `flag`/`error` on existing rows.

**Known limitation, the keeper is not always the copy people actually follow.** A manual spot-check (2026-07-15, 3 clusters / 19 rows) compared each cluster's keeper against the copy with the highest `size` (watcher count). Two clusters agreed: `TQQQ For The Long Term (Reddit Post Link)` kept the 1,242-watcher copy, and `KMLM switcher (single pops)` kept the 25-watcher copy, both the most-watched in their group. One did not: in the `V3.0.4.5 | Beta Baller + TCCC` cluster the `oos_date`/`symphony_id` tiebreak kept a copy with **8 watchers** while a structurally identical sibling had **173**. So the rule optimizes for the longest backtest history, which is the right call for metric quality, but it can flag as `duplicate` the copy the community actually follows. Not changed: watcher count is a popularity signal, not a correctness one, and making it the primary tiebreak would trade away backtest length. Worth revisiting only if a well-known symphony turns up missing from the Working view. (Recorded here from a throwaway audit spreadsheet, since the finding is the part worth keeping.)

Running `flag_name_noise.py` first matters: it removes `TESTPORT #`-prefixed rows from the dedup candidate pool entirely, so one can never win the `symphony_id` tiebreak and become the sole surviving "keeper" of a real strategy family. This is a sequencing choice, not special-case logic inside the dedup script itself.

**MANUAL-ONLY, do not automate.** `dedupe_symphonies.py` makes roughly one live API call per candidate row (hundreds per run) against Composer's unauthenticated API, and a full pass can take 20–30+ minutes. Neither script is wired into GitHub Actions, and neither should be, the deploy workflow excludes `scripts/` entirely, `update-metrics.yml` only ever runs `update_metrics.py` (the curated 36 strategies), and `refresh-full-database.yml` (added v1.12.0, see "Updating the Full Database" above) only ever runs `refresh_full_database.py`. Running this unattended on a schedule risks hammering Composer's API far more often than a human would choose to, with no one watching for rate-limit or correctness problems. Every full-database maintenance script in `scripts/` follows this same manual-only rule except `refresh_full_database.py`, which was deliberately opted into weekly automation as a distinct decision.

---

### Deployment Workflow

Composer Atlas deploys automatically via GitHub Actions on every push to `main`. No manual steps required.

- **Live URL:** https://composeratlas.com (Cloudflare Pages, linked directly to this GitHub repo)
- **Repository:** https://github.com/Azqato/composer
- **Deploy time:** Typically 1-2 minutes after push

To monitor: go to GitHub → Actions tab → find "Deploy to GitHub Pages" run. Green = deployed; red = failed (check logs).

The workflow excludes from public deployment: `data/symphony_scores.json`, `docs/`, `scripts/`,
`README.md`, `.gitignore`, `.github/`, `.git`, and `_site` itself.

> **Discrepancy (verified live 2026-08-24), and it is the most serious finding in this audit.**
> Earlier revisions of this line also listed `strategies.xlsx` and spelled the README `README.MD`.
> Neither matches `.github/workflows/deploy.yml`: the real exclusion list has `README.md` in
> lowercase and no `strategies.xlsx` entry at all, and no file by that name exists in the repository
> (the only spreadsheet is `data/Full Database.xlsx`, which is deliberately committed and served).
> That part is now corrected above.
>
> **The larger problem is that the exclusion list is inert.** Fetched live, GitHub Pages returns
> **HTTP 200** for every path the list is supposed to withhold:
>
> | URL | Status | Bytes |
> |---|---|---|
> | `azqato.github.io/composer/docs/PRD.md` | **200** | 325,375 |
> | `azqato.github.io/composer/README.md` | **200** | 6,915 |
> | `azqato.github.io/composer/scripts/check_live.py` | **200** | 5,855 |
> | `azqato.github.io/composer/data/symphony_scores.json` | **200** | 22,798,603 |
>
> Every byte count matches the working-copy file exactly, so what GitHub Pages serves is the raw
> repository, not this workflow's `_site/` artifact. The most likely cause is that the repository's
> Pages source is set to **Deploy from a branch** (`main` / root) rather than **GitHub Actions**, in
> which case `deploy.yml` builds an artifact nobody publishes. That cannot be confirmed from inside
> the repo (the `gh` CLI is not installed on the maintenance machine), so it is stated as the leading
> hypothesis rather than a fact, and it needs checking in the repository's Pages settings.
>
> On Cloudflare Pages, the canonical host, the same paths correctly **404**, because `.assetsignore`
> is honoured. Nothing here is secret: the repository is public and always has been. What is wrong is
> that two documents describe a privacy boundary that only one of the two hosts actually enforces.
> Tracked in Section 25 as an open risk.
>
> **`.assetsignore` has its own gap.** It withholds `docs/`, `README.md`, `scripts/`,
> `wrangler.jsonc`, `.github/` and the local mockups, but it does **not** list
> `data/symphony_scores.json`, so that 22.8MB file returns 200 on the canonical host too, despite
> `scripts/update_metrics.py`, this document and the README all describing it as not served
> publicly. `data/database.json` (18.7MB) and `data/Full Database.xlsx` (5.8MB) are likewise served
> though no page requests either: the site reads `database_summary.json`. That is roughly 47MB of
> publicly reachable files that nothing on the site fetches. Not a leak, but not what the docs say.

---

### Checking for Broken Composer Links

Periodically verify that `symphony_url` links still resolve on Composer.trade:

1. Open `data/strategies.json`
2. For each entry, open the `symphony_url` in a browser
3. If broken: update the URL or remove the strategy
4. Recommended frequency: monthly

---

### Re-Analyzing Strategy Logic Trees

When a symphony author updates their logic, or when existing `how_it_works`, `signals`, `tags`, or `risk_profile` content needs to be verified against the actual IF/ELSE structure.

**Step 1: Refresh symphony_scores.json.**
```bash
python scripts/update_metrics.py
```

**Step 2: Have an AI analyze the logic trees.** `data/symphony_scores.json` is ~14MB of raw EDN-format logic tree data. Provide the file to Claude Code (or any AI with a large context window) and ask it to:
1. Parse each symphony's logic tree into human-readable IF/ELSE pseudocode
2. Identify: primary trend gate, volatility routing, dip-buy conditions, cross-asset signals, terminal leaf allocations
3. Compare findings to existing `how_it_works`, `signals`, and `tags`
4. Flag discrepancies

**Structural pattern (original 13 zoop 2026 symphonies):** The first 13 strategies all share this structure:
```
[EqualWeight]
  ├── zoop's 2026 Frontrunner (50%)    ← shared base component
  └── [Strategy-specific component] (50%)
```
Strategies added in v1.4.0 and v1.5.0 (11 entries) are standalone symphonies and do not use this shared Frontrunner pattern.

The Frontrunner always contributes: RSI(10) oversold dip-buys (SMH <23 → SOXL; QQQ <28 → TQQQ; SPY <28 → UPRO), XLY RSI >79 → VXX, UVXY RSI >65 → SPXU or TQQQ, default → BIL. Therefore every strategy automatically inherits `rsi` and `vix-tiers` tags.

**Step 3: Update `strategies.json` and `strategies.js`** with corrected `tags`, `signals`, `how_it_works`, and `risk_profile`.

**Step 4: Validate and test.**
```bash
python -c "import json; json.load(open('data/strategies.json')); print('Valid JSON')"
python -m http.server 8000
```

**Step 5: Update PATCHNOTES.md** with a minor version entry.

**Step 6: Commit.**
```bash
git add data/strategies.json data/strategies.js data/symphony_scores.json docs/PATCHNOTES.md
git commit -m "content: re-analyze logic trees and update strategy content - YYYY-MM-DD"
git push origin main
```

---

### Generating the AI Summary

Every strategy page renders an **AI Summary** in a purple-accented box directly above "How It Works." It is a Claude-authored analysis stored in the `ai_summary` field (an array of paragraph strings) and is distinct from `how_it_works`: where `how_it_works` walks through the mechanics step by step, the AI Summary stands back and *evaluates* the strategy for the reader.

**What each summary must cover.** For every strategy, Claude analyzes and then synthesizes:

1. **Structure**: the overall shape of the logic (e.g. cash-first dip-buyer, three-state trend machine, parallel equal-weight components, shared Frontrunner base).
2. **Assets**: the instruments it trades (3x ETFs, sector ETFs, bonds, volatility products, individual stocks).
3. **Signals & logic**: the indicators and gates that drive decisions (RSI thresholds, 200-day MA regime, MACD, volatility tiers, momentum selection).
4. **Performance metrics**: ARR, max drawdown, Sharpe, Calmar, and standard deviation, read together rather than cherry-picked.
5. **Backtest period**: how many years/trading days, and whether that window is long enough to trust.

From that analysis, each summary then states:

- **Why someone would follow it**: the investor profile and the problem it solves.
- **The purpose behind its logic**: the thesis the rules are expressing.
- **Noteworthy characteristics**: anything a reader should weigh carefully, especially **short backtests** (e.g. < ~5 years is period-dependent), **high drawdowns** (e.g. deeper than ~50%), a **Calmar at or below 1.0** (return no larger than the worst loss), or **overfitting risk** in optimized/RL strategies.

**Tone and tenets.** Summaries follow the *Transparency Over Hype* and *Education Before Promotion* tenets: they are even-handed and explicitly discount spectacular-but-fragile backtests rather than amplifying them. If a strategy looks too good because of a short or favorable test window, say so.

**Format.** Two paragraphs is the standard: paragraph 1 covers structure/assets/logic and why-follow/purpose; paragraph 2 covers metrics/backtest period and noteworthy characteristics. Plain text only, with no HTML or markdown inside the strings. The site-wide footer already carries the "not financial advice" disclaimer, so the AI Summary box does not repeat one.

**How to write or update summaries.**

1. Open `scripts/add_ai_summary.py`. It holds an `AI_SUMMARIES` dict keyed by strategy `slug`, each value a list of paragraph strings.
2. Add or edit the entry for the relevant slug, using the strategy's metrics, `how_it_works`, `signals`, `risk_profile`, and (when deeper logic detail is needed) its tree in `data/symphony_scores.json`.
3. Run the script, it rewrites both data files in sync and inserts `ai_summary` immediately before `how_it_works`:
   ```bash
   python scripts/add_ai_summary.py
   ```
4. Validate and preview:
   ```bash
   python -c "import json; json.load(open('data/strategies.json')); print('Valid JSON')"
   python -m http.server 8000
   # http://localhost:8000/strategies.html?slug=<slug>
   ```
5. Update `docs/PATCHNOTES.md`, then commit `data/strategies.json`, `data/strategies.js`, `scripts/add_ai_summary.py`, and the patch notes.

Every strategy must have an entry in `scripts/add_ai_summary.py` regardless of how `ai_summary` is initially written. The script is the canonical store: writing `ai_summary` directly into the JSON entry and skipping the script means the next `add_ai_summary.py` run will warn and leave the entry unchanged, but it also means the summary is not tracked in version control in the canonical location. Always keep the script and the data files in sync.

---

### Troubleshooting

**Site not updating after push**
1. GitHub → Actions tab → check build/deploy status
2. If failed: check the error log
3. If deployed but looks old: hard refresh (Ctrl+Shift+R) or clear browser cache
4. GitHub Pages CDN propagation can take up to 5 minutes

**Strategy or glossary page shows blank / spinner stuck**
- Open browser dev tools → Console tab
- Check for JavaScript errors
- Confirm `data/strategies.js` and `data/glossary.js` exist and contain valid JavaScript
- If using Python HTTP server, also confirm `data/strategies.json` and `data/glossary.json` are valid JSON

**JSON parse error in browser**
- Look for `SyntaxError: Unexpected token` in the browser console
- Validate: `python -c "import json; json.load(open('data/strategies.json')); print('OK')"`
- Common causes: trailing comma on last array item, missing quotes, unclosed bracket

**Strategy not found**
- Confirm the `slug` in `strategies.json` exactly matches the `?slug=` query parameter in the URL (case-sensitive)

**A live URL returns 403 and you are sure it exists**

Check the `User-Agent` before checking the deploy. **Cloudflare returns HTTP 403 to Python's default
`urllib` User-Agent on every URL, including `robots.txt`**, as ordinary bot protection. It looks
exactly like an outage from a script and exactly like a healthy site from a browser.

`scripts/check_live.py` has always sent `User-Agent: composer-atlas-check-live/1.0` and is therefore
unaffected. Anything else written in a hurry against `composeratlas.com` needs the same treatment:

```python
req = urllib.request.Request(url, headers={'User-Agent': 'composer-atlas-check-live/1.0'})
```

**A blanket 403, on `robots.txt` as much as on a page, is the signature of the bot filter rather than
a broken deploy.** A genuinely missing file returns 404 with the header set, which is how the
sitemap's absence was distinguished from the site being down during the v1.25.1 verification.

**A newly pushed file 404s on composeratlas.com for a minute or two**

Normal. Cloudflare Pages took roughly 30 seconds to serve a newly added `sitemap.xml` in the v1.25.1
deploy. Poll rather than concluding the deploy failed.

**`check_live.py` reports a byte mismatch on a file you did not change**

Almost certainly line endings. Working copies on Windows are CRLF and the repository stores LF, so a
raw byte compare against what the host serves differs by exactly the newline count. `check_live.py`
normalises before comparing; anything hand-written must do the same. Also expect the Cloudflare Web
Analytics beacon, which is injected at serve time and adds 359 bytes to every page; the script
reports it as a note rather than a failure.

**Local dev, data not loading when opened directly**
- Confirm `data/strategies.js` and `data/glossary.js` are present
- Confirm each HTML page has `<script src="data/strategies.js">` and `<script src="data/glossary.js">` before the `app.js` script tag
- All pages are at root level: all script src paths use `data/` (no `../` prefix needed)

---

### Versioning Convention

| Change Type | Version Bump | Example |
|---|---|---|
| New site sections, breaking schema changes | Major (X.0.0) | Adding user auth |
| New features, new strategies, new glossary entries | Minor (1.X.0) | Adding a new strategy page |
| Metric updates, bug fixes, copy corrections | Patch (1.0.X) | Refreshing trailing return figures |

Update `docs/PATCHNOTES.md` for every change, including data-only updates.

---

## 12. Strategy & Glossary Data Schemas

### Strategy JSON Schema

All fields in `data/strategies.json`. Both `strategies.json` and `strategies.js` must always be kept in sync.

| Field | Type | Required | Description |
|---|---|---|---|
| `slug` | string | Yes | URL slug (e.g., `vix-tier-rotator`). Used as `?slug=` param. Must be lowercase, hyphen-separated, unique. Do not change after a page is live: breaks inbound links. |
| `name` | string | Yes | Display name (e.g., "VIX Tier Rotator") |
| `symphony_url` | string | Yes | Full URL to clone on Composer.trade |
| `symphony_id` | string | Yes | Composer symphony ID (alphanumeric segment from URL) |
| `annualized_rate_of_return` | float | Yes | Annualized return as decimal (e.g., `0.312` = 31.2%) |
| `max_drawdown` | float | Yes | Maximum drawdown as decimal: always negative (e.g., `-0.187` = -18.7%) |
| `cumulative_return` | float | Yes | Total cumulative return since inception as decimal |
| `calmar_ratio` | float | Yes | Annualized return / abs(max drawdown). Higher is better. |
| `sharpe_ratio` | float | Yes | (Return − risk-free rate) / std deviation. Higher is better. |
| `standard_deviation` | float | Yes | Annualized standard deviation of returns |
| `min` | float | Yes | **Worst single-day return.** The period is daily, verified in v1.27.8; see the note below this table |
| `mean` | float | Yes | Mean daily return |
| `median` | float | Yes | Median daily return |
| `max` | float | Yes | **Best single-day return** |
| `trailing_one_month_return` | float | Yes | Return over trailing 1-month period |
| `trailing_three_month_return` | float | Yes | Return over trailing 3-month period |
| `trailing_one_year_return` | float | Yes | Return over trailing 1-year period |
| `backtest_days` | integer | Yes | Backtest length in trading days. Display as `~X yrs (N trading days)` using `Math.round(days / 252)`. |
| `hidden` | boolean | Optional (**v1.41.0**) | When `true`, the strategy is **unlisted**: it does not appear in the strategy grid, the tag filter or the glossary's per-concept counts, and it is left out of `sitemap.xml`. **Its detail page still renders** at `strategies.html?slug=<slug>`, so existing inbound links keep working. Omit the key entirely for a visible strategy; do not write `hidden: false`. Filtering happens in one place, `loadStrategies()` in `js/app.js`. |
| `description` | string | Yes | Short plain-English description (1-3 sentences). No HTML tags. |
| `tags` | string[] | Yes | Concept tags for glossary cross-linking. Must match `slug` values in `data/glossary.json`. |
| `last_updated` | string | Yes | ISO date metrics were last updated (YYYY-MM-DD) |
| `ai_summary` | string[] | Recommended | Claude-authored analysis. Each string becomes a `<p>` inside the AI Summary box, rendered above How It Works. See "Generating the AI Summary" in Section 11. |
| `how_it_works` | string[] | Recommended | Paragraphs explaining strategy logic. Each string becomes a `<p>` tag. |
| `signals` | object[] | Recommended | Signals used. Each: `{ "name": string, "tag": string, "description": string }`. `tag` must match a glossary slug. |
| `risk_profile` | string **or object** | Recommended | Risk summary for the strategy detail page. **Two shapes are valid (V1.20 item 10).** A string is the original single-blob form. An object carries `verdict` (required) plus optional `leverage`, `backtest_limits`, `signal`, `hedge`, `concentration` and `suitability`. **An absent category must be an absent key, not an empty string**: the page prints an explicit "no hedge leg" line for a missing key. Validated by `scripts/check_risk_profiles.py`. |
| `author_note` | string | Optional | Curator note (plain text, no HTML). Displayed on the detail page when present. |
| `tldr` | object | Optional (**V1.20 item 13**) | `{ "thesis": string, "works_well_in": string[], "struggles_in": string[] }`. Rendered as the TL;DR card above everything else. **Both arrays are required when the field is present**: the opposed columns are the reason the format exists |
| `assumptions` | object | Optional (**V1.20 item 14**) | `{ "market": string[], "structural": string[] }`. Market and macro beliefs against technical and structural ones. Either array may be empty; the column is then omitted |
| `regimes` | object[] | Optional (**V1.20 item 15**) | Each: `{ "regime": string, "expected": string, "why": string, "example": string }`. `expected` is authored prose, not a code: the page colours it green, yellow or pink by reading its first word (`Strong`/`Good`, `Poor`/`Bad`/`Weak`, anything else) |
| `regime_note` | string | Optional | Footnote under the regime table. Use it to say where the example figures came from |

**These four fields accept inline `**bold**` and `` `code` ``**, converted by `mdInline()` in
`js/app.js`. That helper is two regexes and does not escape its input, exactly like every other
curated field on the page: the trust boundary is `data/strategies.json` itself, which only a
maintainer writes.

**A live metric quoted in these fields must be a token, never a typed number (v1.45.0).** Write
`{sharpe_ratio}`, not `2.89`. `resolveStrategyTokens` in `js/app.js` substitutes it at render time
from the same object the metrics table reads, so the sentence and the table cannot disagree.
`scripts/check_prose_tokens.py` fails the build on an undefined token or one that reads a null
field, and the full token list is in the `PROSE_TOKENS` object in `js/app.js`.

A token may carry a precision, because the library's prose voice rounds: `{max_drawdown_abs}` is
`78.3%` and `{max_drawdown_abs:0}` is `78%`. `max_drawdown` is stored negative, so use
`{max_drawdown_abs}` for the magnitude and `{max_drawdown}` when the sign is wanted.

**This reverses the previous rule, which was to keep live metrics out of prose entirely.** That was
right while a quoted figure could only be typed by hand: a restated metric went stale on the next
refresh with nothing to catch it, and by v1.45.0 that had happened to 37 figures across 12 pages,
including a Sharpe of 2.63 advertised against a database value of 2.56. A token cannot go stale, so
a live metric is now the *safest* number to put in a sentence.

**Numbers that are not live metrics still must be historical facts about fixed date windows**, for
example "GDXU rose 695.2% during 2025", or a figure belonging to a different strategy in a
comparative sentence. Those stay literals: they do not drift, and there is nothing on this strategy
to resolve them from.

**Metric calculation notes:**
- `calmar_ratio` = `annualized_rate_of_return` / abs(`max_drawdown`)
- `sharpe_ratio`: pull directly from Composer's displayed value; Composer uses its own internal risk-free rate baseline
- `max_drawdown`: the Composer API returns this as a positive number; the script stores it negative. Always store negative.
- `backtest_days`: the API field is `size`; the script maps it to `backtest_days`
- Period returns (min, mean, median, max) represent single-period (typically monthly) returns, not annualized

**Slug convention:**
- Lowercase, spaces → hyphens, remove special characters
- "VIX Tier Rotator" → `vix-tier-rotator`
- "TQQQ/BIL Switcher" → `tqqq-bil-switcher`
- Append `-2` if a collision occurs
- Never change a slug after a page is live

**Extended schema fields (post-MVP, optional):**

| Field | Type | Description |
|---|---|---|
| `inception_date` | string (ISO date) | Date strategy was created on Composer |
| `benchmark` | string | Benchmark ticker (e.g., `"SPY"`) |
| `assets` | string[] | List of tickers the strategy can hold |
| `rebalance_frequency` | string | `"daily"`, `"weekly"`, `"monthly"` |
| `risk_level` | string | `"conservative"`, `"moderate"`, `"aggressive"` |
| `trailing_five_year_return` | float | 5-year trailing return |
| `sortino_ratio` | float | Sortino ratio (penalizes only downside volatility) |
| `beta` | float | Beta relative to benchmark |
| `alpha` | float | Alpha relative to benchmark |

---

### Full Database JSON Schema

All fields in `data/database.json`. This is a separate, lighter schema from
`strategies.json`: it holds the raw ~6,800-entry database (see Section 14 Roadmap),
not the 36 curated strategies. `data/database.js` is its `.js` twin (assigns
`window.DATABASE_DATA`, same file:// compat pattern as `strategies.js`/`glossary.js`).

#### The Primary Key Invariant

**`symphony_id` is the primary key of `data/database.json`. The file is always deduplicated on it.**
No two entries may carry the same `symphony_id`, and every entry must have one.

> **Correction, v1.25.2 (2026-08-24), owner instruction.** The `symphony_url` row below called that
> field "the true unique key", and it is kept as written because it is the reasoning the pipeline was
> built on. **It is wrong, and it is wrong in a way that cost real data integrity.** Composer serves
> the same symphony under more than one path, at least `/details` and `/factsheet`, so a URL is not
> unique per symphony. `sync_storage_to_database.py` deduplicated on the URL string, which meant a
> second URL for a symphony already in the database read as a new symphony and was appended as a new
> row. That is exactly how `chkrQ6BnXCw31n7OIEaK` came to sit in the file twice, identical on all 37
> fields except the URL suffix, showing "Hedged Sector Rotator " twice in every list view and
> counting it twice in every total.
>
> **`symphony_url` remains required and is still the field the pipeline fetches from. It is not the
> key.** The id is.

**Enforced, not merely stated.** `scripts/check_database_keys.py` runs as a deploy gate alongside
`check_html_js.py`, `check_composer_ladder.py`, `check_strategy_extras.py` and `check_asset_sizes.py`, and asserts four
things:

1. every entry has a non-empty `symphony_id`
2. `symphony_id` values are unique across the file
3. the id embedded in `symphony_url` matches the entry's `symphony_id`, since the two are written by
   different code paths and can disagree
4. `database_summary.json` holds the same ids in the same order as `database.json`

**Why a gate rather than only a fix to the script.** Fixing `sync_storage_to_database.py` closes the
path that caused this instance, and it was fixed in the same release. It does not close the class.
`database.json` is also edited by hand: the `AddSymphony.csv` route and the ad-hoc cluster
corrections in Section 14 both write it directly, and no amount of care in a script prevents a hand
edit from adding a row that already exists. The gate checks the artifact, so it holds regardless of
what produced it. Check 4 closes the separate hole that made four symphonies invisible on the live
site until v1.25.1: the site reads the summary, so a summary that silently falls behind the full file
is indistinguishable from those symphonies not existing.

**This invariant is distinct from `dedupe_symphonies.py`.** That script clusters symphonies that are
*different records of similar strategies*, by name pattern and logic tree, and picks a keeper using a
deliberately debatable tiebreak (Section 14, V1.14 Part A; Section 25 item 18). Its judgement calls
stay judgement calls. An identical `symphony_id` is not a judgement call: it is the same symphony,
recorded twice, and it is removed unconditionally.

| Field | Type | Description |
|---|---|---|
| `name` | string \| null | Symphony name as scraped; may be null on entries that never finished scraping |
| `symphony_url` | string | Full URL to the symphony on Composer.trade; always present, the true unique key. **Superseded, v1.25.2: this is not unique per symphony.** Composer serves at least `/details` and `/factsheet` for the same symphony. Still required, still the field the refresh pipeline fetches from, but not the key. See "The Primary Key Invariant" above |
| `symphony_id` | string \| null | Extracted from `symphony_url`; used to call the Composer API. **This is the primary key (v1.25.2).** Unique across the file and never null in practice, both gated by `scripts/check_database_keys.py`. The `\| null` in the type column records what the schema has always permitted rather than what the data contains; every one of the 6,668 current entries has one |
| `annualized_rate_of_return` through `trailing_one_year_return` | float \| null | Same meaning and sign conventions as the matching fields in `strategies.json` Section 12; `null` when the entry has no usable metrics yet |
| `backtest_days` | integer \| null | Backtest length in trading days (API field `size`) |
| `refresh_date` | string \| null | **Renamed from `last_updated` in v1.11.10.** ISO date (`YYYY-MM-DD`) this entry's metrics were last successfully refreshed; only advanced on a successful API call, so a permanently-failing row's `refresh_date` stays frozen at its last success (or `null` if it never succeeded) |

**Extended fields (added v1.9.1, target schema expansion):** every entry has these keys; `null` until the entry has been through `scripts/refresh_full_database.py` under the new schema (full overwrite policy, see Section 11-adjacent script docstring).

| Field | Type | Description |
|---|---|---|
| `sortino_ratio` | float \| null | Downside-only risk-adjusted return |
| `win_rate` | float \| null | Fraction of winning periods |
| `skewness`, `kurtosis` | float \| null | Return distribution shape |
| `tail_ratio` | float \| null | Ratio of right-tail to left-tail extremes |
| `top_one_day_contribution`, `top_five_percent_day_contribution`, `top_ten_percent_day_contribution` | float \| null | How concentrated returns are in a handful of days |
| `herfindahl_index` | float \| null | Portfolio concentration score |
| `annualized_turnover` | float \| null | Trading frequency |
| `trailing_one_day_return`, `trailing_one_week_return`, `trailing_two_week_return` | float \| null | Finer-grained trailing windows, in addition to the existing 1mo/3mo/1yr |
| `last_market_days_holdings` | object \| null | Current live allocation, ticker symbol → dollar amount (e.g. `{"TQQQ": 7537.17, "$USD": 0.36}`). This is where real ticker symbols live, not `active_asset_nodes` |
| `active_asset_nodes` | object \| null | Internal node UUID → weight (e.g. `{"875f367e-...": 1.0}`). **Not a ticker list**; corrected after live validation in v1.9.1, do not use for a ticker/holding filter |
| `total_costs` | float \| null | Sum of the API's `costs` object (`reg_fee` + `taf_fee` + `cat_fee` + `slippage` + `spread_markup` + `subscription`); the per-category breakdown is not separately stored |
| `flag` | string \| null | **Added v1.11.8 as an object, consolidated v1.11.9, split into `flag`+`error` v1.11.11.** Error/warning category for downstream filtering, see V1.14 Part B. One of `"excluded"` (permanent failure, 404/422, e.g. deleted/private/malformed symphony), `"caution"` (backtest succeeded but Composer flagged a data issue, e.g. a holding delisted mid-window), `"retry"` (transient failure, 429/500/503/timeout, cleared automatically by the normal staleness-check retry cycle), or `null` when clean. Written directly by `scripts/refresh_full_database.py` on every API call (see `classify_error()`). |
| `error` | string \| object \| null | **Added v1.11.11**, paired with `flag`. The original message: a plain string for script errors (e.g. `"HTTPError 422: Unprocessable Entity"`), or Composer's own `data_warnings` object when `flag == "caution"`. `null` when `flag` is `null`. There is no separate `script_errors`/`data_warnings` field to cross-reference, this is the sole record of the original error/warning text. |
| `oos_date` | string \| null | **Renamed from `last_semantic_update_at` in v1.11.10, also truncated to date-only.** Date (`YYYY-MM-DD`) of the symphony's last logic edit, sourced from the Composer API's `last_semantic_update_at` timestamp field with the time-of-day/timezone portion dropped. Used by `database.html`'s `oosDaysValue()` to compute "days since last edit" (out-of-sample duration) live at render time, both as a Filter Panel field and a Leaderboard scoring input (Section 14, V1.13): the day-count itself is never stored, only this source date. |

**Known data quality issues (as of v1.9.0):**
- Only ~953 of 6,488 entries have usable metrics; the rest have `flag` set to `"excluded"` or `"retry"` and all metric fields `null`
- The dataset includes non-strategy noise: test ports (e.g. names prefixed `TESTPORT #`), "Invest Copy" duplicates, "Copy of Copy of..." chains, and WIP builds; none of this is filtered yet (see Section 14 Roadmap, Noise Filtering)
- `name` collisions are common (the same strategy cloned/modified many times under a near-identical name); `symphony_url` is the only guaranteed-unique key, not `name`

---

### Database Summary JSON Schema

`data/database_summary.json` (added v1.16, Performance Fix): a derived, lighter subset of `database.json` used by every list/filter/score view (All Strategies, Filter Panel, Screener, Leaderboard). Not hand-edited, regenerated by `scripts/export_summary.py` after every `refresh_full_database.py` run.

**Shape is columnar, not one object per entry:**
```json
{ "fields": ["name", "symphony_url", ...], "rows": [["zoop's 2026 Frontrunner", "https://...", ...], ...] }
```
Field names are stored once in the `fields` array; each entry is a positional value array in `rows`, not a `{key: value}` object. This is the single biggest driver of the size reduction (repeating ~29 field names as object keys across 6,488 entries was most of the old file's weight, not any field's actual data). Reconstruct plain row objects client-side before use (see `rowsFromColumnar()` in `database.html`).

**Field list:** every `database.json` field except `cumulative_return`, `mean`, `min`, `max`, `active_asset_nodes`, `total_costs`, `annualized_turnover`, `herfindahl_index` (dropped, see V1.16/V1.13 for why each is unused). All floats rounded to 4 decimal places (percentages/ratios never need more precision than that in any UI).

There is no `.js` twin naming inconsistency to worry about here, `data/database_summary.js` follows the same convention as every other twin file, assigning `window.DATABASE_SUMMARY_DATA` to the identical columnar payload.

---

### Storage CSV Schema

`data/storage.csv` (added v1.10.1): a single-column, append-only backup of every Composer symphony URL ever shared, referenced, or added to the site or the full database, independent of whether it was ever successfully backtested. Its purpose is durability, not analysis: `database.json` can be rebuilt, re-scoped, or have entries dropped (e.g. during Noise Filtering), but `storage.csv` is meant to never lose a URL once it's been seen.

#### storage.csv Is Larger Than database.json, On Purpose

**These two files answer different questions and are not meant to match.** The gap between them is
the design working, not drift, and it is not a backlog waiting to be cleared.

| | `data/storage.csv` | `data/database.json` |
|---|---|---|
| **What it holds** | **Every symphony URL ever seen**, kept long term whether the symphony is alive, dead, private, deleted, noise, or a duplicate | **Only the symphonies confirmed and approved for the site.** A row here is a row a visitor can see and score |
| **Admission rule** | Nothing is ever excluded. A URL is added on sight | A URL is admitted deliberately, and can be removed again |
| **Removal** | **Never.** Nothing is deleted from this file, ever | Routine. Purged, flagged, de-duplicated, re-scoped |
| **Primary key** | `url` | `symphony_id` |
| **Count (2026-08-24)** | 7,709 rows, 7,708 distinct symphonies | 6,668 entries, 6,668 distinct symphonies |

**The 1,045 symphonies in `storage.csv` and not in `database.json` are there deliberately.** The
largest single contributor is the v1.11.14 purge, which removed 1,004 permanently-dead entries
(404/422: deleted, private, or malformed symphonies) from `database.json` outright while keeping
every one of their URLs in `storage.csv` forever. That purge only ran because the safety invariant
held: `purge_flagged_entries.py` aborts rather than remove a row whose URL is not already in
`storage.csv`, so nothing is ever lost outright and any purged symphony can be re-promoted later.

**The containment runs one way, and only one way.** Every symphony in `database.json` must have its
URL in `storage.csv`; `storage.csv` holding symphonies that `database.json` does not is the design
working. **`database.json` is a subset of the archive, never the other way round.** Check 5 of
`scripts/check_database_keys.py` gates the direction that can be wrong, and deliberately does not
check the direction that cannot.

**Keeping the archive complete: `scripts/sync_database_to_storage.py` (v1.25.4).** The mirror of the
promotion script, and the safe one of the pair: it only widens the archive, which is what the archive
is for. Run it after adding anything to `database.json` by hand. It is idempotent and keyed on
`symphony_id`, so a second URL for a symphony already archived is not appended, which matters in a
file nothing is ever deleted from.

> **Fixed in v1.25.4.** Five approved symphonies had no archived URL: `0jPwZ5Lm2Y3xH24oEijB`,
> `zY4jRnXoFC9e1Pt97YDS`, `P7RLUTtWmTjkJBaNBQT9`, `tlDwKY3NRXjYU61jCt0g` and `jjIQMCxLK5P98Zpczktk`.
> **Four of the five were the same symphonies missing from `database_summary.json` until v1.25.1**,
> which is one cause showing up twice: the hand-run addition routes wrote `database.json` and stopped,
> updating neither the archive before it nor the derived summary after it. All five are archived and
> the gate now holds the invariant.

**This is why `sync_storage_to_database.py` must not be run casually.** It cannot distinguish "a URL
nobody has processed yet" from "a URL deliberately purged as dead", so a blind run resurrects every
dead symphony as a fresh unrefreshed row. That has now happened twice: once on 2026-07-15, when a run
intended to process 10 new `AddSymphony.csv` URLs pulled in 1,055 stale entries, and again on
2026-08-24 during the v1.25.2 verification, when it pulled in 1,045. **Both runs were reverted and
neither was committed.** See the warning in Section 11's AddSymphony workflow, and Section 23's
never-do table.

> **Correction, v1.25.3 (2026-08-24), owner instruction.** The v1.25.2 release logged the size gap as
> open question 23, asking whether the URLs should be promoted into the database. **That was wrong on
> both counts.** It is not an open question, and the gap is not a backlog: the two files hold
> different things by design, which Section 11 has documented since 2026-07-15 and which this audit
> failed to read before writing the question. Question 23 is withdrawn and this table replaces it.

| Field | Type | Description |
|---|---|---|
| `url` | string | Full Composer.trade symphony URL. The only column, and the primary key: one row per unique URL, never duplicated |

**Maintenance:** manually append new URLs as they come up in conversation or get added anywhere on the site; deduplicate against the existing file before adding (`url` is the primary key, exactly one row per symphony regardless of how many times it's been discussed or how many other files reference it). Seeded on creation (v1.10.1) from the union of every `symphony_url` in `data/database.json` and `data/strategies.json`, 6,489 unique URLs at seed time.

**Promoting storage.csv URLs into the database:** `scripts/sync_storage_to_database.py` (v1.11.1) adds any `storage.csv` URL not yet in `database.json` as a new, unrefreshed entry (every field null except `symphony_url`/`symphony_id`), so it gets picked up by the next `refresh_full_database.py` run like any other due row. Already-present symphonies are skipped, keyed on `symphony_id` since v1.25.2.

**It is not, however, safe to run casually**, and the sentence this paragraph used to end with ("run this whenever `storage.csv` has grown") is the advice that caused two reverted incidents. Promotion is an approval decision, one symphony at a time or one reviewed batch at a time, not a sync. Read the table above before running it at all: `storage.csv` deliberately holds symphonies that were removed from the database on purpose, and this script will bring every one of them back. It also has **no dry-run flag** and writes on every invocation, so there is no way to ask it what it would do.

---

### RSI Signals JSON Schema

`data/rsi.json` (added V2.1): 10-day RSI (Wilder's smoothing) for the Frontrunner signal universe plus IWM and DIA, powering `rsi.html`. Not hand-edited, regenerated by `scripts/refresh_rsi.py` (3x/day on weekdays via `.github/workflows/refresh-rsi.yml`, safe to run manually any time).

```json
{
  "refreshed_at": "2026-07-09T22:07:03Z",
  "tickers": [
    { "symbol": "QQQ", "name": "Invesco QQQ Trust", "rsi_10": 34.7, "price": 471.23, "price_date": "2026-07-08" }
  ]
}
```

| Field | Type | Description |
|---|---|---|
| `refreshed_at` | string | UTC ISO 8601 timestamp of the script run that produced this file |
| `tickers[].symbol` | string | Ticker symbol |
| `tickers[].name` | string | Full fund name |
| `tickers[].rsi_10` | number | 10-period RSI, Wilder's smoothing, computed from ~250 days of adjusted daily closes, rounded to 1 decimal |
| `tickers[].price` | number | Latest adjusted close used in the RSI calculation |
| `tickers[].price_date` | string | ISO date of that latest close; never moves backwards between runs. `rsi.html` shows the latest as the badge's close date |

`data/rsi.js` is the `.js` twin, assigning `window.RSI_DATA` to the identical payload, same convention as `strategies.js`/`database.js`.

---

### K-1 Database Schema

`data/k1.json` (added v1.27.0): per-ticker fund structure and the tax form it implies, powering
`k1.html`. Not hand-edited, regenerated by `scripts/refresh_k1.py`. There is no workflow behind it;
structures change only when a fund reorganises, so it is refreshed by hand. See Section 11.

**`inception` (added v1.33.1)** carries the fund's first trading day, rendered on `k1.html` as
"Inception" (labelled "First traded" in v1.33.1 only, renamed in v1.33.2 to match the field name and
the term the rest of the site already uses). **It is joined in at build time and `k1.html` does not load
`data/ticker_inception.js`.** That file is roughly 100 KB once it covers the whole database and the
page needs one date out of it, so loading it would charge every visitor 100 KB to render about 25
bytes. Joined into `k1.json` it costs about 4.7 KB on a 69 KB file and adds no second request. This
is the same argument, and the same answer, as V1.20 item 9 gave for not putting the readout on
`prices.json`.

**A ticker with no known date carries no `inception` key at all**, rather than an explicit null, and
the page omits the row rather than rendering it blank. "Nobody has looked this up" and "this fund has
no start date" are different claims and a missing key is not evidence for either. **185 of the 187
K-1 tickers are held by at least one symphony in the database**, so the full inception refresh reaches
them as a side effect of covering held tickers. **DBS and DBV are held by nothing**, so the sweep will
never reach them and they need an explicit by-name fetch. That is the general rule for this join: the
inception file is built from held tickers, and the K-1 database is not a subset of it.

**Closed v1.34.1: all 187 K-1 rows now carry an inception date.** The full sweep dated 185 of them
and `python scripts/refresh_ticker_inception.py DBS DBV` dated the last two, which is what the
by-name argument exists for.

**etfdb publishes a `Distributes K1` field, and since v1.27.7 it is the primary check.** It sits in
the Tax Analysis block of every fund page and answers this tool's question directly. It was missed
when the database was first built, which is why the structure logic below reads as though it were
the only route. It was not a redundant miss: the flag alone would have been **worse** than what
shipped, for the reason two paragraphs down.

**Structure remains the check on the flag, and the tie-breaker when they disagree.** etfdb omits
`Structure` on some funds while still publishing `Distributes K1` for them, `DRAM` (Roundhill Memory
ETF) being the worked example, and those funds had no answer at all before v1.27.7. Structure also
fixes the tax form, which the flag cannot: a "No" separates neither 1099 from 1099-B nor ETF from
ETN.

| `structure` | Tax form | Why |
|---|---|---|
| Commodity Pool | Schedule K-1 | A partnership for tax purposes. Income, gains and losses pass through to holders. Every leveraged and inverse volatility product, most futures-based commodity funds, and several leveraged Treasury funds |
| ETF | Form 1099 | A regulated investment company under the 1940 Act |
| UIT | Form 1099 | Unit investment trust. SPY, QQQ and DIA are these |
| ETN | Form 1099-B | Senior unsecured debt of the issuing bank, not a fund at all. **Surfaced on the page since v1.27.9:** a blue callout on the answer panel, an `ETN` tag in the table, and an `ETN` filter |
| Grantor Trust | Form 1099-B | A direct undivided interest in the underlying, which is why the physical metal trusts are taxed at the 28% collectibles rate |

**A third, independent field corroborates every row.** The max short- and long-term capital gains
rates fall out of the structure rather than being copied from it, so they are a genuine cross-check
rather than a restatement: `27.84% / 27.84%` is the 60/40 blend that Section 1256 contracts get and
nothing but a commodity pool shows it; `39.60% / 28.00%` is the collectibles rate and means a grantor
trust; `39.60% / 20.00%` is ordinary. Where readings contradict each other the row carries
`agrees: false` and **the page says so rather than picking a winner**, because a contradiction means
either the source page changed shape or the fund is genuinely unusual, and both deserve a human.

**Why the flag is primary but not trusted alone: SOYB and TAGS.** etfdb answers
`Distributes K1: No` for both, and both send K-1s. Teucrium Commodity Trust's own 10-K says the funds
"are treated as a partnership for U.S. federal income tax purposes" and that "the partners report
their share of a Fund's income or loss on their income tax returns", naming TAGS explicitly, and the
trust is absent from EDGAR's register of 1940-Act funds. Promoting the flag to sole authority would
have flipped two correct rows into a wrong answer about someone's taxes. **So where the flag and the
structure disagree, the row is marked `contested`, the structure-derived verdict is the one shown,
and the page raises a warning telling the reader to research that fund themselves** rather than
presenting either reading as settled. One precedent is not a rule, and the warning says that too.

**A `contested` row is resolved by research, recorded in `OVERRIDES`, not by editing the data.** An
override clears `contested`, because the page should print the finding rather than send a reader off
to investigate a question that has already been investigated and answered here.

```json
{
  "refreshed_at": "2026-08-27 10:31:02",
  "source": "etfdb.com",
  "tickers": {
    "USO": {
      "name": "United States Oil Fund",
      "brand": "United States Commodity Funds",
      "structure": "Commodity Pool",
      "distributes_k1": true,
      "k1": true,
      "source_field": "distributes_k1",
      "contested": false,
      "tax_form": "Schedule K-1",
      "st_rate": "27.84%",
      "lt_rate": "27.84%",
      "agrees": true,
      "checked": "2026-08-27"
    }
  }
}
```

| Field | Type | Description |
|---|---|---|
| `refreshed_at` | string | Local timestamp of the run that last wrote the file |
| `source` | string | Where structures were read from |
| `tickers` | object | Keyed by uppercase ticker, sorted on write so a diff shows only real changes |
| `.name`, `.brand` | string or null | Fund name and issuer, as published |
| `.structure` | string or null | The raw structure string. Determines the tax form, backs up the flag, and wins where the two disagree |
| `.distributes_k1` | bool or null | etfdb's own answer, verbatim. `null` where the page does not carry the field |
| `.k1` | bool or null | The verdict. `.distributes_k1` where the two agree or the structure is absent; the structure-derived answer where they disagree; **`null` where neither field is present**. Null renders as "unknown", never as "no" |
| `.source_field` | string or null | Which reading produced `.k1`: `"distributes_k1"` or `"structure"`. Kept so the page can say where an answer came from instead of asserting it |
| `.contested` | bool | `true` when the flag and the structure contradict each other. **Drives the page's warning block.** Cleared by an override, since a researched row is no longer contested |
| `.tax_form` | string or null | The form a holder actually receives |
| `.st_rate`, `.lt_rate` | string or null | Max short- and long-term capital gains rates, kept as the source's own percentage strings |
| `.agrees` | bool or null | Whether every available reading tells the same story, the flag included. `false` means check it by hand; `null` means there was nothing to compare |
| `.checked` | string | ISO date this row was last fetched. Drives the 180-day staleness window |
| `.not_found` | bool, optional | Present and `true` only when the source has no such ticker. Recorded rather than skipped, so the page can say "not an exchange-traded product on record" and a re-run does not keep asking |

`data/k1.js` is the `.js` twin, assigning `window.K1_DATA` to the identical payload, same convention
as `strategies.js`/`database.js`. **Commit both or neither**; the `.js` file is what the page reads
over `file://`.

`data/k1_seed.txt` is the candidate list `--seed` reads. Its header says what it is and is worth
preserving: **a ticker in that file is a request to check it, not a claim about it.** Nothing in the
database is ever inferred from a ticker symbol or a fund's name.

---

### Signal Miner Price History Schema

`data/prices.json` (added v1.15.0): full daily adjusted-close history for the Signal Miner ticker universe, powering `signal-miner.html`. Not hand-edited, regenerated by `scripts/refresh_prices.py`. All signal generation and backtesting happens **client-side in the browser**; this file is the only input. Closes are aligned to a shared master date axis (`null` where a ticker had no bar, e.g. before it listed), so every ticker's `closes` array is the same length as `dates`.

```json
{
  "refreshed_at": "2026-08-15T18:30:00Z",
  "start": "2010-01-01",
  "dates": ["2010-01-04", "2010-01-05", "..."],
  "tickers": {
    "QQQ": { "name": "Invesco QQQ Trust", "group": "Broad market", "closes": [156.5, 157.2, "..."] },
    "GDXU": { "name": "MicroSectors Gold Miners 3x Leveraged", "group": "Leverage", "closes": [null, null, "..."] }
  }
}
```

| Field | Type | Description |
|---|---|---|
| `refreshed_at` | string | UTC ISO 8601 timestamp of the script run |
| `start` | string | Earliest date kept (bounds file size) |
| `dates` | string[] | Master trading-day axis (sorted union of all tickers' days) |
| `tickers` | object | Map of `symbol → { name, group, closes }` |
| `tickers[sym].group` | string | Asset-class group (v1.18.0), drives the chip groups and per-group "All" buttons on `signal-miner.html`. One of: Broad market, Value & Dividend, Sector, International, Bonds, Commodities FX & crypto, Volatility & hedge, Leverage, Inverse. The page falls back to `"Other"` if absent, so the field is additive and safe |
| `tickers[sym].closes` | (number\|null)[] | Adjusted closes aligned to `dates`; `null` before listing or on a missing bar |

`data/prices.js` is the `.js` twin, assigning `window.PRICES_DATA` to the identical payload (compact JSON), same convention as `rsi.js`. Universe is currently **72 tickers** (37 before v1.18.0, 80 before the v1.21.2 duplicate prune); edit the `TICKERS` list in `scripts/refresh_prices.py` to add or remove one, then re-run the script and commit both regenerated files. Each entry is a `(symbol, name, group)` triple, so grouping lives with the ticker list and the page never keeps its own copy.

**Leverage and Inverse are separate groups (v1.22.14).** They were one 22-ticker "Leveraged & inverse" block, by far the largest group and the only one whose "All" button was close to useless: it selected fifteen bull funds and seven bear funds together, which is almost never what anyone wants. Splitting them into **Leverage** (15: TQQQ, QLD, SPXL, SSO, UDOW, SOXL, USD, TECL, RETL, FAS, LABU, TNA, YINN, TMF, GDXU) and **Inverse** (7: SQQQ, PSQ, SPXU, SH, SOXS, TMV, GDXD) makes both "All" buttons express a real intent. Membership is by direction, not by multiple, so the 1x shorts SH and PSQ sit in Inverse alongside the 3x ones. Nothing but the label changed: the universe is still 72 tickers and no price series moved. In the same pass "Factor & dividend" was renamed **Value & Dividend** and "Bonds & cash" was renamed **Bonds**, both keeping every member (BIL and SHV stay under Bonds).

**Partial-history tickers.** Seven funds list after the 2018 start and so carry `null` for their early rows: ETHA (24% coverage), IBIT (30%), SVIX (51%), KMLM, GDXU, GDXD (66% each) and DBMF (84%). They are kept deliberately, but any signal built on them is fit to a shorter sample, and the default Min Time in Market floor of 15% is still too low to screen that out. `signal-miner.html` marks anything below 90% coverage with a dashed chip border and a "limited history" tooltip.

**Refresh cadence:** `refresh_prices.py` runs weekly via `.github/workflows/refresh-prices.yml` (cron `7 2 * * 6`, i.e. 02:07 UTC Saturday, which is **Friday 7:07pm Pacific**, after the Friday close and while markets are closed; plus `workflow_dispatch` for manual runs). Moved there from 08:07 UTC Saturday on 2026-09-06 so it leads the weekly pipeline chain rather than trailing it, see "The weekly data pipeline" in Section 4. Weekly is deliberate: Signal Miner is a research tool over multi-year history, so a slightly stale end date barely affects any signal's metrics. The script takes ~80s to fetch all 72 tickers (a 1s delay between calls dominates); the full Action runs in ~75-90s. If the workflow is ever disabled, the tool keeps working on the last committed snapshot. The page surfaces the `refreshed_at` date in the hero and footer meta so staleness is always visible.

### Signal Miner Runtime Behavior

How the tool behaves while a run is in flight. All of this is client-side in `signal-miner.html`; there is no server component.

**The search space: one window grid, sixteen families (v1.23.0).** What the miner enumerates is the cross product of *families* x *tickers* x *windows* x *levels* x *directions*. Before v1.23.0 each family carried its own inherited window list, four lists that had drifted apart for no stated reason, and only six families existed.

*One grid.* Every family now reads the same fifteen windows: **5, 7, 10, 12, 14, 21, 26, 30, 42, 50, 63, 100, 126, 200, 252**. They are log-uniform, no two closer than 15%, because a window's information content scales with the *ratio* to its neighbour rather than the difference. Each earns its place: 5 (one week), 7 (the short-RSI cluster common in Composer symphonies), 10 (two weeks, and the single most used window in the strategy library at 137 occurrences), 12 and 26 (the MACD legs), 14 (Wilder's default for RSI, ATR, ADX and Stochastic), 21 (one month, the standard realised-volatility estimator), 30, 42 (two months), 50 (golden-cross fast leg), 63 (one quarter), 100, 126 (six months), 200 (Faber's 10-month trend gate, rounded) and 252 (one year, the dominant momentum window in the literature). **20, 60 and 189 were dropped** as near-duplicates of 21, 63 and 200, all within 6%: a comparison family costs the same for any window while scaling with the *square* of the grid, so a window producing an almost identical daily series to one already present is pure cost. `MIN_PERIOD_OPTS` is now exactly this list, so choosing a floor can never silently round to a window the grid does not contain.

*Level grids are uniformly stepped, and scaled or fixed per quantity (v1.23.1).* Every percent-quoted grid steps by a constant amount across its whole range, replacing the hand-written ladders that used to thin out at their extremes (the old drawdown grid ran 2, 4, 6, 8, 10, 13, 16, 20). Grids are declared in percent and generated on an integer lattice of hundredths of a percentage point, so repeated addition cannot drift, and stored as fractions.

Quantities that **accumulate** over the window disperse as sqrt(t): a 10% move over 5 days and a 10% move over 252 days are not the same event. Measured on TQQQ 2010-2026, the old fixed +/-10% cumulative-return grid left only **12% of days inside the grid at 252 days**, so most of its levels were pinned true (or false) across the whole sample and separated nothing. Cumulative return and max drawdown therefore scale their **range** by `sqrt(p / 21)` while holding the **step** fixed at one percentage point, so resolution is constant across windows and only the reach changes. Endpoints snap inward to the step lattice, which keeps every window's levels on the same round values rather than on fifteen offset sets.

**The brackets were set from the data, not from taste.** The first pass used `+/-10%` and `2%` to `20%` at 21 days, numbers that sound reasonable and are not. Measured over all 72 tickers, 2010-2026, that cumulative-return grid covered only **75-81% of days**, and the drawdown grid **49-76%**. Drawdown missed at *both* ends: at 5 days its 1% floor sat above the 1.2% median, so nearly half the sample fell below the grid, while its 9% ceiling sat below the 18% 99th percentile. A threshold nothing ever crosses tests nothing.

The brackets now clear the 5th-to-95th percentile at every window. Cumulative return runs `+/-20%` at 21 days, drawdown `1%` to `40%`, both scaled by `sqrt(p / 21)` and stepped by one percentage point:

| Window | CumRet grid | Levels | Days inside | MaxDD grid | Levels |
|---|---|---|---|---|---|
| 5 | `-9%` to `+9%` | 19 | 92% | `1%` to `19%` | 19 |
| 10 | `-13%` to `+13%` | 27 | 92% | `1%` to `27%` | 27 |
| 21 | `-20%` to `+20%` | 41 | 93% | `1%` to `40%` | 40 |
| 63 | `-34%` to `+34%` | 69 | 93% | `2%` to `69%` | 68 |
| 126 | `-48%` to `+48%` | 97 | 92% | `3%` to `95%` | 93 |
| 252 | `-69%` to `+69%` | 139 | 91% | `4%` to `95%` | 92 |

Two things the table does not say. The **upside tail runs fatter than sqrt(t) predicts**, because leveraged funds compound: 252-day cumulative return reaches +2311% in this universe, so no finite grid brackets it. The grid is sized on percentiles and the extremes stay reachable through the comparison families. And **drawdown is capped at 95%**, because it is bounded by construction and above that almost no day sits on the far side.

"Days inside the grid" is also the wrong measure for drawdown, which is one-sided and non-negative: a 1% floor that 46% of days sit below is a *working* threshold in the `<` direction, not a dead one. The metric that matters is how many levels actually split the sample, counting a level as live if it is between 5% and 95% true:

| Window | CumRet live levels | MaxDD live levels |
|---|---|---|
| 5 | 15 of 19 (was 11) | 9 of 19 (was 7) |
| 21 | 33 of 41 (was 11) | 25 of 40 (was 8) |
| 63 | 57 of 69 (was 11) | 41 of 68 (was 8) |
| 252 | 125 of 139 (was 11) | 70 of 92 (was 8) |

The old grids were not *dead*, they were simply far too few. This is a 3x to 11x increase in thresholds that separate anything.

Quantities that are **rate-like** do not scale, because a longer window makes the estimate steadier rather than larger, so mean daily return and daily volatility keep one fixed grid at every window. **They also cannot take a 2-point step, and this is a real constraint rather than an oversight:** their entire useful range is narrower than one such step. Daily volatility runs about 0.2%/day for a quiet bond fund to 6%/day in a panic, and mean daily return about +/-0.5%/day. Forcing percentage-point steps there would collapse each family to two or three levels. They carry the equivalent *resolution* in their own units instead: std dev of return steps by 0.1 percentage points (59 levels), moving average of return by 0.02 (51 levels, roughly 5% a year per step). The constraint is confined to those two families, because every family supplies its own level function; it places no limit whatsoever on how fine cumulative return or drawdown can go.

*RSI levels step by 2, and are deliberately not scaled.* 10 to 90 in steps of 2 is **41 levels**, up from nine. Threshold families cost `tickers x windows x levels x 2`, **linear** in the level count, unlike the comparison families which square with the window count, so the finer grid adds about 1.2% to a maximal run. sqrt-scaling RSI was tried and **measured wrong**: it assumes the distribution is symmetric about 50, and a trending asset sits above 50 for years, so the scaled grid drifted off the part of the range that actually separates days. Retracted in favour of the fixed fine grid. A separate earlier claim, that levels below 26 and above 80 never separate anything, is also **wrong** and corrected here: they do produce distinct series at short windows, they are simply more than 95% true, which is near buy-and-hold.

*Sixteen families over all nine Composer functions.* Every function in Composer's condition dropdown is now reachable: `current-price`, `cumulative-return`, `relative-strength-index`, `moving-average-price`, `moving-average-return`, `exponential-moving-average-price`, `standard-deviation-price`, `standard-deviation-return`, `max-drawdown`. Families come in three kinds, and the kind is what governs cost:

| Kind | Shape | Specs |
|---|---|---|
| `lvl` | one series against a constant | `n x W x levels(p) x 2` |
| `cmp` | two (ticker, window) operands | `m x (m-1)`, `m = n x W` |
| `self` | two indicators, one ticker, one window | `n x W x 2` |

| Group | Family | Kind | Default |
|---|---|---|---|
| Price | Price vs own moving average | `self` | on |
| Price | Price vs own EMA | `self` | on |
| Price | Moving average of price compare | `cmp` | on |
| Price | EMA of price compare | `cmp` | off |
| Price | EMA vs moving average (same ticker) | `self` | off |
| Return | RSI vs level | `lvl` | on |
| Return | RSI vs RSI | `cmp` | on |
| Return | Cumulative return vs level | `lvl` | on |
| Return | Cumulative return compare | `cmp` | on |
| Return | Moving average of return compare | `cmp` | on |
| Return | Moving average of return vs level | `lvl` | off |
| Risk | Std dev of return compare | `cmp` | on |
| Risk | Std dev of return vs level | `lvl` | on |
| Risk | Max drawdown vs level | `lvl` | on |
| Risk | Max drawdown compare | `cmp` | off |
| Risk | Std dev of price compare | `cmp` | off |

The five that are off by default are off because they are expensive or rarely productive, not because they are broken. Cross-ticker price-scale comparisons in particular (`stdp_cmp`, and the cross-ticker half of `map_cmp` / `ema_cmp`) compare dollar magnitudes, so many of those specs are constant-false and drop out in Pass 1 for having no trades. The *same-ticker* fast-versus-slow half of those families is the golden-cross signal, and is the reason they exist.

*Sizing.* At 72 signal tickers with the 10-day floor (13 active windows), the eleven default families produce **3,936,096 specs**; all sixteen produce 4,931,064; dropping the floor to 5 days (15 windows) takes the default set to 5,142,096. (These are the v1.24.0 figures, after the three price-scale families stopped pairing across tickers; before that they were 4,800,024, 7,522,848 and 6,292,296.) The previous six families on their inherited grids produced 3,042,720 at the same settings, so standardising the grid roughly paid for the new families.

**The level families are 6.5% of the search, which is why their grids can be lavish.** Measured per family at 72 tickers and the 10-day floor:

| Family | Kind | Specs |
|---|---|---|
| `rsi_cmp`, `cum_cmp`, `ma_cmp`, `std_cmp`, `dd_cmp` | `cmp` | 875,160 each |
| `map_cmp`, `ema_cmp`, `stdp_cmp` | `cmp`, same-ticker only | 11,232 each |
| `cum_lvl` | `lvl` | 123,408 |
| `std_lvl` | `lvl` | 110,448 |
| `dd_lvl` | `lvl` | 109,872 |
| `rsi_thresh` | `lvl` | 76,752 |
| `price_ma`, `price_ema` | `self` | 1,872 each |

Five comparison families are **89% of the total**; all four level families together are 11%. The three price-scale families are a rounding error since v1.24.0, having been restricted to same-ticker operand pairs. That asymmetry is the whole argument for lavish level grids: doubling every level count adds a couple of percent, while adding one window to the grid raises each comparison family by roughly `2 x m` specs and there are five of them. The full v1.23.1 pass, halving the step *and* roughly doubling both brackets, took a maximal run from 4,508,712 to 4,800,024, **+6.5%**, in exchange for 3x to 11x more thresholds that separate anything.

*One counter, not two.* `estimate()` used to hand-mirror the arithmetic in `buildSpecs()`, two copies kept in lockstep by hand. Both now call `countSpecs()` / `famSpecCount()`, so the figure shown before a run and the figure the run tests are the same arithmetic rather than two versions of it. Verified across 99 cases (every family, three floors, several ticker counts, plus all families at once) with zero mismatches.

**Specs are stored as columns (v1.23.0).** The same change v1.22.15 made to Pass-1 results, applied to the spec list, which v1.22.15 named as the next largest item. A maximal run now builds over five million specs, and as JavaScript objects that was roughly 300 MB of the tab's ~3.5GB ceiling, held live for the entire run because each stored row indexes back into it. Seven typed arrays (`fi`, `d`, `a`, `b`, `p`, `q`, `lv`) cost **10 bytes per spec**, one allocation per column, with nothing for the garbage collector to trace. A spec object is materialised only where one is genuinely needed: labels, the Composer export, the at-most-150 survivors per target fed into pairing, and the snapshot. Two paths exist by design, `leftRight(spec, cache)` for the pairing path which works from materialised row objects, and `leftRightAt(store, i, cache)` which reads the columns directly so Pass 1 never allocates an object per spec; both funnel into one `boolInto()`. Pass 1 also hands `evalSpecAt` a single reusable `Uint8Array`, since `backtest()` consumes it synchronously, instead of allocating an N-byte array per spec.

**One more correctness fix that came with it.** Price-based indicators (`moving-average-price`, `standard-deviation-price`, `exponential-moving-average-price`, `max-drawdown`) read a `Float64Array` copy of the close series with `NaN` for missing days, not the raw `closes` array. The raw array holds `null` before a ticker listed, and the rolling helpers guard with `v !== v`, which a `null` slips straight past (`null !== null` is false, and `sum += null` adds zero). The existing return-based indicators were never exposed to this because `dailyReturns`/`logReturns` already convert `null` to `NaN` on the way out.

**Verification (2026-08-20).** Headless Edge, driven end to end. `countSpecs` versus `buildSpecs().n` across 99 cases: exact. For all sixteen families the object path and the columnar path (`evalSpec` versus `evalSpecAt`) produce **identical boolean series**, and each emits a well-formed label, `binary-compound` condition and legacy flat block. The grouped family UI, its per-group All toggles and the row-level Default / Select all / Clear were exercised and report the right counts. A live run and a snapshot round trip (run, then reload against the same profile so `localStorage` survives) both render correctly, with sorting correctly inert on the restored view.

**Ticker selection (v1.18.0).** The universe is 72 tickers, which is too many for a flat chip row, so chips render in asset-class groups driven by the `group` field in `prices.json` (see the schema above). Each group carries an **All** toggle, and each of the two rows (Targets, Signals) carries a whole-universe select plus a Clear. The group toggle is a true toggle: if every member is already selected it deselects the group, otherwise it selects all of them. `renderChips()` builds the blocks once at init and holds element maps (`chipEls`, `groupBtns`) keyed by symbol and group name, so `syncChips()` updates state without re-rendering the DOM.

**Why selecting everything is dangerous, and why it is still allowed.** Signal count grows with the square of the **Signal set** (the union, until v1.21.1), and total backtests are `specs × targets`, while the estimate readout shows only `specs`. All 72 tickers as signals is roughly 6.6M before the target multiplier, down from ~8.2M at 80 tickers. This is deliberately not blocked (see the no-hard-cap decision below); the estimate's `warn`/`stop` states and the run confirm are the only guardrails, and a run that large will likely exhaust memory. The per-group buttons exist so that the *useful* bulk selections ("all leveraged", "all bonds") are one click while the pathological one is still a conscious choice.

**Crypto is held as ETFs, never spot.** IBIT and ETHA are in the universe; BTC-USD and ETH-USD are deliberately excluded. Spot crypto trades seven days a week, and since the master date axis is the sorted union of every ticker's trading days, adding it would stretch the axis from ~2,170 trading days to ~2,800 calendar days and insert `null` weekends into every equity series. Indicator windows count **rows**, not calendar days, so `RSI(10)` would silently become 10 calendar days with 2 of 7 missing and a 200-day MA would span ~280 calendar days. That would corrupt every existing signal, not just crypto ones. The ETFs keep the NYSE calendar and, unlike spot, are valid Composer assets, so the "Copy JSON" export stays runnable. Any future non-equity-calendar asset needs the same scrutiny.

**Two-pass model.** Pass 1 backtests every single signal against every target ticker and is the expensive part. Pass 2 pairs surviving signals with AND logic, which is `n²` over the survivors and therefore pruned first. As of v1.16.7 Pass 1 caches **every valid** result (`sigCache`) rather than only those passing the user's thresholds, which is what makes the live filters possible (see Section 14, V2.2).

**CPU load throttle (v1.16.6, reworked v1.16.9, renamed v1.16.10).** Long runs would otherwise pin one core at 100% and heat the machine, since JS is single-threaded. After each batch of 150 signals the loop idles for a multiple of the time that batch actually spent computing, holding a target **duty cycle** regardless of machine speed. Heat tracks the busy *fraction*, not absolute idle seconds, which is why a fixed pause was rejected: a fast CPU clears a batch quickly and the same pause becomes a smaller share of the cycle, so the setting would mean different things on different hardware. `sleep = busy × FACTOR`, so duty ≈ `1 / (1 + FACTOR)`:

| Option | `FACTOR` | Target CPU |
|---|---|---|
| Max | 0.25 | ~80% |
| **High (default from v1.24.7)** | 1.5 | ~40% |
| Medium | 4 | ~20% |
| Low | 9 | ~10% |

**Every level was lowered at v1.22.11, and Max stopped meaning 100%** (owner report: it was crashing browsers). Previously Max ran with `FACTOR` 0, no idle at all. `FACTOR` is derived from the target duty as `100/duty - 1`, verified to round-trip: 0.25 to 80%, 1.5 to 40%, 4 to 20%, 9 to 10%. Since no level is now unthrottled, the old unreachable "max speed" status branch and the `FACTOR ? ... : 0` sleep guard were both removed rather than left as dead code.

**The ceilings stay capped, and this is about heat, not only crashes (owner decision, reaffirmed 2026-08-20 after the memory fix).** Measurement later showed the crashes were largely a memory problem, since the same run held 14.3GB before v1.22.13 and 2.7GB after, which invites the conclusion that lowering Max from 100% treated the wrong cause and could be reverted. It should not be. Raising Max back to 100%, making Max the default, and adding a separate unthrottled option were all offered and **declined**: JS is single-threaded, so a run pins a core regardless of how much memory it holds, and the tool runs on visitors' hardware. If a run is too slow the answer is fewer signals, not a hotter CPU. The throttle is neutralised only inside the headless test harness, never in what ships.

**Batch size scales with the level (v1.22.12): Max 250, High 200, Medium 150, Low 100.** The reason is the `setTimeout` clamp, not responsiveness. Once timers nest, browsers round any requested delay up to roughly 4ms, and `sleep = busy × FACTOR`, so a level with a small `FACTOR` on a small batch asks for a sub-clamp sleep that gets rounded up, holding **less** CPU than the label claims. Measured against the ~29µs/signal implied by a 3,042,720-signal run:

| Option | Batch | Busy | Sleep asked | Sleep actual | Displayed | Real |
|---|---|---|---|---|---|---|
| Max | 250 | 7.2ms | 1.8ms | 4.0ms (clamped) | 80% | ~64% |
| **High (default from v1.24.7)** | 200 | 5.8ms | 8.7ms | 8.7ms | 40% | ~40% |
| Medium | 150 | 4.4ms | 17.4ms | 17.4ms | 20% | ~20% |
| Low | 100 | 2.9ms | 26.1ms | 26.1ms | 10% | ~10% |

Only Max is distorted, and **the distortion always errs toward less CPU, never more**, so the readout overstates load rather than under-reporting it. Closing the gap entirely would need a batch around 550 to lift the requested sleep clear of the clamp, which is back at the size that was in place when Max was crashing browsers, so the honest-but-lower behaviour is preferred. Making the status line report *measured* duty instead of the nominal figure would remove the discrepancy without touching the throttle, and remains open.

**A correction on why Max crashed.** An earlier version of this note asserted the old 500-signal batch was itself a likely cause, on the grounds that the batch boundary is the only point the loop yields. The arithmetic does not support that: at ~29µs/signal a 500-batch blocks the main thread for about 14ms, which is a long frame, not a hang, and nowhere near what makes a browser kill a tab. The plausible causes are the uncapped duty cycle and, more likely at scale, the documented memory ceiling below, since Pass 1 holds a `Uint8Array` per surviving signal. Batch size in the 100 to 250 range is essentially irrelevant to hang risk and was chosen for clamp accuracy instead.

Option values are `max`/`high`/`medium`/`low`, renamed from `full`/`balanced`/`eco`/`cool` at v1.16.10 specifically because the old `eco` value meant the ~25% tier and would have collided with an "Eco" label on the ~10% tier. The status line shows a live estimate of **time remaining** (v1.18.1 added it; v1.22.10 trimmed the projected total and idle-time figures that used to sit beside it, since the CPU percentage already implies why a throttled run outlasts its compute time). The projection itself is unchanged and still drives the remaining figure: total and idle are projected from *compute* measured so far, scaled by the duty factor, and remaining is `projTotal - elapsed` off the wall clock, so the two always agree and remaining counts down monotonically. **Corrected in v1.22.13: the estimate now projects from wall-clock throughput.** `elapsed × (1 - frac) / frac`, suppressed for the first five batches and shown as "estimating..." until then. The compute-scaled projection was rejected because it assumed idle equals `busy × FACTOR` exactly. Whenever real idle ran longer than that, through timer clamping, a backgrounded tab, or GC pauses, `elapsed` overtook the projection and remaining pinned itself at zero: the owner reported "1 second left" at 2,100,585 of 3,050,000. A simulation of a degrading run reproduces it precisely, the old estimator reading 0s at 69% complete where the corrected one reads 206s. The original objection to wall-clock projection was real but small: at a boundary the current batch's sleep has not yet happened, so the first reading understates by one batch's sleep out of `batchNo`, an error that disappears within a handful of batches when any real run has thousands. The five-batch warm-up covers it without inheriting the pinning failure. This only governs speed and heat; results are identical at every setting.

**Last-run snapshot (v1.19.1).** After each run the **top 100 rows by Sortino** are saved to `localStorage` under `composer-atlas.signal-miner.lastrun.v3`, along with the run's sample window, total result count and timestamp. Revisiting the page shows them instead of an empty table. Measured payload is 28KB for singles and 39KB for AND pairs, well inside a 5MB quota; `spec`/`specs` travel with each row so **Copy JSON still works** on restored rows. The key carries a schema version: adding a metric to the saved rows means bumping it (v1 to v2 when `annRet` was added in v1.20.0) so an older snapshot is discarded rather than restored with a permanently blank column. One run rebuilds it.

**Only the displayed rows are saved, and this is a hard limit rather than a choice.** The full run lives in `sigCache`, which holds a `Uint8Array` per surviving signal and reaches hundreds of MB on a large run: past any storage quota, and slower to serialise than simply re-running the backtest. A restored view is therefore **read-only for sorting**: sort headers are marked `is-inert` and do nothing until a fresh run repopulates the cache, because re-ranking only the saved 100 would appear to work while silently ranking a subset. The text filter stays live, since narrowing 100 visible rows is honest, and `snapshotNote` is preserved across re-renders so filtering never hides the fact that a snapshot is on screen.

**Runs use a common sample window (v1.19.0).** Every run is scored over one shared stretch of history: `windowInfo()` starts the window at the **latest** first-valid date among the selected tickers, so the most recently listed fund binds the whole run, and `backtest(arr, lret, s0, nw)` divides the per-day averages by that window length rather than the full axis.

Before this, `tim` and the mean feeding Sortino both divided by `N`, the entire axis, even though a fund that listed partway through has `null` closes earlier and physically cannot fire a signal there. Short-history tickers were therefore penalised for history they never had: IBIT covers ~30% of the axis, so an IBIT signal could not show `tim` above 0.30 however good it was. Measured on a simulated 30%-coverage ticker, `tim` moved 0.166 to 0.555 (correctly, 361 fires out of the 650 days it could fire) and **Sortino had been understated by 70%**. Total return and max drawdown are unchanged, since the same trades happen either way; only the denominators were wrong.

Consequences: metrics are comparable *within* a run but **not across runs with different ticker selections**, so the window is stated in the results meta line and in the pre-run estimate, naming the ticker that binds it. Selecting one recent ticker collapses the window for everything, so the estimate flags a `warn` state below 60% coverage and refuses to run below 30 shared trading days. One known imprecision: indicator warm-up is not added to the window start, so a 200-day signal on the binding ticker loses its first 200 days inside the window. Making the start per-spec was judged not worth the complexity.

**Comparison signals are generated in canonical operand order (v1.18.4).** `X < Y` and `Y > X` are the same condition. `buildSpecs()` originally walked the full Cartesian product of tickers, emitting both `(a,b)` and `(b,a)` with both `GT` and `LT`, so **every two-sided comparison was generated exactly twice, and every AND pair four times** (two spellings per condition). Users saw four identical result rows for one signal, and half of every run's compute went on mirror images.

`pushCmpSpecs()` now emits each unordered operand pair once, ordering operands by ticker index then window, keeping both directions. Coverage is unchanged: `Y > X` is still reachable, spelled `X < Y`. Same-ticker comparisons keep only `p1 < p2`, which drops both the mirror and the degenerate `p1 === p2` (a series compared against itself, always false); different windows on one ticker are real signals and survive. Verified by porting old and new generators and comparing canonicalized meanings: zero coverage lost, zero spurious specs, zero duplicates remaining.

Effect is roughly **2x fewer specs**, so runs are about twice as fast and use about half the memory, which also raises the practical ceiling before a big run exhausts the tab. `estimate()` carries its own copy of the count formula and was updated in lockstep; a comparison family over `m = n × windows` operands is `m × (m-1)` specs, previously `n² × W² × 2`.

**Results rendering is bounded (v1.18.2).** The table shows the top `DISPLAY_CAP` rows (100, reduced from 500) and never orders the full result set. `selectTop()` makes one O(n) pass keeping a size-N buffer, with a fast reject against the worst kept row, so cost scales with rows *kept* rather than rows scanned. This replaced a filter + `slice()` + full `Array.sort()` over every cached row, which on a multi-million-row run allocated several huge arrays and froze the tab for seconds on **every sort click**. The full result set stays in `lastResults`, so sorting still ranks across all of it; only the ordering work is bounded.

Supporting changes: the results text filter is debounced 250ms (it fired on every keystroke), and matching uses an allocation-free `containsCI()` rather than building a lowercased string per row. One behavior difference: the old filter searched `label + ' ' + target` as a single string, so a needle spanning that boundary could match; matching is now per-field. Above `BUSY_ROWS` (200k) a render dims the table and shows a spinner before starting, via a double `requestAnimationFrame` so the browser paints the busy state before the main thread is occupied.

**Still synchronous:** `applyFilters()` itself rebuilds `lastResults` from the Pass-1 cache on the main thread, so the section-3 filters can still stall on a very large run. Bounding that would need chunked yielding or a worker; not done.

**Pass 1 no longer caches an array per signal (v1.22.13). This was the tool's real scaling limit.** Pass 1 used to keep the `Uint8Array` of every surviving signal in a `survivorArr` map so Pass 2 could AND them into pairs. At 4,183 bytes each (one byte per trading day) a 3,000,000-signal run held roughly 4GB at a 50% survival rate, crossed the tab's heap ceiling near 2,000,000 signals, and spent the remainder of the run in garbage collection and swap. That matches the owner's report exactly: throughput collapsing at ~2.1M of 3.05M.

The cache was also almost entirely **dead weight**. Pairing reads only the top `SURV_CAP` (150) survivors *per target*, chosen after filtering, quantile pruning and a Calmar sort, so on a seven-figure run well over 99.9% of the cached arrays were never read once. Nothing is cached now: `applyFilters` regenerates the ~150 arrays it needs with `evalSpec` after applying the cap, which is a few hundred thousand operations and finishes in under a millisecond. `sigCache` carries the shared indicator `cache` instead (~30MB for 72 tickers with every family on), and `_si`, which existed only to index the old map, is gone.

**Measured, not argued (2026-08-20).** Both builds were driven through the identical scripted session in headless Edge on the full 3,042,720-signal run that prompted the report (1 target, all 72 signal tickers, all families, combine depth 2), with process memory sampled from outside the browser:

| | Before (v1.22.12) | After (v1.22.13) |
|---|---|---|
| Peak process memory | **14,264 MB** | **2,747 MB** |
| Wall time | 541s, cut off at the harness limit | **139s** |
| Completed | **No.** Renderer died, zero DOM dumped | **Yes** |
| Result | n/a | 2,483,189 single + 8,182 combined |

Survival on that run was 81.6%, so the old cache alone accounted for 2,483,189 x 4,183 bytes = 10.4GB, which matches the measured peak once the baseline and `allSingles` are added. The old build could not finish the run at all.

A separate scripted session, small enough for both builds to complete, was diffed cell for cell across twenty result rows and every metric column: **byte-for-byte identical**. The refactor changes memory and nothing else.

**Nothing about behaviour changed.** Re-filtering is still instant and still does no single-signal backtesting, because what was expensive was never the array construction, only its retention. Two cheaper ideas considered and rejected as unnecessary once this was found: skipping the cache when Combine signals is 1 (it is now never built at all), and bit-packing the arrays to one bit per day (there is no longer a large population to pack).

**Pass-1 results are stored as columns, not as objects (v1.22.15).** A second owner report after v1.22.13: the run finished faster but the tab still died with a memory error, on a machine with **48GB of RAM**. That detail is what identifies the ceiling, because it was never the machine's.

**A browser tab's heap ceiling is fixed and does not scale with installed memory.** Measured via `performance.memory.jsHeapSizeLimit` in Edge on that class of hardware: **3,586 MB**. An 8GB laptop and a 48GB workstation get the same allowance. "Out of memory" / "Aw, Snap" is that allowance being exhausted, not the OS running short, which is why adding RAM does nothing and why the fix has to be to hold less.

What remained after v1.22.13 was one JavaScript object per result. A 3,000,000-signal run yields roughly 2,500,000 of them and each costs about 300 bytes: object header and slack, eight separately heap-allocated doubles (V8 no longer stores doubles inline in objects), and a `label` string built eagerly for every row when only the 100 on screen are ever read.

Columns instead: eight `Float64Array`s for the metrics, a `Uint32Array` of spec indices and a `Uint8Array` of target indices. **69 bytes per row**, flat, one allocation per column, outside the object heap and holding nothing for the garbage collector to trace. Row objects are materialised only where one is genuinely needed: the `DISPLAY_CAP` rows on screen, the `SURV_CAP` per target fed into pairing, and the saved snapshot. Labels are derived from the spec at that moment via `specLabel`, which is the same trade the survivor cache lost: recomputing on demand beats retaining for a population that is never read.

Two related savings came with it. `selectTop` now carries **indices** through its scan and materialises only the rows it keeps, where before it built a throwaway object per candidate on every sort click. And `applyFilters` built `rows = allSingles.filter(...)`, a second full array of row objects alongside the first, so a large run paid for its results twice; the passing set is now a `Uint32Array` of indices at four bytes per row.

| | Before (v1.22.14) | After (v1.22.15) |
|---|---|---|
| Peak JS heap | 1,144 MB | **527 MB** |
| Peak process memory | 2,459 MB | **1,502 MB** |
| Wall time | 140s | **110s** |
| Result | 2,483,189 single + 8,182 combined | identical |

The heap figure is the one that matters, since that is what the 3,586 MB ceiling bounds. Roughly **2.2x more headroom**, moving the crash point from about 7.8M retained rows to about 17M. The 21% speedup is a side effect of not tracing millions of objects on every collection.

**Retention is per signal PER TARGET, and the estimate line is not.** The pre-run estimate counts signals and deliberately excludes the target count because the target set does not change how many conditions exist. Rows do not work that way: Pass 1 keeps one per (signal, target), so two targets on a 3M-signal run retains up to 6M rows while the estimate still reads 3,042,720. When sizing a run against the ceiling, multiply.

**Verified against the previous build**, both driven through an identical scripted session over 47,163 results covering the default sort, sorting by a text column and by a numeric one, two text filters, a live Time-in-Market re-filter, the single-row export, the combined ladder export and the baseline row. Output **byte-for-byte identical**, 25,088 characters. The snapshot round trip was tested separately (run once, reload against the same profile so `localStorage` survives) because that path builds the result set from a plain array rather than the store and the first test never reached it. Also identical, with sorting correctly still disabled on the restored view.

**Known remaining cost.** The `specs` array is now the largest single item, roughly **300 MB of the remaining 527 MB**: about 3M small objects built up front by `buildSpecs` and retained for the whole run so a row's `si` index can resolve back to one. Packing those into typed arrays the same way would take the heap to roughly 230 MB, another ~2.3x, but it touches `evalSpec`, `leftRight`, `specLabel` and the exporter, all of which take a spec object today. Deliberately left out of v1.22.15 rather than bundled into it. **Done in v1.23.0** (see below), which was also what made the sixteen-family expansion affordable.

**The `ti` column is a `Uint8Array`,** which caps a run at 255 targets. The universe is 72 tickers, so this cannot bind today; Pass 1 throws explicitly rather than silently truncating if it ever does.

**No hard signal cap (v1.16.4; thresholds recalibrated v1.24.2).** Large runs are warned about, not blocked. Above `SIGNAL_WARN_CAP` (1,200,000 signals) a `confirm()` projects how long the run will take at the selected CPU setting (v1.24.5), and the user can proceed or cancel. The pre-run estimate readout escalates ahead of that: a `warn` state above `SIGNAL_WARN_SOFT` (600,000) and a `stop` state above the cap. **What actually binds, as of the 2026-08-21 measurements in Section 14 item 3: time, not memory.** A genuinely maximal run (51 full-history tickers, 2,064,072 specs) peaks at 977 MB against a ~4.2GB ceiling, roughly 24%, so the heap is no longer the thing that kills a run; v1.22.13, v1.22.15 and v1.23.0 between them cut what a run retains by well over an order of magnitude. The same run costs about 3.5 minutes unthrottled and 17 minutes at Medium, and the 72-ticker default is about 30 minutes at Medium. The confirm dialog was reworded in v1.24.5 to match: it projects a duration from the measured throughput and the selected CPU duty rather than warning about browser sluggishness, and it says that a run has no cancel button, so the only way to stop one is reloading the page. The fix for a run that is too big is fewer signals (fewer tickers, or a family switched off) or fewer targets, not a gentler throttle, which only trades wall time for responsiveness. Note that raising Min Time in Market does not help, because that filter runs after Pass 1 and the rows are already stored by then.

**Ticker selection defaults and persistence (v1.18.3; extended to settings v1.24.7).** First visit starts at Target `TQQQ` with signal tickers `QQQ`, `SPY`, `IWM`, `DIA`. After that the selection is restored from `localStorage` under `composer-atlas.signal-miner.tickers.v1`, and the six section-3 settings from `composer-atlas.signal-miner.settings.v1`. Two keys rather than one, so clearing either never disturbs the other.

**This reverses a deliberate earlier decision, on the owner's instruction.** Until v1.24.7 only the ticker sets persisted, and the stated reason was that CPU load and the filters govern how heavy a run is, so they should stay a conscious choice rather than something inherited from a forgotten session. The counter-argument that won: a visitor who tunes six controls and refreshes has lost work for a reason they cannot see, and the risk the old rule guarded against is now covered by a **Default** button that restores everything in one click. The residual risk is real and worth naming: someone who leaves CPU load on Low will find every future run slow with no indication why, because the control looks the same whether it was chosen this session or three weeks ago.

**Signal families persist too**, on the owner's instruction, so the whole of section 3 behaves one way rather than two. They are stored as a **list of the ids that are ON**, not a map of every family. That asymmetry is deliberate: a family added to `FAMILIES` in a later release is absent from a returning visitor's stored list and therefore defaults to OFF, rather than silently switching itself on for everyone and enlarging every run. A new family changes how heavy a run is, so it should be opted into. Ids in storage that no longer exist are ignored, so removing a family cannot strand a stale entry.

`syncFamilies()` is the single choke point every path that changes a checkbox goes through, including the group **All** buttons, so persistence hangs off that one call rather than off the individual boxes. Stored symbols are validated against the current universe on load, so pruning a ticker from `prices.json` (see the duplicate-ETF roadmap item) cannot strand a stale selection in someone's browser. A stored-but-empty selection is honoured rather than overwritten with defaults: only the *absence* of a stored value counts as a first visit, so hitting Clear and refreshing shows the cleared state. All storage access is wrapped in try/catch, so private mode or disabled storage degrades to defaults instead of breaking the page.

**Annualized return column (v1.20.0).** The results table shows `annRet` immediately after Total Return, sortable like any other column. It is a CAGR over the **run's common sample window**, not over days in market: a signal that sits in cash most of the time is not credited as though the idle stretches never happened. Because `cum` is already a cumulative log return the implementation is `Math.exp(cum * 252 / nw) - 1`, avoiding a fractional power of a possibly-tiny base; this is exactly equal to `(1 + total) ** (252 / nw) - 1`.

**It does not add a ranking dimension.** `nw` is computed once per run and passed to every `backtest()` call, so within a single result set `annRet` is a strictly monotone transform of `total` and sorts in identical order. It exists to make a magnitude readable (400% over eight years versus over two), not to give a second opinion on which signal is best; Sortino and Calmar are the columns that rank differently. For the same reason `annRet` is deliberately excluded from `quantilePrune`, where it would apply the Total Return cut a second time. If the sample window ever becomes per-row, this note stops being true and the column becomes independently meaningful.

**Max drawdown and Calmar corrected (v1.21.0).** Two metric bugs, both found by adding the buy-and-hold baseline, which put an obviously wrong number on screen where signal rows had hidden it.

`maxDD` was `ret - peakRet`, an absolute gap in return units, rather than `eq / peakEq - 1`, a percentage of the peak. The two are equal only while the equity multiple stays near 1.0. Once a series compounds, the gap is denominated in the grown equity and passes -100%: **TQQQ over the 2010 axis reported -16761% against a true -81.7%**, and SPY -133.6% against -33.7%. This had been wrong since the tool shipped and got worse with the longer axis. Its practical bite was the **Max Drawdown floor**: at the `-0.8` default, anything that had compounded at all failed the filter, so the tool was quietly discarding its best results. `backtest` now tracks `peakEq` as the high-water mark of `Math.exp(cum)`.

`calmar` divided **total** return by drawdown, which is only comparable between runs of equal length. On the 2010 axis buy-and-hold TQQQ scored 418 that way against a real Calmar of 0.52, and the "at or below 1.0 is a warning sign" guidance elsewhere in this document silently stopped applying. It now divides `annRet` by drawdown, the standard definition, which is window-length independent. This is a deliberate divergence from the source notebook, and it changes Calmar sort order.

**`tim` denominator (v1.21.0).** Divided by `nw` where the loop iterates `N - max(1, s0)` times, so an always-on signal scored 0.9998 rather than 1.0 when `s0` was 0, and the two window cases disagreed by a day. Now divides by the loop's exact iteration count. Cosmetic at 1 day in 4183, but the baseline makes it visible, and `tim === 1.0` for buy-and-hold is a useful check that the window plumbing is right.

**Buy-and-hold baseline (v1.21.0, benchmarks fixed in v1.22.0).** Each run backtests the degenerate always-on signal over the run's window, rendered as a strip above the results table. Benchmarks are a **fixed set** (`BASELINE_TICKERS` = TQQQ, QQQ, SPY, BIL) rather than the run's selected targets, so the yardstick does not move when the selection changes and two runs stay comparable to each other. BIL is the cash floor: it is what a signal earns while switched off, so a strategy that cannot beat it is not paying for its complexity.

A benchmark may list after the run's window opens (TQQQ starts 2010-02-11, the axis 2010-01-04), so each is clamped to `max(win.s0, firstValidIndex(sym))` and the strip shows "from <date>" when its window is shorter, rather than crediting it with flat days it did not exist for. A benchmark pruned from the universe is skipped, so `BASELINE_TICKERS` cannot break the page.

**BIL's ratio metrics are extreme, and that is left unannotated on purpose (owner decision, v1.22.3).** Cash has near-zero drawdown, so Calmar (annRet / |maxDD|) explodes: BIL scores 3.11 over the full window and **402 over a 2.6-year one**, with Sortino above 6,000. The arithmetic is correct and the result is a useful reductio of any ratio that puts drawdown in the denominator, so the numbers are shown as computed with no caveat text. An explanatory note was added in v1.22.1 and removed in v1.22.3 as unnecessary hand-holding.

**The baseline strip carries no explanatory copy at all** (v1.22.3): the numbers and the "Buy & hold benchmarks over the same window" heading stand alone. The note that used to sit under it was also the source of the v1.22.2 outage, so anything added back here should be checked with the string-termination linter rather than eyeballed. Every signal is a bet that being in the target *sometimes* beats being in it *always*, and without that reference the table has no scale. It reuses `backtest()` unchanged rather than deriving the numbers separately, so any difference from a signal row is attributable to the strategy and not to differing arithmetic. Rendered outside the table deliberately: baselines must not sort, must not be filtered away, and must not consume one of the 100 display slots. Carried in the snapshot; an older snapshot without them simply hides the strip.

**Conditions come from the Signal set only (v1.21.1).** `run()` passes `cmp` to `buildSpecs`, not the `universe` union of targets and signals. Before this, selecting TECL as a target and XLK/KMLM as signals still generated TECL conditions with no way to opt out: the Signal set could only add tickers, never restrict them, which made the two boxes' labels misleading.

Self-referential rules (`if RSI(TECL) > 79 then hold TECL`) remain fully reachable by putting the ticker in **both** boxes, which reproduces the old spec set exactly (verified: 708 specs either way on the reported case). The union could only ever add, so this is strictly more expressive, not a reduction in coverage.

`universe` is still correct for the two calls above it and must not be changed: `windowInfo(universe)` because a target's listing date bounds the common sample window, and `buildCaches(universe, ...)` because `targetLret` reads `cache[t].lret`. Only the `buildSpecs` call moved.

`estimate()` keeps its own copy of the count formula and now uses `compares.size` rather than the union size. **This is the third time that duplicate formula has needed a matching edit** (v1.18.4, v1.20.0, v1.21.1); it is a standing drift risk and worth collapsing into one shared function if it needs touching again. Verified in lockstep across four selection shapes, with an added assertion that no condition references a ticker outside the Signal set.

A run with an empty Signal set is now rejected with an explanatory message rather than silently producing nothing.

**Filter defaults (recalibrated v1.24.7, owner's values).** Min Time in Market **15%**, Max Drawdown floor **69%**, prune quantile `0` (v1.16.8, so nothing is trimmed before pairing and all qualifying signals show by default), combo depth `2`, min period `10`, CPU load **High**. The previous values were `0.05` and `-0.8` (v1.16.4) with CPU on Medium.

**Both floors are now entered as percentages**, and drawdown is entered **unsigned**: a floor of `69` means "reject anything that fell more than 69% from a peak". Asking someone to type a minus sign in front of a number already called a floor was a small, permanent papercut. `applyFilters` divides by 100 and negates the drawdown; the store still holds fractions and nothing about the comparison changed. An unparseable floor now falls back to `-1` (admits everything) rather than `NaN`, which silently emptied the table, since a filter that cannot be read should not be the strictest filter there is.

**The stricter defaults cost about 2% of the leaderboard, not most of it.** Measured on a default run: 36,523 displayed rows under the old floors, 35,706 under the new ones. Worth knowing, because tightening two filters at once looks like it should be dramatic.

**One source of truth: `DEFAULT_SETTINGS`.** This used to live in three places (the init defaults, `loadDefaults`, and `loadExample`) with a note to keep them in sync by hand. They are now one object keyed by element id, and the HTML attributes carry the same values so the controls are correct before any script runs. The `settings` harness asserts the two agree, which is the failure this arrangement is designed to make impossible to ship. Two buttons in the Target tickers row restore a whole preset: **Default** (v1.22.4) calls `loadDefaults()`, which puts back `DEFAULT_TARGETS` / `DEFAULT_COMPARES` plus `DEFAULT_SETTINGS` and writes it through to storage, and **Community V2 Example** calls `loadExample()`, which loads the 8-ticker heavy run and deliberately drops min period to `5` (its own filters, `5%` and `80%`, are unchanged in meaning from when they were written as `0.05` and `-0.8`). Both loaders null `sigCache`, since changing the ticker set makes the previous run's cached results inapplicable to the live filters. Prune quantile applies within each target ticker and runs **sequentially** across total return, profit factor, Sortino, and Calmar (matching the source notebook), so its effect compounds: `0.5` does not leave half the signals, it leaves what survives the top half on each of the four metrics in turn.

---

### Metric Display Guidelines

**Formatting:**
- Float percentages: display as `+XX.X%` or `-XX.X%` (multiply by 100, 1 decimal place; always include sign)
- Ratios (Sharpe, Calmar): plain decimal `X.XX`, no percent sign
- All numeric values: monospace font (`font-mono`)
- `last_updated`: human-readable (e.g., `Jun 8, 2026`)

**Color coding:**

| Value Type | Color |
|---|---|
| Positive return / ARR / trailing returns | `--color-green` |
| Negative return / max drawdown | `--color-pink` |
| Calmar ratio, Sharpe ratio | `--color-primary` (no color coding) |
| Standard deviation | `--color-primary` |
| Min period return (negative) | `--color-pink` |
| Max period return (positive) | `--color-green` |
| Mean / median period return | `--color-yellow` |

**MetricsTable display order (as implemented in `renderMetricsTable()`):**
1. Returns: Ann. Return, Cumulative Return
2. Risk: Max Drawdown, Std Deviation
3. Risk-Adjusted: Sharpe Ratio, Calmar Ratio
4. Daily Distribution: Worst Day, Mean Day, Median Day, Best Day (**relabelled in v1.27.8**;
   these were shown as "Min Month" through "Max Month" and the period was wrong)
5. Trailing Returns: 1-Month, 3-Month, 1-Year
6. Metadata: Backtest Period, Last Updated

---

### Canonical Tag Vocabulary

Tags must match the `slug` of a glossary entry in `data/glossary.json`. The 8 tags below were the
full set at MVP and the table is kept as written:

| Tag | Glossary Slug | Concept |
|---|---|---|
| `rsi` | `rsi` | Relative Strength Index |
| `200d-ma` | `200d-ma` | 200-Day Moving Average |
| `momentum` | `momentum` | Momentum Investing |
| `vix-tiers` | `vix-tiers` | VIX Tier Rotation |
| `leveraged-etfs` | `leveraged-etfs` | Leveraged ETFs |
| `sharpe-ratio` | `sharpe-ratio` | Sharpe Ratio |
| `calmar-ratio` | `calmar-ratio` | Calmar Ratio |
| `max-drawdown` | `max-drawdown` | Max Drawdown |

Add new tags only when a corresponding glossary entry exists or is planned.

---

### Glossary Concept JSON Schema

All fields in `data/glossary.json`. Both `glossary.json` and `glossary.js` must always be kept in sync.

```json
{
  "slug": "string",          // URL slug, must match tag values in strategies.json
  "name": "string",          // Display name
  "category": "string",      // "indicator" | "risk-metric" | "asset-class" | "strategy-concept"
  "description": "string",   // One-sentence definition (under 160 chars)
  "formula": "string|null",  // Mathematical formula in plain text, or null
  "related_tags": ["string"],// Tags in strategies.json that map to this concept
  "last_updated": "string",  // ISO date of last content revision (YYYY-MM-DD)
  "sections": [
    {
      "title": "string",
      "paragraphs": ["string"],
      "table": {              // Optional: renders as a two-column table
        "headers": ["string"],
        "rows": [["string"]]
      }
    }
  ]
}
```

**Category values:**

| Value | Display Label | Badge Color | Used For |
|---|---|---|---|
| `indicator` | Indicator | Blue | RSI, 200d MA, momentum signals |
| `risk-metric` | Risk Metric | Pink | Sharpe ratio, Calmar ratio, max drawdown |
| `asset-class` | Asset Class | Yellow | Leveraged ETFs, bonds, equity indices |
| `strategy-concept` | Strategy Concept | Purple | VIX tiers, defensive rotation, rebalancing |

**Required sections (in order):** Definition, How It Works, In Practice, Limitations

**Optional sections:** Additional sections with any title. All 8 MVP entries include a "Building with [Concept] in Composer.trade" essay section.

**Canonical glossary entries (current; 20 total):**

| Slug | Name | Category |
|---|---|---|
| `rsi` | RSI | indicator |
| `200d-ma` | 200-Day Moving Average | indicator |
| `sma` | Simple Moving Average | indicator |
| `ema` | Exponential Moving Average | indicator |
| `macd` | MACD | indicator |
| `momentum` | Momentum Investing | strategy-concept |
| `vix-tiers` | VIX Tiers | strategy-concept |
| `mean-reversion` | Mean Reversion | strategy-concept |
| `volatility-decay` | Volatility Decay | strategy-concept |
| `zoop` | Zoop's Strategies | strategy-concept |
| `original` | Original Strategies | strategy-concept |
| `backtesting` | Backtesting | strategy-concept |
| `leveraged-etfs` | Leveraged ETFs | asset-class |
| `managed-futures` | Managed Futures | asset-class |
| `inverse-etfs` | Inverse ETFs | asset-class |
| `sharpe-ratio` | Sharpe Ratio | risk-metric |
| `calmar-ratio` | Calmar Ratio | risk-metric |
| `max-drawdown` | Max Drawdown | risk-metric |
| `standard-deviation` | Standard Deviation | risk-metric |
| `annualized-return` | Annualized Rate of Return | risk-metric |

**Glossary entry checklist (before committing):**
- [ ] `slug` is lowercase, hyphen-separated, unique
- [ ] `slug` matches a tag value used in `strategies.json`
- [ ] `category` is one of the four valid values
- [ ] `description` is one sentence, under 160 characters
- [ ] `sections` includes all required sections: Definition, How It Works, In Practice, Limitations
- [ ] `last_updated` is today's date
- [ ] Identical entry added to `data/glossary.js`
- [ ] JSON validates: `python -c "import json; json.load(open('data/glossary.json')); print('OK')"`
- [ ] Detail page renders correctly at `http://localhost:8000/glossary.html?slug=your-slug`

---

## 13. Composer API Reference

Base URL: `https://api.composer.trade`

### Authentication

Most endpoints require no authentication. Try without auth first. If auth is required:

```
x-api-key-id: <key-id>
authorization: Bearer <key-secret>
```

Get credentials: Composer.trade → Settings → API Access → Generate New API Key.

Composer Atlas uses only the two unauthenticated endpoints listed below. No credentials are stored or required.

### Rate Limits

| Endpoint | Documented Limit |
|---|---|
| All endpoints (default) | 1 req/sec |
| `POST /symphonies/{id}/backtest` | 500 req/sec |

**Empirically observed (v1.9.4-v1.9.5):** the documented 500 req/sec ceiling does not hold in practice. Four one-time tests against `/backtest`, at four different rates:

| Test | Result |
|---|---|
| Sequential, 1 call per 2 seconds (0.5 req/sec), the original throttle | 140 consecutive calls, **zero** failures |
| Sequential, 1 call per second (1 req/sec) | 25 succeeded, then `HTTP 429: Too Many Requests` |
| ~2 concurrent req/sec | 25 succeeded, then 429s |
| ~20 concurrent req/sec | 25 succeeded, then 429s |
| ~100 concurrent req/sec | 25 succeeded, then 429s |

**Conclusion: this behaves like a token-bucket limiter, not a flat requests-per-second cap.** Burst capacity is ~25 requests, refilling at roughly the rate already proven safe (~0.5 req/sec, i.e. 1 call per 2 seconds). At 0.5 req/sec, consumption matches the refill rate, so the bucket never empties and the run sustains indefinitely (140/140, zero failures). At every faster rate tested, from 1 req/sec all the way to 100 concurrent req/sec, the initial ~25-request bucket drains and then every subsequent call gets throttled until it refills, regardless of how much faster than 25/window the attempted rate was. Whatever is enforcing it is likely a Cloudflare layer in front of the documented API limit, not the API's own application-layer limit. Failed calls do not corrupt data: `apply_backtest_result()` is never called on failure, and `refresh_date` is only advanced on success, so a 429'd row just stays correctly marked "due" for the next run.

**Practical takeaway:** stick to the existing 1-call-per-2-seconds sequential throttle for any bulk refresh. There is no known safe way to go faster without triggering the bucket; do not re-test higher rates without a specific reason, each test costs ~25 wasted/retried calls plus whatever cooldown the bucket needs to refill.

The sequential, 1-call-per-2-seconds throttle already used by `update_metrics.py` and `refresh_full_database.py` is the validated, sustainable approach; it processed 140 consecutive rows with zero failures before being intentionally paused. Do not attempt higher concurrency against this endpoint without re-testing carefully at small scale first.

### Backtest Endpoint

`POST /api/v0.1/symphonies/{symphony-id}/backtest`

**Request body used by `update_metrics.py`:**

```json
{
  "capital": 10000,
  "broker": "alpaca",
  "slippage_percent": 0.0005,
  "apply_reg_fee": true,
  "apply_taf_fee": true
}
```

**Key response fields (under `stats`):**

| Field | Type | Notes |
|---|---|---|
| `annualized_rate_of_return` | float | Maps 1:1 to schema field |
| `cumulative_return` | float | Maps 1:1 |
| `calmar_ratio` | float | Maps 1:1 |
| `sharpe_ratio` | float | Maps 1:1 |
| `standard_deviation` | float | Maps 1:1 |
| `min`, `mean`, `median`, `max` | float | **Daily** distribution: maps 1:1 |
| `trailing_one_month_return`, etc. | float | Maps 1:1 |
| `max_drawdown` | float | **Returned as positive by API; stored as negative in schema** |
| `size` | integer | Backtest days; stored as `backtest_days` in schema |

Full response also includes `dvm_capital`, `tdvm_weights`, `rebalance_days`, `last_market_days_holdings`, `costs`, `legend`, `data_warnings`, `benchmark_errors`.

**Available `stats` fields not yet captured by any schema** (confirmed live against 5 real symphonies on 2026-07-07; candidates for the Leaderboard/Screener target schema, see Section 14 Roadmap):

| Field | Notes |
|---|---|
| `sortino_ratio` | Downside-only risk-adjusted return; strong leaderboard/screener candidate |
| `win_rate` | Fraction of winning periods |
| `skewness`, `kurtosis` | Return distribution shape; tail-risk indicators |
| `tail_ratio` | Ratio of right-tail to left-tail extremes |
| `top_one_day_contribution`, `top_five_percent_day_contribution`, `top_ten_percent_day_contribution` | How concentrated returns are in a handful of days |
| `herfindahl_index` | Portfolio concentration score |
| `annualized_turnover` | Trading frequency; proxy for fee/tax drag not otherwise modeled |
| `trailing_one_day_return`, `trailing_one_week_return`, `trailing_two_week_return` | Finer-grained trailing windows than the three currently stored |

**Available top-level fields not yet captured by any schema:**

| Field | Notes |
|---|---|
| `last_market_days_holdings` | Current live allocation (ticker → $ amount); screener candidate ("currently holding TQQQ") |
| `active_asset_nodes` | **Not a ticker list** (corrected in v1.9.1 after live validation): a dict of internal node UUID → weight. Real ticker symbols live in `last_market_days_holdings` instead. |
| `costs` (`reg_fee`, `taf_fee`, `cat_fee`, `slippage`, `spread_markup`) | Real cost drag beyond the net return figure |
| `data_warnings` | Composer's own flag that a backtest's underlying data may be shaky |
| `dvm_capital`, `rebalance_days` | Full daily capital time series; heavy, more suited to a future performance chart than a leaderboard row |

### Logic Tree Endpoint

`GET /api/v0.1/symphonies/{symphony-id}/score`

| Param | In | Required | Notes |
|---|---|---|---|
| `symphony-id` | path | yes | |
| `score_version` | query | yes | `"v1"` or `"v2"`: use `"v1"` |

Returns the symphony's full IF/ELSE logic tree as a nested JSON object. The `step` field on each node indicates its type: `"root"`, `"if"`, `"asset"`, `"group"`, `"filter"`, etc. The `children` array contains nested nodes.

Used by `update_metrics.py` to refresh `data/symphony_scores.json`, and by `nodes.html` to count nodes.

**Note that this endpoint is CORS-blocked.** It returns HTTP 200 with `vary: Origin` and **no
`access-control-allow-origin` header**, so a browser can reach it but cannot read the response. This
is not a transient failure and there is no header or origin that lifts it. Python has no such
problem; anything running in a page needs a relay or a paste fallback. See the Nodes data flow in
Section 10.

#### Counting Nodes

Composer prices its tiers by node count and **does not show that number anywhere in the platform**.
Composer support, relayed 2026-08-17, gave the definition: each asset, each IF statement, each
FILTER block, each GROUP container, and each weighting method block. Mapped onto the `step` values
this endpoint actually returns:

| Composer's category | `step` value | Counted |
|---|---|---|
| Each asset (stock or ETF) | `asset` | yes |
| Each IF statement | `if` | yes |
| Each FILTER block | `filter` | yes |
| Each GROUP container | `group` | yes |
| Each weighting method block | any `wt-*` (`wt-cash-equal`, `wt-cash-specified`, `wt-inverse-vol` observed) | yes |
| (not a node) | `root`, the symphony itself | **no** |
| (not a node) | `if-child`, the THEN/ELSE branch container | **no** |

**Why `if-child` is excluded, since it is the one judgement call here.** It is generated structure
rather than anything visible in the editor: across 15 real symphonies sampled at v1.26.0, `if-child`
appeared **exactly twice per `if`, without exception** (5,162 against 2,581). Counting it would
treble every conditional. `nodes.html` matches `wt-*` by prefix rather than against a fixed list, so
a weighting method this repo has not seen still lands in the right category, and any unrecognised
step is counted as one node each **and flagged on screen**, so a Composer schema change surfaces
instead of silently skewing the total.

**The count runs far higher than people expect**, because an asset counts every time it appears. A
filter over six tickers is six asset nodes plus the filter, and reusing that set inside several IF
branches counts it again each time. Measured examples: a single-asset symphony is 2 nodes, zoop's
2026 Frontrunner is 21, and one real community symphony ("Portfolio Consolidation 1") is **5,935**,
of which 4,470 are assets.

### Symphony ID Reference

All Composer Atlas curated strategies with their Composer symphony IDs. **No count is given in
the heading on purpose: it was wrong twice before ("All 24" against a 31-row table) and a number
here goes stale every time the library grows.**

**The table itself drifted anyway, and worse, because it went stale silently.** An earlier note
claimed it matched `data/strategies.json` exactly. By 2026-09-01 it was missing five entries: the
three added in v1.38.0, Rain's Unified Best Signals from v1.39.0, and zoop's Frontrunner from
v1.40.0. All five are appended below. Removing the count fixed the visible half of the problem and
left the invisible half in place, which is the more useful lesson: a hand-maintained mirror of a
data file needs a check, not a caveat. Nothing generates or validates this table today.

| Strategy | Symphony ID |
|---|---|
| zoop's 2026 Frontrunner | `4aI4kVT5cEc0XJpTLei3` |
| zoop's Holy Grail (2026 Edition) | `Y2xvfu7iFNyO6up77gBI` |
| zoop's TQQQ FOR THE LONG TERM (2026 Edition) | `yIMvLUHfzAMATCpOKr9T` |
| zoop's Excellent Adventure (2026 Edition) | `YIiBr33X4rRTVlOWhCNq` |
| zoop's Sometimes TQQQ (2026 Edition) | `uAaEkEq8cPOmGgfEWTOU` |
| zoop's Safety Checks (2026 Edition) | `RLt1Rzz79I6Fa2X9QKqY` |
| zoop's Manhattan Project (2026 Edition) | `cCi1mupGsluFmre7HpOm` |
| zoop's KMLM Switcher (2026 Edition) | `4AuTagHMeiS4usdZEuDK` |
| zoop's UPRO FTLT (2026 Edition) | `9ETFQi5cmSWq2mT4ZH2d` |
| zoop's Leveraged TQQQ Symphony (2026 Edition) | `U6lT1G0PdE9fUxoy2opg` |
| zoop's TQQQ 200d MA 3x Leverage (2026 Edition) | `ZBpjzxS9RkLzft9NNWhO` |
| zoop's SOXL Growth (2026 Edition) | `wcEUcb13v7M8bEluRc1h` |
| s90 50/40 maxDD (Half Low Catch) | `K8ql2SKFd4VDBemIstEr` |
| The Holy Grail (Original) | `MmQbpf2U5TMQFmr9Nt2e` |
| TQQQ For The Long Term | `HukRwDJLlYPLMbrQbua5` |
| Wooden ARKK Machine 2.2 | `kl2dR0Rlp4RgZUHAJY2k` |
| Super Semiconductors | `zTV33nu3o0h5fKpT6IqL` |
| The Four Horsemen of the Apocalypse | `vkJ5YCvzJLBu2KKF6Oy0` |
| SOXX Group | `7PBSP926Mp40r6bPnP0j` |
| SOXL Growth v2.4.5 RL | `CW8oWU12S6vEvn2Hh7jD` |
| Inside Nancy Pelosi's Chips - V3 | `HgK8mCeBnH4fQFNcfZ7q` |
| Top Cap by MA + RSI ETF Hedge | `wadbe3IfwvSES5vk6yiu` |
| Mean Reversion Comparison to Python Code | `KJqNBGxYyyKuCcEfdHhq` |
| SPY, Energy, Chips, Commodities | `rtyBIBOKEY2cPSbJSQX8` |
| Simon's KMLM Switcher | `u5iBJE751BM5FKPRJvKf` |
| 10d BND vs. 10d SPHB (Original) | `0HCtnEKGw1PRt8Om77a3` |
| Dip Buying Tech | `98cACZSS00eDg8Kv5BBV` |
| Ob Os Staple my Bonds (Original) | `OmMmeWyyAu0IRN2yOP6k` |
| Sometimes TQQQ (Original) | `MyRyWhvbdxTsRfzHmE1U` |
| Triple Accelerator | `0jPwZ5Lm2Y3xH24oEijB` |
| The Gold Miner (Original) | `tlDwKY3NRXjYU61jCt0g` |
| Beta Ballers (Original) | `mlgAKFuUIPZiCT0aV7ho` |
| TQQQ or Not (Original) | `g0J87gnk7SausotpUoCt` |
| Safe Sectors or Bonds (Original) | `DtlEo2Y1DWR7hngZkxTB` |
| Rain's Unified Best Signals (Original) | `sEUgeRfSayPbBh8mJxSy` |
| zoop's Frontrunner | `zPBn8HkmTIQ5BEJdff0v` |

Use these IDs with `/backtest`, `/score`, `/versions`, and portfolio endpoints.

### Composer Indicator Window Limits

The lookback windows Composer's editor accepts, as reported by the owner on 2026-10-16. Any site tool that
takes an indicator window (the RSI Backtester today, anything built on other indicators later) must accept
exactly this range and no narrower: a box that silently rejects a value Composer allows is a bug (the RSI
Backtester's first version ignored windows above 50). Out-of-range input is pulled to the nearest limit and
shown, never dropped.

| Indicator | Window (days) |
| --- | --- |
| Cumulative Return | 1 to 1,000 |
| Exponential Moving Average | 2 to 252 |
| Max Drawdown | 2 to 1,000 |
| Moving Average of Price | 2 to 1,000 |
| Moving Average of Return | 2 to 1,000 |
| Relative Strength Index | 2 to 252 |
| Standard Deviation of Price | 2 to 1,000 |
| Standard Deviation of Return | 2 to 1,000 |

Long windows need that much price history before the indicator has a value, so they shorten any backtest
built on `data/prices.json` (which starts 2010-01-01). Tools should show the tested date range so the
shortening is visible.

### Composer Symphony JSON: Writing and Cleanup

The owner's rules for any symphony JSON the site writes (the RSI Backtester's **Copy JSON**, any
future export) and for cleaning up a symphony downloaded from Composer. Set 2026-10-16; the cleanup
below was run on zoop's Wash Sale Symphony and the owner confirmed the result backtests identically
in Composer.

**Writing a symphony**

- **One signal for a holding is a standard condition:** flat fields only (`lhs-fn`, `lhs-val`,
  `lhs-fn-params`, `comparator`, `rhs-fixed-value?`, `rhs-val`) and no `condition` block. This is
  exactly how Composer saves a plain rule. Wrapping a single signal in "any of" was tried and
  rejected.
- **Several signals for the same holding become one IF on "any of":** `condition` is
  `{"condition-type": "compound", "operator": "any", "conditions": [...]}`, one `binary` condition
  per signal, each keeping its own ticker, window and level. The flat fields describe the first
  signal. Only rules next to each other in the IF / ELSE IF order are merged; merging across a rule
  that holds something else would change which rule wins.
- **Structure:** root, one `wt-cash-equal`, then nested `if` steps. Every `if` has exactly two
  children (the rule and an ELSE) and the next rule sits inside the ELSE. Rebalance daily.
- **Copy to clipboard only.** No download button.
- **Short description:** "Built with the Composer Atlas RSI Backtester." plus the link that reloads
  the setup.
- **Descriptions of symphonies Claude builds (owner, 2026-10-31).** Applies to every symphony JSON
  Claude generates, cleans, flattens, condenses or re-tunes for the owner in a Claude session. It
  does not apply to anything the site exports for a visitor (the RSI Backtester keeps its own short
  description above) unless the owner asks.
  - **Hard limit: 128 characters for the whole `description` string,** counted with Python
    `len()`, spaces, punctuation and the credit line included. Never over 128.
  - **Ends with the credit line,** exact text: `Made using ComposerAtlas.` It is the last sentence,
    separated from the summary by one space, and appears exactly once (check before adding it to a
    description that may already carry it or an older credit wording; replace an older wording
    rather than stacking a second). With its leading space it takes 26 characters, so the summary
    before it has at most 102.
  - **2 to 4 sentences in total, the credit line counting as one,** so the summary is 1 to 3 short
    sentences or fragments. Each ends with a period.
  - **What the summary says:** a high-level executive summary of the idea behind the symphony (what
    it holds, what it reacts to, what it is trying to do), not a list of its rules, tickers in
    every branch, or exact thresholds. Very brief specifics are welcome when they fit and help a
    reader judge it, such as "Sharpe-tuned", "simulated since 1938" or "RSI(10), 200/100/50d MA".
    Do not put performance numbers (CAGR, drawdown, Sharpe values) in it: they go stale and vary
    by backtest window.
  - **Style:** plain words, no em-dashes, "zoop" always lowercase if it appears.
  - **Cleaning or flattening an existing symphony:** replace its description with a fresh one that
    follows these rules. If the old description says something the owner may want kept, ask first.
  - **Check before shipping:** print the final string with its `len()` and sentence count, and
    confirm it reads back the same from the clipboard.
  - **Example** (114 characters, 4 sentences): "Trend-gated TQQQ. Buys dips, hedges rallies with
    SH. Sharpe-tuned, simulated since 1938. Made using ComposerAtlas."

**Cleaning up a downloaded symphony**

Any public symphony can be read from
`https://api.composer.trade/api/v0.1/symphonies/<id>/score?score_version=v1` (the Converter uses
the same endpoint). The cleanup must never change what the symphony holds on any day.

1. **Strip editor leftovers:** `collapsed?`, `exchange`, `price`, `dollar_volume`, `has_marketcap`,
   `suppress_incomplete_warnings`, `name` on assets, and the window on `current-price` (it takes
   none).
2. **Remove structure that cannot matter:** a `wt-cash-equal` with one child (except the one under
   root), a filter or weight whose children are all identical (it picks the same thing whatever it
   ranks), an IF whose two branches hold the same thing, a group around a lone asset.
3. **Keep:** every named group, since those are the author's labels; and duplicated sub-strategies
   under a filter, because removing a copy changes what the filter picks.
4. **Group by holding:** merge an IF and the ELSE IF directly inside it when both hold the same single
   asset, into one "any of" rule as above. Never fold an `all` compound into `any`. List a repeated
   signal once. Repeat until nothing changes.
5. **Verify before handing over.** Run the original and the result through a random-scenario
   evaluator: each binary condition gets a seeded random truth, and each filter ranks its children
   by a seeded hash of the child's own allocation, so identical behaviour scores identically. Every
   scenario must give the same allocation. Two checker traps produced false mismatches the first
   time: number formatting (`1` against `1.0`) in the ranking key, and `current-price` windows in the
   condition key.
   A third trap shipped a broken symphony (2026-10-19, "Bad function parameter -
   relative-strength-index" in Composer): older symphonies keep a flat rule's window in
   `lhs-window-days` / `rhs-window-days` instead of `lhs-fn-params` / `rhs-fn-params`. Grouping
   read only the `-fn-params` fields, so the merged binaries had no `params` window, and the
   checker read the same wrong field on both sides and passed. Read the window from either field
   when converting, key a missing window as missing (never as blank), and before delivery scan
   every binary for a non-price function without `params`.
6. **Deliver** minified, to the owner's Downloads folder, with before and after counts. **Size is
   always stated in Composer nodes** (owner, 2026-10-19), never characters or kilobytes, including
   when confirming a clipboard copy: read the clipboard back and count its nodes.

| zoop's Wash Sale Symphony | Original | Cleaned | Grouped |
|---|---|---|---|
| Size | 425 KB | 318 KB | 302 KB |
| IF blocks | 462 | 460 | 400 |
| Weight wrappers | 436 | 5 | 5 |
| Holdings | 528 | 511 | 451 |
| Nesting depth | 42 | 39 | 35 |
| Named groups | 143 | 143 | 143 |

5,000 random scenarios matched across all three versions, and the Composer backtest matched.

**Composer's size limit: 10,000 nodes.** The editor shows the count (for example "22,430/10,000
nodes") and will not save a symphony over it. A node is every step except the `if` wrapper: each
`if-child` (rule and ELSE), asset, group, filter and weight counts once; the `if` that holds a rule
and its ELSE does not, and neither do the conditions inside a rule. Count it locally before handing
over: walk the JSON and count every object with a `step` other than `if`. That count matched
Composer exactly (22,430) the first time it was checked, 2026-10-19.

### Flattening a Symphony Under the Node Limit

Set 2026-10-19, when "zoop's wash sale monstrosity" (the Wash Sale Symphony with an 8-regime
SPY 200/100/50-day frontrunner) came out at 22,430 nodes. Flattened, it was 3,450, imported and
backtested in Composer.

**Why it blows up.** A gate tree (IF SPY > 200d MA, then > 100d, then > 50d) has one leaf per
regime, and every leaf ends in its own ELSE. When that ELSE is a large sub-strategy, it is copied
once per leaf. Eight regimes times two trees put sixteen copies of a 1,394-node block in one file.

**The fix: move the gates into the rules, and the big ELSE out of the tree.** Each tree becomes one
straight IF / ELSE IF chain, and the large block appears once, at the very end.

- **Every rule carries its regime as an "all of" condition:**
  `{"condition-type": "compound", "operator": "all", "conditions": [...]}` with one `binary` per
  gate plus the rule's own signal, for example
  `SPY price > SPY 200d MA, SPY price > SPY 100d MA, SPY price < SPY 50d MA, QQQ RSI(10) < 31 → SSO`.
- **Gate binary format:** `{"lhs": {"fn": "current-price", "ticker": "SPY"}, "condition-type":
  "binary", "comparator": "gt", "rhs": {"fn": "moving-average-price", "ticker": "SPY", "params":
  {"window": 200}}}`. Above the line is `gt`, below is `lt`. (The tree's ELSE is "not above", so the
  two differ only on a day the close equals the average exactly.)
- **An "any of" inside a regime cannot nest inside the "all of"**, because Composer conditions are
  one level deep. Split it: one rule per signal, each with the full gate list. A regime with three
  dip signals and twelve overbought signals becomes up to fifteen rules. They are tiny next to the
  block they replace.
- **Order:** within a regime, keep the original rule order (dips before overbought). Regimes are
  mutually exclusive, so the order of the regimes in the chain does not matter.
- **Omit switched-off rungs** (a dip level of 0, an overbought level above 100) instead of writing
  them.
- **Flat fields on an "all of" rule describe the first gate** (`lhs-fn: current-price`,
  `rhs-fn: moving-average-price`, window). Composer decides on `condition`, not the flat fields.
- **New ids everywhere.** Every copied block gets fresh uuids; check that no id repeats.

**Verify before handing over**, as with cleanup: evaluate the flattened file and the original tree
on the same history and require a 0.0 difference in daily returns. The evaluator must read
`condition` before the flat fields: the first check read the flat gate fields of an "all of" rule,
ignored the RSI signal, and reported a false mismatch.

| zoop's wash sale monstrosity | Nested gate tree | Flattened |
|---|---|---|
| Composer nodes | 22,430 (refused) | 3,450 |
| Size | 5.35 MB | 937 KB |
| Copies of the 10-strategy block | 16 | 2 |
| Rules per tree | 7 gates, 8 leaf cascades | 109 in one chain |

Composer backtest of the flattened file, 2020-12-16 to 2026-10-18 with fees and 1 bp slippage:
118.7% a year, -15.9% max drawdown, Sharpe 3.1, against the original Wash Sale Symphony's 102.4%,
-17.7% and 2.9 on the same settings.

### Tuning Regime Symphonies: What the Out-of-Sample Tests Showed

Recorded 2026-10-31 from the TQQQ-only regime symphony (TQQQ price against its own 200, 100 and
50-day moving averages, eight regimes, TQQQ RSI(10) bands holding TQQQ, 75/25 TQQQ/SH or SH). The
symphony is the owner's; these are the takeaways for tuning any symphony like it.

**Full-sample numbers are mostly fit.** Tuned on 2010-2026, the shipped blend shows 81.7% a year,
-37.8% max drawdown and Sharpe 1.71. Tuned on one half and run on the other, the same pipeline kept
about half the return and Sharpe 1.0 to 1.2. Quote the held-out number when describing a tuned
symphony, never the in-sample one.

**Finer weight steps add fit, not edge.** Letting every band choose its TQQQ/SH split in 25% or 10%
steps raised in-sample Sharpe to as much as 1.99, and scored 1.22 to 1.28 out of sample, the same as the
coarser version. The 75/25 bands the owner prefers are as good as anything finer.

**UVXY as the hedge failed the holdout.** With UVXY in place of SH the backtest rose to 113.8% a year,
but tuned on 2012-2019 and run on 2019-2026 it scored Sharpe 0.63 to 0.71 with drawdowns past -80%,
worse than holding TQQQ.

**A second engine and a longer history.** The owner's separate Backtester project runs symphony JSON
headless with Crescendo's formulas. On real prices it matched this project's Python results exactly,
and its Synthetic mode simulates TQQQ and SH before they existed. That allowed the cleanest test so
far: tuned only on simulated 1990-2010, the blend made 45.1% a year, -36.9% and Sharpe 1.20 on real
2010-2026, against 40.8%, -81.7% and 0.87 for holding TQQQ. Tuned on 1990-2026 it shows 72.7% a year,
-59.9% and 1.35. Use the Backtester from a scratch runner only: nothing in that repository is changed
from this project.

**Before 1990 the edge disappears.** Tuned on 1938-1990 the blend matched holding TQQQ on 1990-2026
(Sharpe 0.55 each), and the 1990 version lost 3.3% a year on 1938-1990 (16.4% a year in 1970-1989).
The best single fit across 1938-2026 reached only Sharpe 0.99, though it did beat holding TQQQ in every
era. Either the dip-buying edge belongs to the post-1990 market, or simulated data that old does not
represent a leveraged growth fund. The data cannot separate the two.

**Start simulated history when the underlying index began.** The owner's rule: a simulated series is
only used back to the real start of the index it stands in for, for example 1985 for the Nasdaq-100
(TQQQ, QQQ), not the 1938 stand-in the Backtester offers. Earlier rows are a model of a different
market, so they are not a tuning or testing sample. Say which start date a result uses.

### Full Performance Breakdown of a Symphony

When the owner asks for a **full breakdown** of a symphony's performance, give all three of these,
each with CAGR, max drawdown and Sharpe, the exact start and end dates, and holding the main fund (or
the symphony's benchmark) over the same window for comparison:

1. **Full backtest on available data.** Real prices only, from the first day every ticker in the
   symphony trades (and its longest indicator window has filled) to the latest close. This is what
   Composer itself can show.
2. **Full backtest since the underlying index began.** Simulated prices back to the real start of each
   holding's underlying index, for example 1985-01-31 for the Nasdaq-100 behind TQQQ and QQQ, and
   1957-03-04 for the S&P 500 behind SPY, SSO and SH. With several underlyings, start at the latest of
   their inception dates, so every holding is backed by a real index on every day. Look up any other
   index's inception date and state it.
3. **Full backtest on all synthetic data.** The longest history the simulation offers (the
   Backtester's Synthetic mode reaches 1938 for TQQQ), labelled as a model of an older market, not a
   sample of the fund.

Run all three through the owner's Backtester project (Standard mode for 1, Synthetic mode with a start
date for 2 and 3), with the scratch runner described in "Tuning Regime Symphonies" above, and say
which engine produced the numbers. If a ticker has no simulated history, 2 and 3 equal 1; say so
instead of leaving them out. Mark which windows the symphony was tuned on, because a tuned window is
in-sample and flatters it.

---

## 14. Roadmap

### Where the Project Is Right Now

**Current phase: V2.2, "Scale and Discovery".** Everything through V2.1 has shipped and is live.
The MVP, the curated library, the glossary, the full community database with its leaderboard and
screener, the four tools and the live RSI page are all built, public and maintained on automated
refresh schedules.

**What the current phase is actually about.** Not new sections. The remaining V2.2 work is depth on
what already exists: refreshing the curated set to newer strategy versions, cross-linking the
curated pages to their rows in the community database, and giving the Signal Miner some defence
against the overfitting its own search space makes inevitable. That last item is the largest open
piece of product work on the site and is designed but unbuilt (Section 14 items A, B and C below,
and Section 25 risk 6).

**Version numbering is not phase numbering, and the two have diverged.** Releases are semantic
versions (`1.24.8` at the last release before this audit). Roadmap phases are `V1.0` through `V4.0`
and describe scope, not release order. Several phases were built well ahead of their numbered slot
at the owner's explicit request, notably V1.16 before V1.11 to V1.15, and V2.1 before V1.17. Where
that happened it is stated in the phase's own status line. Do not try to reconcile the two
numbering schemes; they answer different questions.

### Milestones

| Phase | Scope | Status | Landed at |
|---|---|---|---|
| V1.0 | MVP: vanilla stack, 13 strategies, 8 glossary concepts, deploy pipeline | Complete | v1.0.x, 2026-06-08 |
| V1.1 | Polish and content quality: logic-tree rewrites, metrics script, `file://` and Pages link fixes | Complete except a Lighthouse pass | v1.1.5 |
| V1.2 | Data tooling and structure refactor: flat root `.html`, `?slug=` routing | Mostly complete; field validation still open | v1.2.1 |
| V1.3 | Documentation consolidation: 12 files to 4 | Complete | v1.3.0 |
| V1.4 to V1.6 | Strategy library growth to 25, glossary growth to 20, repo rename | Complete | v1.6.0 |
| V1.7 | AI summaries on every strategy page | Complete | v1.7.0 |
| V1.9 to V1.9.5 | Full database foundation: schema, refresh pipeline, API rate-limit characterisation | Complete | v1.9.5 |
| V1.10 to V1.13 | Filter panel, screener, leaderboard scoring model, storage backup, nav restructure | Complete, built ahead of slot | v1.11.x |
| V1.14 | Noise filtering: name-pattern flagging and logic-tree de-duplication | Complete | v1.11.22-23 |
| V1.15 | Full-scale refresh: every entry through at least one real API attempt | Complete; now maintained weekly | v1.11.23 |
| V1.16 | Performance fix: columnar summary export, page weight | Complete, built ahead of slot | v1.11.0 |
| V1.17 | Leaderboard scoring revision: reweighting, clamp constant, real S+ rank cut | Complete | v1.14.0-1 |
| V1.18 | Leaderboard scoring revision II: out-of-sample weighting, and a simpler factor set | **Complete.** Shipped 2026-09-07 as two permanent models behind a toggle, Simplified default and canonical, on 3,175 true out-of-sample backtests | v1.74.0 |
| V1.19 | K1 Lookup: `/k1`, structure-derived K-1 database, refresh script | Complete | v1.27.0, ETN display v1.27.9 |
| V1.20 | Strategy page rebuild: database join, outlier and out-of-sample disclosure, K-1 cross-link, regime and risk sections | **Complete.** All 19 items shipped; 13, 14, 15 complete on all 24 visible strategies (v1.68.0); item 16 stores the daily series and the features it unblocks are tracked in Section 14 C3 | v1.72.0 |
| V2.0 | Full database goes public | Complete | v1.12.0 |
| V2.1 | Live RSI signals page | Complete, built ahead of slot | v1.13.0 |
| **V2.2** | **Signal Miner robustness (items A, B, C).** Split 2026-09-07: the curated-set refresh and library expansion moved out to V2.6. **A shipped** (parameter plateau scoring, verified by `run_harness.py plateau`). **C's empirical null shipped 2026-09-08 as v1.79.0**; the other five rating components C names remain unbuilt and are not queued. **B, walk-forward validation, is NOT built**, and it is the only item here that can fail a rule outright rather than caveat it | **A and C shipped, B outstanding** | Through v1.79.0 |
| V2.3 | Community signals: external submission form, curator notes, related strategies | Backlog, lowest priority | Not started |
| V2.4 | Overfit Check: paste a symphony, test it against the definition of overfitting using the 5,228 symphonies whose logic has gone a year unedited | Requested and specified 2026-08-28, respecified the same day after the owner rejected peer ranking, then **sequenced late at the owner's request**. **Tier 1 shipped 2026-09-06 as v1.75.0**, then substantially corrected in **v1.76.0** (fitted-era split, graded Overfit Score, the ceiling finding); Tiers 2 and 3 remain as specified | **Tiers 1 and 2 Complete** (Tier 2 shipped v1.77.0, 2026-09-08); Tier 3 remains hard-blocked on price coverage |
| V2.5 | Documentation audit against the external standard, and social sharing tags on every shareable page | Queued 2026-09-07, executed 2026-09-08. **Social sharing tags shipped v1.78.0** on all twelve pages; the **documentation audit shipped v1.78.1** and its findings are in Section 24. Open question 27 is now ruled: the checker stays manual | **Complete** | v1.78.1 |
| V2.6 | Curated content: the zoop evergreen replacement (11 strategies), and the Cohort A library expansion (7 strategies) | **Split out of V2.2 and sequenced behind V2.5 by owner decision, 2026-09-07.** Neither is blocked; both are large content builds rather than product work. **The owner ruled on 2026-09-08 that this needs a dedicated working session and must NOT be started opportunistically at the tail of another run**, because it turns on judgement calls only the owner can make about which strategies earn a page and what each one says. A spare hour at the end of a session is the wrong time to open it | **Held for a dedicated session** |
| V3.0 | Formerly Monetization Expansion | **Removed entirely, 2026-08-15.** Not deferred | n/a |
| V4.0 | Signal discovery and robustness tooling, five candidate external forks | Ideation only. No work to begin until V2.x is well underway | Not started |

### Explicitly Deferred

Recorded so none of these reads as an oversight. Each was considered and set aside for a stated
reason, and each remains a legitimate future item.

| Item | Status | Reason |
|---|---|---|
| OR combining, and Composer's `any`/`all` multi-ticker conditions | **Deferred indefinitely** | Asked for directly by the owner and still worth doing. It is the largest single expansion of what the Miner can express, and it is genuinely two features that were conflated in discussion and must be kept apart. Full write-up retained below |
| Option B: single source of truth for curated metrics | **Deferred, not rejected** | Would stop `strategies.json` backtesting the curated set independently of `database.json`. Option A (cross-link only) was chosen first because it is purely additive navigation |
| Signal Miner sparklines | Deferred | Explicitly, at V2.1 |
| CSV export of a filtered screener result set | Deferred | Never built; still a reasonable equivalent of the Finviz reference |
| De-duplicating near-identical Signal Miner result rows | **Declined by the owner, 2026-08-20** | Not considered a real problem. Recorded so it is not re-proposed as new |
| Per-ticker handling of reformed funds (SVXY's 2018 change from -1x to -0.5x) | **Explicitly waived by the owner** | Accepted known tradeoff |
| Tiebreak on "watched by N" popularity in the dedupe pipeline | Wanted, blocked | The API this pipeline uses does not expose it |
| User accounts, saved strategies | **Removed permanently** | Will never be built. Not iceboxed |
| Client-side search (Fuse.js or similar) | Backlog | Never started |
| Strategy comparison view, per-strategy performance chart | Backlog | Never started |
| Price data for UPRO, AGG, CORP and STIP (`refresh_prices.py`) | **Backlog, requested 2026-10-19** | Signal tickers in the owner's Wash Sale Symphony that the price set lacks (UPRO is used 41 times). Needed before the RSI Backtester or any full-symphony simulation can evaluate that symphony end to end |
| Twitch Check (compare live trading to the backtest) | **Backlog, requested 2026-10-19, data source TBD** | A sibling of Overfit Check. It would line up a symphony's live daily returns against the backtest's daily returns over the same days and report the share of days that match within a tolerance, the share where live beat the backtest, and the share where it fell short. The user sets the tolerance (default 0.25 percentage points per day). Blocked on data: live returns are account-scoped in Composer's API (`portfolio/accounts/{acct}/symphonies/{id}` needs auth) and are not public, so the source is open (pasted data or a local script are the candidates). Distinct from Overfit Check, whose OOS is a backtest re-run after the last logic edit, not real fills |

### Guides Content Roadmap

**Added 2026-10-07**, when the Guides collection shipped with its first seven entries. See
`docs/PRD.md` "The Guides Collection" in Section 6 for what the collection is and the owner's
attribution ruling, and `docs/DESIGN.md` Section 7 for the component.

**The standing rule for this collection: seven good guides beat fifteen thin ones.** Every guide
carries a visible `last_updated` that has to mean something, so each one is a recurring review
commitment rather than a one-time write. The collection is capped at roughly a dozen. Anything that
is really a definition belongs in the glossary instead.

**Priority order, highest first.**

| # | Proposed guide | Category | Why it earns a slot | State of the source |
|---|---|---|---|---|
| ~~1~~ | ~~**Clearing wash sales at year end**~~ | `execution` | **SHIPPED 2026-10-07** as `clearing-wash-sales-before-year-end`. Kept in this table rather than deleted, because the spec below is what the page has to keep being true to on review | Written. The spec below is now the **review checklist** for it |
| 2 | **What the Signal Miner is doing to your p-value** | `testing` | The largest hole in the collection, and the only one on this list that is about **our own tooling** rather than about Composer. We ship a tool that searches thousands of signal combinations and ranks them, and nothing tells a reader that the best of 5,000 random signals is *expected* to look excellent. `overfit.html` measures the problem the Miner manufactures; this guide is the link between them | Needs writing from scratch. Pulls in multiple comparisons and sample size, both absent from the glossary |
| 3 | **Permutation testing and the walk-forward knee** | `testing` | `permutation` and `walk-forward` are both absent from the glossary. Highest-value testing guide after #2 and the hardest of these to write honestly, because it is easy to make a judgement call read like a recipe | Ideas in hand from the ingested Masters material. Written in site voice, no verbatim text |
| 4 | **The mean reversion death spiral and the volatility switch** | `testing` | The glossary's `mean-reversion` entry defines the rubber band. This covers the failure mode: a dip-buy ladder that averages into a trend instead of a reversion, and the switch that gets you out | Source material in hand. **Needs framing discipline** so it does not restate the glossary entry |
| 5 | **Swapping a K-1 ETF for a cleaner equivalent** | `instrument-risk` | `k1.html` flags 187 tickers and then leaves the reader there. The substitution logic is the missing half of a tool we already ship | Candidate substitutions noted (UGL to GLD, DIG to ERX, DBC to PDBC). **The volume and expense reasoning in the source is from 2022 and must be re-verified before anything is published** |
| 6 | **Cash drag and the cost of being out** | `execution` | `cash drag` is absent from the glossary. When a risk-off leg should hold BIL or SHV rather than sit in cash, and what the difference costs across a backtest | Needs writing from scratch |
| 7 | **Correlation is not diversification** | `instrument-risk` | The glossary covers correlation as a statistic. The guide covers 2022, when the diversifying legs stopped diversifying at the moment it mattered. Pairs with the shipped `the-bond-leg-is-not-one-thing` | Needs writing from scratch |
| 8 | **Profit factor at fine granularity** | `testing` | Absent from the glossary. The smallest item here; **may be better folded into #3 than shipped alone** | Ideas in hand from the Masters material |
| 9 | **Sizing across two symphonies** | `execution` | The shipped `sizing-a-symphony` handles one in isolation. The follow-on is what happens when two symphonies both hold TQQQ and the real exposure is double what either backtest implies | Needs writing from scratch |

**Not a guide.** The ingested Composer blog momentum links are links rather than content. If they go
on the site they belong on a reading list page, not inside a guide. Recorded so it is not
re-proposed as a guide.

#### The Wash Sale Guide: Spec, the Owner's Technique, and the Review Checklist

**Status: shipped 2026-10-07** as `clearing-wash-sales-before-year-end`. Everything below was
written as a spec before the guide existed and is retained as the **review checklist**. This is
the page on the site most likely to go stale in a way that matters, because tax rules change
and its errors land on someone's return. Re-read this list against the live page whenever its
`last_updated` is refreshed.

**The owner's year-end technique, in his own description, recorded 2026-10-07.** He combines all the
symphonies he runs into a single symphony, replaces the holdings with securities he has not bought
at any point during the year, and then rebuys the original holdings after January.

**Why this is the right shape for a Composer guide, and not merely generic tax content.** Ordinary
tax-loss harvesting advice assumes a human decides every purchase. Composer does not work that way.
A live symphony rebalances on its own schedule, so **the automation itself can repurchase a security
inside the wash sale window and void the loss without the owner doing anything or seeing it
happen**. Collapsing many symphonies into one is what makes the set of holdings small enough to
reason about, which is the insight the guide exists to convey. That is a platform-specific point
that no general tax article will tell a Composer user.

**What the guide must get right.** These are the points where a plausible-sounding version would be
wrong, so they are recorded here rather than left to be rediscovered:

- **The rule's window is 61 days around the sale, not the calendar year.** A loss is disallowed if a
  substantially identical security is bought within 30 days *before or after* the sale. The owner's
  "nothing bought during the year" test is therefore **stricter than the rule requires**, which is
  safe, but the guide must state the actual rule rather than the proxy, or a reader will apply the
  proxy somewhere it does not fit.
- **The window crosses the year boundary, which is the whole trap.** Selling in late December and
  repurchasing in early January is still a wash sale. "After January" clears a December sale; a
  January 2nd repurchase does not. The guide must be explicit about counting 31 days forward from
  the sale date rather than waiting for a new tax year.
- **"Substantially identical" is the unsettled part.** The replacement holding has to not be
  substantially identical to what was sold. Two ETFs tracking the same index are a genuine grey
  area that the IRS has not ruled on cleanly, and the guide must say that it is unsettled rather
  than pick a side and present it as settled.
- **A repurchase in an IRA permanently disallows the loss**, rather than merely deferring it. Worth
  naming because a reader running a taxable symphony and a retirement account will not expect the
  two to interact.
- **Disallowed losses are deferred, not destroyed**, in a taxable account: the basis adjusts. The
  guide should say so, because the common misreading is that a wash sale costs you the loss
  outright.

**Disclaimer requirement, which is stricter than the rest of the collection.** Every guide carries
"Not investment advice". This one additionally **must not read as tax advice**, and must tell the
reader to confirm their own situation with someone qualified. It is the only page on the site where
a reader could act on a misunderstanding and get a letter from the IRS for it.

### V1.0: MVP

**Launched:** 2026-06-08 | **Status:** Complete
**Live URL:** https://azqato.github.io/composer/

- [x] Vanilla HTML/CSS/JS scaffolded (zero build dependencies)
- [x] GitHub Pages deployment configured (rsync workflow; docs/scripts excluded)
- [x] `data/strategies.json` with 13 strategies
- [x] Strategy index page (all 13 with key metrics)
- [x] 13 strategy detail pages (logic breakdown, metrics table, Composer CTA)
- [x] Concept glossary index and 8 detail pages
- [x] Cross-linking: strategies and glossary
- [x] Top navigation: Strategies, Glossary, About, Individual Stocks, Leveraged Strategies, Support
- [x] About page, Support link, Custom 404 page
- [x] Dark mode design system
- [x] Mobile-responsive layout

### V1.1: Polish + Content Quality

**Status:** Complete (at v1.1.5)

- [x] All 12 strategy pages rewritten from logic tree analysis (v1.1.0); 13th added (v1.1.7)
- [x] `scripts/update_metrics.py` live (v1.0.8)
- [x] Fix: navigation broken on `file://` protocol: `u()` helper added (v1.0.4)
- [x] Fix: all links broken on GitHub Pages: case-insensitive BASE detection (v1.1.2)
- [x] Footer simplified to match azqato.github.io (v1.1.3)
- [~] ~~Google AdSense integration (pending approval)~~, **dropped.** Monetization was removed from the product entirely (see Non-Goals and Tenet 7): the site takes donations through Buy Me a Coffee only, runs no ads, and collects no user data. This line survived the monetization removal because it sits in a completed historical section rather than the live backlog.
- [ ] Performance audit and Lighthouse optimization

### V1.2: Data Tooling + Structure Refactor

**Status:** Mostly Complete (at v1.2.1)

- [x] `scripts/update_metrics.py` pulls from Composer API (backtest + score), no auth required
- [x] Streamlined URL-based strategy addition workflow documented in Runbook (v1.8)
- [x] Folder structure consolidated: flat root `.html` files; `strategies/` and `glossary/` subdirs eliminated (v1.2.0)
- [x] URL patterns: `?slug=X` replaces `/detail/?slug=X` (v1.2.0)
- [x] `u()` helper simplified: depth-agnostic (v1.2.0)
- [ ] Validation: script checks required fields before writing

### V1.3: Documentation Consolidation

**Status:** Complete (at v1.3.0)

- [x] 12 scattered documentation files consolidated into 4 canonical docs: `README.md`, `docs/PRD.md`, `docs/DESIGN.md`, `docs/PATCHNOTES.md`
- [x] All operational, technical, API, schema, roadmap, security, and tenet content moved into `docs/PRD.md`
- [x] File naming standardized from `.MD` to `.md`

### V1.4: Strategy Library Expansion + Infra

**Status:** Complete (at v1.4.2)

- [x] 5 new strategies added: Holy Grail (Original), TQQQ For The Long Term, Wooden ARKK Machine 2.2, Super Semiconductors, The Four Horsemen of the Apocalypse: library grows to 18 (v1.4.0)
- [x] GitHub repository renamed from `Azqato/ComposerAtlas` to `Azqato/composer`; GitHub Pages URL updated (v1.4.1)
- [x] BASE URL detection made repo-rename-proof: hostname-based (`*.github.io`) instead of hardcoded string match (v1.4.2)

### V1.5: Strategy Library Expansion + Glossary Expansion

**Status:** Complete (at v1.5.9)

- [x] 6 new strategies added: SOXX Group, SOXL Growth v2.4.5 RL, Inside Nancy Pelosi's Chips V3, Top Cap by MA + RSI ETF Hedge, Mean Reversion Comparison to Python Code, SPY Energy Chips Commodities: library grows to 24 (v1.5.0)
- [x] 9 new glossary concepts added: SMA, EMA, MACD, Mean Reversion, Volatility Decay, Standard Deviation, Annualized Return, Managed Futures, Inverse ETFs: glossary grows to 17 (v1.5.2)
- [x] Zoop's Strategies glossary entry added with overview of all 11 zoops-* symphonies and headline metrics (v1.5.3)
- [x] Backtesting glossary entry added covering general backtest mechanics and Composer-specific behavior: glossary grows to 19 (v1.5.6)

### V1.6: Strategy Library Expansion

**Status:** Complete (at v1.6.0)

- [x] Simon's KMLM Switcher added: library grows to 25 (v1.6.0)

### V1.7: AI Summaries

**Status:** Complete (at v1.7.0)

- [x] `ai_summary` field added to all 25 strategies; Claude-authored analysis box renders above How It Works on every strategy page (v1.7.0)
- [x] `scripts/add_ai_summary.py` added; "Generating the AI Summary" runbook and schema field documented (v1.7.0)
- [x] Homepage: "Longest Backtest" fifth stat added to stats bar; strategy grid sorted by backtest length (longest first) (v1.7.1)

### V1.9: Full Database Foundation

**Status:** Complete (at v1.9.0)

- [x] Investigated `data/Full Database.xlsx` (6,488 rows from a prior Google Apps Script scrape); found only 953 rows have usable metrics, the rest failed on the script's daily `urlfetch` quota (v1.9.0)
- [x] Confirmed live against 5 real symphonies that Composer's actual API (not scraping) returns far more data than currently captured: `sortino_ratio`, `win_rate`, `skewness`, `kurtosis`, `tail_ratio`, concentration metrics, live holdings, cost breakdown; documented in Section 13 (v1.9.0)
- [x] `data/database.json` created as the canonical JSON source, imported from the xlsx via `scripts/import_full_database.py` (v1.9.0)
- [x] `scripts/refresh_full_database.py` built: resumable, checkpointed (every 10 rows), captures the API's actual error text into `script_errors` on failure (v1.9.0)
- [x] Validated the refresh script against 105 rows live (5 + 100), 0 failures (v1.9.0)
- [x] `database.html` template shipped: tabbed page (All Strategies / Leaderboard / Screener); All Strategies renders a paginated table against the full dataset, the other two tabs render a "Coming Soon" state (v1.9.0)
- [x] `.db-tabs` / `.db-table` component patterns documented in `docs/DESIGN.md` (v1.4 design doc revision) (v1.9.0)
- [x] Nav/footer updated with a "Database" link (v1.9.0)
- **Partially pushed (v1.11.2, corrected here):** the original plan was to hold this entire initiative back until V1.16 (Performance Fix) was done. What actually happened: once V1.11-V1.13 and V1.16 were all built, the *code* (`database.html`, `css/main.css`, `js/app.js`, the full-database scripts) was pushed to `main` and is live, deliberately **without** the data files (`data/database.json`/`.js`, `data/database_summary.json`/`.js`, `data/storage.csv`, `data/Full Database.xlsx`). The live `database.html` will 404 trying to fetch `database_summary.json`, an accepted, intentional state, not a bug. Data gets pushed separately once it's ready. See PATCHNOTES v1.11.3 for the exact commit.

### V1.9.1: Target Schema Expansion

**Status:** Complete (at v1.9.1)

- [x] Decided the full field set via 7 clarifying questions: all newly-discovered stats fields (sortino_ratio, win_rate, skewness, kurtosis, tail_ratio, concentration metrics, annualized_turnover, finer trailing windows), both holdings fields, costs summed into `total_costs`, and `data_warnings` (v1.9.1)
- [x] Decided schema shape (flat, top-level, matching `strategies.json` convention), null-handling (explicit null, never omit a key), and refresh policy (full overwrite every successful call) (v1.9.1)
- [x] `refresh_full_database.py` updated to capture the expanded field set (v1.9.1)
- [x] `import_full_database.py` updated so a fresh xlsx import also initializes the extended fields to null (v1.9.1)
- [x] All 6,488 existing entries in `database.json` migrated in place to carry the new keys (null where not yet refreshed), without disturbing the 105 rows already refreshed under the old schema (v1.9.1)
- [x] Validated live against 5 real symphonies; discovered and corrected a documentation error: `active_asset_nodes` is not a ticker list (it's node UUID → weight), real ticker holdings are in `last_market_days_holdings` (v1.9.1)
- [x] Full Database JSON Schema (Section 12) and API Reference (Section 13) updated to match

### V1.9.2: file:// Loading Fix

**Status:** Complete (at v1.9.2)

- [x] Bug: `database.html` shipped in v1.9.0 with `fetch()`-only data loading, no `window.*_DATA` global fallback like every other page uses; failed with "Failed to fetch" when opened via `file://` (double-click) instead of a server (v1.9.2)
- [x] `data/database.js` added (assigns `window.DATABASE_DATA`), matching the `strategies.js`/`glossary.js` convention (v1.9.2)
- [x] `scripts/import_full_database.py` and `scripts/refresh_full_database.py` updated to write the `.json`/`.js` twins in sync, matching `update_metrics.py` (v1.9.2)
- [x] `database.html`'s inline `loadFullDatabase()` now checks `window.DATABASE_DATA` first, `fetch()` fallback (v1.9.2)
- [x] Verified via local HTTP server smoke test; `.js` twin syntax validated (v1.9.2)

### V1.9.3: All Strategies Table Redesign

**Status:** Complete (at v1.9.3)

- [x] Reformatted the All Strategies table to match a reference community strategy-search tool's density and layout (toolbar header with result-count pill, sortable columns with click-to-toggle asc/desc arrows, sticky first column, icon-style first/prev/next/last pagination), while keeping the site's existing dark palette, `Inter`/`JetBrains Mono` typography, and color-coding conventions intact (v1.9.3)
- [x] Finalized the public-facing column set via clarifying questions: Symphony, ARR, 1-Year Trailing Return, Max Drawdown, Sharpe, Calmar, Sortino, Win Rate, Backtest Length, Last Updated, and a Data Warnings indicator; explicitly excluded Cumulative Return, Volatility, skewness/kurtosis/tail ratio, turnover, and total costs from the public table for now (v1.9.3)
- [x] Client-side sort implemented on the full dataset (not just the visible page), nulls always sort last (v1.9.3)
- [x] Symphony column widened to a fixed 420px with ellipsis truncation and a hover tooltip (`title` attribute) for the full name, after two rounds of "wider please" turned up names too long to reasonably fit unwrapped (v1.9.3)
- [x] Security fix found while widening the column: `name` is community-sourced from many different authors (unlike the curated 25 strategies), so inserting it into `innerHTML` and an HTML `title` attribute without escaping was an XSS risk; added `escapeHtml()` and applied it, plus `encodeURI()` on `symphony_url` (v1.9.3)
- [x] Intro copy corrected: no longer claims the database is "every symphony pulled from Composer.trade"; now accurately describes it as a community-sourced database gathered from many locations (v1.9.3)

### V1.9.4: xlsx Export Tool + Table Width Fix

**Status:** Complete (at v1.9.4)

- [x] `scripts/export_full_database_to_xlsx.py` added: local-only, occasional-use script that regenerates `data/Full Database.xlsx` from `data/database.json` (the reverse direction of `import_full_database.py`), so the spreadsheet can still be reviewed offline even though it's no longer part of the live pipeline. Nested fields (`last_market_days_holdings`, `active_asset_nodes`, `data_warnings`) are serialized to a JSON string per cell (v1.9.4)
- [x] Confirmed `Full Database.xlsx` is otherwise frozen: nothing in the pipeline writes back to it since v1.9.0, `database.json`/`.js` are the sole canonical source (v1.9.4)
- [x] Kicked off a full-scale `--force` background refresh of all 6,488 entries under the new v1.9.1 schema (a `--force` flag was added to `refresh_full_database.py` so already-touched rows aren't skipped by the 7-day staleness check and get backfilled with the new fields too); this is V1.12's work started early since it's a long-running, throttled background job with no reason to wait (v1.9.4)
- [x] Fixed: the All Strategies table was clipped by `.container`'s 1280px max-width, cutting off the rightmost columns. Added a `.db-table-bleed` wrapper (92vw, capped at 1600px, centered) that only activates above a 1300px viewport so the table gets natural side padding instead of running edge-to-edge; below that width it stays in the normal container and scrolls horizontally as before (v1.9.4)

### V1.9.5: API Rate-Limit Testing

**Status:** Complete (at v1.9.5)

- [x] The `--force` background refresh from v1.9.4 was paused at 140/6,488 rows (clean, zero failures) to test whether a faster approach was viable before committing hours of wall-clock time to the sequential throttle (v1.9.5)
- [x] Four one-time tests run against `/backtest` at four different rates (~100 concurrent req/sec, ~20 concurrent req/sec, ~2 concurrent req/sec, and fully sequential 1 req/sec): all four topped out at exactly 25 successful calls before `HTTP 429: Too Many Requests` started, regardless of rate. Combined with the original 0.5 req/sec throttle's 140/140 clean run, this points to a token-bucket limiter (burst capacity ~25, refill rate ~0.5 req/sec) rather than a flat requests-per-second cap. Findings documented in Section 13 (v1.9.5)
- [x] Added an early-bail safeguard to the concurrency and sequential tests (stop after 3 consecutive all-fail batches/calls) so a confirmed rate-limit doesn't get burned through pointlessly (v1.9.5)
- [x] Confirmed no data corruption from the failed calls: `script_errors` is set but `last_updated` is untouched on failure, so every rate-limited row remains correctly queued as "due" for the next run (v1.9.5)
- [x] Conclusion: the sequential 1-call-per-2-seconds throttle already built into `refresh_full_database.py` is the only rate confirmed safe for a sustained run; no further rate testing planned. 240 rows now carry the full v1.9.1 schema (140 sequential + 25 x 4 test runs). Resuming the full sequential run is a normal next step whenever wanted, not blocked on anything new (v1.9.5)

### V1.10: Strategy Library Expansion

**Status:** Complete (at v1.10.0)

- [x] 10d BND vs. 10d SPHB (Original) added: contrarian SOXL/SHV switcher using BND vs. SPHB relative RSI(10), with UVXY and SOXX RSI guards (v1.10.0)
- [x] Dip Buying Tech added: three-branch SPY 200d MA baseline with QQQ RSI(10) < 30 XLK dip-buy; backtested from April 1999 (v1.10.0)
- [x] Ob Os Staple my Bonds (Original) added: V0.0 defensive baseline using QQQ oversold dip-buy and lower-RSI rotation between XLP/VBF; backtested from 1999 (v1.10.0)
- [x] Library grows to 28 strategies (v1.10.0)

### V1.10.1: Database Rename + Storage Backup

**Status:** Complete (at v1.10.1)

- [x] `data/full_database.json`/`.js` renamed to `data/database.json`/`.js`; `window.FULL_DATABASE_DATA` renamed to `window.DATABASE_DATA` for consistency with the `STRATEGIES_DATA`/`GLOSSARY_DATA` naming convention. All references updated across `database.html`, `scripts/import_full_database.py`, `scripts/refresh_full_database.py`, `scripts/export_full_database_to_xlsx.py`, and this document. Script filenames themselves were intentionally left unrenamed (only the data files), and historical `docs/PATCHNOTES.md` entries describing past work under the old filename were left as an accurate record rather than rewritten (v1.10.1)
- [x] Resumed the full-scale forward refresh (paused since v1.9.5) against the renamed `database.json`, 6,127 rows due (v1.10.1)
- [x] `data/storage.csv` added: single-column (`url`), append-only, deduplicated backup of every symphony URL ever shared or referenced, independent of `database.json`'s scope so it survives future noise-filtering drops or rebuilds. Seeded with 6,489 unique URLs from the union of `database.json` and `strategies.json`. Documented in Section 12 (v1.10.1)
- [x] Fixed a stale doc: Metric Display Guidelines (Section 12) still said percentages render to 2 decimal places; corrected to 1, matching the `formatPct()` change made earlier but never reflected in the docs (v1.10.1)

### V1.10.2: Nav Restructure

**Status:** Complete (at v1.10.2)

- [x] Top nav reordered to About, Strategies, Database, Glossary, Support (was Strategies, Glossary, Database, About, Individual Stocks, Leveraged Strategies, Support) (v1.10.2)
- [x] Removed the direct external nav links to Individual Stocks and Leveraged Strategies (originally added in v1.5.7); the sites themselves aren't gone, just moved out of primary nav (v1.10.2)
- [x] Added a "More From Azqato" section to `about.html`: a short description of each sibling site and its relevance to Composer Atlas, plus a CTA button linking to each (v1.10.2)
- [x] Footer nav links reordered to match (v1.10.2)

### V1.11: Filter Panel (Shared Component)

**Status:** Complete (built ahead of its roadmap slot, per explicit user request, alongside V1.12-V1.13)

**Decisions locked before implementation:** ships on **All Strategies** first, placed above the result-count line; holdings filter included at launch (accepting a heavier data payload, addressed by V1.16 instead of scoping the filter down); reuses click-to-sort column headers rather than a separate Order-by dropdown.

**Design reference (community "Symphony Search Tool"):** searchable field-picker + operator + value per row, "Add filter" to stack rows (AND logic), Cancel/Apply, empty state until a filter exists.

- [x] `createFilterController(opts)` in `database.html`: a reusable factory (not a separate loaded file, both consuming tabs live in the same HTML page, so a JS module boundary wasn't necessary, shared functions were enough), each tab instantiates its own controller with independent applied/pending filter state
- [x] `FILTER_FIELDS`: 20 filterable fields (all core return/risk/ratio metrics, `backtest_days`, derived `oos_days`, plus a `holding` type for ticker matching against `last_market_days_holdings`) and `NUMBER_OPS` (`=`, `>`, `<`, `>=`, `<=`, `between`, the last accepting a `"min, max"` value)
- [x] `matchesFilter()` / `matchesAllFilters()`: the actual filter engine, client-side, no backend
- [x] Wired into All Strategies (`allFilterController`) and Screener (`screenerFilterController`); Leaderboard also got its own instance (`leaderboardFilterController`) for consistency, though not originally scoped as a V1.11 requirement
- [x] `.filter-panel`, `.filter-row`, `.filter-empty` CSS added to `css/main.css`, documented in `docs/DESIGN.md`

### Overfit Method Audit (2026-10-15)

**Status: the redesign below was approved by the owner and shipped 2026-10-15 (see PATCHNOTES, "Overfit Check: the cone test"). Par is retired.**
The owner asked for an "extreme analysis" of whether the Overfit Check defines and rates overfitting
accurately, against academic research, competing tools and our own data. This section is the
reference copy of that work so it does not need to be redone.

#### Summary

- **The measurement holds up.** The fitted-era split, the edit-date out-of-sample window and the
  score's arithmetic are sound. The Overfit Score is exactly `100 x (1 - Pardo's walk-forward
  efficiency)`, a standard industry quantity.
- **The verdict does not.** The par-relative verdict (including the verdict box, `401d503`) mostly
  reads noise, and par excuses the very thing the literature defines as overfitting.
- **Recommendation:** keep the engine, rewrite the judgement layer as a self-referential cone test
  against each symphony's own backtest (details below).

#### Research findings (academic)

1. **Overfitting is defined by selection, not intent.** Bailey, Borwein, Lopez de Prado and Zhu
   define backtest overfitting as choosing a configuration because its backtest looked best among
   many tries; the inflated backtest then reverts out of sample. The reversion is the symptom.
   This contradicts par's premise above ("mean reversion guarantees a gap after an extreme backtest
   whether or not anything was overfit").
2. **Decay is the norm and its size is known.** Industry habit is to halve a backtested Sharpe;
   Harvey and Liu show the correct haircut is nonlinear. Suhonen, Lennkh and Perez: bank-built
   alternative beta strategies lost a median ~73% of their Sharpe live, more when complex; only
   8.4% improved live and ~30% went negative. Falck, Rej and Thesmar: published strategies keep
   about 50% of in-sample performance; outlier-sensitivity of the in-sample Sharpe and signal
   complexity explain ~15% of decay variance, publication year ~30%.
3. **Backtest Sharpe barely predicts live Sharpe.** Wiecki et al. (Quantopian, 888 algorithms):
   R^2 < 0.025 for Sharpe; volatility and max drawdown do persist; more backtesting by the author
   means a larger in-sample/out-of-sample gap; non-linear classifiers on many features reach R^2 0.17.
4. **Formula tests need a trial count.** The Probabilistic and Deflated Sharpe Ratios correct for
   luck and the number of variants tried; Arnott, Harvey and Markowitz's protocol asks researchers
   to record that count. Nobody knows it for a Composer symphony.
5. **The practical standard is live-versus-predicted with noise accounted for:** Pardo's
   walk-forward efficiency (50% or better is commonly called robust) and pyfolio's Bayesian cone
   (projects the backtest forward and checks whether live returns stay inside).

#### Competitive findings

| Platform | What it does about overfitting | Relevance to Atlas |
|---|---|---|
| Composer | Shows an "OOS Start Date" (last edit) on symphony pages; metrics are not split and no verdict is given | Atlas is already well ahead |
| QuantConnect | Probabilistic Sharpe Ratio on backtests | Useless on our data: PSR = 1.000 for every fitted era, rank corr -0.28 with live Sharpe |
| StrategyQuant | Re-runs on perturbed data and parameters: Monte Carlo, walk-forward matrix, multi-market | Needs full price data: our V2.4 Tier 3, still blocked on price coverage |
| pyfolio / qf-lib | Backtest cone drawn against live returns | Closest precedent for the proposed design |
| Allocate Smartly, Portfolio123, QuantMage | Nothing systematic found | None |

#### Empirical findings on our data

**Method.** 3,125 symphonies whose full backtest and OOS re-run end within 7 days of each other
(of 3,472 scored); 2,622 of them past the 365-day gate. Fitted-era daily mean and volatility are
backed out by moment decomposition. Composer's Sharpe is `mean_daily * 252 / sd_annual` with no
risk-free rate (verified on a real row), so:

```
m_O   = SR_O * sd_O_annual / 252          s_O = sd_O_annual / sqrt(252)
N_I   = backtest_days - N_O
m_I   = (N_F m_F - N_O m_O) / N_I
s_I^2 = (N_F (s_F^2 + m_F^2) - N_O (s_O^2 + m_O^2)) / N_I - m_I^2
```

This reproduces the shipped fitted rates independently (median ratio of log rates 0.999, p10
0.992, p90 1.001; rank corr 1.000). All figures below are from the 2026-10 data snapshot.

**1. The verdict mostly reads noise.**
- Standard error of the score from OOS luck alone, `100 (1+d) sd_O / sqrt(T_O) / fitted`: median
  22.9 points (p25 13.6, p75 35.4), against verdict thresholds of 5 and 15.
- After removing the par-style size effect, the residual the verdict reads has reliability 0.14
  (86% noise). Par alone explains 43% of score variance.
- Only 43 of 352 "Overfit" calls (12%; 17% on the unclamped score) and 7 of 418 "Probably overfit"
  (2%) are distinguishable from par at 95%. Across all eligible rows, 3.8% are significantly worse
  than par versus 2.5% expected by chance.
- The shipped "Overfit" rate falls as evidence grows: 24.1% (1-2 live years), 10.9% (2-3), 6.0%
  (3+). A sound test should find more with more data.
- Median width of a 95% range on "share kept": 110 points.

**2. Par excuses overfitting.**
- Self-referential test `z = (m_O - m_I) / sqrt(s_I^2/N_I + s_O^2/N_O)`: median z -2.11; 54.4%
  below -1.96 (2.5% expected if backtests were honest forecasts), 27.1% below -3, 0.5% above +1.96.
  On the log cone with OOS noise only (see proposal): 62%.
- 946 of 1,852 "No overfitting signal" rows (51%) fell short of their own backtest beyond luck;
  206 of 1,070 (19%) even among green boxes with no caution line. No "Overfit" row is consistent
  with its backtest.
- Failure rate by fitted-rate fifth: 36% (1-49%/yr), 48% (49-92%), 56% (92-164%), 71% (164-324%),
  99% (325%+). Median share kept on the compounding scale: 56%, 39%, 36%, 27%, 8%.
- `mlgAKFuUIPZiCT0aV7ho` (advertises "AR: 8962.9%"): fitted +9,655%/yr over 2.9 yrs, live +24%/yr
  over 3.9 yrs; score 99.7 vs par 99.4 gives "No overfitting signal". Its cone: +4,171% to
  +22,184%/yr.

**3. Composer backtests behave like the literature's overfit populations.**
- Sharpe: fitted median 2.36, live median 0.94, median haircut 63%. Live Sharpe at or above fitted:
  4.6%. Negative live Sharpe: 4.1% (bull-market sample).
- Persistence (rank corr, fitted to live): volatility +0.93, annualized return +0.17, **Sharpe
  -0.31** (-0.32 where OOS is at most 30% of the window).
- Walk-forward efficiency: median 22%; only 19.6% reach 50%.
- Predictors of the shortfall z on low-contamination rows (rank corr): fitted Sharpe -0.73, fitted
  return -0.47, turnover -0.50, tail ratio -0.50, tickers it can hold -0.50, fitted length +0.34,
  top-5%-days share of return +0.57 (smooth curves decay more). Kurtosis, skew, best-day share:
  weak. Max drawdown's apparent signal vanishes once contamination is limited.
- PSR is 1.000 for every fitted era. A median 10.1-year Sharpe of 2.36 would need about 10^13
  zero-skill variants to arise by luck (Bailey and Lopez de Prado expected-maximum formula), so
  trial-count corrections cannot be applied.

**4. Predictive validity (1,797 symphonies with 2+ live years; early window judged, outcome = raw
last-12-month return, so no shared term):** early own-backtest z +0.256 (+0.296 partial on fitted);
early score minus par +0.184; raw early return +0.168. Flagged early by z: median +7.0% next year
versus +20.2%; par "Overfit" versus "No signal": +12.4% versus +17.3%. (Early z versus shortfall
against the promise, +0.686, is a shared-term artifact and must not be quoted.)

**5. Page caveats that are now factually wrong.**
- "+0.93 with annualized excess return over SPY, ~80% tail shared": measured 0.53 (eligible) to 0.58
  (all decomposed), 67-73% of the worst fifth shared; the pre-split score gives 0.57-0.62.
- "rank correlation -0.56" for how much a backtest gives up versus its size: wrong sign. Score vs
  fitted rate is +0.574 (all scored), +0.658 (eligible).

**6. Limits.**
- Every live window is 2022-2026; SPY ran +17 to +20%/yr in every vintage. Score versus SPY return in
  the window: -0.01. No method here has been seen in a bear market.
- Survivorship: score minus par is +2.3 for 365-548 untouched days and -4.3 for 1,095+ (partial corr
  -0.197 on fitted). z is flat across lengths and vintages, score minus par drifts ~5-7 points.
- Simple-rate scale exaggerates decay at the top: top fitted tenth median score 99.3 (26% at 100)
  versus 95.5 on the compounding scale; all eligible 77.7 versus 70.0.

#### The redesign (shipped 2026-10-15)

1. **Verdict = cone test against the symphony's own backtest.** No population, no weights:
   ```
   kept  = ln(1 + live rate) / ln(1 + fitted rate)
   range = kept +/- 1.96 * (live volatility / sqrt(live years)) / ln(1 + fitted rate)
   Fell short of its backtest    whole range below 100%
   Beat its backtest             whole range above 100%
   Too early to tell             range covers both 0% and 100%
   Consistent with its backtest  otherwise
   ```
   Eligible mix: Fell short 62%, Consistent 9%, Too early 29%, Beat 0.5% (54% fall short if the
   backtest's own noise is also counted). By live length, Fell short 59.6% / 61.2% / 65.1% and Too
   early 35.8% / 32.9% / 16.9% for 1-2 / 2-3 / 3+ years: it gains power as data accrues.
   Reader line: "If it really had its backtest's edge, 95% of N-year live records would land between
   A% and B% a year. It made C%."
2. **Retire par as the yardstick;** optionally recast it as a base rate ("of backtests this size,
   71% fell short of their own promise").
3. **Score on the compounding scale with its range,** whole numbers only.
4. **Replace the 365-day gate with the noise rule** plus a ~63-trading-day floor: 183 of the 500
   testable gated rows fall short decisively.
5. **Fix the two caveats; add an SPY-in-each-era line;** guard cash-like strategies
   (`JhjdVrxpOpQlAqxAH08P` "beats" +1% with +5% only because T-bill rates rose).
6. **Optional:** show the warning signs individually with base rates, never combined.

Cost: one new index field (OOS volatility, from `oos.json`) in `scripts/build_overfit.py`, a
rewrite of the verdict and caveats in `overfit.html`, docs.

**Worked examples (shipped call / proposed call):** `iM4mdWcn3DPeUNZPsYNW` TQQQ FTLT 2.0, +192% to
+30% over 2.2 yrs, cone +37% to +525%: No signal / Fell short. `C8QUEQBKayzmaSBz7MAZ`, +43% to +33%:
No signal / Consistent. `Xc7QRMe6sawhO6pKkp7S`, +81% to +30% over 2.8 yrs: No signal / Too early.

**Why this is the owner's call:** it overturns the par doctrine recorded above. The proposed test is
purely self-referential, which matches the "against its own promise" framing and the 2026-08-28
rejection of peer ranking more closely than par does.

#### Sources

- Bailey, Borwein, Lopez de Prado, Zhu, The Probability of Backtest Overfitting: https://papers.ssrn.com/abstract=2326253
- Bailey, Lopez de Prado, The Deflated Sharpe Ratio: https://papers.ssrn.com/abstract=2460551
- Harvey, Liu, Backtesting: https://people.duke.edu/~charvey/Research/Published_Papers/P120_Backtesting.PDF
- Arnott, Harvey, Markowitz, A Backtesting Protocol in the Era of Machine Learning: https://papers.ssrn.com/abstract=3275654
- Falck, Rej, Thesmar, Why and how systematic strategies decay: https://arxiv.org/pdf/2105.01380 (summary: https://cfm.com/why-and-how-systematic-strategies-decay/)
- Wiecki et al., Quantopian 888-algorithm study: https://quantpedia.com/quantopians-academic-paper-about-in-vs-out-of-sample-performance-of-trading-alg/ , https://www.cxoadvisory.com/big-ideas/in-sample-vs-out-of-sample-performance-of-888-trading-strategies , https://hedgefundalpha.com/strategies/comparing-backtest-sample-performance-large-cohort-trading-algorithms/
- Suhonen, Lennkh, Perez: https://hedgefundalpha.com/strategies/alternative-beta-strategies-complexity-magical-backtests/
- pyfolio Bayesian tear sheet: https://nbviewer.jupyter.org/github/quantopian/pyfolio/blob/master/pyfolio/examples/bayesian.ipynb
- qf-lib AnalyticalCone: https://qf-lib.readthedocs.io/en/stable/_autosummary/qf_lib.common.utils.confidence_interval.analytical_cone.AnalyticalCone.html
- QuantConnect PSR: https://quantconnect.com/forum/discussion/6483/probabilistic-sharpe-ratio/p2/comment-31723
- StrategyQuant robustness cross-checks: https://strategyquant.com/doc/strategyquant/cross-checks-automated-strategy-robustness-tests
- Composer backtests: https://help.composer.trade/article/215-7-how-do-backtests-work-in-composer
- Pardo, The Evaluation and Optimization of Trading Strategies (2008)

### The Overfit Verdict Box

The Overfit Check renders a score, a band label and a par mark, and a reader still had to assemble
"is this one overfit?" out of them. The verdict box states it, above the score, because the call is
the answer and the score is the working.

**The call is the distance from par, not the score.** This follows the page's own doctrine: the
score contains no population data at all, par is the only place the population enters, and an
extreme backtest reverts whether or not anyone fitted it. So 15 or more points above par is
"Overfit", 5 to 15 is "Probably overfit", within 5 either way is "No overfitting signal". The
5-point band is the one the prose verdict already used; they share it deliberately so the box and
the paragraph below it can never contradict each other.

**Two guards keep the label honest.**

1. **The caution line.** A score of 75 or more that still sits within 5 points of par is labelled
   "No overfitting signal", which on its own reads as "this one is fine" about a strategy that kept
   almost nothing. The box says so in the same breath, and gives up its green styling, so colour
   does not say "fine" next to a pink "Did not survive".
2. **The days gate runs first.** 674 of 3,472 scored rows have had a logic edit inside the
   365-day window. They carry a score because the backtest can still be split, but the window is
   too short for this test, and the prose verdict already told the reader there is no verdict yet.
   The box therefore checks `days` before it looks at the score, says "No verdict", and explains
   why a number is on screen underneath it anyway.

"No verdict" is treated as a result rather than an absence: it always names which reason applies,
rather than leaving the question the reader arrived with unanswered.

### Shareable Screener Links

The Screener holds its whole state in module-scope variables, so a shareable link is just a
serialisation of them. It goes in the **URL fragment**, not the query string: a fragment never
reaches the host, and it stops a filtered view being indexed as a page of its own. Format:

```
database.html#screener&view=riskAdjusted&tier=2&q=tqqq&sort=sharpe_ratio&dir=asc&page=3&f=calmar_ratio.5,sharpe_ratio.3
```

Only non-default state is written, so an untouched Screener produces a bare `#screener`.

**The one real decision here is how bucket filters are encoded.** The options in each dropdown are
deciles of the dataset as currently loaded (`buildBucketOptions`), so their thresholds move every
time the database is refreshed. Two encodings were available:

- **By threshold** (`calmar_ratio.min=1.69`): reproduces the exact numeric filter forever, but after
  a refresh that number is no longer one of the ten options, so the dropdown could not show it as
  selected. The link would survive as a filter the UI cannot display.
- **By option index** (`calmar_ratio.5`): means "the fifth Calmar bucket". The threshold behind it
  drifts as the data grows, but it always resolves to an option that exists and that the dropdown
  can display.

Index won, because the index is the only thing the UI can actually express: the dropdown offers
deciles, not free numeric entry. The consequence is deliberate and worth knowing: **a shared link
tracks the decile, not the number.** A link to "top 10% Calmar" shared today still means top 10%
next month, against different thresholds.

Everything read from a fragment is validated against the live options (view name against
`SCREENER_VIEWS`, tier and bucket indexes against their option lists, sort key against the chosen
view's sortable columns), so a hand-edited or stale fragment degrades to the default rather than
throwing.

The URL is written by `writeScreenerHash()`, called from `renderScreenerPage()`. Every state
change in that tab ends in a render, so that single hook covers all of them, and it no-ops when the
Screener is not the visible tab, which is also what clears the fragment when you switch tabs. It
uses `replaceState`, not `pushState`: the name search re-renders on every keystroke, and pushing
would bury the back button under hundreds of entries.

Reading happens once, in the loader, after `buildBucketOptions()` (it resolves option indexes
against those options) and before the first `renderScreenerPage()` (which would otherwise overwrite
the fragment with the default state). `applyScreenerHash()` returns whether the fragment was a
Screener link, and the loader uses that to call `activateDbTab('screener')`.

### V1.12: Screener Tab

**Status:** Complete (full multi-view switcher built now, per explicit user decision, not deferred to a later pass)

**Design reference (Finviz):** Order-by control skipped per decision (reuses click-to-sort headers instead); the secondary column-view tab row was built in full now.

- [x] Reuses the V1.11 Filter Panel component (`screenerFilterController`) as-is
- [x] `SCREENER_VIEWS`: three switchable column sets, Overview (ARR/1Y/Max DD/Sharpe/Calmar/Backtest), Risk-Adjusted (Sharpe/Calmar/Sortino/Win Rate/Max DD/Std Dev), Distribution (Median/Skewness/Kurtosis/Tail Ratio/three Concentration columns), each reusing the same `.db-table` rendering pattern with a different `columns` array
- [x] View-switch tabs render as `.db-tab` buttons nested inside the Screener panel (visually distinct row from the top-level All Strategies/Leaderboard/Screener/Metrics tabs)
- [x] Own sort state and pagination, independent of All Strategies' (switching views resets sort, since different views expose different sortable columns)
- [x] **CSV export of the filtered result set (done v1.32.2).** Two buttons in the Screener
  toolbar, by owner ruling when asked to pick one: **Export view .csv** writes the active column
  view plus `symphony_id` and the Composer URL, and **Export all fields .csv** writes every scalar
  field the database holds. Both export the **whole filtered set, not the visible page**, which is
  the entire point: the page shows 20 rows and a typical filtered set is thousands.

  **Values are written raw (`0.4264`), never display-formatted (`42.64%`).** A percent sign turns
  the cell into text the moment it opens in a spreadsheet, and the export exists to be calculated
  on. Formatting is a display concern and does not cross the boundary.

  **Three details that are not obvious and were each verified rather than assumed.**

  1. **The UTF-8 BOM is load-bearing.** Without it Excel reads the file as the system codepage and
     mangles every non-ASCII symphony name, and plenty carry accents and emoji.
  2. **Unranked rows export blank, not zero.** Rank, tier and score live in `rankBySymphonyId`, not
     on the entry, and 7 rows of 6,547 are in the Screener pool but absent from the ranking. Zero is
     a score; blank is an absence, and writing `0` would put seven fake bottom-ranked rows into
     every export.
  3. **The all-fields column list is the union across every row, and excludes any key seen holding
     an object anywhere.** The first implementation decided scalar-ness from the first row carrying
     the key, and `last_market_days_holdings` is `null` on some rows and a map on others, so a
     first-row `null` admitted it and every populated row exported the literal string
     `[object Object]`. **This is the same class of bug `export_summary.py` shipped at v1.25.1**,
     which derived its column list from entry zero. Caught by the headless test, not by review.

  **Verified in headless Edge** against the real 6,547-row working pool: both modes export 6,547
  data rows; 12 columns for the Overview view and 31 for all-fields; **zero ragged rows in either
  mode**, including the 616 symphonies whose names contain a comma; every cell in the six numeric
  Overview columns parses as a plain number across roughly 39,000 cells; and a comma-bearing name
  round-trips through a real quote-aware parser back to exactly 12 fields.

### V1.13: Leaderboard Tab

**Status:** Complete (built ahead of its roadmap slot, per explicit user request, alongside V1.11-V1.12)

**Sequencing conflict, resolved as an accepted known gap:** the scoring model excludes noise-flagged entries from the ranking pool, but Noise Filtering (V1.14) ships *after* Leaderboard, so the `is_noise` flag won't exist yet at launch. Confirmed live in the preview below, TESTPORT/Invest-Copy/duplicate-name entries do show up in the early top ranks. **Decision: accepted as-is for now**, Leaderboard ships without noise-exclusion and gains it once V1.14 lands; order does not swap.

**Design reference (user-specified):** relative-percentile methodology adapted from the sibling Individual Stocks site's screener (`azqato.com/stocks/screener.html`, source: `github.com/Azqato/stocks` `screener.js` + `docs/PRD.md`). Core mechanics: rank every metric by percentile among eligible entries (not raw value), apply a clamp curve so only the top ~22% of a metric earns full marks (keeps a perfect score rare), missing data scores a hard zero against a fixed denominator, and tiers are assigned by rank (not absolute score) with ties rounding up into the better tier.

**Locked scoring model: 20 metrics, 1,000 points total, across 7 categories.**

| Category | Metric | Direction | Points |
|---|---|---|---|
| **A. Return** | `annualized_rate_of_return` | higher better | 100 |
| | `median` | higher better | 100 |
| **B. Trailing Returns** | `trailing_one_year_return` | higher better | 50 |
| | `trailing_three_month_return` | higher better | 25 |
| | `trailing_one_month_return` | higher better | 15 |
| | `trailing_two_week_return` | higher better | 10 |
| **C. Risk-Adjusted** | `sharpe_ratio` | higher better | 50 |
| | `calmar_ratio` | higher better | 50 |
| | `sortino_ratio` | higher better | 50 |
| | `win_rate` | higher better | 50 |
| **D. Downside Risk** | `max_drawdown` | higher (less-negative) better | 100 |
| | `standard_deviation` | lower better, inverted | 100 |
| **E. Asymmetry / Shape** | `skewness` | higher better | 40 |
| | `tail_ratio` | higher better | 30 |
| | `kurtosis` | lower better, inverted | 30 |
| **F. Concentration / Fragility** | `top_one_day_contribution` | lower better, inverted | 50 |
| | `top_five_percent_day_contribution` | lower better, inverted | 25 |
| | `top_ten_percent_day_contribution` | lower better, inverted | 25 |
| **G. Longevity** | `backtest_days` | higher better | 75 |
| | OOS days (derived from `oos_date`) | higher better | 25 |

Category totals: A 200 / B 100 / C 200 / D 200 / E 100 / F 100 / G 100 = **1,000**. Three "major" categories (Return, Risk-Adjusted, Downside Risk) at 200 each; four "supporting" categories at 100 each.

**Explicitly excluded from scoring, with reasons:**
- `cumulative_return`: redundant with ARR compounded over `backtest_days`; would double-reward long-running strategies who'd already score well on Longevity
- `mean`: near-duplicate of ARR (same "how much does it make on average" concept, different units)
- `max` (best single period): ambiguous alone, conceptually overlaps with the Concentration category anyway
- `herfindahl_index`: no clear better/worse direction for this domain, many of these strategies deliberately concentrate into 1-2 leveraged ETFs by design; kept as a potential future display-only context column, not scored
- `total_costs`, `annualized_turnover`: removed per explicit decision, not scored
- `min` (worst single period): removed per explicit decision, likely too correlated with `max_drawdown` for this leveraged-ETF-heavy dataset (the worst single month and the worst drawdown tend to be the same crash event for these instruments)

**Mechanics:** each metric's raw values are ranked across all eligible entries, ties averaged, converted to a percentile (inverted for "lower better" metrics), then `points = clamp(cap × (percentile - 0.22) / (1 - 2×0.22), 0, cap)` where `cap` is that metric's point value from the table above. Missing data scores 0 for that metric only; the 1,000 denominator never shrinks. Tiers by rank over the eligible pool: S/A/B/C/F at 10/10/20/25/25%, ties round up into the better tier, plus a special **S+** for a perfect 1,000/1,000. Clamp constant stays at **0.22** for launch.

**Validated with a live preview (v1.10.x, this session):** ran the full model against the 2,282 entries refreshed so far. The math held up correctly (proper score differentiation, missing-field entries still scored, tiers computed correctly), and the top 25 confirmed the sequencing gap concretely, roughly 10-12 of the top 25 rows were distinct strategies, the rest were the same handful of strategies double- or triple-counted via TESTPORT ports, "Invest Copy"/"Copy of" clones, and renamed duplicates (e.g. three "Golden Ratio FTLT" name variants, two "Lowcore" TESTPORT numbering variants of the same strategy). Confirms Noise Filtering (V1.14) is doing real, necessary work later, not a nice-to-have.

- [x] Implemented the scoring engine per the table above: `computeScores()` (percentile rank + clamp curve per metric, summed to a 0-1,000 score) and `computeTiers()` (rank-based cuts with round-up ties and the S+ carve-out), both in `database.html`
- [x] Eligibility gate: only entries with `sharpe_ratio` present (the same proxy used throughout this session's live previews for "has been refreshed") enter the ranking pool; the toolbar explicitly states how many entries were excluded as not-yet-refreshed
- [x] Reuses the V1.11 Filter Panel (`leaderboardFilterController`, filters the already-ranked pool) and the standard `.db-pagination` pattern
- [x] Table columns: Rank, Tier (`.tier-badge`), Score (`X / 1,000`), Symphony, ARR, Sharpe, Calmar, Max Drawdown
- [x] Shipped without noise-exclusion (accepted gap, documented above); wiring in the V1.14 `is_noise` exclusion is still pending until that field exists
- [ ] **Post-rollout:** re-evaluate the 0.22 clamp constant against the actual score distribution at full scale; explicitly deferred, not skipped
- [ ] Surface `sortino_ratio` and `win_rate` more broadly once V1.15 Full-Scale Refresh completes (resumed v1.11.4, was 3,706/7,685, now processing remaining rows)

### V1.14: Noise Filtering

**Status:** Implemented (v1.11.22). Both Part A and Part B are built and have run against the live database.

**Part A: Name-based noise (non-strategy rows)**

- [x] **Implemented (v1.11.22):** `scripts/flag_name_noise.py` flags `TESTPORT #`/`[Work]`/`STILL BUILDING` rows with `flag = "excluded"` (reuses the existing level rather than introducing a new one). Run against the live database: **88 rows flagged.**
- [x] **De-duplication policy decided (v1.11.16, revised v1.11.17) and implemented (v1.11.22):**
  - **Clustering (candidate-finding only):** group rows by normalized name, strip `TESTPORT #N: ` prefix, leading `Copy of ` chains (one or more), and `(Invest Copy)` suffixes, then compare what's left. Name matching is only ever used to find *candidates* to check, never as the actual duplicate decision, real data shows two rows can share an exact literal name and have meaningfully different metrics (`V2 Holy Grail Simplified w/RSI Divination - without VIXen` appears twice with ARR 180.8% vs 215.2%), so name alone is not trustworthy evidence of duplication in either direction.
  - **Primary identity check, logic-tree structural equality (v1.11.17, supersedes the metrics-tolerance approach as primary):** for each candidate cluster, fetch `GET /api/v0.1/symphonies/{id}/score?score_version=v1` (Section 13, Logic Tree Endpoint) for every member, one lightweight GET per row, no backtest execution required. Strip every `id` field (Composer assigns a unique UUID to *every* node, root and nested, even for literal clones) and the root-level `name` field (carries the "Copy of"/"TESTPORT" text), then compare the canonical (sorted-key) JSON. An exact match after stripping means the rows are structurally identical strategy logic, not just similar-performing. Verified live against the real "Holy Grail simplified" 4-row cluster below: all four hash identically after stripping, confirming they're the same underlying symphony.
    - This is preferred over metrics comparison because it needs no tolerance threshold (exact match, not "close enough") and no same-day-refresh alignment (logic is stable until someone edits it; backtest metrics drift day to day even for genuinely unchanged logic).
  - **Fallback, metrics comparison (used only if the logic-tree endpoint is unavailable/fails for a candidate):** compare `annualized_rate_of_return`, `max_drawdown`, `trailing_one_year_return`, `cumulative_return`, `sharpe_ratio`, `calmar_ratio`, `backtest_days`, restricted to same-`refresh_date` rows only (force a refresh of the whole cluster first if members weren't refreshed the same day). "Identical" = within **3 percentage points** absolute for the percentage-scale fields (ARR, max drawdown, 1Y return) or **3% relative difference** for the rest (Sharpe, Calmar, cumulative return, backtest days): validated against real near-miss pairs in the live data (e.g. "The Holy Grail" 151.8% ARR vs. its "Buy Copy"/"Canonical" cluster at 151.7% ARR, 0.05pp apart, correctly merges; "Holy Grail simplified" at 134.9% vs. "The Holy Grail" at 151.8%, 16.9pp apart, correctly stays separate).
  - **Tiebreak among identical rows:** keep the one with the longest `oos_date` (longest continuously-unedited logic). If `oos_date` also ties (or all are null), fall back to the lexicographically earliest `symphony_id`: arbitrary but deterministic.
  - **Future-state idea (2026-07-15), validated by a manual sanity-check sample:** user wants the tiebreak to eventually prefer whichever cluster member has the highest "Watched by N" popularity count. Not exposed by the API this pipeline uses (`/backtest`, `/score`): only shown on the rendered Composer web app page. A one-off headless-Chrome scrape (not part of the shipped pipeline) of 13 clusters (51 symphonies, ~3% of the 179 total duplicate clusters) found the current `oos_date`/`symphony_id` tiebreak picked the most-watched member in only **2 of 13 clusters**: in the other 11, a differently-suffixed variant (usually the plain, unsuffixed name) had dramatically more watchers than the `symphony_id`-selected "kept" row, e.g. one cluster's kept row had 1 watcher against a same-cluster alternative with 1,755. Strong enough a pattern to justify eventually rebuilding the tiebreak around this signal, but still **not buildable as an automated pipeline step today**: no API access to the count, and hammering ~400+ rendered pages via headless Chrome per full-database refresh is a fundamentally heavier, slower integration than every other JSON-API call this pipeline makes elsewhere. Until a real data source exists (API support, or a deliberate decision to accept the scraping cost on a slower cadence), **per-cluster manual overrides are handled ad hoc** on explicit user request: flip `flag`/`error` for every affected cluster member directly in `data/database.json` (not just the two rows being swapped, every row in the cluster references the kept `symphony_id` in its `error` field, and all of them need updating together or the cluster's cross-references go inconsistent), regenerate `database.js`/`database_summary.json`/`.js` via `scripts/export_summary.py`. **Clusters corrected this way so far (2026-07-15):** The Holy Grail, Mean Reversion Comparison to Python Code, TQQQ FTLT w/Sideways Market Mods (FINAL), Nuclear Energy with Feaver Frontrunner V5, S&P Symphony w/ Leverage, TQQQ or Not - Non-Degen Gambler Variant, "We know this works. We just get greedy." (old kept row's page was inaccessible/likely dead, an added reason to swap), Inside Nancy Pelosi's Chips- V3, Copy of Holy Grail simplified.
  - **Tiebreak has no name-based priority (confirmed v1.11.18):** per user decision, the `symphony_id` tiebreak is used exactly as specified, with no special-casing for `TESTPORT #`/WIP-marker names even though that can produce a counterintuitive "keeper" (see examples below). Simplicity over a bespoke priority rule for what's already an arbitrary fallback.
  - **Real examples, `symphony_id` tiebreak (v1.11.18):**
    - 4-way "Holy Grail simplified" cluster (`TESTPORT #016: Copy of Holy Grail simplified`, `Copy of Holy Grail simplified (Invest Copy) (Invest Copy)`, `Copy of Holy Grail simplified`, `Copy of Copy of Holy Grail simplified`): confirmed structurally identical via the logic-tree check, `oos_date` also identical across all four. This is the example that motivated running `flag_name_noise.py` *before* the dedup pass: by the time dedup actually ran, `TESTPORT #016:` had already been flagged `excluded` by the name-noise pass and was never a dedup candidate at all, so the `symphony_id` tiebreak among the remaining three picked `Bpq9NoCpCJfN0nrKk5dC` ("...(Invest Copy) (Invest Copy)") as the keeper instead, confirmed against the real post-run data. A legitimate-looking name stays visible in "Working," exactly the outcome the sequencing was designed for, achieved without any tiebreak special-casing.
    - "TQQQ For The Long Term V2 (226.7% RR/46.1% Max DD)" cluster (6 rows) splits into two identical sub-groups plus one genuine remix (`...+ The Holy Grail`, different metrics, correctly excluded): one 2-row sub-group where `oos_date` actually differs (2022-08-24 vs 2022-12-04) so the *primary* rule decides directly, no tiebreak needed; one 3-row sub-group where `oos_date` ties for all three, falling to the `symphony_id` sort, which keeps an `(Invest Copy)`-suffixed row (`Ipvw0S4HlF8GNa7Oe6TP`) over the plain-named one, same shape of arbitrary-but-accepted outcome as the first example.
  - **Candidate-finding signal (elaborated v1.11.18):** name-normalization alone, no corroborating signal (e.g. `last_market_days_holdings`) needed. Reasoning: the actual duplicate decision is made by the exact logic-tree structural check, which can't be fooled, so the two possible failure modes of the name-based candidate filter are asymmetric. A false positive (coincidentally similar names grouped together) is harmless: the structural check just fails to match and both rows are correctly kept, at the cost of one extra cheap API call. A false negative (a real duplicate published under a name too different to normalize together) is a soft failure: that pair just doesn't get deduped this pass, the database stays slightly noisier than ideal, but nothing is ever wrongly deleted. Since a wrong deletion is the only outcome that actually matters and the structural check already fully guards against it, a corroborating signal mostly adds complexity (holdings can legitimately differ between two real duplicates just from market-price timing) without reducing the one real risk. Do tighten the normalization regex itself, though, it's currently missing `(Buy Copy)`, which appears in the live data alongside `(Invest Copy)`.
  - **Disposition of the losers, revised v1.11.18, supersedes the v1.11.16 "delete outright" decision for dedup specifically:** per user decision, duplicates are **flagged, not deleted**. Extend the `flag` field's value set with a new `"duplicate"` level (alongside `"excluded" | "caution" | "retry"`); every cluster member except the kept "original" gets `flag = "duplicate"`, all rows stay in `data/database.json`. This is a real policy change from the earlier "delete outright, preserve URL in storage.csv" plan, that treatment is unchanged for the already-executed 404/422 `excluded` purge (v1.11.14), it's specifically the dedup losers that get the flag-and-keep treatment instead.
  - **UI built (v1.11.20):** per user decision, `"Duplicates"` added as a 4th flag-mode option (not folded into "Broken"), positioned between "Broken" and "All". Full mode order/labels: `default` → **Working**, `flagged` → **Broken** (`caution`/`excluded` only), `duplicates` → **Duplicates** (`flag === 'duplicate'` only), `all` → **All**. "Working" (the default view) excludes all three noise categories, `caution`, `excluded`, and `duplicate`: via a shared `isNoiseFlag()` check.
  - **Pipeline built and run (v1.11.22):** `scripts/dedupe_symphonies.py` implements the full policy above, normalize-name clustering restricted to `flag == null` rows only, logic-tree structural check with the metrics-tolerance fallback, `oos_date`→`symphony_id` tiebreak. Tested against a real 5-member "Holy Grail" family before the full run (correctly kept the hand-computed winner; correctly left two near-miss rows alone since their names didn't normalize into the same candidate cluster, an accepted soft-miss, not a bug). **Full run results:** 362 candidate clusters (842 candidate rows) processed; **225 rows flagged `duplicate`** (229 total including the earlier validation test); **23 logic-tree fetches failed** (mostly `404`s, likely symphonies deleted/made private between when they were scraped and this run; those rows were left ungrouped rather than force-refreshed, a known, accepted gap in this pass, not a crash). Final database-wide flag tally: 6,221 clean, 229 duplicate, 88 excluded, 88 caution, 14 retry (6,640 total). `database_summary.json`/`.js` and `Full Database.xlsx` regenerated to match.
- [x] **Resolved (v1.11.22):** the exclusion-rule patterns (`TESTPORT #`, WIP markers) are flagged, not deleted, reusing the existing `excluded` level rather than a new one, since the practical effect (hidden from default views) is the same as a permanently-failing row. See `scripts/flag_name_noise.py` above.

**Part B: Data-quality noise (error/warning-based): policy decided v1.11.4, implemented as a schema field v1.11.8, consolidated to the sole write target v1.11.9**

**Final counts (v1.11.8, full 7,685-row refresh complete):** 1,113 entries (14.48%) carry a `script_errors` value, 88 (1.15%) carry a `data_warnings` value. This is a large jump from the earlier partial-sample audit (1.3%/0.5% at 3,707/7,685 rows): the batch of rows processed in the second half of the refresh run failed at a much higher rate (~28% of that batch, almost entirely `422`), concentrated in previously-unrefreshed rows rather than spread evenly. The 422/404 rows have not been spot-checked by hand to confirm they're genuinely dead/private/malformed symphonies rather than some other artifact of that batch; worth a sample check before relying on the "excluded" set for anything user-facing. Breakdown:

| Error | Count | Disposition |
|---|---|---|
| `404 Not Found` | 84 | Permanent, symphony deleted, private, or bad ID from the original scrape. Filter out of default views. |
| `422 Unprocessable Entity` | 920 | Permanent, symphony can't be backtested (empty/malformed logic, zero allocations). Filter out of default views. |
| `429 Too Many Requests` | 68 | Transient, retry, don't filter |
| `500` / `503` / `TimeoutError` | 41 | Transient, retry, don't filter |

`data_warnings` are a different kind of signal, not a fetch failure: `"Close price data is not available for TICKER after DATE"`, meaning a holding in that symphony stopped trading mid-backtest-window. The backtest still succeeded; the metrics are just potentially skewed by the delisting. Decision: filter these out of default Leaderboard/Screener views too (metrics computed over a window with a delisted holding aren't a fair comparison), but keep them visible in All Strategies with a ⚠ indicator rather than hiding them outright, since the row itself is real and refreshed, just caveated.

- [x] **Implemented (v1.11.8):** rather than a boolean `is_excluded`/`is_noise` flag, added a single derived `flag` field, initially via a one-time migration script backfilled onto all 7,685 entries, see Full Database JSON Schema (Section 12) for the shape. `flag.level` is `"excluded"` (404/422), `"caution"` (`data_warnings` present), `"retry"` (429/500/503/timeout), or the field is `null` for clean rows. Final tally at the time: 1,004 excluded, 88 caution, 109 retry, 6,484 clean.
- [x] **Consolidated (v1.11.9):** `flag` is now the *only* error/warning field. `scripts/refresh_full_database.py` was rewritten to compute and write `entry["flag"]` directly on every API call (`classify_error()` for failures, inline classification of the API's `data_warnings` response for successes) instead of writing separate `script_errors`/`data_warnings` fields. Those two raw fields were stripped from all 7,685 existing entries in `data/database.json`/`.js` (their content is preserved verbatim in `flag.reason`, nothing was lost). The one-time migration script (`scripts/add_flag_field.py`) was deleted since its job, backfilling `flag` from fields that no longer exist, no longer applies. Extensively tested against two independent live batches (50 records from the front of the array, 50 from the back, forced re-refresh via `--force`/a manual bottom-slice test harness): both runs produced correctly-shaped `flag` values, including a real transient `429` hit during the second test that was correctly classified `"retry"`; post-test audit confirmed all 7,685 entries are free of `script_errors`/`data_warnings` and `flag.level` counts remain internally consistent (6,484 clean + 88 caution + 109 retry + 1,004 excluded = 7,685).
- [x] `scripts/export_full_database_to_xlsx.py` (nested-field serialization list updated to drop `data_warnings`, keep `flag`) and `scripts/export_summary.py` both re-run after the consolidation, `Full Database.xlsx` (36 columns, down from 38) and `data/database_summary.json`/`.js` (28 fields, down from 30) are back in sync with `database.json`.
- [x] **Renamed (v1.11.10):** `last_updated` → `refresh_date`, `last_semantic_update_at` → `oos_date` across `data/database.json`/`.js`, `database_summary.json`/`.js`, `Full Database.xlsx`, `scripts/refresh_full_database.py`, `scripts/export_full_database_to_xlsx.py`, `scripts/import_full_database.py` (legacy, already out of sync with the current xlsx column layout independent of this rename), and `database.html`. `oos_date` is also now truncated to plain `YYYY-MM-DD` at write time (previously stored the Composer API's full timestamp with time-of-day and timezone, e.g. `2026-03-16T08:11:33.345904-04:00[America/New_York]`); the live "days since" computation in `oosDaysValue()` is unaffected since it only ever needed the date portion. This rename is scoped to `database.json`'s schema only, `strategies.json`/`glossary.json` each have their own separate `last_updated` field, untouched. Tested with a live `--force 20` batch after the rename; spot-checked entries show correctly-named fields and a properly truncated `oos_date` sourced from a real API response, not just the retroactive backfill.
- [x] All Strategies' ⚠ badge (already present in `database.html`, previously reading `e.data_warnings` directly) fixed to read `e.flag && e.flag.level === 'caution'` instead, since `data_warnings` no longer exists post-consolidation, this was a live regression introduced and caught/fixed within this same session, not a pre-existing gap
- [x] **Split (v1.11.11):** per user decision, `flag` is no longer an object, it reverted to being just the category string (`"excluded" | "caution" | "retry" | null`), paired with a new sibling field `error` (the original message: a string for script errors, or Composer's `data_warnings` object for `"caution"` rows). `scripts/refresh_full_database.py`'s `classify_error()` now returns a plain string; `apply_backtest_result()` and both failure branches in `main()` set `entry["flag"]`/`entry["error"]` separately. `database.html`'s ⚠ badge updated to `e.flag === 'caution'`. Migrated all 7,685 existing entries by splitting the `{level, reason}` object; counts unchanged (1,004 excluded, 88 caution, 109 retry, 6,484 clean). Tested live against a mixed batch (15 clean rows + 5 known-`excluded` rows, forcing both the success and failure write paths in the same run): verified correct `flag`/`error` shapes on all four cases (clean, 422, 404, caution), zero entries left in the old object shape.
- [x] **Reset (v1.11.12):** per user decision, all 197 `caution`/`retry`-flagged entries had `flag`, `error`, and `refresh_date` reset to `null`, putting them back in the "due" queue for the next `refresh_full_database.py` run rather than spot-checking them individually. `excluded` entries were left untouched at this step.
- [x] **Reordered (v1.11.13):** per user decision, the trailing field order in every entry is now `oos_date`, `refresh_date`, `flag`, `error` (previously `flag`, `refresh_date`, `oos_date`, `error`).
- [x] **Purged (v1.11.14):** per user decision, skipped the hand spot-check and removed all 1,004 `excluded` (404/422) entries from `data/database.json` outright rather than just flagging them for UI exclusion. All 1,004 URLs were confirmed already present in `data/storage.csv` (the durable URL backup) before removal, so nothing is lost, any of them could be re-promoted back into `database.json` unrefreshed via `scripts/sync_storage_to_database.py` later. Built `scripts/purge_flagged_entries.py` (see Operational Runbook, "Purging Flagged Full-Database Entries") as a reusable tool for this and future cleanses, rather than a one-off script, takes one or more `flag` levels as arguments, enforces the storage.csv safety invariant, and regenerates every downstream export in one run. Database now has 6,681 entries (down from 7,685).
- [x] **UI exclusion built (v1.11.15):** `isNoiseFlag(e)` (`e.flag === 'caution' || e.flag === 'excluded'`, deliberately excluding `'retry'` since transient failures aren't noise) now gates default views:
  - **All Strategies**: per user decision (overriding the earlier "keep caution visible, badge only" plan), now defaults to *excluding* flagged rows too, via a 3-state toggle, **Default** (excludes), **All** (shows everything), **Broken** (shows only flagged rows). The ⚠ badge is kept regardless of mode.
  - **Screener**: same 3-state toggle (Default/All/Broken), independent state from All Strategies. **Removed 2026-07-13**: see the dated addendum at the end of this section; Screener is no longer toggleable, always Working-only.
  - **Leaderboard**: per user decision, **not** user-toggleable, always excludes flagged rows from the eligible/scoring pool, no toggle shown. Recomputes scores/tiers from the filtered pool (percentile rank depends on the pool, so this can't just be a post-hoc render filter like the other two tabs).
  - Implemented in `database.html`: `isNoiseFlag()`, `FLAG_MODES`/`FLAG_MODE_LABELS` (`{default: 'Default', all: 'All', flagged: 'Broken'}`), `applyFlagMode()`, `flagToggleHtml()`, plus per-tab `recompute*Entries()`/`recomputeLeaderboard()` functions wired into every filter/sort/toggle interaction path.
  - Verified via a headless-Chrome CDP smoke test (no `chromium-cli`/Playwright available in this environment; drove Chrome's DevTools Protocol directly over its remote-debugging websocket): All Strategies counts moved correctly across all three modes (Default 6,549 / All 6,681 / Broken 132 at test time), Leaderboard confirmed to have zero flag-toggle elements present, Screener toggle confirmed present with the "Broken" label, zero console errors.
- [x] **Screener redesigned (v1.11.15):** per user decision, replaced Screener's hidden Filter Panel (shared component with All Strategies) with an always-visible, Finviz-style bucketed filter grid, one label+dropdown per numeric field (20 fields: all `FILTER_FIELDS` except `holding`, plus a free-text Symphony Name search), laid out in a responsive CSS grid. All Strategies is explicitly unchanged and keeps its existing hidden, specific-value (field/operator/exact-value) Filter Panel, per user decision, the two tabs intentionally have different filter UIs now, not a shared component.
  - Bucket thresholds are **not hardcoded**: `buildBucketOptions()` computes each field's 25th/50th/75th/90th percentile live from the actual loaded dataset once after `dbEntries` loads, so the buckets stay meaningful as the database grows/changes instead of going stale like fixed numbers would.
  - `backtest_days` and `oos_date` (via `oosDaysValue()`) use a `duration` formatter producing natural-language labels (`"Over 11 months"`, `"Over 3.5 years"`) instead of raw day counts, per user request.
  - Verified live via the same CDP harness: selecting "ARR: Over 50%" correctly cut the result count from 6,549 to 3,268; name search for "zoop" correctly returned 119; `oos_date`/`backtest_days` bucket labels read naturally; zero console errors. One real bug caught and fixed during testing: the CSS grid initially rendered as a single stacked column in a screenshot, turned out to be stale browser cache serving pre-edit `main.css`, not a layout bug; confirmed correct multi-column grid once cache was disabled for the test session.

- [x] Part A (name-based noise) implemented v1.11.22, see above, `scripts/flag_name_noise.py`

- [x] **Search + Screener refinements (2026-07-13):**
  - Added a "Search by name..." textbox (`.db-search-input`) to the left of the Filter button on **All Strategies** and **Leaderboard**, filtering by symphony name substring, case-insensitive (Screener already had its own name search inside the bucket grid). All three name-search boxes, including the pre-existing Screener one, now filter **live on every keystroke** instead of requiring Enter or blur, re-rendering the table also recreates the search input itself (same innerHTML-replacement pattern as everything else in this file), which would otherwise steal focus every keystroke; fixed by restoring focus and cursor position immediately after each re-render.
  - **Removed Screener's 3-state flag toggle** (Default/All/Broken, built v1.11.15) entirely, per user decision, Screener is now always Working-only (unflagged, non-duplicate), matching Leaderboard's existing non-toggleable behavior. Only All Strategies still has a toggle (the 4-state Working/Broken/Duplicates/All from Part A above).
  - **Bucket dropdowns expanded** from the original 4-5 sparse options (25th/50th/75th/90th percentile for "higher is better" fields, 75th/50th/25th for "lower is better" fields) to a uniform **9 deciles (10th-90th percentile, 10% steps) + Any = 10 total options**, for all 20 fields regardless of direction, still ordered loosest-to-strictest (e.g. ARR: "Over 10%" → "Over 220%"; Std Deviation: "Under 70%" → "Under 13%"). Verified locally via a headless-Chrome DOM dump confirming exact option counts and ordering on both a "higher" and a "lower" field before shipping.

### V1.15: Full-Scale Refresh

**Status:** Complete. Every entry has been through at least one real API attempt; ongoing maintenance now happens via the weekly `refresh-full-database.yml` workflow (v1.12.0) rather than a one-time push.

- [x] `scripts/refresh_full_database.py --force` launched in the background against all 6,488 entries, populating the full v1.9.1 field set for every row, not just `last_updated`/`script_errors` (started v1.9.4)
- [x] **Race condition found and fixed (v1.11.3):** `refresh_full_database.py` loads `database.json` into memory once at startup and periodically overwrites the whole file with that in-memory copy on every checkpoint. Running `sync_storage_to_database.py` (or `import_full_database.py`, or any other script that writes `database.json`) while a refresh is still running in the background gets silently clobbered on the refresh script's next checkpoint, the sync appeared to succeed (correct file on disk immediately after), then reverted back to the pre-sync state a few checkpoints later. Caught when a routine entry-count check came back wrong; recovered by stopping the running refresh, re-running the sync, and restarting the refresh against the now-correct file. **Operational rule going forward: never run another script that writes `database.json` while a refresh is running in the background; stop it first.**
- [x] Monitor for new failure patterns beyond the original quota error: none found so far, the resumed run (v1.11.4) is producing the same 404/422/429/500/503/timeout shapes as the paused run, no new error type
- [x] **Recovery outcome (final, v1.11.22-23):** of the original 7,685-entry database, 1,004 rows were permanently 404/422-broken and purged (v1.11.14); a further 88 name-pattern-noise rows and 229 near-identical duplicates were flagged (not deleted) rather than counted as "recovered." Final live database: 6,640 entries, 6,221 of them clean with usable metrics. A precise "recovery rate" against the original error set was not separately tracked as its own metric beyond these final counts, the practical outcome (clean vs. flagged vs. purged, and why) is fully captured by the `flag` field breakdown above.
- [x] **Policy decided (v1.11.4)** for rows that fail after a real API attempt, see V1.14 Part B: 404/422 are permanent (flag and exclude from default views, implemented there, not here); 429/500/503/timeout are transient (leave unflagged, let the normal staleness-check retry cycle clear them on a future run)
- [x] Leaderboard, Screener, and the Filter Panel re-verified against the full refreshed (and now deduplicated) dataset throughout V1.14's implementation and testing (v1.11.15-23): all three were live-tested via the CDP harness against real, current data at every step, not just the original partial dataset they were originally built against

### V1.16: Performance Fix (Data Weight)

**Status:** Complete (built ahead of its roadmap slot, per explicit user request, before V1.11-V1.15)

**Correction made during implementation:** the "<500KB" target this item was framed around (Section 10, Performance Targets) is actually scoped to `Total page weight (home)`, the homepage specifically, not database.html. That number never literally bound this page; citing it as a hard constraint on database.html in earlier roadmap entries was a mistake, corrected here rather than silently carried forward. The underlying concern (an oversized payload still hurts load time and the Lighthouse/LCP targets that do apply broadly) was real regardless.

**What was tried and what actually worked:** dropping unused fields alone (`cumulative_return`, `mean`, `min`, `max`, `active_asset_nodes`, `total_costs`, `annualized_turnover`, `herfindahl_index`) only reduced the file by ~26%, most of the weight wasn't any single field, it was JSON format overhead: every one of 6,488 objects repeating full field names as keys, plus indentation whitespace. The real fix: **columnar format** (`{ fields: [...], rows: [[...], ...] }`, field names stored once, not per-entry) combined with **rounding floats to 4 decimal places** (percentages/ratios never need more precision than that in any UI). Net result on the live dataset: ~11.5MB uncompressed → ~2.3MB uncompressed (79.9% reduction), ~540KB gzipped (what a browser actually transfers in production; Cloudflare Pages serves gzip/brotli automatically).

- [x] `scripts/export_summary.py` added: derives `data/database_summary.json` + `.js` from `data/database.json`, columnar layout, 4-decimal float rounding, drops the 8 unused fields listed above
- [x] `database.html` rewired to load `database_summary.json`/`.js` (`window.DATABASE_SUMMARY_DATA`) instead of the full `database.json`/`.js`; a `rowsFromColumnar()` helper reconstructs plain row objects client-side so the rest of the page's code is unaffected by the wire-format change
- [x] Verified end to end: page loads, data renders, size reduction measured and confirmed (see above)
- [ ] Re-measure actual Lighthouse/LCP numbers once the page is live (not yet possible pre-deploy)

### V1.17: Leaderboard Scoring Revision

**Status:** Complete (2026-07-13). Supersedes V1.13's scoring model (that section is left intact above as the historical launch record; this section is the current live methodology).

**Why this happened:** user feedback (2026-07-08) that the V1.13 scoring "isn't as good as I would like it to be," with no specifics initially. Rather than guess, the actual mission was established first: *identify symphonies with the best return and a long backtest, while being relatively safe, with long-term performance*: a narrower, more specific goal than V1.13's original "well-rounded across 20 stats" design. V1.13's real problems against that mission, identified before any rework began:

- Longevity was only 10% of the score (100/1,000), despite "long backtest" being an explicitly named, co-equal requirement.
- Half the model (Asymmetry/Shape + Concentration/Fragility, 200/1,000) was metrics most people don't reason about at all (Skewness, Kurtosis, Tail Ratio, three "top-day contribution" stats), heavily redundant with Max Drawdown/Standard Deviation.
- Four separate risk-adjusted ratios (Sharpe/Calmar/Sortino/Win Rate) mostly measured the same underlying idea from slightly different angles.
- The clamp constant (0.22) was flagged at V1.13 launch for "post-rollout re-evaluation against the actual score distribution at full scale", that re-check never happened.
- S+ required a literal perfect 1,000/1,000, which meant it never fired in practice, confirmed live: even the single best-scoring strategy in the entire 6,225-entry eligible pool topped out around 890-900/1,000, nowhere near a perfect score, because no strategy clears the clamp's full-marks threshold on all 20 metrics simultaneously.

**Process:** rather than rebuild from a blank slate, every metric from V1.13 was individually rated 1.0-10.0 for how directly it serves the stated mission, with a written rationale per rating (self-reviewed once for internal consistency, e.g. Sortino Ratio was initially under-rated relative to Standard Deviation despite being the more mission-aligned metric, since it only penalizes downside volatility rather than symmetric swings; corrected on review). Point weights were then derived proportionally from those importance scores (`points = 1000 × score ÷ sum-of-all-scores`), not from a category-based allocation. Two real strategies (zoop's "TQQQ FOR THE LONG TERM (2026 Edition)" and "Sometimes TQQQ (2026 Edition)") were used as running test cases throughout, same backtest length and `oos_date`, very different Return/Safety profiles, to concretely observe how weight changes actually moved real scores, rather than reasoning about it in the abstract. All candidate models were validated by running them against the live `database_summary.json` (6,225 eligible entries) via a throwaway Python test script mirroring `database.html`'s exact scoring code, output to a reviewable xlsx (url/tier/score), before anything touched the live site.

**Locked scoring model: same 20 metrics as V1.13, reweighted, no categories dropped:**

| Metric | Points | Metric | Points |
|---|---|---|---|
| Annualized Rate of Return | 99 | Top 1-Day Contribution | 43 |
| Max Drawdown | 98 | Skewness | 37 |
| Backtest Days | 97 | 3-Month Trailing Return | 32 |
| Calmar Ratio | 96 | Top 5% Day Contribution | 32 |
| Sharpe Ratio | 85 | Tail Ratio | 27 |
| Sortino Ratio | 75 | OOS Days | 25 |
| 1-Year Trailing Return | 64 | Standard Deviation | 25 |
| Median Period Return | 59 | Top 10% Day Contribution | 21 |
| Win Rate | 48 | 1-Month Trailing Return | 16 |
| | | 2-Week Trailing Return | 11 |
| | | Kurtosis | 10 |

Sums to exactly **1,000**. Same excluded-from-scoring set as V1.13 (`cumulative_return`, `mean`, `min`, `max`, `herfindahl_index`, `total_costs`, `annualized_turnover`): those exclusion reasons were never in question, only the weighting of what's already scored.

**Category regrouping (display only, for the per-row breakdown modal and Methodology modal, doesn't affect scoring math):** V1.13's 7 categories collapsed to 4, matching the mission's actual shape rather than an arbitrary split: **Return** (6 metrics, 281 pts), **Risk-Adjusted / Downside Risk** (6 metrics, 427 pts), **Shape & Concentration** (6 metrics, 170 pts), **Longevity** (2 metrics, 122 pts).

**Clamp constant raised from 0.22 to 0.14.** The clamp's "full marks" threshold is exactly `1 − Q`: V1.13's 0.22 meant anyone at or above the 78th percentile on a metric scored identically, with no reward for being at the 99th vs. the 80th. Tested empirically against the live pool at Q = 0.10 through 0.30: **lower Q raises the full-marks bar and pushes scores down** (Q=0.10 dropped the pool's top score to 867.6); **higher Q lowers that bar and pushes scores up** (Q=0.25 → 903.1 top score, Q=0.30 → 931.4). Landed on **0.14**: meaningfully tighter than V1.13's 0.22 (more differentiation among strong performers) without inflating the whole distribution the way Q=0.25+ started to. Confirmed this reshuffles rank order at the margins, not just score magnitude, as Q moves (different strategies benefit depending on exactly which of their metrics sit in the "almost-but-not-quite full marks" zone): an accepted, expected side effect, not a bug.

**S+ redefined as a real rank cut, not an unreachable perfect score.** New tier cuts: **S+ = top 0.25%**, **S = next 9.75% (top 0.25-10%)**, A = next 10% (10-20%), B = next 30% (20-50%), C = next 25% (50-75%), F = bottom 25%. This carves S+ out of what used to just be "S," rather than shifting every other tier's definition down a notch. Initially set to top 1% (62/6,225 entries), tightened to top 0.25% after launch feedback that 1% produced too many S+ entries, confirmed live: **16 entries land in S+** (≈0.26% of the 6,225 eligible pool) at the final cut.

- [x] `database.html`: `SCORE_METRICS` weights, `CLAMP_Q`, `TIER_CUTS`, `SCORE_CATEGORIES`, and `computeTiers()`'s S+ logic all updated to match
- [x] Methodology modal narrative text rewritten to describe the new mechanics (4 categories, ~14% clamp threshold, S+/S/A/B/C/F rank cuts)
- [x] Verified locally via a headless-Chrome screenshot of the live Leaderboard tab and Methodology modal before pushing, tier distribution (S+ 62 / S 560 / A 623 / B 1,868 / C 1,559 / F 1,553) and top-15 scores matched the validated Python test script exactly
- [x] Eligibility gate unchanged from V1.13 (unflagged + `sharpe_ratio` present, not user-toggleable)

### V1.18: Leaderboard Scoring Revision II (Out-of-Sample Weighting)

**Status:** Not started. Logged 2026-08-25 from a public discussion of the live Leaderboard. This is
the successor to V1.17 and nothing here is decided; it is a specification of the problem, what the
data can and cannot currently support, and the open questions, so the work does not start from a
blank page.

**The trigger.** The owner posted the live Leaderboard publicly on 2026-08-25, describing the scoring
as "a rough draft" that still needs work on "some criteria". A community member (Spacer) responded
with a specific, checkable observation: **a symphony sitting at the top of the Leaderboard has
underperformed SPY across its six months of out-of-sample time.** The owner agreed the OOS weight is
"way too low" and backtest length correspondingly too high, and added that the factor set as a whole
was "kinda just thrown in there" and that the goal is a **simpler** model, closer to the sibling
Individual Stocks screener at `azqato.github.io/stocks/screener.html`.

**What the model does today** (V1.17, live since 2026-07-13, full table above):

| | Points, of 1,000 | Share |
|---|---|---|
| `backtest_days` | 97 | 9.7% |
| OOS days, derived from `oos_date` | 25 | 2.5% |
| Longevity category total | 122 | 12.2% |

So backtest length outweighs out-of-sample length **roughly four to one**, which is the imbalance
being complained about, and the complaint is arithmetically fair.

#### The finding that reframes the request

**The model has no out-of-sample *performance* metric at all, only out-of-sample *duration*.** This
matters more than the weighting, and it should be settled before any weight is touched.

- `oos_date` is **not** an out-of-sample return. It is the symphony's last logic edit, sourced from
  the Composer API's `last_semantic_update_at` and truncated to a date (Section 12). `database.html`
  derives "days since last edit" from it live. The stored quantity is a **date**, and the scored
  quantity is a **day count**.
- Every one of the 29 fields in `data/database_summary.json` was checked. There is no field
  measuring performance since `oos_date`, and **no benchmark of any kind**: SPY appears nowhere in
  the dataset.

**Therefore raising the OOS-days weight would not fix the case that prompted this, and would most
likely make it worse.** The symphony in question has six months of untouched history, which is a
respectable OOS *duration*. Scoring OOS duration harder rewards it further. The actual complaint,
"it underperformed SPY out of sample", is about OOS *return against a benchmark*, and the model
currently cannot express that sentence at all. Reweighting is the wrong lever for the stated problem;
it is a real but separate issue.

#### A cheap first step that uses only fields already present

**Some trailing-return windows are already fully out-of-sample, and nothing exploits that.** If a
symphony's OOS duration is at least 365 days, then `trailing_one_year_return` covers only days after
the last logic edit, so it *is* a true out-of-sample return. The same holds for
`trailing_three_month_return` at 90 days, and so on down the trailing set. The data to identify
which windows qualify is already in every row.

That yields an **OOS-valid trailing return**: pick the longest trailing window that fits entirely
inside the symphony's OOS period, score that, and score nothing where no window qualifies (a hard
zero against the fixed denominator, exactly as the model already treats missing data). It needs no
new API calls, no new fields, and no backtesting.

**Measured against the live pool on 2026-08-25**, over the 6,471 eligible entries (unflagged,
`sharpe_ratio` present):

| OOS duration | Entries | Share | Longest fully-OOS trailing window |
|---|---|---|---|
| 365 days or more | 5,127 | **79.2%** | 1 year |
| 90 to 364 days | 1,126 | 17.4% | 3 months |
| 30 to 89 days | 185 | 2.9% | 1 month |
| Under 30 days | 31 | 0.5% | 2 weeks or less |
| No `oos_date` | 2 | 0.03% | none, scores zero |

So `trailing_one_year_return` is **already a genuine out-of-sample return for four rows in five**,
and some window qualifies for 99.97% of the pool. The cheap step is not only cheap, it applies almost
everywhere.

**That distribution also calibrates Spacer's floor proposal, and warns about the weighting one.**
A one-year OOS floor would exclude about 21% of the pool, which is a real cut but not a drastic one.
It cuts the other way for weighting: since 79% of rows already clear a year, **OOS duration barely
separates the pool at the top**, so weighting duration harder mostly reshuffles rows that all already
look fine on it. More evidence that duration is the wrong quantity to lean on, and OOS *return* is
the one that would actually discriminate.

**It still does not give the benchmark comparison**, which is the other half of what was asked for.
That needs SPY's trailing returns stored alongside, one extra row refreshed on the same weekly
cadence, so the score can ask "did this beat SPY over the window it was actually out of sample for"
rather than "did this go up". Cheap, but a real scope addition and a real decision.

#### Spacer's two proposals, and what each costs

1. **A minimum OOS duration before OOS weight is boosted.** This fits the existing machinery well,
   because it is an **eligibility rule, not a weighting change**, and the model already has an
   eligibility gate (unflagged, `sharpe_ratio` present). A floor such as "no S+ or S tier without N
   days of OOS" is expressible today with no change to the point table at all.

2. **Dynamic scaling, where OOS weight rises with OOS length.** Attractive, and it **conflicts with a
   load-bearing property of the current model**, so it cannot be dropped in unexamined. Every metric
   has a fixed cap and the caps sum to exactly 1,000, which is what makes two rows' scores
   comparable and what lets missing data score zero without shrinking the denominator. A weight that
   varies per row means a denominator that varies per row, and scores stop being comparable across
   rows. Two ways out, both worth costing before choosing: renormalise every row back to 1,000 after
   applying its own weights (comparable again, but a row's score then depends on its own weighting,
   which is hard to explain in the breakdown modal), or keep the cap fixed and vary the *input*
   instead, for example by scoring a confidence-adjusted OOS return that already carries the
   duration inside it. **The second is the smaller change and preserves the fixed denominator**,
   which is the recommendation to evaluate first.

3. **Spacer proposed "or both", and both is coherent**: the floor decides who is eligible for the
   reward, the scaling decides how much of it they get. If only one is built, the floor is the
   cheaper and the more explainable.

#### The simplification strand, which is a separate decision

The owner also wants the model **simpler**, in the direction of the Individual Stocks screener. That
is a different axis from OOS weighting and the two should not be conflated in one pass. Worth
recording that V1.17 already went through this exercise once, cutting 7 categories to 4 for display
while keeping all 20 metrics scored, and that its own analysis found the Asymmetry/Shape and
Concentration/Fragility groups (six metrics, 170 points) to be the least mission-aligned and most
redundant with Max Drawdown and Standard Deviation. **That is the obvious place to cut**, and it is
already documented above with reasons, so the simplification does not need to be re-derived.

#### Design session 2026-09-03: what was decided, and the finding that reframes this a second time

Three decisions are taken and one is deliberately parked. Everything in this subsection was measured
against the live pool of **6,681 eligible rows** rather than reasoned about, by
`scripts/analyze_leaderboard.py`, which mirrors `database.html`'s engine exactly (clamp constant,
average-rank ties, fixed denominator, tier cuts), so every number here is a number the site would
show. It is manual-only and read-only, and it exists so these figures can be re-derived rather than
trusted, and re-run once the model shape is settled. Figures below are its 2026-09-03 output; the
pool drifts by a row or two a day as the weekly refresh lands.

**Decided: out-of-sample statistics come from the API, windowed, not from a trailing-window proxy.**
The section above proposed inferring an out-of-sample return from whichever trailing window happens
to fit inside the OOS period. That was the right idea given what was known on 2026-08-25 and it is
now superseded, because **the Composer backtest endpoint accepts a date range and requires no key.**

- `scripts/refresh_full_database.py` has always posted to
  `api.composer.trade/api/v0.1/symphonies/{id}/backtest` with **no auth header at all**. What it
  never did was pass a date range.
- **`start_date` and `end_date` are honoured.** Passing `start_date` equal to the symphony's
  `oos_date` returns all 27 stats computed on out-of-sample days only: a genuine OOS annualized
  return, max drawdown, standard deviation, Sharpe, Sortino, Calmar and cumulative return, over the
  symphony's actual untouched period. Verified live on three symphonies of differing OOS length,
  **no nulls in any of the 27 fields**, roughly one second per call, and the start date snaps
  forward to the next trading day on its own.

  | Symphony | OOS span | Trading days | OOS return | SPY, same span | Excess |
  |---|---|---|---|---|---|
  | zoop's 2026 Frontrunner | 2026-03-16 to 2026-09-03 | 119 | +17.79% | +15.87% | +1.92pp |
  | `xvgru5wD...` | 2023-03-17 to 2026-09-03 | 869 | +137.52% | +106.00% | +31.52pp |
  | `U9QE6NXD...` | 2025-09-29 to 2026-09-03 | 234 | +17.97% | +17.15% | +0.82pp |

**Decided: the benchmark is already in the repo, so it costs nothing.** The section above records
that "SPY appears nowhere in the dataset" and treats storing a benchmark as a real scope addition.
That is true of `database_summary.json` only. **`data/prices.json` carries SPY daily closes from
2010-01-04**, refreshed weekly by `.github/workflows/refresh-prices.yml` for the Signal
Miner, and the site already ships it. No new API, no new field, no new cadence. One alignment rule
falls out of this: the API runs through today while `prices.json` ends at the last price refresh,
so the OOS request must pass **`end_date` equal to the last date in `prices.json`** and land both
sides on the same day. (The price job moved to Friday evening on 2026-09-06 so that this lag is two
days rather than a week; see "The weekly data pipeline" in Section 4.)

**Decided (owner, 2026-09-03): rows under a year of OOS time are percentiled within their duration
group,** rather than annualised or excluded. A symphony with 120 untouched days is ranked against
others with roughly 120, not against one with 900. This makes no annualisation claim and needs no
arithmetic anyone can dispute, and it preserves the percentile logic the rest of the model already
uses. The alternative measured badly: annualising the excess triples the apparent severity of the
short-window group, from a median of -2.35pp to **-9.91pp**, purely from compounding noise.

**Decided (owner, 2026-09-03): a 365-day OOS floor gates S+ and S.** Spacer's proposal, adopted
as an **eligibility rule rather than a weighting change**, so it needs no change to the point table
and cannot break the fixed denominator. It cuts about 22% of the pool out of the top two tiers;
those rows can still reach A. With true OOS statistics rather than a trailing proxy, the floor is
now about statistical confidence rather than data availability, which is a better thing for it to
be about.

**Parked: the model shape.** The owner asked for time to digest the six-metric proposal. Note that
the proposal needs reworking regardless, because with true OOS statistics the out-of-sample pillar
can carry its own return, drawdown and duration rather than a single excess number, which is a
different and better shape than the one put forward.

##### The delivery mechanism: a separate workflow, scoped to a derived candidate set

**The constraint is time, not money.** `.github/workflows/refresh-full-database.yml` already runs
4.5 to 5 hours against GitHub's 6-hour job ceiling, with a 340-minute step cap and deliberate
checkpoint-and-resume handling because it runs that close to the edge. A second API call per row
roughly doubles it and does not fit. Three ways out were costed; **the owner chose the first two
together (2026-09-03)**:

1. **A separate weekly workflow** writing `data/oos.json` and its `.js` twin, keyed by symphony id,
   on a different day from the full refresh. The existing job is not touched.
2. **Scoped to a candidate set** rather than the whole pool, which is what makes the separate job
   short instead of merely parallel.
3. Rejected: cutting the 2-second throttle. Calls take about one second, so the throttle is a
   politeness margin rather than a measured limit, and establishing otherwise means deliberately
   probing someone else's rate limiter.

**The candidate set is derived from the pillar's own weight, not chosen.** This is the part that
makes scoping safe rather than arbitrary. A row with no OOS data scores **zero** on the OOS pillar,
which is not a new mechanism: it is the rule the model already publishes for missing data anywhere,
that the denominator never shrinks so an incomplete strategy can never outscore a complete one by
having fewer things to fail. Because a missing pillar scores zero and a present one scores at least
zero, **fetching OOS data can only raise a row's score, never lower it.** So a row whose in-sample
score sits more than the pillar's full weight below the current cutoff for rank *D* mathematically
cannot enter the top *D* even with a perfect OOS record, and there is no reason to spend a call on
it. Measured against the live pool:

| Protect the top | OOS pillar worth | Score cutoff | Candidates | Share of pool |
|---|---|---|---|---|
| 100 | 150 | 668.6 | 1,512 | 22.6% |
| 100 | 250 | 568.6 | 2,590 | 38.8% |
| 250 | 250 | 542.6 | 2,878 | **43.1%** |
| 500 | 250 | 509.8 | 3,226 | 48.3% |

At a quarter of the scale for the OOS pillar and the top 250 protected, that is 2,878 calls, roughly
**1.6 hours** at the existing 2-second throttle. Comfortable inside a single job with room for the
pool to grow. The exact figures will move once the model shape is settled, but the *rule* for
setting them does not.

**What this design does and does not claim.** The leaderboard becomes a two-stage screen: a cheap
in-sample pass over the whole pool narrows the field, and an expensive out-of-sample pass confirms
or demotes. This is the same shape the Signal Miner roadmap uses for plateau scoring and
walk-forward (V2.2 items A and B), and it has the same property, worth stating plainly rather than
discovering: **the out-of-sample stage can demote a row but cannot promote one from nowhere.** A
symphony with mediocre in-sample statistics and a spectacular out-of-sample record will not be
found. The derived cutoff bounds that blindness exactly rather than hand-waving at it: nothing
outside the candidate set could have reached the protected ranks anyway.

##### The failure mode this must be gated against

**`start` and `end` are silently ignored.** Only `start_date` and `end_date` are honoured; the
shorter names return the full backtest with a 200 and no warning of any kind. A refresh script that
used the wrong key would appear to work perfectly and would quietly publish **in-sample numbers
labelled out-of-sample**, which is the worst outcome this whole item could produce, since it would
make the leaderboard look validated precisely where it is not.

The gate is cheap: the response carries `first_day` as an epoch day number, so
**assert that it equals the requested start date and discard the row otherwise.** That converts a
silent catastrophe into a loud, per-row failure. It belongs in the refresh script itself rather than
in a deploy gate, because by deploy time the wrong numbers are indistinguishable from right ones.

#### Shipped shape, 2026-09-06: two models, both permanent

The model shape parked on 2026-09-03 was settled by the owner on 2026-09-06, and it settled in a way
the spec did not anticipate: **not one revised model, but two, side by side, permanently.**

**Owner decision: both models stay indefinitely, with no transition label on either.** The Leaderboard
carries a toggle. Simplified is the default and the canonical one; Advanced is the existing 20-metric
1,000-point model, unchanged in every weight. Neither is framed as superseding the other, and there is
no "beta", "new" or "legacy" badge anywhere, because the owner has not decided whether either will be
retired and a label would announce a decision that has not been taken.

**The Simplified model.** Five metrics, 100 points.

| Pillar | Points | Metrics |
|---|---|---|
| Out of sample | 35 | Excess return over SPY, 35 |
| Return | 25 | Annualized Rate of Return, 25 |
| Risk | 25 | Max Drawdown 15, Standard Deviation 10 |
| Track record | 15 | Backtest Days, 15 |

Everything else in the engine is untouched: the same 0.14 clamp, the same average-rank tie handling,
the same fixed denominator so missing data scores a hard zero, the same rank-based tier cuts.

**Duration is not scored.** It decides eligibility and grouping only. This was a deliberate reversal
of the draft: the 2026-08-25 spec treats OOS days as a metric worth 25 points in the Advanced model,
and repeating that in a model whose whole argument is out-of-sample evidence would pay twice for the
same fact. So the Simplified model spends nothing on duration and instead uses it twice as a rule:
rows are percentiled **within** duration groups (90-364, 365-729, 730+), and S+ and S require 365 days.

**Rejected on measurement, not taste: splitting the OOS pillar 15 excess / 10 OOS max drawdown.**
That was the draft-1 proposal and it was wrong. Measured correlation between out-of-sample max
drawdown and in-sample max drawdown is **+0.901**, which is precisely the double-counting this
revision exists to remove. All 35 points go to excess return.

**The 90-day measurement floor.** `MIN_OOS_DAYS` in `scripts/refresh_oos.py` was raised from 30 to 90
on 2026-09-06. A four-week record is too thin to hang 35 of 100 points on, it was the noisiest
duration group by a distance, and such rows cannot clear the 365-day tier floor in any case. They
score zero on the pillar, which is what the model already does with missing data everywhere else.

**What the toggle does not do.** It is a Leaderboard view, not a site mode. The Screener's Rank, Score
and Tier columns, its "or better" tier filter, and the strategy pages all read the **Simplified** model
and only that one, so a symphony's rank means one thing wherever it is quoted. Both models are scored
up front on the same pool in `recomputeGlobalRanking`, so switching is a re-render, never a re-score.

**A disagreement view ships with it.** A "Model diff" button lists the strategies whose ranks move
most between the two models, restricted to rows reaching the top 500 of either. Two models that agreed
everywhere would not be worth carrying two of, and this is the view that says what the second one buys.

#### The tie question, answered by measurement 2026-09-07

The design session predicted that a five-metric model would leave the top of the table full of shared
scores, and that the 35-point excess metric would break most of them. **Both halves of that were
wrong, and the real cause was somewhere else entirely.**

Against the full 3,175-row dataset, 59 of the top 100 shared a score. But the page was sorting on the
score it *displays*, rounded to one decimal, rather than the score it *computes*. Ranking on the
unrounded total instead drops that to **14 of the top 100**, with no change to any weight, cut or
rule:

| | top 20 | top 100 | top 500 |
|---|---|---|---|
| Ties when sorting on the rounded score | 8 | 59 | 396 |
| Ties when sorting on the real score | 2 | **14** | 101 |

**And the residual ties should not be broken.** Every one of the 14 is a near-duplicate: the same
strategy re-uploaded under a different name, so it carries identical statistics and earns an
identical score. "Copy of Hedged Sector Rotator w/cs" and "JM465 - Copy of Copy of Hedged Sector
Rotator", "DeETF FTLT | 2013-01-09" and "TESTPORT #179: DeETF FTLT | 2013-01-09". Ordering those
against each other would be arbitrary noise presented as a judgement.

**So no published tie-break rule ships**, which is the outcome to prefer: a rule that fires only on
copies of the same strategy would add a paragraph of methodology to explain a distinction that does
not exist. The lesson worth keeping is more general than this item, and is the reason it is recorded
here rather than in a commit message alone: **a leaderboard that sorts on a rounded number is
inventing ties it then has to explain.** Round for display, rank on what you computed.

The remaining duplicate-detection question, that these copies are not caught by the `duplicate` flag
because they are separate `symphony_id`s with different names, is a pre-existing dedupe concern and
is deliberately out of scope here.

#### What the first full run actually measured

| | |
|---|---|
| Rows with an out-of-sample record | 3,175 of 6,676 eligible (47.6%) |
| By duration group | 616 at 90-364 days, 905 at 365-729, 1,654 at 730+ |
| Candidates that returned nothing | 94 of 3,267, about 2.9%, retried on the next run |
| Demoted to A by the 365-day floor, inside the top 10% | 112 |
| Tier counts | S+ 16, S 540, A 779, B 2,003, C 1,669, F 1,669 |
| Rank correlation between the two models | +0.816 across the pool |
| Of the 845 rows reaching either model's top 500 | only 51, 6%, land within 50 places of each other |

That last row is the one that justifies carrying two models rather than one. The two agree broadly
across the whole pool and disagree almost completely at the top, which is exactly where anyone
actually looks. The Advanced model's number one has 180 days out of sample; the Simplified model's
has 619 days and a +104pp record against SPY.

#### Open questions to settle before building

1. ~~Is the target OOS *return*, OOS *return against SPY*, or both?~~ **Overtaken by the API
   finding above.** With a windowed backtest the question is no longer which single number to
   derive, but which of the 27 out-of-sample statistics the OOS pillar spends its weight on. That
   is part of the parked model-shape decision.
2. ~~Does SPY (or another benchmark) get stored in the dataset?~~ **Settled 2026-09-03: it already
   is,** in `data/prices.json`, refreshed weekly for the Signal Miner.
3. ~~Floor, dynamic scaling, or both~~ **Settled 2026-09-03: the floor, at 365 days, gating S+ and
   S.** Dynamic scaling is not being built; percentile-within-duration-group achieves the same end
   without a per-row denominator.
4. Does the metric count come down in the same pass, or a later one? Doing both at once makes it
   impossible to attribute a rank change to either. **Still open, and now cheaper to resolve:** the
   validation script below can score the intermediate models and attribute each rank change to the
   stage that caused it, so one shipping pass does not have to mean one analytical step.
5. **How is the change validated?** V1.17 set a good precedent worth repeating: score candidate
   models against the live pool in a throwaway Python script mirroring `database.html` exactly,
   review the output as a spreadsheet, and only then touch the site. The specific symphony Spacer
   named should be one of the named test cases, the way two of the owner's own symphonies were at
   V1.17.

- [x] Decide questions 1 to 3 above (2026-09-03); question 4 remains open
- [x] ~~Add an OOS-valid trailing return~~ superseded: fetch true OOS statistics from the API with
  `start_date` = `oos_date`
- [x] Decide on and, if adopted, add a stored benchmark: SPY, already present in `data/prices.json`
- [ ] **Decide the model shape** (parked at the owner's request, 2026-09-03). Everything below
  depends on it, because the pillar weight sets the candidate-set cutoff
- [ ] `scripts/refresh_oos.py`, writing `data/oos.json` and its `.js` twin, with the `first_day`
  assertion, checkpointing and resume behaviour mirroring `refresh_full_database.py`
- [x] `.github/workflows/refresh-oos.yml`, weekly, Monday 03:07 UTC (Sunday 8:07pm Pacific), the
  last link in the prices/full-database/out-of-sample chain so both of its inputs are fresh when it
  runs. See "The weekly data pipeline" in Section 4
- [x] Rework the scoring model in `database.html`: two models behind a toggle, model-aware breakdown
  and Methodology modals, and a Model diff view (2026-09-06)
- [x] Ship: the first complete run landed 2026-09-07 01:02 UTC, 3,175 rows
- [x] Re-validate against the live pool before shipping (2026-09-07)
- [x] Settle the tie question with full data (2026-09-07). See below: the prediction was wrong, the
  cause was rounding rather than the model, and no tie-break rule is needed

### V1.19: K1 Lookup

**Status:** Shipped and complete (v1.27.0, closed out at v1.27.9). Every item below is done.

**What it is.** `k1.html` answers a single question for a single ticker: **does holding this issue
you a Schedule K-1 instead of a 1099?** It matters because a K-1 arrives late, often after the April
filing deadline, complicates a return, and can produce taxable income in a year the holder sold
nothing. Composer symphonies route into leveraged and inverse volatility products constantly, and
those are exactly the funds that do this.

**It replaces a manual spreadsheet.** The owner kept an 88-ticker sheet, checking each fund's page by
hand and recording Yes or No. That sheet is the origin of the database and its 88 rows were the first
thing loaded into it. The file itself was removed once the database carried everything it held.

**The signal is legal structure, not a published K-1 flag.** No source publishes the flag directly.
`Structure` on the fund page does determine it: Commodity Pool means K-1, ETF and UIT mean 1099, ETN
means 1099-B, Grantor Trust means 1099-B at the collectibles rate. A second, independent field
corroborates every row: the max short and long-term capital gains rates fall out of the structure
rather than being copied from it, so 27.84/27.84 is the Section 1256 blend that only commodity pools
get. Where the two readings contradict, the row is marked `agrees: false` and the page says so
rather than picking a winner. See Section 13.

**The lookup is local, and it had to be.** The upstream source sits behind bot mitigation and sends
no CORS header, so no browser and no public relay can read it from the page. `scripts/refresh_k1.py`
fetches on a maintainer's machine and the site ships the answers, which is also why the page is
instant and works offline.

- [x] `scripts/refresh_k1.py`, `data/k1.json` and its `.js` twin, seeded from `data/k1_seed.txt`
- [x] `k1.html`, nav, footer, homepage card, `check_live.py` coverage
- [x] Independent verification of a sample against sources the script does not use
- [x] **Display whether the ETF is an ETN (v1.27.9).** Requested by the owner 2026-08-27,
  shipped 2026-08-28. No new fetching: `structure` was already in the database, and `ETN` is one of
  its six values. **Six of the 187 rows are ETNs:** FNGD, FNGU, GDXD, GDXU, VXX and VXZ, which are
  among the most heavily traded tickers the site touches. GDXD and GDXU are held by a featured
  symphony today.

  Three surfaces, deliberately different in weight:

  1. **A blue callout on the answer panel** (`.k1-etn`), shown whenever `structure` is `ETN`,
     including for live unverified lookups since `classifyLive` parses the same field. It states
     that no assets are held on the holder's behalf, that the holder is an unsecured creditor of the
     issuing bank rather than an owner of securities, and that the issuer may call the note, suspend
     issuance, or delist it, at which point the note can trade away from the index and stay there.
  2. **An `ETN` tag** on the ticker cell in the fund table, so the fact is visible when scanning
     rather than only after a lookup.
  3. **An `ETN` filter pill**, which cuts across the K-1 axis rather than sitting beside it: every
     ETN is also a "No", so the filter narrows that list rather than adding a fourth state. The CSV
     export follows the filter and names the file `...-etn-<date>.csv`.

  **The callout is quieter than `.k1-warn` on purpose.** Pink means the answer on the page may be
  wrong; blue means the answer is right and a different risk sits beside it. Styling both the same
  would teach a reader to skim both. The count in the explainer paragraph is written from
  `DB.tickers` at render time rather than typed, so it cannot go stale when the refresh script adds
  an ETN

### V1.20: Strategy Page Rebuild

**Status:** In progress. Specified and approved 2026-08-28. **Items 1, 4, 5 and 7 shipped in
v1.28.0**, item 17 in v1.27.8, and **items 2, 3, 8 and 12 in v1.30.0**, which is steps 1, 2 and 3 of
the sequencing below complete. **Step 4 (items 6 then 9) is next.**

**Items 13, 14 and 15 were piloted on a single strategy (v1.29.0 to v1.29.3), out of sequence, at
the owner's request**, and are now **complete on all 24 visible strategies (v1.43.0 to v1.68.0,
2026-09-02)**. `gold-miner-original` was the pilot; the item 19 gate was cleared when the layout was
approved in v1.43.0, and the remaining 23 pages were then written one per commit. The 12 hidden zoop
2026 editions are out of scope by design and carry the unlisted banner instead.

**The pilot-first instruction earned its place.** Two section moves came out of the first review
(v1.29.1, v1.29.3) before the structure was approved, which is exactly the rework that writing 24
pages against an unreviewed shape would have multiplied.

**What going out of order actually costs.** The sequencing put items 10 and 11 before Tier 3 because
they are schema changes and rewriting fresh prose is waste. That risk is **smaller than it looks for
these three**, because 13, 14 and 15 introduce their own new fields (`tldr`, `assumptions`,
`regimes`) rather than editing `risk_profile` or `signals`, so item 10 cannot invalidate them by
changing a shape they do not use. **The real exposure is overlap, not rework:** item 10 splits
`risk_profile` into named categories including Whipsaw and Signal, and the pilot's Struggles-in
column and regime table now say some of the same things in better form. When item 10 is done, the
question will be what `risk_profile` is still for, not how to migrate it.

**Origin.** The owner shared a third-party Composer strategy analysis page and asked what could be
taken from it. The analysis that followed is summarised here rather than in a chat log, because the
half of it that matters is the data audit, not the design admiration. **The screenshot is a source
of structure, not of palette:** it is a light editorial print-style page and this site is dark
(the base was `#0d0d0d` when this was written, `#16191f` since v1.82.0). What is worth copying is how it organises information, and specifically that it turns
prose into structures that force an author to name failure modes.

**Where each item came from.** The owner asked for both the screenshot's sections and any missing
ones worth adding beyond it, so the two are mixed together in the tiers below. This table keeps them
separable, because "we took this from a page we admired" and "we found this in our own data" are
different claims and only one of them is checkable against the source.

| # | Item | Origin |
|---|---|---|
| 1 | Build-time database join | **Ours.** Infrastructure, not a section. Nothing in the source implies it |
| 2 | Hero metric strip | **Screenshot** |
| 3 | Secondary metric grid | **Screenshot** |
| 4 | Outlier-dependence disclosure | **Ours.** From Section 14's C3 spec, which already argued for this test on mined signals, plus three fields sitting unused in `database.json` |
| 5 | Out-of-sample panel | **Ours.** `oos_date` is a Composer field the source page has no equivalent of |
| 6 | Assets tab | **Screenshot** |
| 7 | K-1 warning line, cross-linked to `/k1` | **Ours.** The one item nothing else could produce: it needs the v1.19 K-1 database, which is this site's own work |
| 8 | Provenance chip | **Ours** |
| 9 | Backtest-window explainer | **Ours, and an inversion of the screenshot.** The source shows real against simulated history; that distinction was measured and does not apply here, so this states why a window is short instead. See "Deliberately not copied" below |
| 10 | Split `risk_profile` into categories | **Screenshot**, for the grouping (Leverage and Structural, Whipsaw and Signal, Hedge, Concentration) |
| 11 | Signal Types table | **Screenshot**, including the `x2` badge for repeated signals |
| 12 | Glossary links on metric labels | **Ours.** The glossary is this site's; the source has nothing to link to |
| 13 | TL;DR card | **Screenshot** |
| 14 | Underlying Assumptions | **Screenshot** |
| 15 | Market Regime Analysis | **Screenshot**, including the example-period column |
| 16 | Store per-strategy daily returns | **Ours.** A pipeline change, and the only way item 15 scales past a curated 31 |
| 17 | Distribution metrics mislabeled | **Ours.** A live correctness bug found while auditing the data for the items above, not a feature from either source |
| 18 | Mobile horizontal overflow | **Ours.** Pre-existing, found while measuring the v1.28.0 work |
| 19 | Structure sign-off gate | **Owner.** Added 2026-08-28 after reviewing the pilot. Not a section and not a bug: a hold point |

**Eight of the nineteen came from the screenshot** (2, 3, 6, 10, 11, 13, 14, 15). **Ten came out of
auditing this site's own data** (1, 4, 5, 7, 8, 9, 12, 16, 17, 18), and two of those, items 17 and
18, are bugs rather than features. **Item 19 is the owner's**, added after seeing the pilot. **The single most differentiating item on the list,
item 7, is one the source page could not have suggested**, because it depends on a K-1 database this
project built.

**The finding that shapes the whole phase: the data is already here.** All 31 featured strategies in
`data/strategies.json` join cleanly to `data/database.json` on `symphony_id`, with zero misses. That
join exposes **20 fields the strategy pages have never shown**, including `sortino_ratio`,
`win_rate`, `skewness`, `kurtosis`, `tail_ratio`, the three `top_*_contribution` outlier fields,
`herfindahl_index`, `annualized_turnover`, `total_costs`, `last_market_days_holdings` and
`oos_date`. **Nine of the seventeen items below need no new writing and no new fetching at all**,
which is why the sequencing puts them first.

**Three of those fields are strong content on their own:**

- **Outlier dependence is already computed and never displayed.** For `zoops-holy-grail-2026` the
  best 5% of days produced **137.5%** of total return. Above 100% means that without those days the
  strategy is a net loser. Section 14's C3 write-up already argues for exactly this test on mined
  signals and even specifies the phrasing; the featured strategies have had the number sitting in
  the file the whole time.
- **`oos_date` makes a real out-of-sample claim possible.** It records the last logic edit, so
  days-since is genuine out-of-sample time. `holy-grail` has been unchanged for **1,500 days**
  while the 2026 zoop editions sit at **165 to 214**. That is a quality difference between
  strategies that the pages currently hide entirely.
- **Turnover is extreme and undisclosed:** 23x to 75x annually across the featured set, with
  `total_costs` beside it. A backtest that models no spread overstates a 75x strategy far more than
  a 5x one, so this is a direct qualifier on every headline number on the page.

**The cross-link nothing else can make.** Joining holdings against the v1.19 K-1 database shows
**12 of the 31 featured strategies currently hold a fund that issues a Schedule K-1**:
`s90-half-low-catch` (AGQ, ZSL, UGL, GLL, VIXY, UVXY), `four-horsemen` (SCO, SVXY, UUP, VIXY,
UVXY), `super-semiconductors` (UUP, VIXY, UVXY), `simons-kmlm-switcher` (SVIX, UVXY),
`spy-energy-chips` (DBC, VIXM), `nancy-pelosi-chips` (DBC), and six more holding UVXY. This is a tax
fact about a real holding that Composer itself does not surface, and it is computable today from two
files already in the repo.

---

**Tier 1: free. The data exists, the work is joining and rendering it.**

- [x] **1. Join the featured strategies to `database.json` at build time (v1.28.0).**
  `scripts/build_strategy_extras.py` writes `data/strategy_extras.json` and its `.js` twin, keyed by
  slug, at **31 KB against the 5 MB `database.json` a browser join would have cost**. It carries 13
  database fields plus the resolved holdings, so items 2, 3, 6 and 8 need no further build work.

  **It fails loudly on a miss, and that was tested rather than assumed.** A join miss raises
  `SystemExit` naming every affected slug. Verified by faking two bad `symphony_id` values and
  confirming the raise. `scripts/check_strategy_extras.py` is a fourth deploy gate: it rebuilds the
  join in memory and demands byte equality with both committed files, which catches a stale join, a
  twin that drifted, and a featured strategy with no database row. Verified in both directions.

  **Wired into both refresh workflows as of v1.31.1, revising the v1.28.0 decision.** The original
  call was to keep the rebuild out of `update-metrics.yml`, on the reasoning that a join miss should
  fail the person who caused it, at their desk, rather than break the nightly metrics job and its
  sitemap commit for everyone. That reasoning was sound for the failure it imagined and blind to the
  one that actually happened.

  A join **miss** is a human configuration error: a featured strategy with no database row. A **stale
  join** is something else entirely, and it has no person at any desk. `refresh-full-database.yml`
  rewrites `database.json` every Sunday and `update-metrics.yml` rewrites `strategies.json` every
  night, both unattended, both legitimately changing values the join depends on. Neither rebuilt it.
  So the automated jobs manufactured the exact staleness the fourth deploy gate exists to catch, and
  the gate then blocked the deploy for everyone anyway, which is the outcome the original decision
  was trying to avoid, arrived at by the one route it did not consider.

  This happened for real on **2026-08-30**: the weekly refresh landed as `e2dc066` and left
  `check_strategy_extras.py` failing on `main`, which fails `deploy.yml` before it builds. It was
  caught by hand during unrelated documentation work, not by anything designed to catch it.

  **A third workflow joined them in v1.42.1: `refresh-prices.yml`.** The join began reading
  `data/prices.json` in that version, for the SPY best-days baseline, so the weekly Saturday price
  commit would otherwise have left the extras stale against a fresh join until the daily metrics job
  rebuilt them that evening: a roughly 13-hour window in which any deploy fails. It follows
  `update-metrics.yml`'s philosophy, rebuilding before the commit step with no `if: always()`.

  All three workflows now run `build_strategy_extras.py` and commit its two outputs. The original intent
  is preserved rather than discarded, and each workflow keeps its own failure philosophy:
  `update-metrics.yml` runs the rebuild **before** its commit step with no `if: always()`, so a
  genuine join miss stops the job and ships nothing (loud, and the next daily run retries);
  `refresh-full-database.yml` runs it with `if: always()`, matching the surrounding steps, so a join
  miss turns the job red without discarding hours of checkpointed refresh progress.

  **`k1.json` is the remaining hole, and it is deliberate.** It is the third join input and no
  workflow touches it, because `refresh_k1.py` is hand-run. That path still depends on remembering,
  exactly like the manual `database.json` routes described in risk 5. The deploy gate is the backstop
  for both.

  **One correction the join forced.** The keys of `last_market_days_holdings` are the ticker
  universe the logic can reach; the values are the current position, and most are `0.0`. So the
  pages say a strategy **can hold** a ticker, not that it does. Of the 14 strategies holding a K-1
  issuer or an ETN, only 2 hold one as of the last market day, so "holds" would have been wrong 12
  times out of 14.
- [x] **2. Hero metric strip above the fold (v1.30.0).** Annualized return, max drawdown, Sharpe
  and backtest period, as four tiles directly under the description and above the Open in Composer
  button. Two columns on a phone, four from 720px.

  **The complaint it fixes was structural, not decorative.** The metrics table is sidebar-only on
  desktop and rendered below every prose section on mobile, so the first thing a phone visitor saw
  was three paragraphs and no numbers. The tiles read from `strategies.json`, which every strategy
  has, so this section is not guarded: it is the one part of V1.20 that renders identically whether
  or not the build-time join loaded.
- [x] **3. Secondary metric grid (v1.30.0).** Seven tiles under a Deeper Metrics heading: Sortino,
  win rate, tail ratio, skewness, kurtosis, Herfindahl index and annualized turnover. Every label
  links to the glossary per item 12, and every tile carries a one-line plain-language gloss so the
  grid is legible without following a link. Two columns on a phone, three from 640px, four from
  1180px.

  **Total costs was specified here and is deliberately not shown.** It is cumulative dollars on an
  unstated notional: the figures run from $19,866 to $13.2 billion across the 31, and dividing by
  `cumulative_return` gives a ratio spanning 7.3 to 3,493, so no field on this site supplies a
  denominator that would make one strategy's costs comparable to another's. It stays carried in the
  join, ready if a notional is ever recorded. The grid says this in a note rather than omitting it
  silently.

  **The Herfindahl index does not describe today's position, and the note says so.** Checked against
  `last_market_days_holdings`: `super-semiconductors` stores 0.641 while its current holding is SMH
  alone, which is 1.00. It arrives with the backtest statistics, alongside Sortino and turnover, so
  it describes the backtest. Labelling it as current concentration would have been wrong on at least
  4 of the 31.
- [x] **4a. Fixed in v1.43.0.** The Outlier dependence panel read as a strategy-specific warning
  for a number that is normal for any volatile series. The card is now **"Reliance on its best
  days", benchmarked against SPY over the same window**, and the `warn` colour and the "net loser"
  sentence are gone from every page. Raised by the owner 2026-09-02, confirmed by measurement the
  same day. The card prints
  `top_five_percent_day_contribution` and, above 100%, warns "the other 95% of days lost money on
  net: remove those days and this strategy is a net loser". That sentence is arithmetically true
  and materially misleading, because the denominator is **net** return, which is a small residual
  of much larger gross gains and losses.

  Computing the same statistic on plain buy-and-hold price series from `data/prices.json`:

  | Series | Best 5% of days, as a share of net return |
  | --- | --- |
  | **SPY** | **202.5%** |
  | QQQ | 188.6% |
  | XLP | 222.9% |
  | GLD | 311.9% |
  | TLT | 729.2% |

  For SPY the up days sum to +1,624%, the down days to -1,379%, and the net is +245%. The best 5%
  of days are +497%, which is 202% of that net. Nothing about SPY is outlier-dependent; the ratio
  is just large whenever a small net sits under a large gross.

  **The library's range is 73% to 263%, so nearly every curated strategy scores BETTER than
  buy-and-hold SPY on this measure, while 28 of 36 carry the red `warn` treatment.** The panel is
  currently telling readers that most of the library is a net loser without its best days, using a
  threshold that plain SPY also fails.

  **A true statement that reliably produces a false impression is not "stated as arithmetic and
  left that way"; it is the same failure mode as the recited statistics, one level up.**

  **CLOSED 2026-09-02 in v1.43.0.** Piloted on `gold-miner-original` in v1.42.1, approved by the
  owner, and rolled out to all 36 strategy pages. `isLayoutPilot` and every pre-pilot branch are
  deleted, so there is one renderer again. Verified by rendering all 36 pages in headless Edge and
  asserting the shape on each: 33 benchmarked (4 above SPY, 29 below) and 3 with no baseline.
  Details of the decision, unchanged from when it was made: The owner considered
  deleting the panel outright, which was defensible: the metric is broken at the root, and the
  correct replacement is a roadmap item rather than a rewording. It was kept because the spread at
  the tail is real information (`rains-unified-best-signals` at 73% against `nancy-pelosi-chips` at
  263% is a genuine difference in how concentrated a return is), and because removing a disclosure
  in the same week it was found to read favourably is the wrong instinct to build in. Four changes:

  1. **Benchmark, not threshold.** The headline number becomes the strategy against SPY over the
     same window: gold miner reads **46%**, "a little under half as reliant on its best days as the
     index", instead of a bare 87% that a reader cannot place. `build_strategy_extras.py` computes
     the baseline from `data/prices.json`, matched per strategy to its own `backtest_days`.
  2. **One card shape in both directions, only the body sentence differs.** The first pass gave
     the below-SPY case a bare line under the grid instead of a card, arguing that a measure passing
     29 of 33 does not earn a paragraph on every page. **The owner reversed it on sight of the
     render**, and was right: two cards with a loose line beneath them reads as a card that failed
     to load, which is the exact ambiguity the line was meant to avoid. The standing rule from item
     10 is that absence states itself, and a card saying "46% as much" states it better than a
     footnote does.
  3. **No `warn` colour.** The strategies clustered near parity sit inside the gap between
     Composer's formula and ours, so a hard line at exactly 100% would be new false precision in
     place of old. The prose distinguishes above from below without a colour asserting it.
  4. **The single-best-day figure is dropped** from the pilot card. It carries the identical
     small-denominator flaw and adds nothing the 5% figure has not already said.

  **A measurement error in the first pass, found while implementing and worth recording.** The
  scratch comparison that produced these ratios matched SPY's window with
  `min(backtest_days, len(closes) - 1)`, which **silently truncated** rather than refusing. Three
  strategies backtest roughly 27 years against the 16 years of SPY closes in `data/prices.json`
  (`ob-os-staple-bonds`, `dip-buying-tech`, `safe-sectors-or-bonds-original`), so their "same
  window" ratios compared a 27-year strategy figure to a 16-year SPY figure. Two of them were among
  the six the first pass reported as worse than SPY. With the windows genuinely matched the count is
  **4 of 33 above SPY, 29 below, and 3 with no honest baseline at all**, and those three fall back
  to the pre-pilot card rather than to a fabricated comparison. **The failure shape is the one this
  whole item is about: a function that returns a plausible number instead of refusing.**

  **A fourth branch the pilot never exercised, added at rollout.** Three strategies
  (`dip-buying-tech`, `ob-os-staple-bonds`, `safe-sectors-or-bonds-original`) backtest roughly 27
  years against the 16 years of SPY closes in `data/prices.json`, so no same-window baseline exists.
  **They deliberately do NOT fall back to the pre-v1.43.0 card**, whose threshold is the thing this
  item exists to remove: a page with no benchmark is exactly where a reader is least equipped to
  discount it. They print the figure with its own limitation attached instead.

  **Still open: this is the best available today, not the destination.** The honest version needs
  per-strategy daily returns (**V1.20 item 16**, unbuilt): "drop the 10 best days and 34% a year
  becomes 12%" has no small denominator to go unstable, needs no benchmark, and would let both
  sides be computed with one formula instead of two.

- [x] **4. Outlier-dependence disclosure (v1.28.0).** Stated as plain arithmetic and left that way:
  no score, no badge, no rating. **25 of the 31 featured strategies are above 100%**, which means
  the other 95% of their days lost money on net, and the panel says exactly that when it applies.
  The range runs from **79.4%** (`simons-kmlm-switcher`) to **260.2%** (`nancy-pelosi-chips`). Below
  100% the copy switches to naming what the remaining 95% of days contributed, rather than implying
  a problem that is not there. The single best day's contribution is given beside it.
- [x] **5. Out-of-sample panel (v1.28.0).** Days since the last logic edit, with the date, computed
  in the browser so it does not go stale a day after the build. Both halves are said: the days after
  an edit are genuinely out of sample because they were not available to be fitted to, **and** logic
  also sits untouched when nobody is maintaining it, so a long stretch says nothing about whether the
  strategy still suits the market it trades now.

  **`gold-miner-original` has no `oos_date`**, so the panel renders "Not recorded" and tells the
  reader to treat the whole backtest as in-sample until it is. Hiding the panel for that one
  strategy would have quietly turned a missing measurement into no question at all. Dates are
  compared in UTC on both sides, or a browser west of Greenwich reads one day short.
- [x] **6. Assets section (done v1.34.0). Shipped as a plain section, not a tab** (owner ruling).
  The specified `.db-tabs` reuse was rejected on the grounds that `strategies.html` is one continuous
  scroll today with no tab state anywhere on it: tabs would have hidden the new content behind a
  click, added `?tab=` deep-link handling, and shortened a page that is not too long. It sits between
  the risk profile and the K-1 notices, so what the strategy holds is read immediately before the tax
  consequences of holding it.

  **The gap between the two halves is the reason the section exists, and it is larger than expected.**
  Across the 31 featured strategies the median universe is **6 tickers** and the median position is
  **1**, and **not one strategy holds its full universe**. `super-semiconductors` can reach **31
  tickers and is holding SMH alone**. Nothing else on the page showed this, and the Deeper Metrics
  note already has to warn that the Herfindahl index describes the backtest rather than today's
  position; this is where a reader can now see the position directly rather than inferring it from a
  number that disagrees with it.

  **Percentages only, never the stored values** (owner ruling). `last_market_days_holdings` holds
  **aggregate dollars across Composer**, not weights: `four-horsemen` reads $229,544,631 and
  `super-semiconductors` reads $417,186. That is not the reader's money and printing it would be a
  wall of unexplained millions; normalised, the same numbers are the strategy's own allocation, which
  is the question a reader is actually asking. The total is guarded, because a strategy fully in cash
  would divide by zero and print `NaN%` on every row.

  Each row carries the ticker (linked to its K-1 entry), a proportional bar, the share, the fund's
  inception date from V1.20 item 9, and a K-1 or ETN badge in the same two colours `/k1` already
  uses. Tickers in the universe but not held are listed separately as chips, worded so that **a
  ticker in that list reads as one the strategy may buy, not one it has abandoned**.
- [x] **7. K-1 warning line, cross-linked to `/k1` (v1.28.0).** Affects **12 of 31** for K-1 and,
  now that v1.27.9 made ETNs visible, **2 more for ETNs**, so 14 strategies carry a notice. Every
  verdict is resolved from `data/k1.json` at build time and never restated, so a correction to the
  K-1 database propagates rather than going stale in a second place. Each ticker links to
  `k1.html?t=TICKER`.

  Two notices on one component, colour-matched to `/k1` so a visitor who has seen that page reads
  these without being taught: yellow for K-1, blue for ETN. The 27 held tickers absent from the K-1
  database are all individual stocks, deliberately purged at v1.27.5; the build reports them in its
  run summary so a genuinely missing **fund** would be noticed.
- [x] **8. Provenance chip at the top of the page (v1.30.0).** Above the tags, so the age of the
  numbers is read before the numbers are.

  **There are genuinely two ages on this page, and the chips say so rather than averaging them into
  one reassuring date.** The headline strip and the sidebar table come from `strategies.json` and
  carry its `last_updated`; the Deeper Metrics grid, the outlier panel, the out-of-sample panel and
  the holdings notices come from the build-time join and carry `database.json`'s `refresh_date`.
  Those two differ on all 31 strategies today, by one to seven days. When they agree the page falls
  back to a single "Data refreshed" chip, and when the join has not loaded at all only the one chip
  it can honestly state is rendered.

  **The dot turns yellow past 14 days.** That is long enough to mean the nightly refresh has stopped
  running rather than merely slipped over a weekend.
- [x] **9. Backtest-window explainer (done v1.33.0).** A third card in Beyond the Backtest, giving
  the window's length, the earliest date it could have started, and the holding that sets that date.

  **`prices.json` was the specified source and it is the wrong instrument. It was not used.** The
  original spec proposed deriving inception as a lower bound from each ticker's first non-null
  close, and hedging the copy with "at least" to cover the gap. Two measurements killed that:

  1. **Coverage was overstated in this very item.** It claimed `prices.json` "covers 72 of the 105
     tickers the featured strategies hold". That conflated *72 tickers in the file* with *72 of the
     105*. The real overlap is **44 of 105**, because 28 of the file's tickers are Signal Miner
     universe entries the featured strategies never touch.
  2. **The 2010-01-04 floor makes the derived date wrong far more often than right.** Measured:
     **48 of the file's 72 tickers report 2010-01-04 as their first close**, which is the file's own
     start date, not theirs. It cannot tell "listed in 2010" from "listed in 1993". SPY would have
     been reported as starting in 2010 when it launched 1993-01-29, and QQQ as 2010 when it launched
     1999-03-10. A readout built on it would have been confidently wrong about the exact thing it
     exists to state, and no amount of "at least" hedging repairs a date that is off by 17 years.

  **Adding the 61 missing tickers to `prices.json` was considered and rejected** (owner question,
  2026-08-30). It fixes only the first problem and not the second, and it charges the cost to the
  wrong page: `prices.json` exists for Signal Miner, +61 tickers is roughly +1.9 MB on every Signal
  Miner load for tickers its universe does not use, and the feature needs **one date per ticker
  (~25 bytes), not 4,188 closes (~32 KB)**, a roughly 1,300x overpay. `strategies.html` also loads
  no price data at all today, so this would have added a multi-megabyte dependency to a page
  carrying a 30 KB join, reversing the V1.16 page-weight work.

  **Built instead: `data/ticker_inception.json`**, one true first-trade date per ticker from Yahoo's
  `meta.firstTradeDate`, written by `scripts/refresh_ticker_inception.py` and joined at build time by
  `build_strategy_extras.py`. **105 of 105 featured tickers dated, in 2 KB.** Inception dates do not
  change, so the file is fetched once and refreshed rarely, and runs are additive so `--all` extends
  it rather than replacing it.

  **Extended to the whole library in v1.34.1: 3,634 of 3,684 tickers dated, 95 KB**, in a single
  unattended run of about two hours at the 2s throttle. The file now covers every ticker held
  anywhere in `database.json`, which is the prerequisite for extending any inception-derived readout
  past the featured 31.

  **The 50 undated tickers were classified, not waved through.** They are not throttling damage and
  not a bug:

  - **Delisted through acquisition or going private**, which Yahoo serves as a hard 404: K
    (Kellanova), WBA (Walgreens), ANSS (Ansys), HES (Hess), ZIMV and the rest of that group.
  - **Warrants, and unfixable rather than a symbol-mapping bug.** Composer writes them `IONQ/WS`,
    which normalises to `IONQ-WS` and 404s. **The correct Yahoo symbol `IONQ-WT` resolves and still
    returns `firstTradeDate: null`**, so correcting the suffix would recover zero dates. Checked
    directly before deciding not to fix it.

  Every consumer already degrades correctly on a missing date, which is why 50 gaps need no special
  handling: `k1.html` omits the row, and the backtest-window card suppresses itself when any holding
  is undated rather than computing a floor from a subset.

  **The specified sentence asserts a false cause on 13 of 31 strategies, so it was not shipped.**
  The spec's wording, "14.8 years, limited by UVXY", presumes the limiting holding explains the
  window's length. Measured against all 31 featured strategies:

  - **Not one backtest starts before its floor.** The bound is real and both datasets agree.
  - **Not one starts at it either.** 18 of 31 begin within a year of the floor, where the limiting
    holding does explain the window. The other 13 begin well after, up to **5.6 years late** for
    `zoops-kmlm-switcher-2026`.

  So the card switches copy on the measured headroom. Under a year it says the window is about as
  long as it could be and names the holding. Over a year it says the opposite and says why that
  matters: **the start date was chosen, and start dates are among the easiest things to fit a result
  to.** That second case is a more useful disclosure than the one originally specified, and it only
  became visible because the exact-inception source made the comparison possible.

  **Ties are kept, not collapsed.** Whole leveraged families launched on one day (SOXL and SOXS both
  2010-03-11, GDXU and GDXD both 2020-12-03); naming one arbitrarily would change between rebuilds
  for no visible reason. **Incomplete coverage suppresses the card** rather than guessing: one
  undated holding could be the true floor, so `dated` and `total` are carried and the card renders
  only when they agree.

**Tier 2: restructuring content that already exists.**

- [x] **10. Split `risk_profile` into named categories. Complete: all 36 strategies carry the
  object shape as of v1.36.0.** Piloted on `four-horsemen` in v1.35.0, signed off, then the
  remaining 30 rewritten.

  **The screenshot's four categories were not used, because they were never checked against our own
  text.** Section 14 records the source of the proposed grouping as a screenshot of a comparable
  tool, adopted as "the right shape". Reading all 31 strings shows the four are each genuinely
  attested but cover roughly a third of what is written, and miss the two largest themes outright:

  | Theme | Count | In the screenshot's four |
  | --- | --- | --- |
  | Opens with an aggressiveness verdict | **31 of 31** | no |
  | Recites Sharpe / Calmar / std dev / ARR | **29 of 31** | no |
  | Leverage, decay, roll cost | **23 of 31** | yes |
  | Discusses the backtest window | **20 of 31** | no |
  | Signal design, whipsaw, missing gate | 13 of 31 | yes |
  | Hedge instrument named | 12 of 31 | yes |
  | Concentration | 8 of 31 | yes |
  | Suitability advice | 5 of 31 | no |
  | Complexity / auditability | 5 of 31 | no |

  **Six categories are shipped instead**, derived from those counts: `verdict`, `leverage`,
  `backtest_limits`, `signal`, `hedge`, `concentration`, plus an optional `suitability` tail.
  Complexity folds into `signal`, because the logic tree **is** the signal design.

  **Categories are ordered by measured frequency, not by severity.** Ranking them by danger would be
  a judgement this site has no grounds to make, and it is the same rule that keeps the outlier panel
  from turning its arithmetic into a score.

  **An absent category states itself** ("No hedge leg: this strategy has no inverse or volatility
  position to cushion a drawdown") rather than being omitted, because a missing heading cannot be
  told apart from an unwritten one.

  **The duplicated statistics had already gone stale, which settles the question of keeping them.**
  `four-horsemen`'s prose said "Sharpe 2.18, Calmar 3.68, and standard deviation of 50.6%" while the
  live values were **2.15, 3.60 and 50.8%**; its max drawdown read 45.4% against an actual 45.3%, and
  the Holy Grail figure it cited as 62.3% had become 62.6%. `update_metrics.py` refreshes the metrics
  nightly and cannot rewrite prose, so every duplicated figure drifts. Bare statistics are therefore
  dropped and the metrics table owns them; **comparisons are kept**, because "meaningfully lower than
  Holy Grail at comparable annualised return" is a claim the table cannot make.

  **One correction the rewrite had to make:** the original implied the comparison ran over a shared
  window. It does not. `four-horsemen` is 3,677 trading days against 3,741 for both Holy Grail and
  TQQQ For The Long Term, so the pilot says the windows are "close rather than identical".

  **Both shapes render side by side by design** while the rewrite proceeds one strategy at a time, so
  a string keeps rendering exactly as it did before this item existed.

  **`scripts/update_metrics.py` needed no change**, verified: it mutates named fields in place on the
  loaded dict and re-dumps the whole object, so the reshaped field survives the nightly job.

  **Open question for the owner, deliberately not decided:** whether `check_risk_profiles.py` becomes
  a fifth gate in `deploy.yml`. It catches a failure no existing gate can see, a mistyped category key
  renders as silently missing content, but adding a deploy gate changes what can block a release and
  that is not a call to make as a side effect of a content edit.
- [x] **10a. Rewrite the remaining 30 `risk_profile` strings. Done in v1.36.0.** 20,657
  characters of prose became 29,525 across 6 categories, and the `Attribution: created by ...`
  sentences were deleted from `super-semiconductors` and `soxx-group` rather than relocated,
  because **`author_note` already carried the identical credit on both**.

  **Thirteen comparative claims were wrong and were corrected during the rewrite.** This is what
  the stale-statistics finding from the pilot looks like at full scale. Every comparison kept in
  the new prose was re-checked against the live metrics before being written:

  | Strategy | The claim | What is actually true |
  | --- | --- | --- |
  | `soxl-growth-rl` | "second-highest max drawdown, behind Inside Nancy Pelosi's Chips" | **The ordering flipped.** It is now the deepest in the library. |
  | `soxl-growth-rl` | "the highest standard deviation in this library" | Second, behind The Gold Miner. |
  | `soxl-growth-rl` | "the longest backtest in the library" | **Wrong when written**, not drift. Two unleveraged 27-year strategies are far longer. Corrected to "longest of the leveraged strategies". |
  | `nancy-pelosi-chips` | "the highest max drawdown in this library" | Second, behind SOXL Growth (Original). |
  | `nancy-pelosi-chips` | "Calmar of only 0.85, the only strategy below 1.0" | **Four** strategies are now below 1.0. |
  | `mean-reversion-py` | "Calmar of 1.00 is barely above break-even" | It has since fallen below 1.0. |
  | `s90-half-low-catch` | "second only to SOXL Growth RL on volatility" | Third, and its own max drawdown had drifted from 29.6% to 41.0%. |
  | `top-cap-ma-rsi` | "Sharpe puts it above most leveraged ETF strategies" | **21 of 31 are higher.** |
  | `top-cap-ma-rsi` | "max drawdown is the lowest in this sub-category" | `super-semiconductors` is lower. |
  | `zoops-leveraged-tqqq-symphony-2026` | "among the higher-risk strategies in the library" | Mid-pack library-wide. True only within the zoop set, which is how it now reads. |
  | `zoops-excellent-adventure-2026` | "at the upper end of the aggressive spectrum" | Mid-pack. Claim dropped. |
  | `wooden-arkk` | "standard deviation among the highest in the library" | Roughly eighth. Claim dropped. |
  | every strategy | trading-day counts quoted in prose | All had drifted. `wooden-arkk` alone moved from 1,028 to 1,076. |

  **Absence claims were grounded in data, not in the old prose.** Omitting a category makes the page
  assert something ("No hedge leg: this strategy has no inverse or volatility position"), so every
  omission was checked against the strategy's reachable ticker universe in `strategy_extras.json`
  rather than against what the original string happened to mention. That produced **8 absent rows
  across 6 strategies**: `leverage` omitted only on the two genuinely unleveraged strategies
  (`dip-buying-tech`, `ob-os-staple-bonds`), `hedge` omitted only where no inverse or volatility
  instrument is reachable at all (those two plus `bnd-vs-sphb`), and `signal` omitted where the
  original recorded no signal-design risk and inventing one would have been fabrication.

  **The same data grounded the positive claims.** Naming the actual hedge leg is what makes several
  of these categories useful: `soxx-group`'s only defensive position is SOXS, 3x inverse
  semiconductors, so its defensive state is itself a leveraged bet on the same sector;
  `gold-miner-original`'s is GDXD, with the same problem; and `simons-kmlm-switcher` holds SVIX
  alongside UVXY, which are opposite sides of the same trade. None of that was in the original
  prose.

  **`.risk-box` is now unexercised.** No strategy is a string any more. The renderer branch and the
  CSS rule are kept deliberately, because `risk_profile` is hand-edited and the string form stays
  valid per `check_risk_profiles.py`; a future entry written as a string must render, not vanish.
- [x] **10c. Statistics removed from every prose field, and drift made detectable. Shipped
  v1.37.0.** Fixing `risk_profile` in v1.36.0 fixed one field's copy of the numbers and left the
  other copies in place. `ai_summary` renders a few hundred pixels above the risk profile on the
  same page and recited the same statistics.

  **The measurement: 131 checkable numeric claims across the prose fields, 89 of them stale, on 29
  of 31 strategies.** Most were rounding drift of the kind the pilot found. Two strategies were
  wrong by margins no reader could discount:

  | Strategy | Field | Prose said | Actually |
  | --- | --- | --- | --- |
  | `s90-half-low-catch` | Calmar | 24.81 | **11.69** |
  | `s90-half-low-catch` | annualised return | 735% | **479%** |
  | `s90-half-low-catch` | max drawdown | 30% | **41%** |
  | `s90-half-low-catch` | Sharpe | 3.04 | 2.59 |
  | `zoops-manhattan-project-2026` | Calmar | 4.43 | 3.86 |
  | `zoops-manhattan-project-2026` | max drawdown | 35% | **39%** |

  `s90-half-low-catch` was advertising a Calmar more than double the real figure and a drawdown a
  third shallower than the real one, **overstating the strategy in both directions at once, on the
  same page that displayed the correct numbers in a table.**

  **Three more comparative claims were wrong and are corrected, not merely stripped.**
  `soxl-growth-rl`'s summary called its drawdown "the second-deepest in the entire library"; it is
  now the deepest. `nancy-pelosi-chips` claimed "the weakest risk-adjusted profile in the library"
  and "the deepest max drawdown here"; `dip-buying-tech` has a weaker Sharpe and Calmar, and SOXL
  Growth (Original) has a deeper drawdown. `mean-reversion-py` described "a Calmar of exactly 1.00,
  the breakeven line"; it has since fallen below it, which reverses the point being made.

  **Durations are dropped, start dates are kept.** `backtest_days` grows every night, so "roughly
  14 years" drifts; "the backtest begins in late 2011" is a fixed fact, and it is the half that
  tells a reader which crises the record contains. The window card added in v1.33.0 owns the length.

  **`scripts/check_stat_drift.py` is the durable half.** It parses every performance figure out of
  every prose field, compares it to the live metric, and fails on a mismatch, with the tolerance set
  to the prose's own rounding so a claim written to one decimal is wrong only if it rounds to
  something else. It is the piece that was missing: this rot went unnoticed through every nightly
  `update_metrics.py` run because nothing was looking.

  **The checker had a real bug, and the fault-injection tests caught it before it shipped.** The
  number pattern `[\d.]+` captured the sentence-ending period, `float("3.68.")` raised, and a
  `try/except ValueError: continue` swallowed the claim in silence. **Every figure that ended a
  sentence was invisible to it.** A checker written to find silent failures was failing silently.
  The except clause is gone: if the pattern is ever wrong again it raises rather than under-reports.
- [x] **10b. Which advisory checkers become deploy gates. Ruled by the owner 2026-09-02, shipped
  in v1.70.0.** The question had widened past the two scripts it started with, so it was put as
  three:

  | Checker | Ruling |
  | --- | --- |
  | `check_asset_sizes.py` | **Gated.** Fifth step in `deploy.yml`. |
  | `check_risk_profiles.py` | Advisory. Runs, reports, cannot block. |
  | `check_stat_drift.py` | Advisory. Runs, reports, cannot block. |

  **The one that gates is the one with a body count.** On 2026-09-01 a routine refresh pushed
  `data/symphony_scores.json` 210 KB past Cloudflare's 25 MiB per-file limit, which rejects the
  whole deployment, and roughly a day of work sat on `main` unpublished with no symptom but a red
  build in a dashboard. `data/database.json` and its `.js` twin are at 76% of the limit and grow
  weekly, so the same failure is queued rather than hypothetical. The other two guard failures that
  are real but have never occurred, and one of them (`check_stat_drift`) now reports **0 checkable
  claims** because the v1.44.0 to v1.68.0 rollout replaced every hardcoded figure in prose with a
  token, which is the intended end state rather than a broken checker.

  **State plainly what the gate cannot do.** `deploy.yml` publishes to GitHub Pages and is **not**
  the live path. Cloudflare builds independently from the same push, so this gate cannot stop a bad
  deploy from reaching production. What it converts is an opaque Cloudflare failure into a red check
  naming the file and its size: the difference between noticing in minutes and noticing in a day.
  A gate that actually blocked publication would have to live on Cloudflare's side.

  **Folded in by the same ruling: `.git/` added to `.assetsignore`.** A build log reported reading
  140 files from the assets directory where a clean clone holds 91 tracked ones. wrangler may
  exclude the repository already, but if it does not, `/.git/` serves the full history and every
  stray file ever committed. One defensive line closes the question without testing the live site.
- [x] **11. Signal Types table (v1.71.0).** The 91 signals on the 24 visible strategies now carry
  `type` and `indicator` alongside `name`, `tag` and `description`, rendered as a table.

  **Measuring first changed all three parts of the spec**, and the owner ruled on each 2026-09-02:

  | Finding | Ruling |
  | --- | --- |
  | **The `x2` dedupe badge had nothing to dedupe.** Zero exact within-strategy duplicates across all 24. One name repeats *across* strategies ("SPY 200-Day MA Trend Gate"). | **Dropped.** Building it would have meant inventing duplicates to justify it. |
  | **A real table fights the descriptions.** Median description is **259 characters**, 75 of 91 over 200. A fifth prose column recreates the phone overflow fixed in v1.69.0. | **Table with detail rows.** The four scannable fields share one row, the description gets a full-width row beneath, and below 640px the whole table becomes a labelled stack. |
  | **`Threshold / Trend / Selection` did not cover the data.** 11 of 91 describe a holdings set rather than a condition. | **Four types**, adding `Composition`. |

  **The four types, as applied:**

  | Type | Count | Meaning |
  | --- | --- | --- |
  | `Threshold` | 45 | An indicator against a fixed number (`RSI(10) > 79`). |
  | `Trend` | 23 | An asset against its own moving average, or one asset's reading against another's. |
  | `Selection` | 14 | Rank a pool, take the top or bottom N. |
  | `Composition` | 9 | Describes the holdings set or structure, not a condition. |

  **`indicator` is derived from the symphony tree, never from the prose.**
  `scratchpad/inventory.py` walks each cached tree and reports every (function, window) pair it
  actually computes, split by `if` condition versus `filter` sort key. **All 119 indicator labels
  across the 91 signals were verified present in their own strategy's tree.** A label is capped at
  three per signal and a bare family name (`RSI`, `MA return`) is used where one signal spans so
  many windows that naming them all would be noise.

  **The automated drafter got roughly a third of the types wrong**, which is the reason all 91 were
  read by hand. It matched the word "basket" in a description and filed a live condition under
  `Composition`. Machine drafting set the floor here; it did not set the answer.

  **Two schema variants store the same window, and reading only one is a live trap.** A comparison
  node carries its lookback either as `<side>-window-days` **or** nested as
  `<side>-fn-params.window`. Reading only the first is the cause of the `relative-strength-index(None)`
  artifact that had appeared in scratchpad tree printers for weeks. It was never a defect in any
  symphony.

  **The cross-check found zero content defects across 91 signals.** Five appeared to name an
  indicator absent from their tree; all five were the checker's own regex, four confusing
  `moving-average-return` with `moving-average-price` and one reading "200-day MaxDD" as a 200-day
  moving average. It did find two typography slips in signal prose, an en-dash and a `->` written as
  an arrow glyph, both fixed. The v1.68.2 sweep had not covered these fields.

  **Verification.** All 24 pages rendered in headless Edge and every one of the 91 rows compared
  against the data: name, type, indicator chips, detail row and header count. A hidden strategy was
  rendered too, to confirm the pre-item-11 shape degrades to "not categorised" and "none" rather
  than to blanks. 0px overflow at 375, 390, 768 and 1280px on the content-heaviest pages.
  `scripts/check_signal_types.py` guards the schema going forward and is **advisory**, per the item
  10b ruling.

- [x] **12. Link metric labels to the glossary (v1.30.0).** **The seven missing terms were written
  first and shipped in v1.27.8** (Sortino Ratio, Win Rate, Skewness, Kurtosis, Tail Ratio,
  Herfindahl Index, Annualized Turnover), taking the glossary from 20 terms to 27, because surfacing
  a metric a visitor cannot look up adds jargon rather than understanding. The linking itself landed
  in v1.30.0.

  **One map, `METRIC_GLOSSARY` in `js/app.js`, covering 13 labels**, applied by `metricLabel()` to
  the hero strip, the Deeper Metrics grid and the existing sidebar metrics table in one place. 23
  linked labels render on a strategy page.

  **An unmapped label stays plain text on purpose.** A link that lands on "No concept with slug" is
  worse than no link, so Cumulative Return, the four Daily Distribution rows and the three Trailing
  Returns rows are unlinked until the glossary defines them. The fix for a missing term is to write
  the term, which is exactly the order v1.27.8 established.

**Tier 3: new written content, and this is where the real cost is. Every item multiplies by 31.**

- [x] **19. GATE: the owner reviews and explicitly approves the structure before it is written for
  any strategy beyond the pilot. Signed off 2026-09-02 in v1.43.0.** Added 2026-08-28, immediately
  after reviewing v1.29.0 to v1.29.3. The gate held: nothing beyond the pilot was written until the
  layout was approved, and items 13, 14 and 15 then rolled out to the remaining 23 visible
  strategies across v1.44.0 to v1.68.0.

  **STILL OPEN, and not resolved by the v1.43.0 approval.** The owner approved the
  `gold-miner-original` page on 2026-09-02, and that approval covers the v1.42.x **layout** changes
  only: section order, the Assets section, and the best-days card. Items 13, 14 and 15 are authored
  **prose** on the same page and were not what was under review. The two are easy to conflate
  because they share a pilot slug. They do not share a gate.

  **This is a hold point, not a task, and it is the highest-leverage item in the phase.** The pilot
  exists to be judged, and the owner's verdict on it was "good as a rough draft, it needs more
  refinement organizationally". Writing 30 more strategies against a structure that is still being
  refined would multiply every organisational decision by 30 before any of them are settled, and
  Tier 3 is the one tier where that mistake cannot be undone cheaply: item 10 already showed that a
  schema change is survivable, but 30 pieces of authored prose written to the wrong shape are not.

  **Evidence the gate is already doing work.** Two structural corrections came out of the first
  review alone, both from the owner and neither anticipated: the K-1 and ETN notice moved below Risk
  Profile (v1.29.1), and Market Regime Analysis moved above it (v1.29.3). Those are section-ordering
  decisions, exactly the class of thing that is cheap to change once and expensive to change thirty
  times.

  **What sign-off should cover**, so that approving it means something specific:

  1. **Section order and which sections exist at all.** Two changes already; assume more.
  2. **Whether `risk_profile` survives.** The regime table and the Struggles-in column now overlap
     it, which is item 10's open question. Deciding this before writing avoids authoring content for
     a section that is about to be absorbed.
  3. **The shape of each section's content**: how many items in Works well in against Struggles in,
     how long an assumption runs, how many regimes is the right number. The pilot used 3 and 4, 4
     and 5, and 6, chosen for one strategy rather than as a standard.
  4. **How much research a regime table is allowed to require.** The pilot's took a reconstruction
     of the strategy's state machine validated against the pipeline's turnover figure. That is
     defensible once and it is the whole argument for item 16.

  **Sign-off is recorded here with a date when it happens**, so a later reader can tell an approved
  structure from one that was never reviewed.

  **Signed off 2026-09-02 in v1.43.0.** The approval was of the whole page layout, not the three
  sections alone: the canonical section order moved into `docs/DESIGN.md` under **Strategy Page
  Section Order**, `isLayoutPilot` and every pre-pilot branch were deleted, and items 13, 14 and 15
  were then rolled out to the remaining 23 visible strategies across v1.44.0 to v1.68.0.

- [x] **13. TL;DR card. Complete: all 24 visible strategies, v1.43.0 to v1.68.0.** Core Thesis callout
  with a green rule, above opposed **Works well in** / **Struggles in** columns.

  **The format did what it was chosen to do.** Writing the Struggles-in column for this strategy
  forced the finding that its worst case is not a down market but a directionless one: through 2026
  to 21 August, GDXU fell 23.5% **and** GDXD fell 81.9%, so both leveraged legs lost at once and
  only GLD was up. Nothing on the existing page said that, and the prose sections had not been
  written in a shape that would have surfaced it.
- [x] **14. Underlying Assumptions. Complete: all 24 visible strategies, v1.43.0 to v1.68.0.**
  Two columns: market and macro beliefs against technical and structural ones. Four and five items
  respectively for the pilot.

  **The split is the content.** A belief about the world fails differently from a belief about the
  instrument, and separating them is what stops the section becoming a list of caveats. It produced
  the sharpest single line on the page: the strategy is named and described by its RSI gates, and a
  reconstruction of the logic over real prices shows **those gates fired on 10.6% of days**, with
  the momentum branches making the other 89.4% of the decisions.
- [x] **15. Market Regime Analysis table. Complete: all 24 visible strategies, v1.43.0 to
  v1.68.0.** Six regimes across regime, expected, why and example period. The example column was not dropped
  for space: the table scrolls inside its own `overflow-x` wrapper instead, per the rule the v1.12.0
  mobile audit set.

  **Every example is a real price move over a fixed window**, computed from `data/prices.json`, so
  none of them goes stale on a refresh. The regimes themselves were identified by reconstructing the
  strategy's state machine over those same closes. **That reconstruction was checked before it was
  trusted:** it changes asset every 4.2 trading days against the 60.7 annual rebalances the pipeline
  independently reports. It is a reading of the logic, not a backtest, it carries no fees or
  slippage, and the page says so in a footnote under the table.

  **This is the item that decides whether Tier 3 scales.** It took real research per strategy, and
  the whole point of item 16 is to compute this table rather than write it.

**Tier 4: needs data the pipeline sees but does not keep.**

- [x] **16. Per-strategy daily returns are stored during refresh (v1.72.0).** `data/daily_returns.json`
  and its `.js` twin hold a day-aligned return series for each of the 24 visible strategies, written
  by `scripts/update_metrics.py` on every run.

  **Sized before committing, as this entry required.** One live backtest was measured four ways.
  The series arrives as `dvm_capital`, a day-indexed portfolio value map the pipeline had been
  reading straight past. Stored as a day array plus returns at six decimal places it costs about
  35 KB per strategy and **1.24 MB for all 24**, against a 25 MiB per-file ceiling. The same storage
  for the 6,668 community database rows would be 233 MB, so this entry's warning stands and the
  scope stays strategies-only. **Owner ruling 2026-09-03: visible 24 only, and storage now, derived
  features later.**

  **Six decimal places, chosen by measurement.** Against the unrounded series, recomputed Sharpe
  moves by 7.7e-7 and annualized return by 1.5e-6, while the file is 20% smaller than at 8dp.

  **Three conventions were pinned against the API rather than assumed:**

  | Question | Answer | Cost of getting it wrong |
  | --- | --- | --- |
  | How is a year measured? | `(n + 1) / 252`, not calendar days | 4.8e-3 on annualized return |
  | What does `size` count? | Returns, so `n + 1` daily values | An off-by-one on every series |
  | Are trading days contiguous? | No, so the day array is stored explicitly | Silent date drift across holidays |

  **The backfill cost zero extra API calls, now and forever.** Rather than a one-off script, the
  staleness skip in `update_strategies()` was widened: fresh metrics alone no longer license a skip
  if a visible strategy has no stored series. Anything added later backfills itself on the next run.

  **`scripts/check_daily_returns.py` recomputes four metrics from each stored series and compares
  them against the published figures.** Across all 24 the observed worst deviations were max
  drawdown 4.1e-6, volatility 6.5e-4, Sharpe 2.4e-3 and annualized return 1.2e-3, and the series
  length matches `backtest_days` exactly on every one. The residual is convention, not error. Both
  new checkers are **advisory**, per the item 10b ruling.

  **What this unblocks, none of it built yet:** worst month, VaR and CVaR, time in market, the
  year-jackknife and outlier-removal tests in Section 14's C3, and computing item 15's regime tables
  rather than writing them, which is the only way that section scales past a curated 24.

**Fixes, independent of the above.**

- [x] **17. The distribution metrics were mislabeled, and are now correct (v1.27.8).**
  `renderMetricsTable` showed `min`/`mean`/`median`/`max` as "Min Month" through "Max Month". They
  are **daily**. Three independent checks agree: volatility drag requires an arithmetic mean
  compounded over a year to exceed the geometric annualized return, which holds for **31 of 31**
  strategies read as daily and **0 of 31** read as monthly; the monthly reading implies 3% to 7%
  annual returns against stated ARRs of 90% to 277%; and the stored `max` of 54.63% for strategies
  holding SOXL matches SOXL's best single day of 54.79% on 2025-04-09. The PRD contradicted itself
  too, calling them "single-period" in Section 12 and "Monthly distribution" in the API mapping
  table. **This was a live correctness bug, not a cosmetic one:** it told visitors the worst month
  was -15% when that figure is a single day.

- [x] **18. Strategy detail pages scroll horizontally on a phone. Fixed in v1.69.0.** The cause was
  not what this entry assumed. `.detail-main` already carried `min-width: 0` and the bug survived
  because **on mobile `.grid-2` is a single column and both children share that one track**, so the
  floor was on the wrong element: `.detail-sidebar` had none, and its min-content widened the track
  to 429px with `.detail-main` simply filling it. The fix is on the track rather than the item,
  `grid-template-columns: minmax(0, 1fr)` and `minmax(0, 2fr) minmax(0, 1fr)` at the desktop
  breakpoint, which makes the container immune to whichever child misbehaves next. Verified 0px
  overflow at 320, 375, 390, 414, 768, 1024 and 1280px, and the regime table still scrolls inside
  its own wrapper rather than being clipped.

  **A site-wide sweep at 390px came with it and found one more live page overflowing**,
  `signal-miner.html` by 65px: `.sl-selgroup` is a flex row of `white-space: nowrap` buttons given
  `width: 100%` below 640px, with no `flex-wrap`. Fixed in the same release. Every other page was
  already clean. `signal-lab.html` appeared in the first sweep only because it is a redirect stub
  that forwards to the miner.

  **Reproducing this needs an iframe, not a window size.** Headless Edge refuses to size its window
  below roughly 477px, so `--window-size=390,844` silently measures a 477px viewport and the bug
  does not appear. The harness (`measure_overflow.py`) embeds the page in a fixed-width iframe and
  measures inside `contentDocument`, which reproduced the recorded 453 against 375 exactly.

  **Original diagnosis, kept for the record. Pre-existing, found during the
  v1.28.0 work and measured as unchanged by it.** At a 390px viewport the document's `scrollWidth`
  is **453px against a `clientWidth` of 375px**, identical before and after that release, so the new
  sections neither cause nor worsen it. Localised: `.grid-2` computes to **327px wide while its
  single `1fr` track resolves to 429px**, and `.detail-main` fills the track. `.detail-main` already
  carries `min-width: 0`, which is the usual fix and is not working here, so the cause is further
  down. Same class of bug as the two `.db-tabs` and `.page` overflows fixed at v1.12.0. **Not
  bundled into v1.28.0 on purpose:** it is unrelated to the four items that release delivered, and
  a layout fix on every strategy page deserves its own change and its own before-and-after.

---

**Deliberately not copied from the source page**, recorded so the reasoning is not rediscovered:

- **The "simulated history" row.** The source models leveraged ETFs backwards from their
  underlyings and shows real and simulated backtests side by side. **That distinction does not apply
  to us, and this was measured rather than assumed:** comparing every featured strategy's
  `backtest_days` against the inception of its youngest holding gives a gap of zero or negative in
  every case, so Composer already truncates to real traded history. Item 9 is the useful inversion.
- **VaR, CVaR, Kelly, worst month, time in market.** Not computable from what the site ships. They
  need item 16 first.
- **The Logic Flow tree.** Excluded by the owner: too large for most symphonies.
- **The light editorial palette.** Structure only; the site's dark system stays.

---

**Recommended sequencing.** The ordering is driven by one fact: Tier 1 costs no writing, Tier 3
costs writing times 31, so anything that changes the schema should land before the writing starts.

1. ~~**Item 1 first, alone.**~~ **Done, v1.28.0.** Everything in Tier 1 depends on the join, and it
   is the only item that can fail in a way that silently empties a page. Landed with the build-time
   miss check and a deploy gate. **In practice it did not land alone:** the join is only observable
   through something that renders it, so shipping it with nothing attached would have meant shipping
   an untested file. Steps 1 and 2 went out together, and the sequencing point still held, because
   the join was written and its failure modes tested before any section consumed it.
2. ~~**Items 4, 5 and 7 next.**~~ **Done, v1.28.0.** The highest differentiation per unit of work on
   the list, and none of them needed a single word written per strategy. Outlier dependence,
   out-of-sample duration, and the K-1 cross-link are each things no competing page shows.
3. **DONE (v1.30.0). Items 2, 3, 8 with item 12's linking.** The visual reorganisation, done in one
   pass so the page is not restructured twice. Item 3 without item 12 ships unexplained jargon, so
   they went together, and doing so is what forced the glossary-coverage question to be answered
   rather than deferred.
4. **Item 6, then item 9.** The Assets tab is self-contained. Item 9 goes after it because the
   inception caveat is easier to word once the holdings are already displayed beside it.
5. **Items 10 and 11 before any of Tier 3.** Both are schema changes. Doing them after the new prose
   is written would mean rewriting it, and item 10 already requires reworking 31 existing strings.
6. **Item 19, the gate. A hold point, not a task.** The owner reviews the pilot's structure and
   explicitly approves it. **Nothing in items 13 to 15 is written for a second strategy until this
   is signed off.** It sits here rather than earlier because a structure can only be judged from a
   finished example, and it sits here rather than later because the next step multiplies every
   unresolved organisational question by thirty.
7. **Item 13, then 14, then 15**, in that order and ideally on a few strategies first. **Write three
   strategies fully before writing thirty-one**, because the value of the Works well in / Struggles
   in format cannot be judged from a template, only from whether it produces something honest on a
   strategy whose weaknesses are already known. **Started early, at the owner's request: one
   strategy shipped in v1.29.0 as a pilot** ahead of steps 3, 4 and 5. See the status note at the
   top of this section for what going out of order does and does not cost.
8. **Item 16 last, and only if item 15 proves worth scaling.** It is the only item requiring a
   pipeline change and a storage decision, and its main justification is computing item 15 rather
   than writing it. If the regime tables turn out to be better written by hand for a curated set,
   this item does not need to happen at all.

**One scoping warning.** Tiers 1 and 2 apply cleanly to the 31 featured strategies. **They do not
generalise to the 6,668 rows in the full database**, which have no `description`, `signals`,
`risk_profile` or any other written content, and never will. Nothing in this phase should be
designed in a way that implies the full database will eventually get the same treatment.

### V2.0: Full Database Goes Public

**Status:** Complete (v1.12.0)

**What actually happened, corrected from the original plan:** the original plan was one clean push once every gate was cleared. Instead, the code (`database.html` and its supporting CSS/JS/scripts) was pushed to `main` on v1.11.2 while the data files were deliberately held back until the full refresh and V1.14 noise-filtering pass completed. The data files went live on v1.12.0. `deploy.yml`'s rsync exclusion list was left unchanged, it already didn't touch the `database.json` family, and `Full Database.xlsx` (a local-only review artifact, not fetched by the live site) was never included in the exclusion list either since nothing needed excluding.

- [x] Full docs and content audit of `database.html`, Leaderboard, and Screener (v1.12.0): no em-dashes found; copy reviewed and accurate. Mobile responsiveness audit **found and fixed two real, pre-existing sitewide CSS bugs**, not specific to this page: (1) `.nav-cta` (the "Open Composer" button) had the same specificity as `.btn`'s `display: inline-flex` and lost the cascade regardless of source order, meaning the button never actually hid on mobile anywhere on the site; fixed by reordering `.nav-cta`'s rule after `.btn`'s. (2) `.db-tabs` (used for the page-level tabs, Screener's view switcher, and the new flag-mode toggle) had no `overflow-x`, so on narrow viewports its content silently forced the whole page to scroll horizontally instead of scrolling internally; fixed with `overflow-x: auto`. Also fixed a `database.html`-specific instance of the same root problem: `.page` (a `flex: 1` child of `body { display: flex }`) had no `min-width: 0`, so its widest descendant (the data table) could force the whole page wider than the viewport instead of letting `.db-table-wrap`'s own `overflow-x: auto` contain it. Verified via headless-Chrome screenshots at a 390px mobile viewport before and after each fix.
- [x] Pushed the data files (`database.json`/`.js`, `database_summary.json`/`.js`, `storage.csv`) live (v1.12.0)
- [x] Update Section 6 Feature List: moved "Full Database Initiative" from "In Progress" to "Shipped" (v1.12.0)

### V2.1: Live RSI Signals Page

**Status:** Complete. Built ahead of its numbered slot, immediately after V2.0, ahead of V1.17/V2.2/V2.3, per explicit user request (2026-07-08/09). Same "built ahead of schedule" pattern as V1.16.

**What it is:** `rsi.html` displays live 10-day RSI (Wilder's smoothing, computed from ~250 days of adjusted daily closes; was ~45 until 2026-10-16, which left values 0.1 to 0.6 points off Composer) for the 20-ticker Frontrunner signal universe (XLF, SPYV, VTV, SPY, IOO, UUP, FXI, QQQE, XLK, QQQ, XLE, VOX, TECL, SOXX, RETL, XLY, EEM, GLD, XLP, TLT) plus IWM and DIA (added 2026-10-16 at the owner's request), so a visitor can glance at the site and know which tickers are oversold/overbought right now. See Section 12 (RSI Signals JSON Schema) for the `data/rsi.json` shape.

**RSI methodology:** Wilder's smoothing on adjusted daily closes (Composer's exact method is unconfirmed, but this is the industry-standard match, a QuantConnect staffer pointed at `MovingAverageType.WILDERS` as the closest replication of Composer's own displayed values). Formula, edge cases, and validation approach documented in `scripts/refresh_rsi.py`.

**Color thresholds (revised 2026-07-09, post-launch):** the original 70/30 scheme rendered every one of the 20 tickers as "Neutral" on the day it launched (all 20 landed between 34.7 and 65.2), making the page look inert. Replaced with a narrower band, tuned against that live data: ≥79 Extreme Overbought, 70–78 Overbought, 42–69 Neutral, 29–41 Oversold, ≤28 Extreme Oversold. Colors are literal hex values in `css/main.css` (not existing design tokens; the user specified a distinct green→red gradient for this page rather than reusing `--color-green`/`--color-pink`): `.rsi-extreme-overbought` `#00ff00` bold, `.rsi-overbought` `#2fb92f`, `.rsi-neutral` `#b0b0b0`, `.rsi-oversold` `#e04545`, `.rsi-extreme-oversold` `#ff0000` bold. The inner tiers' initial values (`#008900`/`#890000`) were repainted brighter after launch, too low-contrast against the dark table background to read. **Also fixed post-launch:** the rules were originally bare classes (`.rsi-oversold { ... }`), which lost the cascade to `.db-table td`'s own `color` rule (higher specificity: class+type beats a single class): the color-coding silently never rendered at all until the selectors were rescoped to `.db-table td.rsi-oversold` etc.

- [x] `scripts/refresh_rsi.py`: fetches Yahoo Finance daily bars (`v8/finance/chart`, no API key), computes Wilder's RSI(10), writes `data/rsi.json` + `data/rsi.js` atomically
- [x] `rsi.html`: sortable table (Ticker/Name/RSI(10d)/Signal), default sort descending by RSI, no pagination. Badge reads "As of <close date> close · refreshed <time>" (was "Last refreshed" only, until 2026-10-16: a late run could show today's refresh time over yesterday's close)
- [x] **No day roll-back (2026-10-16):** Yahoo can leave the newest day's adjusted close blank in the evening; the script uses the plain close for that day, and `keep_newer()` never replaces a saved row with one from an earlier `price_date`. Found when the 8:14 PM ET run (scheduled 6:07 PM, delayed by GitHub) overwrote Oct 16 values with Oct 15's
- [x] Nav: "RSI" link added to `js/app.js` (desktop + mobile), slotted after "Database" and before "Azqato Invests"/"Glossary"
- [x] `.github/workflows/refresh-rsi.yml`: automated 3x/day weekdays, cron `7 15,19,22 * * 1-5` (post-open/pre-close/post-close across both EDT/EST). Originally `0 15,19,22 * * 1-5` (on-the-hour); never fired on its first weekday test (Mon 2026-07-13) because on-the-hour is GitHub Actions' most congested scheduling slot. Offset 7 minutes past the hour, matching `refresh-full-database.yml`'s existing pattern, to fix.
- [ ] Sparklines: explicitly deferred to a future pass

### V2.2: Scale + Discovery (Curated Library)

**Status:** In progress, current phase. **Rescoped 2026-09-07 by owner decision.**

**What changed.** V2.2 had carried three unrelated things: two curated-content builds (the zoop
evergreen replacement, and the Cohort A library expansion) and one product build (Signal Miner
robustness, items A, B and C). The owner moved **both content items behind V2.5** and kept the
Signal Miner work as the active phase. The content items are now **V2.6** and their full
specifications stay below rather than moving, because they are long, they are already written, and
splitting a specification across two sections to match a scheduling change costs more than it
explains. Read the two bulleted content items below as V2.6 work.

**Why the split is worth recording rather than just re-ordering a list.** These are two different
kinds of work with different failure modes. The content items are bounded and well specified: 11
replacements and 7 expansions, each one a known workflow, and the only real risk is the sheer
volume of full-tree reads. The Signal Miner work is genuinely unsolved product design, it is
recorded as **the largest open product risk on the site** (Section 25, item 6), and it is the piece
where the tool currently overstates its own results. Interleaving them would have meant the risky
item competing for attention with a long grind. **Neither content item is blocked**, which is worth
stating so a later reader does not go looking for a dependency that does not exist.

- [ ] **Replace 11 of the 12 curated "zoop's X (2026 Edition)" strategies with newer "evergreen" versions; remove the 12th (decided/confirmed 2026-07-15, all source symphonies now in the full database, not yet applied to the curated set)**: user authored updated, more evergreen versions of the curated zoop 2026-Edition strategies. Full mapping, confirmed by the user:

  | Curated slug (2026 Edition) | Action | New evergreen symphony | New symphony_id |
  |---|---|---|---|
  | `zoops-2026-frontrunner` | Replace | zoop's Frontrunner | `zPBn8HkmTIQ5BEJdff0v` |
  | `zoops-holy-grail-2026` | Replace | zoop's Holy Grail | `qnFKsfL4NDBq1Wo5nCHk` |
  | `zoops-tqqq-long-term-2026` | Replace | zoop's TQQQ FOR THE LONG TERM | `qWe1S4jert7Wa79vu9FA` |
  | `zoops-excellent-adventure-2026` | Replace | zoop's Excellent Adventure | `vjJPExm36O3jAod0A0sH` |
  | `zoops-sometimes-tqqq-2026` | Replace | zoop's Sometimes TQQQ | `O5qvETvjnTxedtkNcn2N` |
  | `zoops-safety-checks-2026` | Replace | zoop's Safety Checks | `JnaYNpe3F1uL1mlScIZZ` |
  | `zoops-leveraged-tqqq-symphony-2026` | Replace | zoop's Leveraged TQQQ Symphony | `md0zmf8GE94tcvMRaGyr` |
  | `zoops-tqqq-200d-ma-3x-2026` | Replace | zoop's TQQQ 200d MA 3x Leverage | `Xaxkq31xztXXs12SExKM` |
  | `zoops-soxl-growth-2026` | Replace | zoop's SOXL Growth | `89DLODa3ARMwGUQP9cDx` |
  | `zoops-upro-ftlt-2026` | Replace **(confirmed, ticker changed UPRO→SPXL)** | zoop's SPXL FOR THE LONGTERM | `q0nwmcUDGKtg7sMydVxV` |
  | `zoops-kmlm-switcher-2026` | Replace | zoop's KMLM Switcher | `0SO8z4JkRVgiyhlkS2Xx` |
  | `zoops-manhattan-project-2026` | **Remove, no replacement** |, |, |

  All 11 new symphonies are refreshed with real backtest data in `data/database.json` as of 2026-07-15. **Applying this is still a bigger lift than a normal database addition**: replacing a curated strategy means re-running the full "Adding a Strategy from a Composer URL" workflow (logic tree, AI summary, `how_it_works`/`signals`/`risk_profile` content) for each of the 11 new symphonies, then removing all 12 old slugs (11 replaced + 1 removed outright) from `data/strategies.json`: not just adding the database rows, which are already in place.
- [~] **Curated-library expansion candidates, mined from `data/database.json` (drafted 2026-08-31; top 3 of Cohort A built in v1.38.0, remainder deferred)**: two cohorts of candidate additions surfaced by scanning the full database. Each new entry is a full "Adding a Strategy from a Composer URL" workflow, so the rest is batched future work, not a quick data drop.

  **Cohort A, most-remixed "originals" (primary target).** The site's existing "(Original)" featured entries follow a rule: feature the seed of a concept that the community has remixed heavily (TQQQ FTLT, KMLM Switcher, Holy Grail, etc.). A name-phrase clustering pass over all 6,669 database names (counting distinct symphonies per shared phrase, after stripping author-attribution chains like "DereckN / Garen / BrianE" and version/date tags) found the largest **non-featured** remix families. The **top 3 were built in v1.38.0** (owner picked the specific original symphony for each of those three, which is why their built IDs differ from the auto-suggested ones). The remaining seven, plus honorable mentions, are the reference backlog. "Recommended original" was chosen as the plainest name with the longest backtest, a proxy for earliest since inception date is not a stored field:

  | Remix family | ~Versions in DB | Recommended / built original | symphony_id | Status |
  |---|---|---|---|---|
  | Beta Baller | ~194 | Beta Ballers (Original), owner-picked V3.0.2 build | `mlgAKFuUIPZiCT0aV7ho` | **Built v1.38.0** |
  | TQQQ or Not | ~79 | TQQQ or Not (Original), owner-picked "TQQQ or not/Pop" | `g0J87gnk7SausotpUoCt` | **Built v1.38.0** |
  | Safe Sectors or Bonds | ~50 | Safe Sectors or Bonds (Original), "(29,32,1999)" | `DtlEo2Y1DWR7hngZkxTB` | **Built v1.38.0** |
  | WAM (Wash / Market Assassin) | ~45 | WAM | `PT0MPMH3D1jVPQ4dDSbL` | Deferred |
  | All Weather (Dalio template) | ~49 | All Weather (No Leverage, No Inverse) | `WEIWaUG6KezasMkBDejI` | Deferred |
  | Black Swan Catcher | ~41 | Pure Black Swan Catcher | `v54pjoQDNWLlPolNVW2b` | Deferred |
  | Tangency Portfolio | ~40 | Tangency Portfolio (~34y backtest) | `G6q9h6Gq10FU0T1Ie6db` | Deferred |
  | Uncorrelated (Mix) | ~40 | Uncorrelated 1 | `LHMIBySjwWKF7JL0ADnq` | Deferred |
  | Pop Bots | ~38 | OG v2.1 Double Pop Bots (BrianE, Oct 2011) | `g33fjz01aHQjbX0skf8p` | Deferred |
  | Sandy's Golden Dragon | ~34 | Sandy's Golden Dragon 3.0 | `mJKMWMDYGsQnkQBm1dEN` | Deferred |
  | Commander BND (honorable mention) | ~33 | Commander Bond Retirement | `LuL8N8qc4O1Q8D2WUdLA` | Deferred |
  | Four Corners (honorable mention) | ~31 | Four Corners (No Leverage) | `6iBNNfeGXhfQibyGohWf` | Deferred |
  | Cathie's One Night Stand (honorable mention) | ~28 | Cathie's One Night Stand (Hawk), long-backtest copy | `K5XxqnCKGXh8mRYKxFRX` | Deferred |

  **"NOVA" (~99) was excluded**: it is an author brand prefixed across many different strategies, not one remixed concept. Version counts are name-match approximations and the "original" picks are best-effort, not confirmed-earliest; where the owner supplied a specific original for a built entry, the built `symphony_id` above is authoritative.

  **Cohort B, trend-gap picks (cool, but deferred, per owner 2026-08-31).** A separate quality scan (backtest >=1,000 days, ARR >15%, max DD better than -55%, Sharpe >1.0, holdings verified) for strong symphonies in **trends the curated set does not cover**: crypto ([Interstellar Crypto BTC](https://app.composer.trade/symphony/DpGUZ9C2JlkeJSACC8G5/details) `DpGUZ9C2JlkeJSACC8G5`), global-macro/commodity (Combo 10 FrankRound `7ExFmXDSm50l7Ny4LKHP`), non-correlated ensemble (`YGuokJ1v4xLtBDony0QS`), unleveraged quality (NOVA Best No Leverage `REA8lSqNhmSPbAUxwjDb`), managed futures (TQQQ or BTAL or DBMF `NbHMZZQEaCwoWntsO1zF`), inflation hedge (Drawdown Protection Inflation v3 `FF4qXNAGS8FD1rhXexy9`), mega-cap stock momentum (IFF Power of Correlation `TwuMI72ZkbobsMWB91x3`), commodity all-weather (Steadfast Portfolio V5 `0OmkeZAS4w1uwSlxMWC2`), capital preservation (Magic Sauce `7fI331il6gG6QnoGClIO`), longest-track tactical (Primary Collection Gobi `ILmPIKhRAZNiYWaA5Km0`). **Deferred in favor of Cohort A.**
- [x] **Add "Leaderboard Ranking" as an option for the Screener (built 2026-08-15, v1.17.0)**: the V1.17 Leaderboard score/tier now surfaces inside the Screener, both ways as decided:
  - A **"Leaderboard Tier" select** in the filter grid, alongside the existing bucket filters. Options are cumulative ("S+ only", "S or better", … "C or better") rather than exact-match, to match the threshold semantics every other bucket filter already uses ("Over 12%", "Better than -30%") so the grid reads consistently.
  - **Sortable Rank / Tier / Score columns on all three `SCREENER_VIEWS`** (Overview, Risk-Adjusted, Distribution), via a shared `RANK_COLUMNS` spread so the three view definitions can't drift.
  - **Implementation note, scoring is global, not per-filter.** `computeScores()`/`computeTiers()` run once over the full eligible pool in a new `recomputeGlobalRanking()`, which fills a `rankBySymphonyId` index that both the Leaderboard and the Screener read. The original wording of this item ("against the Screener's already-bucket-filtered pool") was **deliberately not followed**, because re-scoring inside the filtered subset would make the tier filter circular: filtering to "S or better" would immediately re-tier the survivors, so the set could never settle, and the two tabs would disagree about the same symphony. `recomputeLeaderboard()` was reduced to filtering only, and `recomputeGlobalRanking()` runs before the Screener renders. Rows not yet refreshed are in the Screener pool but not the ranking, so they show a dash and are excluded when a tier floor is active.
- [x] **Homepage redesigned as a marketing/landing page (2026-07-15)**: `index.html`'s strategy grid (all 29 cards rendered inline) was removed entirely, now that `strategies.html` covers that listing on its own page (also sorted by longest backtest first, per the same-day change above). New structure: hero (rewritten copy framing the whole site, not just curated strategies; primary CTA "Browse Strategies" → `strategies.html`, secondary "Glossary" → `glossary.html`), a new 4-card "Explore the Site" grid (Strategies / Database / RSI Signals / Glossary, each linking out), and a new 3-step "How to use this site" section (Browse a strategy → Read the breakdown → Check live signals) tying the site's pieces together narratively. Modeled structurally (hero + eyebrow-labeled card-grid sections) after a landing page built for a sibling Azqato project, adapted to Composer Atlas's own design tokens and voice, not copied verbatim. New CSS: `.grid-4` (responsive 1/2/4-column grid, mirrors `.grid-3`'s breakpoints), `.explore-icon`, `.step-num` (numbered circle badge). Verified locally via desktop and mobile headless-Chrome screenshots, and confirmed all four explore-card links resolve correctly via a DOM dump, before pushing.
- [x] **SUPERSEDED 2026-09-09 (v1.81.0): the stats bar was removed from the homepage entirely** by
  owner instruction, and its four CSS rules, used by nothing else, went with it. The item below is
  kept because its reasoning is the reason the bar is gone. It called the values **hardcoded static
  values, not yet wired to live data, update by hand after each full database refresh**, and by
  2026-09-09 two of the five had drifted: **Last Refreshed read Sep 1, 2026 against an actual
  refresh date of Sep 6**, and **Median ARR read +50.7% against a measured +50.6%**. A
  hand-maintained figure on the highest-traffic page is a drifting number by construction, which is
  exactly what Section 27's rule forbids in a description and had never been applied to body copy.
  The alternative was the derived stats file the item itself proposed; the owner chose removal.
- [x] **Stats bar redesigned (2026-07-15)**: replaced the original 5 stats (Strategies/Best Sharpe/Top ARR/Concepts/Longest Backtest, all cherry-picked maximums from the curated 29) after a full scoring pass rating ~30 candidate stats 1-10 for homepage importance (see conversation record; the two "max" stats were flagged as a highlight-reel framing at odds with the site's Transparency Over Hype tenet). New 5 stats, chosen for honesty and site-wide scope rather than cherry-picked extremes: **Strategies** (6,640, full database scale), **Median ARR** (+48.7%, full-DB median, not a cherry-picked max), **Median Drawdown** (-34.7%, full-DB median), **Curated** (29, ties back to the hero's primary CTA), **Last Refreshed** (a freshness/trust signal). Currently **hardcoded static values**, not yet wired to live data, update by hand after each full database refresh until a small derived stats file (e.g. `data/site_stats.json`, written alongside `export_summary.py`'s existing output) replaces this; loading the full `database_summary.json` client-side just for these numbers was explicitly rejected, it would blow the homepage's own <500KB total-page-weight target (Section 10, Performance Targets) many times over. Also removed the now-dead `data/strategies.js`/`data/glossary.js` script tags from `index.html` (~331KB combined, no longer read by any homepage JS once the stats stopped being computed client-side and the strategy grid was removed): a real page-weight win, not just cleanup.
- [x] **Mobile overflow bug at ~390px width (hardened 2026-08-15, v1.16.7)**: paragraph text and the nav hamburger appeared to overflow/cut off at narrow mobile widths, sitewide (seen on `strategies.html` and `about.html`). Investigation: the shared chrome (hero, stats bar, footer) already uses `flex-wrap` + `clamp()` + `box-sizing:border-box`, and `about.html` is pure prose in `.container`, so no single wide element was the cause; the remaining realistic triggers were a long unbreakable token forcing width and the absence of any horizontal-overflow safety net. Fix: hardened `body` with `overflow-x: clip` (prevents stray sideways scroll without making `<body>` a scroll container, so `position:sticky`/`fixed` and the fixed nav are unaffected) and `overflow-wrap: break-word` (long tickers/IDs/URLs wrap instead of forcing width). **Caveat:** applied without an in-session browser repro (no headless Chrome available this session); should be visually re-verified at ~390px on a device, and if the clip is masking a specific offending element, that element can still be tracked down separately.
- [x] **Signal Miner: use a common sample window per run (done 2026-08-20, v1.19.0)**: raised 2026-08-20 while questioning the 2018 start date, and it is a **correctness issue independent of how far back the data goes**. `backtest()` divides by `N`, the length of the *entire* date axis, for both `tim` (`active / N`) and the mean feeding Sortino (`sumRet / N`). But a ticker that listed partway through the axis has `null` closes before that, so its signals can never fire there. The result: any signal touching a short-history ticker has its Time in Market structurally capped and its Sortino diluted by a stretch of history where the ticker did not exist. IBIT covers 30% of the current axis, so an IBIT signal cannot exceed `tim` 0.30 no matter how good it is, and its mean return is divided by roughly 3.3x more days than it could ever trade.

  Fix: compute the run's window as the intersection of the selected tickers' available history (start at the latest first-valid date among them, which is what the user proposed), and backtest over that window only. Then every row in a given run is scored on the same sample and the metrics are comparable again.

  **Consequences to handle:** metrics become dependent on the ticker selection, so results are no longer comparable *across* runs with different selections; the window in use must be shown prominently near the results. Selecting one recent ticker collapses the window for the entire run, so the UI should warn before a short-history ticker (already dashed in the chip list) drags an otherwise long sample down to two years.

- [x] **Signal Miner: extend price history before 2018** (done v1.20.1): `START_DATE` moved from `2018-01-01` to `2010-01-01`. The axis went from 2170 to **4183 trading days** (2010-01-04 onward) and `prices.json` from 1363KB to **2573KB**, close to the 2.6MB estimate. 2010 was chosen over 2000 because it covers the whole leveraged-ETF era (TQQQ, UPRO, SPXL, TNA, FAS, TMF all launched 2010 or earlier) while going further back mostly adds nulls: little of this universe existed before 2010, and the common sample window means one modern ticker in a selection collapses the window anyway. Every visitor pays the file size on load, which is what bounds it.

  **A latent bug was found doing this and is the real lesson.** `fetch_daily_closes` requested a hardcoded `range=10y` and then filtered to `START_DATE`, so the start date could only ever *narrow* that ten-year window, never widen it. The first re-run returned every ticker starting 2016-08-22 (exactly ten years back) and looked completely normal: correct schema, plausible prices, no error. The script now sends explicit `period1`/`period2` epoch bounds. **When changing the window, verify the reported first date actually moved**, because this class of bug is invisible in the output.

  **Reformed funds: accepted as a known tradeoff (owner decision, 2026-08-20).** SVXY was reformed in February 2018 from -1x to -0.5x, so its earlier history describes a different product. This was raised and **explicitly waived**: no per-ticker valid-date overrides, one global `START_DATE`. Signals on SVXY spanning early 2018 are measuring a blend of two products. Post-fetch check refines the scope: this affects **SVXY only**. Yahoo's VXX is the Series B ETN with no data before 2018-01-25, so there is nothing to splice there. Fund identity does not interact with the common sample window, which keys off listing dates.

  **Post-change data state (as of v1.20.1, before the v1.21.2 prune):** 55 of 80 tickers had full coverage; the rest list partway through, so the common sample window binds more often than it used to. One known data hole: 2026-08-11 is missing a close for 6 thin-volume tickers in the current universe (QQQE, VIGI, BNDW, KMLM, DBMF, LABU; SVIX was a seventh before it was pruned), 1 row in 4183, pre-existing and treated as a zero return by `backtest`.

- [x] **Signal Miner: multi-select rows and export one combined symphony** (done v1.22.0): suggested by Haverel Mink in the Composer Discord (2026-08-20). A checkbox per row plus **Copy combined JSON** emits one Frontrunner-shaped symphony from the whole selection.

  **Shape chosen: nested if/else-if ladder**, of the three options considered (ladder, equal-weight branches, AND). `composerThenChild(row)` was extracted from `buildComposerSymphony` so the single and combined exports build a rung through the same code path and cannot drift.

  **Corrected in v1.22.5: Composer ladders NEST.** v1.22.0 shipped on a wrong belief about the schema, that one `if` step could hold many sibling `if-child` branches with the last carrying `is-else-condition?: true`. It cannot. An `if` step takes **exactly two** children, a condition branch and an else, and rung N+1 sits **inside** rung N's else. The owner supplied a screenshot of a real Composer symphony whose rungs step one indent deeper each time, which is the nesting, not siblings. The combined export was unusable for five versions; the single-row export was never affected because with one rung both shapes coincide, which is exactly why the bug survived review. `composerLadderIf(rows, i)` now recurses: the deepest else holds the cash asset, every shallower else holds the next `if`. Structural verification ported to Python asserts the invariant directly, that every `if` has exactly two children and every else holds exactly one thing, rather than re-encoding the assumption it is meant to be testing, which is how the original port passed a broken builder.

  **Priority order is Calmar descending** (owner decision), which resolved the open ordering question without any reorder UI: ladder position is a real strategy decision, since branch 1 pre-empts branch 2 on every day both fire, so deriving it from a metric keeps the export deterministic rather than dependent on click order. `NaN` Calmar sorts last via an `-Infinity` fallback rather than landing arbitrarily.

  **Mixed-target selections rotate, they do not blend (disclosed v1.22.9).** A user pointed out that picking several targets for a Frontrunner is misleading because the export buys only one. That is right about the mechanics: an `if` ladder resolves to exactly one asset per day, so a selection spanning three targets is a rotation between them. It was left **allowed** rather than blocked, because a deliberate rotation is a legitimate strategy and forcing one target per export would remove it. Instead the combine bar states the consequence whenever the selection spans more than one target, including the point that each row's metrics describe its own `(signal, target)` pair standalone and therefore say nothing about the rotation. Single-target selections show no extra text, keeping the bar quiet in the common case.

  Selection is held in a `Map` keyed by `target|label` rather than by display index, so it survives re-sorting, filtering and the 100-row `DISPLAY_CAP`: a selected row can scroll out of the visible set and still export. A new run clears it, since those row objects belong to the previous result set.

  **The caveat now lives in the exported JSON only (v1.22.4).** The combined symphony's behaviour is *not* the combination of the rows' displayed metrics: each was backtested standalone holding cash when off, so chaining them produces a strategy nobody has measured, and a ladder of individually strong signals can be worse than any of its parts. **The caveat is no longer surfaced anywhere in the product (owner decisions, 2026-08-20).** First the explanatory paragraph under the combine bar was removed as too much text (v1.22.4), leaving the warning in the exported symphony's `description`; then that sentence was cut too (v1.22.6), so the description now states only what the export is and how its branches are ordered. The caveat remains true and remains documented here; it is simply not repeated to the user. Computing real metrics for the composed rule remains open and would need a fresh backtest of the composed condition.

  Verified by porting the builder and asserting: branch order matches Calmar descending, `NaN` sorts last, exactly one else child and it is last, each branch holds its own row's target, AND-pair rows keep both conditions, and all node ids are unique.

- [x] **Signal Miner: Calmar as the default ranking metric** (done v1.22.0): the table's initial `sortKey` moved from `sortino` to `calmar`, and `saveResults` keeps the top 100 by Calmar to match, so the snapshot preserves the same rows the user was ranked on. This only became sensible after the v1.21.0 Calmar fix: while Calmar divided *total* return by drawdown it grew with backtest length and was not comparable across runs, so ranking by it would have rewarded whichever run had the longest window. Snapshot key bumped to `v4` because stored rows were ranked by a different metric.

  **Follow-up, resolved in v1.22.1:** the AND-pairing survivor cap was left ranking by Sortino when the display metric changed, so the pool feeding pairing was Sortino-selected while the table ranked by Calmar. It now ranks by Calmar too, with the same `-Infinity` NaN fallback used by the ladder builder. This was split into its own release deliberately: it changes which survivors reach `SURV_CAP` and therefore **which AND pairs exist at all**, so it alters results rather than just their order, and folding it silently into a display-metric change would have made that invisible.


- [x] **Signal Miner: standardize the window grid, expand to sixteen families, pack specs columnarly** (done 2026-08-20, v1.23.0 and v1.23.1). See "The search space" and "Specs are stored as columns" in Section 12 for the full write-up. Summary of what landed: one fifteen-window log-uniform grid for every family, replacing four inherited grids; RSI levels stepped by 2 (41 levels); uniformly stepped, data-sized level brackets for cumulative return and drawdown; six families to sixteen covering all nine Composer functions, eleven on by default, grouped Price / Return / Risk; `estimate()` and `buildSpecs()` collapsed onto one `countSpecs()`; specs packed into seven typed arrays. A maximal default run went from 3,042,720 to 4,800,024 signals.

  **Three things were tried and rejected, recorded so they are not re-proposed:**
  - **sqrt-scaling RSI levels.** Measured wrong. It assumes the distribution is symmetric about 50, and a trending asset sits above 50 for years, so the scaled grid drifts off the part of the range that separates days. sqrt scaling remains correct for cumulative return and drawdown, which accumulate.
  - **A 2-percentage-point step for every level grid.** Impossible for std dev of return and moving average of return: their entire useful range is narrower than one such step. They carry equivalent resolution in their own units instead. The constraint is confined to those two families and limits nothing else.
  - **De-duplicating near-identical result rows** (several rows differing only in a window that produces almost the same series). Raised by the assistant, **declined by the owner 2026-08-20**: "i dont think its actually an issue. for 252 days this makes sense." Do not re-open it as a correctness problem; if it is ever revisited it is a presentation choice, not a bug.

---

**Next up on the Signal Miner, in the order agreed 2026-08-20, revised 2026-08-21.** These are the items worth doing on their own merits. The largest piece of the original v1.23 plan, OR combining and Composer's any/all conditions, was **deferred indefinitely by the owner on 2026-08-21** and now sits at the bottom of this section with its full rationale preserved.

- [x] **1. Recalibrate the estimate warn/stop thresholds** (done 2026-08-21, v1.24.2). Now **600,000** for the yellow estimate line and **1,200,000** for the confirm, replacing 45,000 and 100,000. The numbers come from a measurement rather than from scaling the old ones: Pass 1 runs at roughly **4.5 ns per spec-target-day** (timed in headless Edge with the throttle disabled), so against a 3,930-day sample with one target the confirm now sits at about 1.8 minutes at Medium and an ordinary eight-ticker run (91,232 specs, about 8 seconds) says nothing at all.

  **Known blind spot, left in deliberately.** These are spec counts, not units of work, so a three-target run does three times the work at the same count and does not warn any earlier. Projecting wall time would fix it, at the cost of turning an exact quantity into a prediction that varies with the visitor's hardware. If this is ever revisited, that is the trade to weigh.

- [x] **2. Skip cross-ticker operand pairs for the price-scale families** (done 2026-08-21, v1.24.0). `map_cmp`, `ema_cmp` and `stdp_cmp` now carry `same: true` and pair only a fast window against a slow window on one ticker. A default run fell from 4,800,024 signals to 3,936,096, a saving of 863,928 or 18.0%.

  **The measurement changed the argument, which is worth recording.** The item was written on the assumption that cross-ticker price pairs are constant-false. Measured across all 72 tickers, 2010-2026, at windows 5, 21, 63 and 252, only **42.5%** of `map_cmp` cross pairs never separate a day, so the original claim in this document was too strong. The real defect is inertness, counted as state changes over the sample:

  | Family | Cross-ticker pairs | Same-ticker pairs |
  |---|---|---|
  | `map_cmp` | median **1** flip, 94.5% flip fewer than 12 times | median 51 flips, 7.4% inert |
  | `ema_cmp` | median **1** flip, 94.3% flip fewer than 12 times | median 53 flips, 8.3% inert |
  | `stdp_cmp` | median 9 flips, 54.1% flip fewer than 12 times | median 26 flips, 26.4% inert |
  | `rsi_cmp` (control) | median 212 flips, 2.5% inert | median 455 flips, 0.0% inert |
  | `cum_cmp` (control) | median 223 flips, 1.5% inert | median 134 flips, 1.2% inert |

  The median cross-ticker price pair changes state **once in sixteen years**: a date wearing a condition's clothes rather than a signal. The two scale-free controls flip hundreds of times, which is what establishes that the effect is about price scale and not about comparison families generally. `stdp_cmp` is the weakest of the three at 54% inert, and its flag is the first to reconsider if coverage is ever missed.

- [x] **3. Re-measure the memory ceiling on the new search space** (done 2026-08-21). Measured, not assumed, and the answer changed what the Miner's limiting resource is.

  Memory, from `python scripts/run_harness.py memory`, one target (QQQ) at Max with the throttle disabled:

  | Selection | Specs | Rows stored | Sample days | Peak heap | Bytes per row |
  |---|---|---|---|---|---|
  | 20 tickers | 390,320 | 364,526 | 2,381 | 127 MB | 366.6 |
  | 40 tickers | 1,321,440 | 1,180,689 | 1,747 | 477 MB | 423.9 |
  | 72 tickers (all) | 3,936,096 | 3,181,976 | 270 | 1,011 MB | 333.1 |
  | 51 tickers (full history) | 2,064,072 | 1,886,073 | 3,904 | 977 MB | 543.3 |

  **Read the last row, not the third.** Selecting all 72 tickers looks like the maximal run and is not: IBIT and ETHA cover only ~30% of the date axis, so including them collapses the common sample window to 270 days and each stored row is cheap. The 51 full-history tickers are what a real maximal run looks like, and it costs about the same heap for half the specs.

  **The heap ceiling read 4,192 MB**, against the 3,586 MB recorded earlier on the same 48GB machine. Both figures are from the same hardware, so the ceiling is a property of the browser build and moves between versions. Treat any single reading as approximate and do not design to within 20% of it.

  **Conclusion: memory is no longer the binding constraint.** A genuinely maximal run peaks at about **24% of the ceiling**. v1.22.13 (no array per signal) and v1.22.15 plus v1.23.0 (columnar rows, columnar specs) between them took the headroom from "crashes near 2,000,000 signals" to "four times the largest run the tool can currently produce." What binds now is time.

  **Time, from `python scripts/measure_throughput.py`.** This needed a separate rig, because a timed run cannot use the harness in `scripts/harness/_edge.py` at all: that rig depends on `--virtual-time-budget`, and under virtual time the page clock is paused during synchronous compute and fast-forwarded through idle gaps. The same driver reported 1,154 ms of elapsed time for a 4-ticker run and 4,095,136 ms for an 8-ticker one, and summed `busyMs` read 63 ms and 70 ms for runs that really took 3.7s and 9.4s. At 16 tickers the accumulated virtual time exceeded the budget and Edge shut the browser down mid-run. `measure_throughput.py` therefore launches Edge itself with no virtual time and no `--dump-dom`, and the driver reports through `console.info`, which the parent process reads off stderr and timestamps with its own clock.

  | Compare tickers | Specs | Work (spec-target-days) | Run | ns per unit |
  |---|---|---|---|---|
  | 8 | 91,232 | 358,632,992 | 9.48s | 26.45 |
  | 16 | 268,992 | 1,057,407,552 | 26.21s | 24.79 |
  | 24 | 533,280 | 2,096,323,680 | 49.97s | 23.84 |
  | 32 | 884,096 | 3,475,381,376 | 81.06s | 23.32 |

  Linear across a 10x range: **23 ns per spec-target-day unthrottled, plus ~1.7s fixed per run** (cache building and rendering). The drift down the last column is that fixed cost being amortised, not a scaling effect.

  **Correction.** An earlier version of this section, of the `SIGNAL_WARN_CAP` comment in `signal-miner.html`, and of the v1.24.2 patch note gave **4.5 ns per spec-target-day**, and all three were shipped to production before the error was found. That number came from `performance.now()` readings taken inside a driver running under virtual time, so it was not a measurement of anything. The real figure is **five times worse**. Nothing timed from inside the virtual-time rig should ever be quoted.

  **What this means for items 1 and 2.** The recalibrated thresholds still land in a sensible place: `SIGNAL_WARN_SOFT` (600,000) is about 4.6 minutes at Medium, `SIGNAL_WARN_CAP` (1,200,000) about 9.1 minutes, and a full 72-ticker default run about 30 minutes. So the confirm dialog is now guarding **the user's afternoon, not the tab's memory**, which is a better thing for it to guard but was not what its wording said. **Reworded in v1.24.5**: it now leads with a projected duration from the measured 23 ns figure, divided by the duty of the selected CPU setting, and states plainly that a run cannot be cancelled. Item 2's restriction of the three price-scale families removed ~2.6M specs from a maximal run, which at 23 ns per unit is roughly **four minutes** off it.

- [x] **4. Persist the headless Edge harnesses into `scripts/`** (done 2026-08-21). They now live in `scripts/harness/` behind one entry point:

  ```
  python scripts/run_harness.py verify      # spec lockstep + dual-path equality
  python scripts/run_harness.py live        # end-to-end run, window, rendering
  python scripts/run_harness.py inertness   # cross-ticker operand degeneracy
  python scripts/run_harness.py memory      # peak heap
  python scripts/run_harness.py settings    # persistence and the Default button
  python scripts/run_harness.py plateau     # parameter plateau scoring (V2.2 item A)
  python scripts/run_harness.py all         # the four gates
  ```

  `verify`, `live`, `settings` and `plateau` gate any change to `signal-miner.html`; the other two are measurement tools. `plateau` (v1.73.0) is the strictest of the four, because the thing it checks has no second symptom: nothing downstream reads the plateau columns, so a wrong number there could sit unnoticed indefinitely. It therefore recomputes every value independently instead of re-reading the page's own. v1.73.1 added the lesson that being strict about the numbers is not the same as being right about the product: it now runs a second pass at the **shipped default settings** and asserts that no cell on that view is empty, because the first version was strict about a hundred values that a visitor never saw. It also flushed out a **thirteenth** trap that had nothing to do with it. `settings` began hanging for its full 900-second wall clock with no output and no JavaScript error, and the obvious reading was that the new feature had broken the page. It had not: the hang reproduced against an **unmodified** page and an unmodified hook, in **2 of 3** baseline runs, and only ever on the **second** Edge launch of the two-phase pair. Edge schedules sync and component-update work at startup once a profile has state to reconcile, so under `--virtual-time-budget` the tab never reaches the idle point `--dump-dom` waits for. `--disable-sync --disable-component-update` fixes it: 6 of 6. Phase 1, on an empty profile, always passed, which is what made it look like a page bug, and the intermittency is why a green run proves nothing here. It also contributed a twelfth trap: **a default-settings sample can be a sample of one.** Its first version asserted across "the rows on screen" and reported 100 rows of which one was a single signal, because at the shipped pairing setting the top 100 by Calmar is 99 combined AND rows. Every single-row assertion was resting on that one row and still printing `ok`. When a driver asserts over whatever is on screen, it must assert *how much* is on screen too. `settings` (v1.24.7) is the first harness to use the two-invocation shared-profile pattern that `_edge.py` always supported and nothing exercised: it tests `localStorage`, so phase 1 writes and phase 2 reads back in a **new browser process** over the same profile, with `run_harness.py` deleting that profile first so phase 1 genuinely starts from nothing. All four traps are encoded once in `scripts/harness/_edge.py` and written up in `scripts/harness/README.md`: the page is an IIFE so internals must come through a spliced `window.__t` hook; reassigned bindings must be exposed by **getter**, since capturing them by value fails silently and makes two harness cases report identical numbers; the CPU throttle feeds back on itself under `--virtual-time-budget` and must be neutralised in the test copy only; and the dumped DOM must be read as **bytes** then decoded UTF-8. Two more were added from this session: `window.confirm` auto-dismisses under `--headless=new` and is stubbed to true, and `renderResults()` is debounced so the results panel becomes visible *before* the table body is filled, meaning a driver must wait on the row count rather than on the panel or it is an intermittent race.

  **What was not recovered.** The earlier behavioural A/B (`runeq.py`) and snapshot round-trip (`runsnap.py`) harnesses were lost with the session that created them and are not reconstructed here. `verify` and `live` between them cover most of what the A/B did. Rebuilding the snapshot round trip is worth doing when `localStorage` behaviour is next touched; it needs two Edge invocations sharing one `--user-data-dir`.

- [x] **5. `scripts/check_live.py`: lint what Cloudflare actually serves** (done 2026-08-21). Fetches each live clean URL, compares byte-for-byte against the committed file (normalising line endings, since the working copy is CRLF), and checks a list of markers that must be present and a list that must be absent. Present-markers name the newest shipped behaviour so a stale deploy is caught even when the byte-compare is confused; absent-markers name things a previous version had, which is what catches a deploy that rolled backwards. Exits non-zero, so it can gate a release. `python scripts/check_live.py signal-miner` checks one page.

- [x] **6. `.assetsignore` so Cloudflare stops serving `docs/`, `scripts/` and `README.md`** (done 2026-08-21). `wrangler.jsonc` sets `assets.directory` to `"."`, so every file in the repository was published as a side effect of deploying the root. Nothing secret was exposed, but this document is an internal roadmap and had a public URL. Also excludes `wrangler.jsonc`, `.github/`, and the `_harness_*` and `_wf-mockup.html` local files as a second line of defence behind `.gitignore`.

- [x] **7. Report *measured* CPU duty rather than the nominal figure** (done 2026-08-21, v1.24.3). The run status line now prints the fraction of wall time actually spent computing, accumulated over every batch, instead of the duty the throttle was asked for. The first five batches still show the nominal figure prefixed with `~`, since a duty measured over one batch is noise. At High, Medium and Low the two agree; at **Max** the requested sleep is frequently shorter than the roughly 4ms floor a browser applies to a nested `setTimeout`, so delivered CPU lands nearer 64% than the 80% on the label. **The ceilings themselves are unchanged and stay that way**: they are capped for heat, on hardware belonging to whoever opens the page. The dropdown describes what is requested, the status line now describes what is delivered.

- [x] **8. Indicator warm-up is charged to the sample-window start** (done 2026-08-21, v1.24.1). `windowInfo(syms, warm)` now starts the window after the longest window in the active grid, so every row is scored on an identical set of days. This was a **ranking bias**, not a precision issue: a 252-day signal had 247 fewer days than a 5-day signal in which to earn return while competing for the same leaderboard slot, so long windows were systematically penalised. Costs 252 days out of 4,183, about 6.0%, and the cost is named in both the estimate line and the results meta line. Per-spec window starts were rejected: they waste no data but make rows non-comparable in a different way and push a branch into the hottest loop. `frac` still deliberately excludes the warm-up so the "limited by TICKER" hint keeps pointing at the ticker.

---

**Robustness items, raised 2026-08-21.** Three of them, attacking the same weakness from different directions. **A shipped its diagnostic half on 2026-09-03 in v1.73.0; B and C remain under design, committed to no version and unbuilt.** They are recorded here because the reasoning is worth keeping. The Miner searches 4.8M signals against one target, so the top of its leaderboard is selected for luck as much as for skill. Everything in the numbered list above makes the search bigger, faster or cheaper. These three ask whether a winning row is *real*. A and B are the two measurements; C is the layer that turns them into something a visitor can act on.

- [~] **A. Parameter plateau scoring: rank on the neighbourhood, not on the peak.** Owner's idea, 2026-08-21. **The diagnostic shipped 2026-09-03 in v1.73.0; the re-ranking did not, and is the only part still open.** See the closing subsection below for what was built, what the first real run measured, and where the design departed from the reasoning here. Everything from this point to that subsection is the original 2026-08-21 argument, kept as written. A row's rank says nothing about whether the parameter it found is a knife edge. Suppose the leaderboard shows `RSI(10) of SMH < 23` at 2.8 Calmar. If `< 22` and `< 24` score 0.9 and 1.1, that 23 is a spike: the rule works at exactly one threshold and nowhere near it, which is what over-fitting looks like from the inside. If instead the whole span from 20 to 28 scores between 2.4 and 2.9, that is a **plateau**, the node fires usefully across a range of values, and the result is far more likely to be a real effect than an artifact of where the lattice happened to land.

  **Why the Miner is unusually well placed to do this, and why it is nearly free.** The search is already exhaustive over a dense, uniformly stepped lattice. Every neighbour of a top-ranked row **has already been evaluated in the same run**. So the neighbourhood statistic is a lookup into work already done, not a second pass. Compare that with walk-forward validation (item B), which costs an entire additional backtest over held-back data. This is the cheapest robustness test available to this tool, and it may be the single highest value-per-unit-of-work item on the whole list.

  **v1.23.1 is a prerequisite that already landed.** The old hand-written level ladders thinned out at their extremes (drawdown ran 2, 4, 6, 8, 10, 13, 16, 20), so "one step away" meant different things in different parts of the range and a neighbourhood width was not comparable between rows. Every percent-quoted grid now steps by a constant amount within a window, which is exactly what makes a plateau width meaningful. RSI steps by 2, cumulative return and drawdown by one percentage point, std dev of return by 0.1, moving average of return by 0.02.

  **Two neighbourhood axes, and they are not the same shape:**
  - **Level.** Only exists for the four `lvl` families. Uniform within a window, so a neighbourhood is plus or minus *k* steps and the plateau width can be quoted in real units ("holds from 20 to 28").
  - **Window.** Exists for every family. The window grid is deliberately **log-uniform** (5, 7, 10, 12, 14, 21, 26, 30, 42, 50, 63, 100, 126, 200, 252), so neighbourhood here must be measured by **index position, not by value**. Plus or minus two index steps at the short end spans 5 to 12 days; at the long end it spans 100 to 252. That is the correct behaviour, since a 10-day and a 12-day window are near-identical series while 100 and 252 are not, but it means the two axes cannot be scored with one formula.

  **What to compute (decide before building, roughly in order of ambition):**
  1. **Neighbourhood median of the ranking metric.** Simplest and probably the strongest single number. A spike has a median far below its peak; a plateau has a median close to it.
  2. **Plateau width.** How many *contiguous* neighbouring levels hold the metric within some tolerance of the peak, say 20%. Quotable directly in the table ("holds 20-28") and the most legible thing a user could see.
  3. **Rank on the neighbourhood median instead of the peak.** The strong version of the idea. Everything above is a diagnostic bolted onto an unchanged leaderboard; this changes what the leaderboard *is*, and removes the incentive for knife edges to reach the top in the first place. Worth costing, but it is a genuine change in the tool's contract and should not be done silently.

  **Cautions and open questions, so they are not rediscovered:**
  - **Holes in the neighbourhood.** The results table holds only survivors. A neighbour that failed the Time in Market floor or the Max DD ceiling was pruned, so a naive lookup would read a spike where there is simply a missing row. The neighbourhood must be read from the Pass 1 metric store *before* filtering, or holes must be counted and reported rather than treated as zeros. Pass 1 already computes metrics for every spec, so this is a question of what is retained, not of extra work.
  - **One-sided neighbourhoods at the bracket edges.** A cumulative-return level sitting at the top of its scaled grid has no neighbour above it. Score it one-sided and say so; do not silently pad.
  - **`cmp` and `self` families get the window axis only.** No level axis exists for them. A comparison row has *two* windows, so its neighbourhood is two-dimensional and the cheapest useful version probably perturbs each independently rather than jointly.
  - **Combined (two-condition) rows** have the union of both conditions' axes. Almost certainly out of scope for a first version; score singles only and say so. **This was written, shipped, and was wrong.** See the note below.
  - **This is not the de-duplication idea, which the owner declined on 2026-08-20.** That was about hiding near-identical rows from the table. This is the opposite: it deliberately *reads* those near-identical rows and uses their agreement as evidence. If anything it retires the de-dup question, because a cluster of similar rows stops being visual clutter and becomes the signal itself.

  **From diagnosis to construction: mine the band, not the point (owner, 2026-08-21).** Everything above treats the plateau as a *measurement* bolted onto an unchanged result. The stronger reading, and the one to build toward, is to make the plateau the thing the Miner actually emits. Three steps, increasing in ambition, and the first is close to free.

  1. **Recentre the exported threshold on the plateau instead of the peak.** The cheapest possible use of the neighbourhood, and it adds no specs at all. If a row wins at RSI 78 and its neighbourhood shows 74 through 82 all working, export 78 only when it is near the centre; otherwise export the centre of the plateau. The winning lattice point is merely where noise happened to peak *inside* the plateau, while the centre is the better estimate of where the real effect sits. This is pure post-processing of a run that already happened.

  2. **Band conditions as a first-class node: `77 < RSI < 79`.** This is a genuinely different node shape from anything the Miner emits today, and it is worth being precise about why, because two different things are both called knife edges. A threshold like `RSI < 78` is **not** a knife edge in *firing* terms: a day at RSI 40 fires it too. The fragility is in the parameter, not the trigger. A band is different in kind. It fires only inside a range, which is the natural way to say "stretched but not yet broken", and it is exactly the shape "fires on 77 to 79" describes.

     **The export side is already done.** Composer expresses a band as a `compound` with `operator: 'all'` over a `>` and a `<`, which is precisely what `composerThenChild` already emits for AND-combined rows. The mining side is new: a spec carrying two levels rather than one.

     **Cost, and the bound that keeps it affordable.** Do not mine all level pairs. Cumulative return at 252 days has 139 levels, so `C(139, 2)` is **9,591 bands where there are 139 thresholds**, a 69x blow-up on that one window; across the family it would take `cum_lvl` from 123,408 specs to roughly **2 million**, the size of an entire comparison family, for a single quantity. Mine instead a **small fixed set of band widths centred on each existing level**, say 3, 5, 9 and 15 steps. That is four bands per level rather than `C(L, 2)`, which takes `cum_lvl` from 123,408 to about **246,800**, still around 5% of a run. Width belongs in the spec as a **step count, not a percentage**, so that it stays comparable across the scaled grids where a step means a different absolute amount at every window.

     **The two features feed each other, which decides the build order.** Plateau scoring finds bands *without mining them*: a plateau **is** a band, read off neighbours that were already computed. So build the scoring first, look at what plateau widths actually turn up in real results, and let the data choose the width set instead of guessing it. If real plateaus cluster at 5 to 9 steps, mine 5 to 9.

  3. **Scale in and out across the plateau rather than switching at its edge.** The furthest step, and the largest change to what the Miner produces. Every row today is binary: the signal fires, you hold the target, otherwise cash. A plateau invites a graded response instead. Rather than 0% below RSI 78 and 100% above it, ladder across the plateau: a third of the position at 74, two thirds at 78, the whole position at 82. That is smoother, far less sensitive to any single threshold, and much closer to how good symphonies are actually written.

     **Three cautions, because this one is not cheap.** It changes the *output shape* rather than its parameters, so the backtest must carry fractional positions; it currently carries a `Uint8Array` of in-or-out, which is part of why Pass 1 is fast, and widening that touches the hottest loop in the tool. The export needs a weighted group step rather than the bare `asset` step inside `if-child` that `composerThenChild` emits today, and **Composer's weighting schema must be confirmed before anyone budgets this**, since it has not been verified in this repo. And it multiplies the search if approached naively, because a three-rung ladder is a *triple* of levels. It must therefore be built **on top of** the plateau measurement, using the measured plateau edges as the ladder rungs, rather than searched freely. Built that way it adds essentially no Pass 1 specs, and that is the only version worth doing.

  ---

  **What was actually built (2026-09-03, v1.73.0), and where it departs from the above.**

  Two read-only columns on the results table and no change to the ranking. **Plateau** quotes the range either side of a row's setting that stays within 20% of it, in real units (`20% to 28%`, `21d to 63d`). **Nbhd** is the median of the ranking metric across the row and its immediate neighbours. Both follow the active sort, so "neighbourhood median" always means the median of whatever the table is ranked by. Points 1 and 2 of "what to compute" are done; point 3 is not, and is now a decision with evidence rather than a guess.

  **The one place the reasoning above was wrong: neighbours must NOT be read from the Pass 1 store.** The caution about holes said to read the neighbourhood from the metric store *before* the Time in Market and Max DD filters. That is right about the user-tunable filters and wrong about the store itself, because the store applies a filter of its own that the caution did not account for: Pass 1 only pushes a row when `total > 0` and Sortino and Calmar are finite. So a losing neighbour is not in the store either, and reading the store would report a plateau across the survivors of an invisible filter. A losing neighbour is not a hole. It is a low number, and it is precisely the number that should end a plateau. Each neighbour is therefore **re-evaluated directly** against indicator caches already in memory. The harness proves the distinction rather than asserting it: it scores specs at the far ends of a level grid, which never fire and have a total of exactly zero, and found 17 of 40 probed to be specs Pass 1 had discarded.

  This costs more than the lookup the entry imagined, but not much more, and the entry's cost argument survives: a fixed ring of at most 12 backtests per row, computed only for the <=100 rows on screen and memoised per row and metric. At the measured 23 ns per spec-target-day that is about a millisecond per row.

  **Neither column is sortable, and that is forced rather than chosen.** The value exists only for the rows on screen. A sort on it would order a sample of 100 while appearing to have ordered a set of millions.

  **Combined AND rows are scored too, and the roadmap bullet above saying they should not be was wrong in a way worth keeping on the record.** Its reasoning was that two conditions give a product of two lattices with no honest one-dimensional plateau to quote. That is true and it is beside the point: with pairing at its shipped default the top 100 by Calmar is **99 combined rows and one single**, so the singles-only version rendered a wall of dashes on the view a visitor gets without touching anything. A diagnostic that is invisible by default is not a diagnostic. The owner saw it on the live page the day it shipped and asked whether it was meant to look like that.

  Worse, the evidence was already in hand. The `plateau` harness had reported "100 rows, 1 single, 99 combined" a day earlier and it was read as a **test-sampling** problem, fixed by turning pairing off in the driver, when the same sentence was also a **product** problem. Turning pairing off in a test is precisely how you stop the test from telling you what the default looks like.

  The product of two lattices is still not searched. Each condition's parameters are perturbed **independently** while the other condition is held exactly as it is, the AND is rebuilt, and the row is re-backtested. That is the same one-axis-at-a-time move already used for the two windows of a comparison family, so the cost stays linear in axes: about 24 backtests for the widest combined row against 12 for a single. The cell quotes the tightest axis prefixed by which condition it belongs to (`1: 12d to 14d`); the tooltip names all of them and says explicitly that they are not a joint search.

  **What the first real run measured**, QQQ target against SPY/QQQ/TLT, min period 12: the top 100 **single** signals with pairing off, plus 25 **combined** rows from the shipped default.

  | Plateau width (steps) | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
  |---|---|---|---|---|---|---|---|---|
  | Single rows (of 100) | **18** | 25 | 19 | 17 | 15 | 3 | 1 | 2 |
  | Combined rows (of 25) | **22** | 3 | 0 | 0 | 0 | 0 | 0 | 0 |

  The neighbourhood median runs at **0.89** of the row's own Calmar at the median and **0.73** at the tenth percentile. **Eighteen of the top hundred singles hold at exactly one setting and nowhere adjacent**, which is what over-fitting looks like from the inside, and until this shipped they were indistinguishable from the other eighty-two.

  **The combined row finding is the sharper one, and it was unobtainable until the scope changed.** 22 of 25 combined rows have a plateau width of **zero** on their tightest axis. Some of that is arithmetic rather than fragility, since quoting the tightest of up to six axes is a minimum over more draws than a single's two. But not all of it: a combined row has to survive perturbation on both of its conditions, and the top of the pairing leaderboard is where two separately unremarkable signals happen to intersect on a handful of days. These are the rows the leaderboard puts at the top by default, and they are the rows least likely to survive a parameter nudge. That is worth a reader's attention and it is exactly what the diagnostic exists to show.

  **This is the evidence the band-mining step (2 below) asked for.** Real plateaus cluster at 1 to 4 steps, not the 3, 5, 9 and 15 guessed there. If bands are mined, that is the set to mine. The caveat is that the search radius is 4 steps on the level axis, so a width of 4 is a floor rather than a measurement: 87 of 394 axis ends were still holding when the search ran out. A wider ring would settle whether the tail beyond 4 is real, and costs one backtest per extra step per row.

  **On re-ranking (point 3), which remains open.** The median-to-peak ratio has a usefully wide spread (0.73 to 1.00 between the tenth and ninetieth percentiles), so ranking on it would genuinely reorder the leaderboard rather than reproduce it. That is the argument for doing it. The argument for not doing it silently is unchanged, and there is now a third option the entry did not consider: leave the ranking alone and let the reader sort by neighbourhood median. That is currently impossible for the reason given above, and making it possible means computing the ring for the whole result set, not for a hundred rows. That is a real cost and would need measuring first.

  **Verified by `scripts/run_harness.py plateau`,** a fourth headless gate. It recomputes every plateau independently rather than re-reading the page's own numbers, including rebuilding each combined row's AND from its own boolean pass: **594 axis ends and 560 in-band steps** checked against its own backtest, and **125 neighbourhood medians** reproduced exactly. It runs two passes, and the second one is the point: pairing back **on at the shipped default**, asserting that the number of empty plateau cells on that view is **zero**. That single assertion is the regression test for the bug described above, and no amount of care in the first pass would have produced it. Two further things that could only have been caught this way: the driver's first version rested its entire single-row sample on **one** row; and two independently derived accounts of the same 394 axis ends disagreed by exactly 20, which turned out to be the page saying a plateau "may run wider" in the one case where the grid ended a step later. A third check was added with the combined rows and immediately earned its place: a row perturbed by **zero** steps must reproduce the metric the results table already holds for it, or every neighbour is being compared against a different backtest than the row itself. Both traps are recorded in `scripts/harness/README.md`.

- [ ] **B. Walk-forward validation.** Discussed at length 2026-08-21. A local UI mockup with dummy data **exists and is finished as a mockup**: `_wf-mockup.html`, gitignored and also listed in `.assetsignore`, showing the validation panel, an in-sample against out-of-sample Calmar scatter, and a results table with paired cells and verdict badges. Nothing behind it is built. Keep the file until B is either built or dropped, since it is the only artifact describing what the panel should look like. Every number the Miner reports today is in-sample: the search picked its winners by looking at the same days it then scores them on. Walk-forward holds back a block of recent history, runs the search on the earlier block only, and then scores the winners on days the search never saw. It is the only test here that can actually *fail* a rule.

  **Design points already settled in discussion:**
  - It cannot live in section 3. That panel's copy promises its four filters re-filter live with no re-run, and changing the training window requires a fresh Pass 1. It needs its own panel after it.
  - **Purging and embargo are a non-issue for this tool.** `backtest` uses a strictly one-day horizon (it reads `arr[i-1]` to take `lret[i]`), so a single split point leaks nothing across the boundary. This is a real simplification relative to the general walk-forward literature and it should be stated rather than quietly assumed.
  - **Indicator warm-up must be charged to the training block.** A 252-day signal needs 252 days before its first valid value, which interacts directly with numbered item 8 above. The date readout should show the warm-up cost explicitly rather than burying it.
  - **The dummy data in any mockup must decay honestly.** Most rows should fall apart out of sample, with a handful holding up, because that is what real walk-forward output looks like. A mockup where everything survives would misrepresent the feature it is selling.

  **A and B are complementary, not alternatives.** Plateau scoring is cheap and uses every day of data; walk-forward is expensive and deliberately throws data away. A rule that has a wide plateau *and* holds up out of sample is worth taking seriously. A rule with neither is almost certainly noise, and today the tool cannot tell you which it is looking at.

- [ ] **C. An overfitting rating on every row.** Owner's idea, 2026-08-21. A and B each produce one diagnostic. This is the layer that combines them, plus what the tool already knows, into a per-row judgment of how much to trust the number next to it.

  **The concept in one paragraph.** The Miner searches millions of candidates and reports the single best number it found. That number is the maximum of a very large sample, so it is optimistic by construction, and nothing in the tool currently says so. C adds a second question next to every result: *not how good is this, but how much of this is real.* It answers by attacking the result from three independent directions, all of them cheap because they re-use work the run has already done. **Does the rule survive its own neighbourhood** (C1: move the threshold and the window slightly, see if the result holds). **Does it survive its own history** (C3: remove a year, remove the best few days, split the sample in half). **Does it beat what luck alone would produce** given how many candidates were searched (the N-adjustment, which is the only one that addresses the search size directly). The output is deliberately modest: a badge, one sentence of margin, and the option to see the evidence. The tool's job here is to argue with its own leaderboard.

  **The three sub-sections below are the design as it stands.** C1 is the neighbourhood grid the owner specified, with the two assumptions behind it measured rather than assumed. C2 turns it from a rating into a filter and settles the presentation. C3 adds the return-series family from a practitioner checklist, and marks the one item on that checklist that is the wrong test.

  **Build it as a scorer, never as a search.** Every input below is either already computed during a run, or is a lookup into specs the run has already evaluated. Nothing here should trigger a second Pass 1. If a proposed component needs its own pass, it belongs in A or B, not here.

  **The input the tool has and does not use: how many candidates it looked at.** This is the most important item on this list and the cheapest. A search over 4,800,024 candidates will produce a spectacular best-of-N Calmar **from pure noise**, and the size of that effect is knowable rather than mysterious: it grows with the number of candidates and shrinks with the length and independence of the sample. The Miner already knows N exactly, knows the sample length exactly, and knows how correlated the candidates are (it built them from one lattice). Today it reports a winner's Calmar as though it had tested one hypothesis. **Reporting a row's edge against what the best of N would look like under a null is the single most honest number this tool could add**, and it needs no new backtests at all. The literature calls the general idea a deflated or multiple-testing-adjusted performance measure; the exact formulation should be chosen deliberately, since the standard ones assume independence that a dense lattice badly violates.

  A more expensive but far more defensible alternative to a closed-form null: **measure it**. Score a few thousand random signals with time-in-market matched to the row being rated, take the distribution of their Calmars, and report the row's percentile against it. That is an empirical null built from this exact search space, so it needs no independence assumption. It costs one small extra pass and could be run once per session rather than per row.

  ---

  **C-N. The empirical null, measured 2026-09-07, and corrected the same day.**

  > **CORRECTION, and read it before the figures below.** The first round of this measurement
  > applied only **Pass 1's store admission rule** (`signal-miner.html` line 1585) and missed the
  > shipped **`sl-tim` Min Time in Market filter, which defaults to 15 percent** and is applied at
  > line 1676 when results are filtered for display rather than when the store is built. 15 percent
  > of a 3,942 day window is **592 firing days**. Every figure in the original table was therefore
  > measured on the *store*, which holds rows the page never shows, rather than on the leaderboard a
  > visitor sees. The original table is kept below rather than deleted, because the error is
  > instructive and because deleting a wrong measurement hides that it was made. **The corrected
  > results are in "C-N2" further down, and they change the conclusion in both directions:** the
  > alarming best-of-N growth was a tiny-sample artifact and is much smaller than reported, while
  > the search's *lack of edge* is worse than reported and now holds on every configuration tested.
  > This is the [[harness-must-assert-shipped-default]] failure in its exact textbook shape: the
  > harness measured a population the shipped default excludes.

  The paragraph above was a proposal. It has now
  been built as a measurement harness, `scripts/harness/nulldist.js`, and run. **The harness is not a
  gate and is not shipped to visitors.** It exists to answer whether the N-adjustment is worth
  building at all, and what it would say.

  **One deliberate departure from the proposal above, recorded rather than silently substituted.**
  The proposal says to score *random signals with time-in-market matched to the row*. The harness
  instead **rotates the target's log-return series circularly inside the scored window** and re-runs
  the same search over the same lattice. The proposal's method was not followed because matched
  time-in-market is not enough to make a random boolean array comparable to a real signal: real
  signals fire in **blocks**, and block structure is most of what drives max drawdown, which is
  Calmar's denominator. A random array with the same firing rate and no block structure produces a
  null that is too easy to beat, which biases every reported edge upward. Rotation preserves the
  target's return distribution, its volatility clustering and its drawdown structure; it preserves
  every signal's firing rate *and* its run lengths; and because it searches the same lattice, it
  **preserves the dependence between candidates**, which is the exact assumption this section warns
  that closed-form adjustments violate. The only thing rotation destroys is the alignment between
  signal and target, which is the relationship being tested. **The one artifact is stated rather than
  hidden:** a circular rotation splices the end of the window onto its start, creating one artificial
  day-to-day join per rotation, against a window of 3,942 days.

  **Rotation is bounded inside the scored window**, not applied to the whole axis. `lret` carries NaN
  before a ticker's listing date and `backtest` maps NaN to a zero return, so rotating the full axis
  would drag pre-listing NaNs into the window and quietly convert them to flat days. That would bias
  the null **downward**, which is the dangerous direction: a suppressed null makes a real row look
  better than it is.

  **What was measured.** Four configurations, all on the page's own `backtest()` through the harness
  hook, all ranked on **Calmar because that is the page's shipped default sort**, and all filtered by
  Pass 1's own admission rule so the null is filtered exactly as the real store is.

  **The table below is SUPERSEDED. It measures the store, not the displayed leaderboard.** It is
  retained because the relative comparison within it is still sound (both sides used the identical
  rule) and because the size of the correction is itself the lesson.

  | Target | Signals | Lattice | Sample | Rotations | Real best | Null best p50 | Null best p90 | Real's percentile |
  |---|---|---|---|---|---|---|---|---|
  | QQQ | SPY, QQQ, TLT | 27,972 | 9,324 | 40 | 11.87 | 5.81 | 20.23 | **80** |
  | QQQ | SPY, QQQ, TLT, IWM, GLD, XLK | 68,904 | 6,264 | 24 | 10.35 | 3.07 | 9.41 | **92** |
  | TLT | SPY, QQQ, TLT | 27,972 | 6,993 | 24 | 0.48 | 1.84 | 5.35 | **4** |

  **Four findings, in order of how much they should change the product.**

  **1. The null construction validates itself.** On every configuration the *median* admitted row is
  essentially identical under the real target and under rotation: 0.40 against 0.43, 0.38 against
  0.39, 0.04 against 0.04. Rotation therefore destroys alignment without shifting the metric's level,
  which is precisely what a null has to do to be one. **The entire effect lives in the maximum**, and
  that is the claim the whole section rests on.

  **2. The best-of-N effect is enormous, and it was measured rather than assumed.** The null's
  best-of-k rises steeply with how many candidates were examined. On the first configuration the null
  alone climbs from 0.78 at k=100 to **5.81 at k=9,324**, on scrambled data, purely from taking a
  maximum over more draws. Extrapolating the shape toward the full 4.8M-candidate search is exactly
  the adjustment this component is for.

  **3. The real search's headline number sits inside its own null's range.** On the first
  configuration the real best of 11.87 lands at the **80th percentile** of null bests, and one
  rotation of scrambled data reached **59.20**, five times the real result. At k=100 the real search
  was actually **behind** the null. A leaderboard row is not evidence of anything until it is placed
  against this distribution, and today the tool prints the row and not the distribution.

  **4. The result that settles it: on TLT the search found nothing, and would still have printed a
  leaderboard.** Real best 0.48 against a null median of 1.84 and a null p90 of 5.35, putting the
  real search at the **4th percentile** of scrambled data. Not a weak edge, a **negative** one: 23 of
  24 rotations of pure noise beat it. The Miner as it ships today would present that run's top rows
  in the same table, with the same formatting and the same confidence, as a run that had found
  something. **This is the strongest available argument that item C is not a refinement but a
  correction.**

  **The honesty test above is satisfied.** That test demanded that "most rows should rate badly,
  including rows near the top of the leaderboard", and warned that an implementation rating most of
  the leaderboard as trustworthy is wrong and should not ship. A null whose p90 exceeds the real best
  on two of three configurations rates the leaderboard badly, and one configuration rates it below
  noise.

  **A methodological note worth keeping, because it cost a wrong answer once.** The sample is drawn
  by stride and **then shuffled with a seeded permutation**. The stride alone gives a sample uniform
  over the lattice, but the lattice is ordered by family, then ticker, then window, then level, so
  the sample's *prefix* is not uniform: its first hundred entries are all one family. `best-of-k`
  reads a prefix. The first run reported a suspiciously flat 1.00 at both k=100 and k=300 for exactly
  this reason: it was reporting the best of one family and calling it the best of a hundred
  candidates. **The fix made the result less flattering, not more:** the headline percentile fell from
  92 to 80. That direction is the reason to trust the number.

  **Sortino is not usable as the measured metric, and this is a finding about the page, not about the
  null.** Repeating the first configuration on Sortino returns a real best of **2,065,411** against a
  null median of 298,522. The magnitudes are degenerate: `sortino = meanAll / (negStd + 1e-9)`
  (`signal-miner.html`), so a spec with almost no losing days divides by the epsilon and returns a
  number with no meaning. Calmar has a similar near-zero-denominator shape but is guarded by
  `maxDD !== 0`. **This does not affect the conclusions above**, all of which are on Calmar, the
  shipped default sort. It is recorded because the Sortino column is displayed on the leaderboard
  today and can show values of that magnitude to a visitor.

  ---

  **C-N2. The corrected measurement, against the shipped display filter.** `nulldist.js` now applies
  `sl-tim` at its shipped 15 percent default to both the real search and every rotation, so both
  sides are the population a visitor actually sees. Same rotation method, same lattice, same metric.

  | Target | Signals | Sample | Rotations | Real best | Null p50 | Null p90 | Real's percentile |
  |---|---|---|---|---|---|---|---|
  | QQQ | SPY, QQQ, TLT | 9,324 | 24 | 1.01 | 1.06 | 1.16 | **38** |
  | TLT | SPY, QQQ, TLT | 9,324 | 24 | 0.38 | 0.41 | 0.55 | **33** |

  **Three things changed, and they do not all point the same way.**

  **1. The best-of-N effect is far smaller than first reported, and that finding is retracted.** On
  store rows the null's best-of-k climbed from 0.78 at k=100 to 5.81 at k=9,324. With the shipped
  filter applied it climbs only from **0.72 to 1.06**. The steep growth was almost entirely rows
  firing a handful of days, whose Calmar is a ratio of two nearly empty samples. The general claim
  that a maximum over more candidates rises is still true and still the reason item C exists; the
  **size** of it on this page was overstated roughly fivefold and is corrected here.

  **2. The headline result is worse, not better, and it is no longer a single bad configuration.**
  On store rows the real search sat at the 80th percentile of its null on QQQ and the 4th on TLT,
  which read as "usually finds something, sometimes finds nothing". Against the displayed population
  it sits at the **38th percentile on QQQ and the 33rd on TLT**. Both are near the middle of their
  own null. **On neither configuration tested does the search that a visitor sees beat scrambled
  data.** The earlier TLT result was not an outlier; it was the honest case, and the QQQ result that
  looked acceptable was carried by rows the page filters out.

  **3. The null construction still validates itself**, which is what licenses reading any of the
  above. Median admitted row, real against null: 0.46 against 0.48 on QQQ, 0.04 against 0.04 on TLT.
  Rotation destroys alignment without shifting the level.

  ---

  **C-N3. The wide sweep, 2026-09-08. This answers open question 28.** Two configurations were too
  thin a basis for "the Miner finds nothing", so the null was run across **five targets by three
  `sl-tim` settings, fifteen configurations**, 16 rotations each, everything else held fixed.

  | Target | tim 5% | tim 15% | tim 30% | Real best | Reading |
  |---|---|---|---|---|---|
  | QQQ | 63 | 63 | 63 | 1.01 | Middling, and identical at every filter |
  | TLT | 100 | 69 | 88 | 0.42 to 0.55 | The only configuration that beats every rotation |
  | SPY | 0 | 0 | 0 | 0.77 | **Worse than all 16 rotations** |
  | IWM | 0 | 0 | 0 | 0.54 | **Worse than all 16 rotations** |
  | GLD | 44 | 50 | 56 | 0.56 | Indistinguishable from noise |

  Figures are the real search's percentile among null bests.

  **Four conclusions.**

  **1. No configuration shows a reliable edge.** One cell out of fifteen, TLT at a 5 percent filter,
  beat every rotation, and its neighbours at 15 and 30 percent did not, which is what a lucky draw
  looks like rather than a real effect. The rest sit between the 0th and 69th percentile.

  **2. On SPY and IWM the search is worse than noise, at every filter setting.** Not merely
  unimpressive: **every one of 16 rotations of scrambled data beat the real result**, on both
  targets, six configurations in a row. That is the strongest single finding in this whole exercise
  and it is stable rather than marginal.

  **3. `sl-tim` barely matters, which retires an earlier worry.** The corrected measurement raised
  the possibility that the display filter was driving the result. It is not: QQQ reports 63 at all
  three settings, SPY and IWM report 0 at all three. The filter changes which rows exist without
  changing the real-versus-null verdict.

  **4. The percentile is noisy at this rotation count, and that is stated rather than hidden.** QQQ
  measured 38 in the earlier 24 rotation run and 63 here at 16 rotations with a different sample
  size. Those are the same finding, "middling", read at a resolution the method does not support.
  **Any shipped version must not print a percentile to the point**, which is independent
  confirmation of the design constraint already in this section: coarse buckets, never a number with
  a decimal.

  **The answer to open question 28: the banner would fire on essentially every run, and on current
  evidence that is correct rather than a bug.** Fourteen of fifteen configurations fail to beat
  their own null. The remaining design question is not whether to warn but how to word a warning
  that is nearly always true without training visitors to ignore it, and the honest framing is
  probably that this is a property of brute-force search over a dense lattice rather than a fault in
  any particular run.

  **What this does to item C.** It strengthens the case for building it and weakens the case for the
  specific number first proposed. A component that reported "your best result is at the 38th
  percentile of what this same search finds on shuffled data" would be reporting something true,
  useful, and unavailable anywhere in the tool today. But the owner's chosen presentation, plain
  language only when the result is bad, would then fire on essentially every run measured so far.
  **That is a product question rather than a measurement question and is flagged for the owner
  rather than resolved here.** It is recorded as open question 28.

  **The Sortino degeneracy was fixed in v1.76.8**, after the owner chose the smallest of three
  options: correct the formula, leave the `sl-tim` input range alone, and keep the affected rows on
  the leaderboard with a blank cell rather than evicting them. `sortino` now returns NaN when there
  are fewer than two losing days or when the downside deviation is exactly zero, and **Sortino was
  removed from the store admission rule** so that an undefined value blanks one cell instead of
  deleting a row whose Calmar, return and drawdown are all still real. Without that second change the
  fix would have quietly evicted 131 rows, which is a different product decision than the one taken.
  Largest Sortino on a 27,972 spec lattice falls from 2,065,411 to 1.31, with the store unchanged at
  23,108 rows. Verified by `scripts/harness/sortino_fix.js`, which asserts the returned value rather
  than the rendered cell.

  **A note on the Sortino degeneracy, corrected the same way.** `sortino = meanAll / (negStd + 1e-9)`
  returns values near 2e6 when a spec has fewer than two losing days, because ddof=1 leaves `negStd`
  at exactly zero and the epsilon becomes the whole denominator. Measured on the store, 131 rows
  (0.57%) are degenerate and 43 of the top 100 by Calmar carry one. Measured against the shipped
  15 percent filter, **the number of degenerate rows that reach a visitor is zero**: they fire about
  four days out of 3,942 and the filter discards every one. **So the formula is wrong but the defect
  is latent**, reachable only by a visitor who lowers `sl-tim` toward zero, which the input permits
  (`min="0"`). It is worth fixing as robustness, and it is not the urgent leaderboard contamination
  the first measurement suggested. The harnesses are `scripts/harness/sortino.js` and
  `scripts/harness/floor.js`.

  **What this does not yet decide.** The presentation. The design danger stated below in this section
  is unchanged and is now more acute, not less: these numbers are the strongest possible temptation to
  print a precise score, and a precise score is the one thing this component must not produce. The
  harness output is a measurement, not a proposed UI.

  **The other components, all cheap:**
  - **Plateau width (from A).** A knife edge rates badly no matter how good its number is.
  - **Out-of-sample decay (from B).** The only component that can actually fail a rule outright.
  - **Trade count and firing days.** A rule with a 4.0 Calmar earned across nine trades has almost no evidence behind it, regardless of everything else. This is already available from the backtest and is probably the second cheapest component after N.
  - **Time in market.** Already computed and already a filter. A signal that fires 2% of the time is fitting a handful of days.
  - **Concentration in time.** Whether the entire edge comes from one period, most likely 2020 or 2022. Cheap to approximate by scoring the row over sub-periods it has already been evaluated on.

  **The design danger, and it is the real one.** A single letter grade or 0-to-100 score invites exactly the false confidence it is meant to prevent, and the moment it exists people will optimise against it, which converts a diagnostic into a target and destroys it. **Show the components, and only then a summary.** The summary should be coarse on purpose, three or four buckets rather than a number with a decimal point, because the underlying estimate does not support more precision than that.

  **The honesty test for whether it works.** Given a 4.8M-candidate search, **most rows should rate badly**, including rows near the top of the leaderboard. If a first implementation rates most of the leaderboard as trustworthy, the rating is wrong and should not ship. It exists to make the tool argue with its own output.

  **C-SHIP. Shipped 2026-09-08 as v1.79.0, and what shipped is narrower than the specification
  above.** What is live is the **empirical null**, rendered as a panel above the results table, and
  none of the other components. The plateau, out-of-sample decay, trade count, time in market and
  time concentration components are still unbuilt. This is stated plainly because the section above
  reads like a specification for a composite rating, and a reader who assumes all of it shipped will
  be wrong about five sixths of it.

  **Why the null shipped alone, ahead of a sequencing note saying C cannot ship before A.** The null
  turned out not to need A. It is not a component of a composite score; it is a single question with
  a single answer, and C-N3 established that the answer is almost always "no" (fourteen of fifteen
  configurations failed to beat their own null, and two targets were beaten by every rotation).
  Holding a finding that strong behind four unbuilt components would have meant the tool kept
  presenting a leaderboard it already had the evidence to doubt.

  **How the shipped check works.** After Pass 1, it samples about 1,500 spec indices from the run's
  own lattice with a seeded shuffle, evaluates each signal once, and scores that one sample against
  the real target and against eight circular rotations of it. **Both sides are a best-of-k at the
  same k**, which is the only thing that makes the comparison mean anything, and the panel says "a
  sample of your search" rather than implying the whole lattice was re-run. Inventing a scaling
  factor from the sample up to the full lattice was considered and rejected: it would be a guess
  wearing a number's clothing.

  **The filter distinction bit for the second time, and the panel is corrected for it.** The first
  working version scored both sides against Pass 1's store admission rule only. That is symmetric,
  so the verdict was never unfair, but the *number printed* did not describe the table underneath
  it: Min Time in Market defaults to 15% and is applied at display time, so an admission-only best
  can come from a spec firing a handful of days out of nearly four thousand, which the default
  filter discards before anyone reads it. The shipped panel reads `sl-tim` and `sl-mdd` from the
  live controls exactly as `applyFilters` does. **The correction moved the measured figures
  materially**, from a real best of 1.19 against a null median of 2.30 to a real best of 0.95
  against a null median of 0.96, and brought them into line with C-N2. This is the same error that
  had to be corrected in `scripts/harness/nulldist.js` earlier the same day, which is why it is
  recorded here rather than quietly fixed.

  **What the panel refuses to say.** No percentile, and **no number carrying a decimal point anywhere
  in the verdict**, which `scripts/harness/honesty.js` asserts directly. C-N3 measured the same
  configuration reading percentile 38 once and 63 another time, so any finer figure would be
  reporting noise as precision. The four buckets are: beat every rotation, beat most of them, beat
  some of them, and beaten by nearly all of them. **The components are printed above the bucket**,
  per the design danger noted above, and the components are exact, because they are measurements
  rather than interpretations.

  **The honesty test is satisfied by the shipped build, not merely by the specification.** A default
  QQQ run over a 34,800-signal lattice lands in the third bucket, "indistinguishable from noise",
  with the real best at 0.95 against a null median of 0.96. The tool argues with its own output on
  its own default settings, which was the requirement.

  **Verified by `scripts/harness/honesty.js`**, which does two separate jobs: it checks the render,
  and then it **recomputes the entire check independently from the page's primitives and requires
  the page's printed figures to match**. Eighteen checks pass, including exact agreement on the beat
  count, the real best and the null median. The second job exists because an earlier round of work
  on this page passed 24 render assertions on a verdict that was flatly false. **One behaviour is
  verified by inspection rather than by test:** a new run clears the previous run's panel before it
  starts, which is a single line at the top of the run function and is not covered by the harness,
  because asserting it would mean paying for a second full run.

  **Sequencing.** C cannot ship before A, since plateau width is its backbone and A is nearly free. B strengthens it but is not a prerequisite; the rating can carry an explicit "not validated out of sample" state until B exists. The N-adjusted component could ship on its own, before either, and would be worth doing even if nothing else here is ever built.

  ---

  **C1. The neighbourhood grid, as the owner specified it (2026-08-21).** A concrete rule, with a worked spreadsheet mockup, that turns the plateau idea into a pass/fail a visitor can set for themselves:

  > Miner reports `XYZ RSI(10) > 79` at Calmar 4.0. The user sets a level delta of 1 and a step of 0.25, so the tool re-scores the rule at 78.00, 78.25 ... 80.00. It also sweeps the window, say 10 days plus or minus 2. If Calmar stays within a user-set percentage of the peak, 10% say, across that whole grid, it passes. A rule that passes both axes is far less likely to be an artifact.

  The mockup renders it as a 9-by-5 heat grid with the reported value in the centre: an all-green grid passes, a grid where the centre is an island of green in red fails. **This is the right shape and it should be built this way.** Notes on making it correct:

  - **It is a floor, not a band.** "Within 10%" must mean `Calmar >= 0.9 * peak`, not `|Calmar - peak| <= 10%`. A neighbour scoring 5.0 is not a failure. The mockup's own "Min Calmar 3.6" column gets this right; the prose form of the rule is the ambiguous one.
  - **Do not require every cell to pass.** The mockup's failing grid still has ten green cells scattered through it, which is exactly what noise looks like. A single red cell in an otherwise solid plateau should not fail the row, and scattered green should not pass it. The statistic that handles both is the **largest connected region containing the centre**, quoted as a fraction of the grid. All-green is 100%; the failing example is a centre island of two or three cells.
  - **Report how much the signal actually moved.** Measured on this dataset: RSI(10) puts only **52 to 84 days out of 4,183** inside the 78-to-80 band, depending on the ticker. In absolute terms that is 1.4% of the sample, which sounds like the sweep is barely testing anything. In the terms that matter it is not: for a *rare* `>` signal firing on roughly 100 to 155 days, moving the threshold across that band changes the firing frequency by about **1.6x**, which is a large move. Both readings are true, and which one applies depends on the direction and rarity of the specific rule. So the grid should print the fired-day count at each edge alongside the Calmar. A plateau across a band where the signal did not meaningfully change is not evidence of robustness, it is evidence the band was too narrow, and only the day counts reveal which case you are in.
  - **The window axis is the stronger of the two.** Sweeping 8 to 12 days at a fixed threshold moves the fired-day count by about 140 days, roughly twice what the level sweep moves. If only one axis is ever built, build this one.
  - **Both axes probe OFF-lattice points, deliberately.** The RSI level grid steps by 2 (10, 12 ... 90) and the window grid is the log-uniform list, so `RSI 79` is not a value the Miner can currently report at all, and windows 8, 9 and 11 were never evaluated. That is a feature: the rating is a **finer local refinement than the search**, which is what makes it an independent check rather than a re-read of the same numbers. It also means the refinement may find a better value between lattice points, which should be shown rather than hidden.
  - **Verified: the fine step is not sampling the same signal repeatedly.** The obvious failure mode is that adjacent 0.25 thresholds select an identical set of days, making a "plateau" one measurement repeated nine times. Measured across SMH, QQQ, SPY and XLY: **all nine thresholds produce nine distinct signals, and all five windows produce five distinct signals.** The design is safe at this step size. It would not necessarily be safe at a much finer one, so the tool should count distinct signals in the grid and say so if the number is below the number of cells.

  **External input, relayed 2026-08-24.** A friend of the owner, working from an independent
  conversation with Claude, proposed a plateau check of **plus or minus 3 to 5 RSI points**, a
  **window tolerance of plus or minus 15% to 20% of the window length**, and **two passes: one to
  find single values that show promise, then a second running the plateau-neighbourhood check on
  them.** Logged here because it is the first outside read on this design, and because two of the
  three points are corroboration rather than novelty.

  - **The window tolerance is the same number this spec already carries.** C1 above sweeps "10 days
    plus or minus 2", which is plus or minus 20%. Two independent derivations landing on the same
    figure is worth more than either on its own. Worth relaying back: **the window axis is the
    stronger of the two**, moving the fired-day count by roughly twice what the level sweep moves,
    and it is the one to build if only one ever gets built.
  - **The level range is genuinely wider than what is specced, and it is a different question.** C1's
    grid is plus or minus 1 RSI point at 0.25 steps, a deliberately fine *local refinement* that
    probes off-lattice values the Miner cannot report. Plus or minus 3 to 5 points is the *plateau
    width* statistic from item A, the one quoted in real units as "holds from 20 to 28", which is
    plus or minus 4 around its centre and sits squarely in the proposed range. So both granularities
    are already here at different scales, and the proposal is to widen the coarse one. **Not adopted
    as a fixed number, on the reasoning already stated above:** build the scoring first, look at what
    plateau widths real results actually produce, and let the data choose the width instead of
    guessing it. If real plateaus cluster at 3 to 5 points, that is what it will say, and it will say
    so with evidence.
  - **The two-pass structure is the architecture this spec already requires**, arrived at
    independently. The rating runs on demand for displayed or selected rows, never as a third pass
    over the whole search. **One terminology warning for anyone relaying this:** the Miner already
    uses "Pass 1" and "Pass 2" to mean single signals and pair rows. The proposed second pass is the
    on-demand rating, not the existing Pass 2, and conflating the two would read as a plan to rate
    every pair row in a full search, which is the one thing this design rules out.
  - **The proposal came with an intent to run it overnight. That instinct is wrong, and usefully so**,
    because it is the same misjudgement the next paragraph corrects. At the proposed width the grid
    is roughly 41 level cells by 5 window cells, 205 per row against C1's 45. At 90 microseconds per
    backtest that is about **18 ms per row, so under 2 seconds for a 100-row leaderboard**. Widening
    the range as proposed costs nothing anyone would notice. Overnight only becomes real if the
    rating is applied to every row of a full run, which is exactly what this design rules out.

  **On cost, which is the one place the owner's intuition is too pessimistic.** "Obviously very computational" is the natural read, and it is wrong by about three orders of magnitude, because this is 45 backtests per rated row rather than millions. At the measured 23 ns per spec-target-day, one backtest over a 3,931-day sample is roughly **90 microseconds**, so a 9-by-5 grid is about **4 ms per row** and the entire displayed leaderboard of 100 rows is **under half a second**. Building the handful of off-lattice indicator series costs one pass over the axis each and rounds to nothing.

  The constraint this does impose is architectural rather than computational: rating *every* row of a maximal run would be 45 times a full Pass 1, several hours, so **the rating is computed on demand for displayed or selected rows, never as a third pass over the whole search**. For a Pass 2 pair row, sweep each leg independently (90 cells) rather than jointly (2,025 cells); the joint grid is not worth 45x the cost.

  **What this does not do, and it must not be sold as if it did.** A wide plateau is evidence against *one* kind of overfitting: a rule balanced on a knife edge. It is no defence at all against the multiple-testing problem, because a search over 4.8M candidates will turn up rules with wide plateaus by chance too. This is why the N-adjusted component above is not optional garnish. A row that passes the grid should read as "not a knife edge", never as "not overfit".

  ---

  **C2. It is a filter, not a report, and the grid is machinery the visitor never sees (owner, 2026-08-21).** Two decisions that change what gets built:

  > "If it fails, it moves on to another test." / "The user never needs to see those tables. They just need to know if Miner has found a solution loose enough to fulfil the sweep around the initial solution criteria."

  In the mockup the reported solution sits at the **centre** of each table, RSI level down the left, window in days across the top.

  **The first decision is the larger one.** C above was written as a *rating*: score the rows, show a verdict beside each. "It moves on to another test" is a different product. The Miner walks down its own leaderboard, sweeping each candidate, and surfaces the best one that **holds**, rather than the best one full stop. The tool stops reporting a number and starts reporting a rule it is willing to defend.

  This is affordable, and the existing code has the hook for it. `selectTop(set, n, key, asc, needle)` already takes the depth `n` and never sorts the full set, so walking deeper is calling it with a larger `n`. At roughly 4 ms per candidate, testing the first 100 costs 0.4s, the first 1,000 costs 4s, and even 10,000 is under a minute. The unknown is the **hit rate**, which nobody knows yet and which is itself the most interesting number this feature could produce. If one row in 20 holds, this is instant. If it is one in 50,000, that finding is worth more than the feature: it would mean the leaderboard is essentially all knife edges. **Instrument the hit rate from the first prototype**, because it determines whether this is a filter or a headline.

  **The statistical caveat, which the filter does not remove.** Taking the best row that also survives a robustness check is still selection on the same data: it is a max over a large set, just a differently shaped one. The surviving Calmar is still a best-of-N number and should still be discounted as one. The filter makes the *rule* more defensible; it does not make the *number* less optimistic. Both statements need to be true in the copy.

  **On presentation, since the owner has asked for a recommendation.** The tables are evidence, not interface. Concretely:

  - **One badge per row** on the existing leaderboard: **Holds** / **Fragile** / **Edge** (see the boundary note below). No numbers, no grid.
  - **One toggle**, "only signals that hold up to a sweep", which is the filter version of the same thing, with delta and step tucked behind it at sensible defaults. Note that this cannot behave like the four existing section-3 filters: those promise live re-filtering with no re-run, and this one computes. Filtering the displayed 100 is 0.4s, which is fast enough to feel live; going deeper needs a progress indicator and an honest "testing candidate 400 of 1,000".
  - **The grid on click, for anyone who wants it.** It costs nothing to render something already computed, and hiding the evidence entirely makes the badge unfalsifiable.
  - **Keep exactly one number.** Pure pass/fail throws away the most useful thing the sweep knows: a row whose worst neighbour is 3.99 is not the same as one that scrapes in at 3.61. Surface the **worst Calmar in the connected region** beside the badge, phrased as "holds down to 3.72 across plus or minus 1 RSI and 2 days". That is one short sentence, it is the honest summary, and it prevents the badge from becoming a binary that hides its own margin.

  **Which families to start with, and what the grid looks like for each.** The owner's reading favours RSI threshold and RSI comparison for leveraged targets, which is also the cheapest place to start:

  - `rsi_thresh` is the worked example: **level by window**, exactly the mockup.
  - `rsi_cmp` has **no level to sweep**. Its only parameters are the two windows, so its grid is **window A by window B**, the same 2D shape with different axes. This is worth stating early because it means the feature is not "sweep the level and the window", it is "sweep whatever continuous parameters the family has", and the two RSI families already need two different answers.

  **Two rules that must be decided before building, both of which the mockup cannot show:**

  - **Boundary solutions.** The RSI lattice runs 10 to 90 and the window grid runs 5 to 252. A solution reported at the edge has no neighbourhood on one side. Silently testing the half that exists would let edge solutions pass more easily than interior ones, which is backwards. Either fail them, or test one-sided and badge them **Edge** rather than **Holds**. Do not let them quietly pass.
  - **Defaults, which become the standard.** Whatever delta and step ship will be what almost everyone uses, so they should not be round numbers chosen for looking tidy. The measurement in C1 gives a better basis: pick the delta that moves the signal's **firing frequency** by a target fraction, roughly 25%, rather than a fixed number of RSI points. That adapts automatically to rare and common signals, which a fixed delta does not, and it directly prevents the "band too narrow, everything passes" failure.

  **Generalising beyond RSI is a later step and should stay later.** Every level family (`cum_lvl`, `std_lvl`, `dd_lvl`, `ma_lvl`) has the same level-by-window shape and would work identically. The value of starting with the two RSI families is not that the others are hard, it is that the hit rate and the defaults need to be understood on one family before the answer is generalised to sixteen.

  ---

  **C3. The return-series tests, from a practitioner checklist (contributed 2026-08-21).** Everything in C1 and C2 tests the **parameter lattice**: is the rule balanced on a knife edge. This is a separate family of tests on the **return series**: is the edge real, or is it a few days, one year, or one regime. They are orthogonal, they are both cheap, and a rating that only does the first is testing half the problem.

  The source framing is worth keeping verbatim, because it is a corrective to C2's binary: *"It's pretty subjective. Everyone does it a little differently. It's also a spectrum, so we're really talking about 'to what degree' for each of these."* That tension resolves cleanly. **Binary for the filter, spectrum for the display**: walking a leaderboard needs a stopping rule, so the filter must threshold, but what is shown beside a surviving row should be graded.

  **Cost note for the whole section: essentially free.** Every test below is a re-scoring of a daily return series the row has already produced. A handful of extra passes over 3,931 days is microseconds, so the constraint is screen space and the visitor's patience, not compute.

  **Directly implementable, in rough order of value:**

  - **Leave 2020 out entirely.** The cheapest and sharpest test on the list, and it generalises past the specific year: mask each calendar year in turn and re-score. That is a **jackknife over regimes**, and what it produces is one number, "the worst this rule scores with any single year removed". A rule whose Calmar collapses without 2020 was fitted to 2020. This subsumes the "concentration in time" component sketched earlier in C and should replace it.
  - **Remove the positive outliers but keep the negative ones.** Drop the top *k* daily returns and re-score. The asymmetry is deliberate and correct: it is a stress test, not a fair resample. Report it as plain arithmetic ("the best 5 days out of 3,931 are 61% of total return") and let the number speak. The checklist's own instruction is the right disposition: *if it is not clearly fine, treat it as a risk.*
  - **Monthly return grid.** Outlier negative months and long neutral stretches are both cheap to compute and easy to render as a small heat strip. Closely related to the outlier test: an edge concentrated in a few months is the same finding at a different resolution.
  - **First half against second half.** The "elbow" in cumulative returns, made objective by comparing annualised return across the two halves of the sample rather than by eye. **One technical caution, because getting this wrong would make every rule look broken: a cumulative return chart on a linear axis always shows an elbow, because compounding is exponential.** Eyeballing must be done on a log axis, and the computed version should compare annualised rates, not endpoints.

  **One item on the list is the wrong test, and implementing it literally would waste the effort.** *"If you look at the daily return distribution, does it look like a normal distribution?"* Daily returns are **never** normal, for good strategies and bad ones alike; fat tails and volatility clustering are universal properties of financial return series, not symptoms of overfitting. A normality test would fail essentially every row and carry no information. What the question is reaching for is the item immediately after it, outlier dependence, which is a genuinely sharp test. Fold the two together and keep only the outlier version.

  **Two items need translating, because the Miner has no equivalent of the thing they key on.** *"Does the underwater graph look materially different before and after the start of the Composer backtest?"* and the same question for rolling CAGR. Those work because a published symphony has a **creation date**, and everything after it is unavoidably out of sample. **A mined signal has no such date. Every day the Miner scores is in sample, by construction.** So there is nothing to compare against until item B manufactures the split, and these two items are best read as a specification for what B should *show*: not a scalar decay number, but the **underwater curve and the rolling CAGR curve overlaid, training against held-out**.

  The checklist also supplies a prior that B's write-up was missing, and it is a strong one: when the two halves disagree, **expect the future to resemble the earlier period, not the backtested one.** That is the correct direction of pessimism and it should be stated in the copy rather than left for the visitor to infer.

  **The last item cannot be automated and should not be faked.** *"Does the logic make sense logically."* Nothing computed can answer that. It is worth recording anyway, because it is the sharpest possible statement of what this tool is: **the Miner produces rules with no economic story at all**, selected from 4.8M candidates by their numbers alone. A human asking "why would this work" is applying the one filter the tool structurally cannot. That belongs in the interface as a permanent caveat next to the results, not as a computed score, and it is a standing argument against ever letting the UI describe a mined rule as validated.

  **What this means for the shape of the rating.** Two groups, not one flat list: **parameter robustness** (C1, C2) and **return robustness** (C3). A rule can pass either while failing the other, and the two failures mean different things. A wide plateau with all the return coming from March 2020 is a genuinely robust rule for a world that no longer exists.
---

- [ ] **DEFERRED INDEFINITELY: OR combining, and Composer's any/all multi-ticker conditions.** Asked for directly by the owner on 2026-08-20 (pointing at Composer's `+` button on a condition row), planned as part of the v1.23 rollout, not built, and then **explicitly pushed back with no target date on 2026-08-21** once the scope was clear. It is written up in full here because the reasoning took real work to establish and should not have to be rediscovered. **Do not start this without the owner reopening it.**

  **Why it is worth doing eventually, which is the part that is easy to lose.** The case is not "more features." It is that the tool has a *shape* limit that quietly biases what it can find.

  1. **The search is one-sided, and it is biased toward the fragile half.** Every result today is one condition or two joined by AND, and AND only narrows: `A AND B` fires on a subset of the days `A` fires. So every combination the miner builds is more selective than its parts, and Time in Market goes **down**. That matters because at 4.8M signals against one target the leaderboard is selected for luck as much as skill, and **the fragility of a rule scales with how rarely it fires**. A rule trading on 15% of days rests on a fraction of the sample; one trading on 60% is much harder to fluke. Several top-ranked AND pairs in the 2026-08-20 runs sat at 15-25% Time in Market. OR pushes the other way, toward buy-and-hold. The tool therefore has no access to the naturally more robust half of the space, and a missing hypothesis does not rank badly, it simply never appears.

  2. **OR is a smoothing operator.** An OR of two similar-but-not-identical signals is a less threshold-sensitive version of either one. That is the opposite of overfitting, and it is unreachable today.

  3. **any/all is how Composer strategies are actually written.** The Frontrunner, the reference strategy in this repo, is a ladder: SMH RSI(10) < 23 to SOXL, QQQ < 28 to TQQQ, SPY < 28 to UPRO, XLY > 79 to VXX, else BIL. Read as logic that is "if **any** of these tickers is oversold, go risk-on." Ladders are OR-with-priority and they are the dominant idiom across the strategy library. Composer's `+` collapses one into a single condition: `RSI(10) of any of [SMH, QQQ, SPY] < 28`. The miner can only ever put **one** ticker on the left, so the single most common structural pattern in real symphonies is not in the search space at all.

  4. **A breadth condition is statistically stronger, not merely different.** "Any of ten leveraged funds is oversold" is a statement about market breadth. "SOXL specifically is oversold" can easily be an artifact of one fund's history. Aggregating across a basket averages out idiosyncratic noise, so a breadth signal that works is more likely to be real. This attacks the tool's core weakness rather than adding to it.

  **What it does NOT fix, stated so the case is not oversold.** OR does not solve the multiple-comparisons problem, it only stops the search being one-sided about it. And the any/all half makes overfitting *worse* if the ticker sets are unbounded: given freedom to choose which tickers go in a basket, you can always find a basket that fits the past. The value is entirely contingent on keeping the sets small and meaningful.

  **Two genuinely different features, which were conflated in conversation and must be kept apart when this is picked up:**

  **(a) OR between two conditions.** The smaller half. Combining is AND-only today: `applyFilters` pairs survivors and emits a row whose booleans are `a[i] && b[i]`. Composer's `compound` condition already takes `operator: 'all'` or `'any'`, and `composerThenChild` hardcodes `'all'`. The work: a **Combine mode** control in section 3 (AND / OR / both), an OR variant in the pairing loop, `operator: 'any'` in the export when the row is an OR pair, and a mode column (or a label suffix) so the table never shows two rows that read identically but mean opposite things. Cheap: the survivor set is unchanged and the pairing loop just emits a second row per pair, so "both" roughly doubles the pairing pass, which is already the cheap half of a run. It adds **no** Pass-1 specs.

    **Design caution to settle before building.** An OR pair's Time in Market is at least as high as either single, so OR rows drift toward buy-and-hold exactly where AND rows drift toward over-fitting. The existing Min Time in Market floor screens the wrong direction for them. Expect OR results to need either a separate ranking, a Max Time in Market ceiling, or at minimum a note; do not merge them into the same leaderboard and call it done.

  **(b) any/all across a ticker list inside ONE condition.** The larger half, and what the `+` button actually does. The schema is already in the exporter: a `binary-compound` carries `operator: 'any' | 'all'` and a `tickers: []` array, and `composerCondition` already emits `operator: 'any'` with a single-element array. Mining it means a spec whose left operand is a *set* of tickers.

    **This is combinatorially explosive if left unbounded** and must not be built as "all subsets": 72 tickers is 2^72 sets. Bounded designs worth costing, cheapest first:
    1. **Asset-class groups as the candidate sets** (Leverage, Inverse, Bonds, Value & Dividend, and the rest, straight off the `group` field in `prices.json`). Nine-ish sets instead of 2^72, each with any/all and both directions. Recommended starting point: bounded, economically meaningful, and needs no new UI beyond a checkbox.
    2. The user's whole selected Signal set as one group, which is one extra set per family and effectively free.
    3. Unordered pairs and triples of selected tickers, `C(n,2) + C(n,3)`, already 62,196 sets at 72 tickers before any family multiplier. Only viable on a small selection and it needs its own guard.

    `evalSpec` needs a set-valued left operand (fold `any`/`all` across the member series before comparing), the label needs to name the set, and the spec store needs a set index rather than a single ticker byte. Unlike (a), this **does** add Pass-1 specs, so items 1 and 3 above should be re-checked afterwards if it is ever built.


---

- [ ] **Signal Miner: answer "which signals are best for this target?" properly**: raised by a site user (2026-08-20). The engine already searches the full cross product, so every result row is a `(signal, target)` pair and the reverse question is technically answerable today by selecting one target and many signal tickers. Nothing in the UI says so, and two gaps make the answers hard to trust. Three parts, in priority order:

  1. **Buy-and-hold baseline (do this first).** "Best signal for TQQQ" is meaningless without "compared to just owning TQQQ." The engine already holds the target's own return series (`targetLret`) but never surfaces it, so a 1.4 Sortino looks impressive with no way to see the target alone did 1.6. Add it as a pinned reference row per target, or a "vs hold" delta column. Cheap, and it is what makes every other number interpretable.
  2. **Signal robustness / cross-target view.** Flip the table so each row is one *signal* with columns for how it did across every selected target: median Sortino, count of targets where it beat hold, best and worst. Pass 1 already computes every `(signal, target)` cell, so this needs no new backtesting, only a different reduction over `sigCache`. This is the real "reverse" view, and it doubles as the strongest available defence against the tool's core weakness: a signal that beats hold on 8 of 8 targets is a finding, one that wins on 1 of 8 is almost certainly noise.
  3. **Framing.** Copy plus a preset for the one-target sweep, so the workflow is discoverable at all.

  Also consider grouping results per target (currently the global sort plus a 500-row `DISPLAY_CAP` lets one target monopolize the table when several are selected), though the robustness view largely subsumes it.

  **Deliberately out of scope: deriving signals from the target.** Starting from the target's forward returns and searching for conditions that separate good days from bad is a genuinely different algorithm, closer to feature selection or a decision tree, and fitting conditions directly to the thing being predicted is an efficient way to manufacture beautiful nonsense. If it is ever attempted it needs an out-of-sample holdout split first, which the tool does not currently have.

  **Statistical caveat to surface in the UI when this ships:** pointing tens of thousands of tested conditions at a single target makes the multiple-comparisons problem *sharper*, not softer. The top of a per-target leaderboard is selected for luck as much as skill. The existing warning box covers this generically; a per-target ranking deserves its own note.

- [x] **Prune duplicate ETFs from the Signal Miner universe, by inception date** (done v1.21.2): 80 to **72 tickers**, ~19% fewer signals on a select-all run. Removed: **UPRO, VGSH, VGLT, VGIT, SOXX, VTV, SVIX, IJR**. Kept the older listing in every pair, per owner preference for the inception rule over usage.

  **Method correction, and the main lesson.** The first pass ranked candidates by daily-return correlation. That was the wrong instrument: it measures whether two funds move together, not whether they hold the same thing, and large caps dominate the variance in nearly every pair here. It scored SPY/VTI at 0.9961 and called them duplicates, when one is the S&P 500 and the other is the total market including mid and small caps. Corrected approach: **compare stated mandates first**, use correlation only as a supporting signal. Several pairs were reclassified as genuinely different and kept in full:

  | Kept both | Why they are not duplicates |
  |---|---|
  | SPY / VTI | S&P 500 vs total market incl. mid and small caps |
  | IEF / IEI | "7-10 Year" vs "3-7 Year" Treasury: different duration bucket |
  | BND / BNDW | "Total Bond Market" vs "Total **World** Bond": different geography |
  | QQQ / QQQE | Cap-weighted vs equal-weighted; corr 0.9360, the lowest pair measured |

  **Decisions applied** (inception dates are Yahoo's first traded bar, fetched per ticker with `period1=0`, not the prospectus date):

  | Exposure | Kept | Inception | Dropped | Inception |
  |---|---|---|---|---|
  | S&P 500 3x daily | SPXL | 2008-11-05 | UPRO | 2009-06-25 |
  | 1-3yr US Treasury | SHY | 2002-07-30 | VGSH | 2009-11-23 |
  | Long treasuries | TLT | 2002-07-30 | VGLT | 2010-01-04 |
  | Intermediate treasuries | IEF | 2002-07-30 | VGIT | 2009-11-23 |
  | Semiconductors | SMH | 2000-06-05 | SOXX | 2001-07-13 |
  | Large value | SPYV | 2000-10-02 | VTV | 2004-01-30 |
  | Short VIX | SVXY | 2011-10-04 | SVIX | 2022-03-30 |
  | US small cap | IWM | 2000-05-26 | IJR | 2000-05-26 |

  Two rows are worth remembering. **SPXL over UPRO and SMH over SOXX both go against usage** (UPRO 2,148 vs SPXL 1,508; SOXX 528 vs SMH 499 in the 6,322 clean symphonies of `database.json`), chosen for consistency with the stated inception rule. **IWM/IJR list on the same day**, so inception could not break that tie and usage decided it (218 vs 7). SVIX and IJR were reclassified as "different exposure" but pruned anyway on owner call, SVIX partly because its 2022 listing truncated any run including it to ~26% of history.

  **The prior version of this table in this document was wrong in three ways** and is preserved here only as a caution: 21 of 23 dates were a month late (SPY listed 1993-01-29, recorded as 1993-02); it grouped SHY/SHV/BSV/VGSH/BIL as one "short-term treasuries" cluster to prune down to SHY, when those are different durations (SHY/SHV correlate at 0.37, SHY/BIL at 0.096); and acting on that entry **would have deleted BIL**, which is hardcoded as the cash proxy in `buildComposerSymphony` and is also the single most-held ticker in the entire dataset at 3,304 uses. Verify mandates and check for code dependencies before removing any ticker.

  **Inception is now largely inert as a tiebreak.** With `START_DATE` at 2010-01-01, any fund listing before then has 100% coverage regardless of how much earlier it launched, so the rule only discriminates for post-2010 listings. Every pair in the table above except SVIX had 100% coverage on both sides.


- [ ] Client-side search (Fuse.js or similar)
- [x] **Tag-based filtering on the strategy index (built 2026-08-15, v1.17.0)**: the tags already carried by every strategy are now selectable filters on `strategies.html`, not just read-only labels. A filter bar above the grid groups them into **Signal** / **Risk metric** / **Asset class** / **Collection** (plus an automatic "Other" group so any new tag in the data can never silently go missing from the UI), each chip showing its match count. Only tags actually present in the data are offered, so the bar can never present a combination that returns nothing. **Multiple tags combine with AND** (a strategy must carry every selected tag), which is what makes pairing a signal tag with an asset-class tag useful; the count line switches to "N of 31 strategies" while filtered, and an empty result explains the AND behavior and offers a reset. Selections are mirrored into a **`?tags=` query param** via `history.replaceState`, so a filtered view is linkable and survives a refresh or a back-navigation from a detail page. New CSS: `.tagfilter*` (inactive chips are dimmed so selected ones clearly stand out).
- [ ] Strategy comparison view
- [ ] Performance chart per strategy
- [ ] Expand strategy library toward 50+ entries
- [ ] Expand glossary
- [x] **Fold the ETF → Composer Cloner (`etf-cloner.html`) into the standard linking model (done 2026-08-15, v1.16.3)**: the tool shipped live and indexable at v1.16.0 held out of the footer sitemap and homepage Explore grid. As of v1.16.3 it is folded into both: a footer link in `renderFooter` (`js/app.js`) and an Explore card in `index.html`. It remains intentionally out of the primary nav (same treatment as Converter, which now lives in the Tools dropdown). This closes the temporary exception to the "footer links every public page" rule (Section 6).
- [x] **Signal Miner: live filter updates without a full re-run (done 2026-08-15, v1.16.7)**: changing the section-3 filters (Min Time in Market, Max Drawdown floor, Prune quantile, and the AND-pairing toggle) now re-filters the results instantly, no re-run. Implementation: Pass 1 now caches **every valid** single-signal result (`sigCache`, gated only on `total > 0` and finite Sortino/Calmar, not on the user thresholds) plus the survivor `Uint8Array`s needed for pairing; a new `applyFilters()` re-applies TIM/MDD/quantile/pairing against that cache (debounced 250ms on `input`/`change`) and recomputes only the cheap pairing pass. `run()` builds the cache then calls `applyFilters(true)`. Changing tickers/families/min-period invalidates `sigCache` (they change which signals exist), so those still require a fresh run. Distinct from the existing results-table text filter (`sl-filter`), which was already live.
- [x] **ETF Cloner: normalize share-class tickers to Composer/Crescendo format (done 2026-08-15, v1.16.7; reported via community QA)**: holdings sources rendered multi-class tickers with a dot (`BRK.B`, `BF.B`) or dash (`BRK-B`), but Composer *and* Crescendo require the slash form `BRK/B` or the symphony will not save or backtest. `cleanSym()` now normalizes a trailing single-letter class suffix (`.X`/`-X` → `/X`) after validation, so both input paths (live fetch and file upload) and both the on-screen table and emitted JSON use the slash form. Only a trailing `<sep><one letter>` is rewritten, so plain tickers and multi-letter suffixes are untouched. QA'd against `BRK.B`/`BRK-B`/`BF.B`/`LEN.B` (→ slash form) and `VTI`/`VT`/`AAPL` (unchanged).
- [x] **Full site-wide naming review of every tool/page (done 2026-08-15)**: did one deliberate pass over every public page/tool name for clarity, one-word preference, and cross-tool consistency. **Outcome: keep all current names; no renames recommended.** Verdicts:
  - **Home / Strategies / Database / Glossary / About**: keep. Standard, one-word, self-explanatory.
  - **Converter**: keep. One word, unambiguous.
  - **ETF Cloner**: keep. "Cloner" alone is ambiguous; the "ETF" qualifier is what makes it self-explanatory, so the two words earn their place.
  - **Signal Miner**: keep (renamed from Signal Lab at v1.16.6; "Miner" alone was rejected as reading like crypto/mining-stocks on an investing site).
  - **RSI Signals**: keep. "RSI" alone is jargon and "Signals" alone would collide with Signal Miner, so the pair is the clearest option. It is a live-data page, not a generative tool, so sitting outside the tool naming family is fine.
  - Observation: the three generative tools already form a tidy agent-noun family (Convert**er** / Clon**er** / Min**er**); worth preserving that pattern if a fourth tool is ever added. The one-word-where-possible preference is satisfied except where a qualifier is load-bearing (ETF Cloner, RSI Signals). If a future rename is ever pursued, carry it through all surfaces at once (page `<title>`, nav Tools dropdown + footer + homepage Explore card in `js/app.js`/`index.html`, in-page hero/copy, and a `noindex` redirect stub from the old URL), per the Signal Miner rename pattern.
- [ ] **Cross-link curated strategies ↔ full database (decided 2026-07-13, not yet built, see below)**

#### Cross-linking the curated 31 to the full database (decided 2026-07-13)

**Background:** confirmed all 29 curated strategies (`data/strategies.json`) already exist as rows in the full database (`data/database.json`/`database_summary.json`), matched exactly by `symphony_id`: they are not disjoint datasets, just two views over overlapping data. Both pipelines independently call the same Composer backtest endpoint with identical parameters (`capital: 10000`, `broker: alpaca`, same slippage/fee flags) for the same 30 symphonies, on two separate schedules (`update_metrics.py` vs. `refresh_full_database.py`), both gated by the same 7-day staleness window, genuinely redundant work computing the same numbers twice.

**Two options were considered:**
- **Option A (chosen): cross-link only.** Keep both pipelines fully independent, no schema, script, or workflow changes. Purely additive navigation between the two existing views.
- **Option B (explicitly deferred, not rejected): single source of truth for metrics.** Have `strategies.json` stop independently backtesting the 30 curated symphonies and instead join to `database_summary.json` by `symphony_id` for its numeric metrics, keeping `strategies.json` as an editorial-only layer (`description`/`ai_summary`/`how_it_works`/`signals`/`risk_profile`/`tags`/`slug`, none of which exist in the raw database and can never be derived from it). Rejected for now specifically because it introduces a real coupling risk that needs its own decision before being safe to build: if a curated strategy's row in the full database ever gets `flag`'d (`excluded`/`caution`/`duplicate`/`retry`) or a refresh fails, the curated pages could go stale or blank with no defined fallback. Revisit this as its own future decision, not bundled into Option A.

**Option A implementation plan (not yet built):**
- [ ] Strategy detail pages (`strategies.html?slug=X`) get a "View in full database →" link to that symphony's row in `database.html`. Requires a way to deep-link to a specific `symphony_id`/row that doesn't exist today (e.g. a `?symphony_id=X` query param that pre-filters/scrolls the All Strategies table to that row): this sub-piece needs its own small design pass at implementation time, not just a static link to `database.html`.
- [ ] `database.html` rows whose `symphony_id` matches one of the 30 curated strategies get a small "★ Curated" badge/indicator, linking back to that strategy's `strategies.html?slug=X` detail page. Needs a client-side lookup set built from `strategies.js`'s `symphony_id`s (cheap, only 31 entries, no new data file needed).
- [ ] No changes to `data/strategies.json`, `data/database.json`, `scripts/update_metrics.py`, or `scripts/refresh_full_database.py`: this is UI/navigation only.

**Explicitly not in scope for this item:** eliminating the duplicated metrics refresh (that's Option B, deferred), any change to which fields live in which file, and any change to refresh schedules.

### V2.3: Community Signals

**Status:** Backlog, lowest priority of the open work; deliberately scheduled after all V2.2 items (decided 2026-08-15)

- [ ] **Strategy submission form, deferred as far out as possible; use an external Google Form, not a self-built intake (decided 2026-08-15)**: kept on the roadmap but explicitly last. When it is eventually built, it must **not** be a self-hosted form that posts data anywhere Atlas controls: link out to a **Google Form** instead, so submissions land in the author's own Google account and the site itself never collects, stores, or processes visitor data. That keeps the zero-server posture (Tenet 4) and the no-user-data stance (Section 4, Tenet 7) intact: the site holds only a plain outbound link, with no backend, no form handler, and no personal data touching Atlas. Submissions are then triaged manually into the normal "Adding a Strategy from a Composer URL" workflow. Do not build a native form, a serverless handler, or any email capture as part of this.
- [ ] Curator notes field visible on strategy pages
- [ ] Related strategies section on each strategy page

### V2.4: Overfit Check

**Status:** Requested by the owner 2026-08-28. **Tier 1 shipped 2026-09-06 as v1.75.0**, at
`overfit.html`; see "Shipped shape, 2026-09-06" below for what was built, what the owner decided,
and which of this spec's numbers the build corrected. **Tiers 2 and 3 are not started** and their
prerequisites below still stand. **This spec was rewritten 2026-08-28** after the owner rejected its
first framing; see "What changed and why" at the end, because the rejected version is instructive.

**The ask:** paste a symphony, find out whether it is overfit. Signal overfitness, return
concentration in the best days, and whatever else the research supports.

**Where this sits, and why it is numbered here.** **Placed late in the sequence at the owner's
request, 2026-08-28**, after the specification was written. Numbered V2.4 so the ordering is
unambiguous rather than implied.

**It is not blocked on V2.3.** The community-signals form is deliberately last for its own reasons
and has nothing to do with this tool. The real prerequisites are:

1. **V1.20 finished**, or at least past the item 19 gate. This tool renders the same kind of
   quantitative disclosure the strategy page is being rebuilt around, and building it first would
   settle those presentation questions in the wrong place.
2. **The Tier 2 validation project**, described below. Without it, two of the three tiers are
   unvalidated and the page cannot honestly say much beyond the population table.
3. **The V4.0 architecture decision** for Tier 3 only, which may never come.

**Nothing about the research below expires**, so a delay costs nothing except the tool not existing.
The measurements are recorded in full at the end of this section precisely so that picking this up
later does not mean starting over.

**What it would be:** a new page, `overfit.html`, in the family of `/converter`, `/nodes` and
`/signal-miner`. Not a pass or fail, for reasons the measurements below force. **This spec originally said "not a score" as well; v1.76.0 revises that** to a single unweighted ratio shown beside par, at the owner's request and without conceding the thing the constraint protected. See "The fitted-era split and the Overfit Score" below.

---

#### Start from the definition, because it is measurable here

**Overfitting is not unusualness. It is fitting noise, and the test is whether performance survives
out of sample.** That is a definition with a procedure attached, and this project can run the
procedure: `oos_date` records the last time a symphony's logic was edited, and it is populated on
**6,470 of 6,472 usable database rows**. Days after that edit were not available to be fitted to.

**5,095 symphonies have gone at least a year without a logic edit.** Comparing each one's
backtested annual return against what it actually delivered over the following year:

| | Result |
|---|---|
| Median backtested annual return | **49.4%** |
| Median actual out-of-sample year | **17.6%** |
| Delivered at least their backtest | **22.2%** |
| Delivered at least half of it | 39.1% |
| Merely positive | 77.9% |
| Degraded at all | 77.8% |

**The typical Composer symphony delivers about a third of its backtested annual return once its
author stops editing it.** That single table is arguably a better answer to "is this overfit" than
any per-symphony score, and it is a fact about the population that this site is uniquely positioned
to state, because it has the 6,669 rows and the edit dates.

**One limitation, stated up front because it changes what the number means.** This is
out-of-sample with respect to *editing*, not a clean data holdout: the backtest window still
overlaps the year being measured. It captures the author who kept tweaking until the curve looked
right, which is the dominant way a Composer symphony gets overfit. It does not capture a symphony
overfitted in a single pass and never touched again.

---

#### The measurement that determines whether the tool can work at all

If overfitting is degradation, then a flag is only useful if it **predicts** degradation. So every
candidate flag was tested against the out-of-sample outcome for those 5,095 symphonies.

**The naive test is a trap and has to be controlled for.** Correlating a flag with (out-of-sample
minus in-sample) is partly tautological, because that gap is mechanically anti-correlated with the
in-sample figure. Run raw, in-sample annualized return "predicts" degradation at r = -0.904, which
is regression to the mean wearing a lab coat. **The controlled test holds in-sample return roughly
constant by scoring within its deciles**, and reports the mean rank correlation across the ten:

| Candidate flag | Mean within-decile rho | Consistent? | Verdict |
|---|---|---|---|
| **Annualized turnover** | **-0.316** | negative in **10 of 10** | **The strongest signal in the database** |
| Backtest length | +0.188 | positive in 9 of 10 | Real, weaker |
| Win rate | +0.185 | positive in 9 of 10 | Real, weaker |
| Sharpe ratio | +0.080 | sign flips | Too weak to use |
| **Return from the best 5% of days** | **-0.065** | **sign flips, 4 of 10 positive** | **Does not predict** |

**The metric the request named, and the one V1.20 item 4 already ships, does not predict
out-of-sample failure.** Its within-decile correlation is near zero and its sign is unstable. This
does not make item 4 wrong: outlier dependence is a true and useful statement about what a backtest
rests on. **It makes it the wrong basis for an overfit verdict**, and the tool must not imply
otherwise.

**Turnover is the finding.** Nobody reaches for turnover when asked about overfitting, and it beat
everything else that was tested:

| Turnover quintile | n | Median backtest ARR | Median out-of-sample year | Median gap |
|---|---|---|---|---|
| 1 (0 to 14) | 1,008 | 17.1% | **18.5%** | **+1.5 pts** |
| 2 (14 to 29) | 1,008 | 37.6% | 20.7% | -16.3 pts |
| 3 (29 to 45) | 1,008 | 56.0% | 18.8% | -35.9 pts |
| 4 (45 to 69) | 1,008 | 80.7% | 17.7% | -58.5 pts |
| 5 (69 to 172) | 1,010 | 153.9% | **3.8%** | **-142.4 pts** |

**The lowest-turnover quintile is the only cohort that kept its backtest.** The highest promised
153.9% a year and delivered 3.8%.

**And the honest caveat that has to travel with it:** high turnover degrades returns through
**trading costs and slippage**, which is a mechanical drag, not curve fitting. Both stories predict
this table and the data here cannot separate them. The tool must present turnover as "this is what
predicts a backtest not surviving" and not as proof of overfitting. Distinguishing the two needs
per-trade cost modelling that does not exist yet.

**Also note what did not replicate.** Short backtests are supposed to be the classic tell, and in
the raw data the under-two-year cohort had the *smallest* median gap (-3.0 points) because it also
promised the least (26.0% ARR). Backtest length only becomes a real predictor after controlling for
in-sample return. Any version of this tool that flags "short backtest" without that control will be
wrong in a way that looks authoritative.

---

#### Can AI tell that a signal is probably random?

The owner's second question, and it deserves a direct answer rather than an enthusiastic one.

**Not from the rule itself. That is a limitation of the input, not of the model.** Whether
`RSI(10) of SMH < 23` is a real effect or noise is not a property of that sentence. It is a property
of the relationship between the rule and the price history, and it is simply not present in the text
being read. A more capable model does not fix this, because the information is absent, and a model
asked anyway will produce a confident answer with nothing behind it. **That failure mode is worse
than no feature**, since it is exactly the false authority this tool exists to puncture.

**What AI can genuinely contribute is a prior about mechanism, clearly labelled as a prior.** There
is a real difference between a rule that names a known market effect (momentum, mean reversion, a
volatility regime gate, a flight to quality) and an arbitrary conjunction of unrelated instruments
and lookbacks. A model is decent at telling those apart, and "this rule has no stated mechanism"
is a legitimate observation. **It must never be blended into the statistical measures**, because a
plausible story is not evidence, and the most dangerous overfitted rules are the ones that sound
sensible.

**The rigorous answer to "is this signal likely random" is a multiple-testing correction, and this
project is unusually well placed to compute one.** The question is not whether one rule looks good,
it is how good the best of N tried rules would look under the null of no skill. Search a large
enough space and a spectacular backtest is guaranteed. **The Signal Miner already brute-forces about
4.8 million signals over a fixed universe**, so it can produce the *empirical* null distribution of
best-achievable performance by pure search on this exact data. That is far better than the usual
analytic approximation (Deflated Sharpe Ratio and friends) because it needs no distributional
assumption. **Section 14's Signal Miner item A, parameter plateau scoring, is the same insight from
the other direction** and the two should be designed together rather than twice.

**An architectural constraint that limits the feature as asked.** This site is static with no
server and no accounts, so there is no live model call available for a pasted symphony. An AI
plausibility read would have to be **authored offline and committed**, the way `ai_summary` already
is for the featured 31. **It cannot run on an arbitrary paste** without the server-compute departure
that Section 14's V4.0 notes already rule out pending their own proposal. A live AI verdict on
arbitrary input is not on the table on the current architecture.

---

#### What the tool should actually do, in three tiers

**Tier 1. The population result, and where this symphony sits in it. Needs a database match.**

Show the degradation table above, then this symphony's own in-sample-against-out-of-sample
comparison since its `oos_date`, then its turnover quintile. This is the definitional test, it uses
only fields already in `database.json` and already joined by
`scripts/build_strategy_extras.py`, and it is the strongest thing the site can honestly say.

**Tier 2. Structural read of the pasted tree. Works on anything, no database match needed.**

This is the "signal overfitness" half and it is **largely built already**: `converter.html` accepts
a URL, ID or raw JSON, handles the Composer fetch with its CORS fallback, and walks the tree;
`nodes.html` already counts nodes by type. The overfit page is a third consumer of that parse.
Worth computing: free parameters against sample length; threshold specificity, since a gate at 79
is a fitted number wearing a convention's clothes; near-duplicate thresholds; unexplained window
differences such as a 70-day and a 75-day lookback in adjacent branches; branch count against
distinct assets; depth.

**Tier 2 shipped 2026-09-08 as v1.77.0.** All six measures named above are implemented:
free parameters (fixed thresholds plus *distinct* windows, since a window reused across ten branches
was chosen once), threshold specificity against the conventional RSI levels, near-duplicate gates
within three points on the same indicator, lookback windows within five days of each other,
conditions against distinct assets, and depth. Two decisions inside that are worth recording because
they change the numbers: a comparison between two indicators contributes **no** threshold, since
there is no tunable constant in it and counting one would overstate the parameter count; and only
bounded oscillators are judged against a convention, since a moving-average price level has no
convention to be off and calling one unusual would be inventing a standard. The denominator for the
free-parameter ratio is **`fitted_years`**, the era the author was actually fitting against, not the
out-of-sample window. The page also now accepts **raw symphony JSON**, which is the path that keeps
everything in the browser; a URL or ID asks Composer for the tree as `converter.html` does. The
panel's privacy line was rewritten to say which branch is which, because the old wording promised
more than the feature could keep.

**These are unvalidated.** Unlike Tier 1, none of them has been tested against out-of-sample
outcomes, because the database has no structural complexity field to test with. `active_asset_nodes`
is a map of currently active nodes to weights, so its length is today's diversification, not tree
size. **Tier 2 should be presented as observations about construction, never as a verdict**, until
somebody parses trees at scale and checks whether any of it predicts anything. **That check is
itself a worthwhile project** and would be the first real evidence that structural overfit
detection works at all.

**Tier 3. Parameter perturbation. The strongest per-symphony test, and blocked.**

Asking whether a rule survives one step either side of its fitted threshold requires re-running it,
which requires prices. **`data/prices.json` holds 72 tickers; 3,680 distinct tickers are held across
the database.** Only **1,112 symphonies, 16.7%, hold exclusively covered tickers**, and that counts
current holdings only, so the true figure is worse. UPRO alone is held by 2,271 symphonies and is
not covered. `composer_json_fuzz_tester` (Section 14, V4.0) already implements exactly this sweep
offline and is already named there as the first repo worth forking. Sequence this last, behind
V1.20 item 16 and the V4.0 architecture decision.

---

#### Design constraints

- **No server, no accounts, nothing pasted is stored or logged.** Analysis happens in the browser,
  apart from the Composer API fetch the converter already performs. Tenets 4 and 7.
- **No score out of 100.** A composite invites the optimisation this tool exists to detect, and its
  weights would be unfalsifiable. State the arithmetic.
- **Separate what is validated from what is not.** Tier 1 is tested against 5,095 real outcomes.
  Tier 2 is not tested against anything. Presenting them with equal confidence would be the tool
  committing the error it reports.
- **Every result names what it could not see.**
- **`/overfit` needs the nav, the footer and an Explore card** per Section 10's three registration
  points. Written when the grid had seven cards; on shipping it took the grid from nine to **ten**
  and changed the subhead from "Nine ways..." to "Ten ways...". The count in a spec goes stale, the
  three registration points do not.

#### Sequencing

1. **Tier 1 first**, as a lookup by URL or ID against `database.json`. Reuses the converter's ID
   extraction, needs no new data, and delivers the only validated finding on the list.
2. **Tier 2 second**, as a third consumer of the existing parse, explicitly labelled as unvalidated
   observations.
3. **Validate Tier 2 before promoting it.** Parse trees at scale, test the structural measures
   against out-of-sample outcomes the way turnover was tested here, and keep only what survives.
4. **Tier 3 last**, and only after the V4.0 architecture question is settled.

#### Shipped shape, 2026-09-06: Tier 1

Built as specified, at `overfit.html`, off a new derived file. Three owner decisions shaped it,
taken 2026-09-07: **Tier 1 only**, **lead with the population finding**, and **report both
out-of-sample cohorts side by side**.

**Why there are two population cohorts rather than the one this spec assumed.** V1.18 landed 3,175
true out-of-sample backtests in `data/oos.json` between this spec being written and it being built,
and they measure the same question better per row while being worse as a population. Both are
reported, because each one's flaw is the other's strength:

| | Trailing cohort | True out-of-sample cohort |
|---|---|---|
| What it compares | backtested ARR against the actual last twelve months | backtested ARR against a re-backtest of the untouched window alone |
| n | 5,228 | 3,175 |
| Median backtested return | +48.9% | +101.2% |
| Median actual return | +16.1% | +22.5% |
| Delivered the full backtest | **20.5%** | **4.0%** |
| Delivered at least half | 37.2% | 25.3% |
| Merely positive | 76.4% | 87.6% |
| Beat SPY | not measured | 53.3% |
| The flaw | the backtest window overlaps the year being measured, so it understates the gap | selected by in-sample score for the Leaderboard, so it is roughly the stronger half of the database |

**The disagreement is the finding, and it runs the way you would not guess.** The stronger half of
the database promised more than twice as much (+101.2% against +48.9%) and kept far less of it (4.0%
against 20.5%). A better-looking backtest is not merely no better afterwards: it gives up more of
what it showed you. The honest other half of that sentence, which the page also states, is that the
same cohort still ends up ahead in absolute terms, +22.5% against +16.1%.

**The turnover result replicated almost exactly** against fresh data, a year of drift and a
different cohort definition. Quintile bounds [13.9, 29.1, 45.5, 69.2]; median gaps -0.0, -19.1,
-36.2, -59.0, **-136.1** points; median backtested return climbing +17.1% to +149.5% across the
quintiles while median actual return *falls* +16.5% to +6.2%. A finding that survives being
re-measured on different data is worth more than one that was merely striking the first time.

**A claim this spec implies, corrected by measurement.** Backtest length is the tell everyone
reaches for first, and it separates far less cleanly than turnover. Sorted into quintiles the same
way, the four shortest fifths give up -55.0, -48.4, -40.4 and -46.3 points: not monotonic and barely
distinguishable. Only the longest fifth, ten years and up, keeps its backtest, and it manages that
by promising +19.7% a year rather than +62.9%. **Turnover is doing real work that backtest length is
not**, which is the whole reason the page leads on it.

**`data/overfit.json` and its `.js` twin, from `scripts/build_overfit.py`.** `database_summary.js`
is 4MB and lacks `annualized_turnover` and `total_costs` entirely; `database.js` is 19MB. Neither is
loadable on a tool page. The derived file carries the two cohorts, the turnover table, and a
**columnar** per-symphony index (parallel arrays, not 6,678 object keys) at 701KB, 289KB gzipped.
**Names cost more than every other column combined** (194KB gzipped without them) and are carried
anyway: without a name the result is a wall of numbers about an opaque 20-character id, and the
reader cannot tell whether what they pasted resolved to what they meant. The <500KB page-weight
target is homepage-only, which this page is not.

**It is rebuilt in both jobs that write either of its inputs**, `refresh-full-database.yml` and
`refresh-oos.yml`. It is a derived file with **no deploy gate**, unlike `strategy_extras.json`,
so a skipped rebuild would leave the page reporting last week's population against this week's
database with nothing to catch it.

**Verification is a throwaway headless-Edge driver, not a new harness.** `scripts/harness/` is
signal-miner shaped: it splices a hook past that page's IIFE tail to reach bindings no other page
has. This page is drivable entirely through the DOM, so it needed none of that. 24 assertions, all
passing: the population section renders with no interaction, the full lookup path, an id absent from
the database, input with no id in it, the clear button, and a symphony edited too recently to judge.
**One of them caught a real bug in the driver rather than the page**, which is worth recording:
asserting "no literal null reaches the reader" against `document.body.textContent` fails on the
page's own `<script>` source, because `textContent` includes it. The assertion now walks visible
text nodes only.

**A near miss worth recording.** The first demo symphony chosen had 174 days since its last logic
edit, so the example button landed on the "not enough untouched history to judge" branch and
demonstrated nothing. The example is now one that exercises every branch and whose two measures
disagree. **A demo input has to be chosen against the code paths, not picked for being recognisable.**

#### The period-confusion bug, found by the owner within a day of shipping

**The verdict sentence read `trailing_one_year_return` and described it as "since the logic edit".**
On a symphony untouched for 1,417 days it therefore reported "has lost money since" while the panel
immediately below it reported **+27.7% a year over that same period**. The page contradicted itself
on screen, and the wrong half was the half in bold at the top.

**The lesson is not "check your labels".** It is that this page carries **two measures over two
different spans**, `trailing_one_year_return` (twelve months, always) and the `data/oos.json` re-run
(the whole untouched window, whatever its length), and any sentence built from either one has to
name its span. The bug survived 24 passing assertions because every one of them checked whether text
*rendered*, and none checked whether it was *true*. The regression test added with the fix asserts
the claim, not the presence: on this symphony the verdict must not say the window lost money.

**Fixed by rebuilding the verdict around the better measure.** Where an out-of-sample re-run exists
it now drives the verdict, since it genuinely covers "since the edit"; the twelve-month figure is
only ever described as twelve months. Where the two disagree in sign, the page now says so outright
rather than leaving the reader to find the contradiction.

**Cumulative returns are now shown beside the annualized ones**, at the owner's request, and this
turned out to matter more than a formatting preference. The example symphony returned **+156.2%
cumulative** over 3.9 untouched years, which is +27.7% a year. Its backtested **+725.6% a year
compounds to +353,937%** over the same span. **Compounding is what makes the gap legible**: in
annualized terms it is one number against another, and in cumulative terms it is the difference
between doubling your money and multiplying it by three thousand. The compounded figure is labelled
hypothetical wherever it appears, because the backtest earned its rate over its own window, not
this one.

**One unit inconsistency went with it.** `excess_return` in `data/oos.json` is cumulative, and it
was being displayed directly beneath an annualized return under similarly-shaped labels. SPY's
cumulative return is now shown alongside it so the comparison is between two figures of the same
kind.

#### The fitted-era split and the Overfit Score, 2026-09-07

**This is the largest correction the page has taken, and it came from the owner.** Two things were
wrong with the shipped Tier 1 and they were connected.

**1. The comparison compared a period against a superset of itself.** Composer's backtest runs
through today. So `annualized_rate_of_return` on a symphony untouched for four years *already
contains those four years inside it*. Setting it beside the out-of-sample re-run was not a
promise-versus-delivery test at all: it was a window against a window that includes it, which biases
the gap toward zero by exactly the amount the untouched era went well.

**The fix needs no new API calls, because the arithmetic is exact.** The full window is the fitted
era chained onto the untouched era, so the fitted era can be divided back out:

```
(1 + cum_full) = (1 + cum_fitted) x (1 + cum_oos)
years          = ln(1 + cumulative_return) / ln(1 + annualized_rate_of_return)
fitted_arr     = ((1 + cum_full) / (1 + cum_oos)) ** (1 / (years_full - years_oos)) - 1
```

Verified to **3.55e-15 log points** and resolvable on **3,236 of 3,257** re-run rows; the remainder
have a fitted era under six months, which will not annualize honestly and is left unscored rather
than estimated. **`backtest_days` must not be used to get the window length: it is in TRADING days**
(1,704 of them is 6.77 calendar years), so it would need an assumed conversion factor where the
logarithm needs none.

**2. The owner's correction on what "overfit" means.** The design had drifted toward judging the
untouched era on its own terms, made money or not, beat SPY or not. The owner:

> the point of it being overfit is keeping up with what the backtest was expected to do over time. no?

**Right, and the drift was a real error.** "Made money, beat SPY" answers *is this a good strategy*.
A strategy backtested at +500% a year that goes on to deliver +15% a year is overfit whether or not
it made money, and one backtested at +12% that delivers +11% is not overfit even if SPY beat it. The
question is retention of its own promise.

**The Overfit Score.** `100 x (1 - delivered / fitted)`, clamped to 0 and 100, where both terms are
annualized rates over their own eras. 0 means it kept the whole rate its author was looking at, 100
means it kept none of it.

**Why this does not violate the "no score out of 100" constraint.** That constraint is recorded
above with its reason attached: *a single composite number invites the exact optimisation this page
exists to detect, and its weights would be unfalsifiable*. **The objection is to unfalsifiable
weights, not to a number.** This score has no weights. It is one measured ratio between two printed
quantities, so any reader can recover it, and there is nothing in it to tune. The owner asked for a
graded result rather than a binary on 2026-09-07 and this is the shape that grants it without
granting the thing the constraint was protecting against.

**Distribution across the 3,236 scored strategies:** p10 28.6, p25 58.2, p50 **79.1**, p75 94.9,
p90 100. 4.0% score 0 and 12.6% score 100.

**Par, and why the score is never shown alone.** Retention is itself strongly tied to how large the
backtest was: rank correlation between fitted rate and score is **-0.556**. Mean reversion
guarantees a gap after an extreme backtest whether or not anything was overfit, so a raw 95 is
damning against a par of 60 and unremarkable against a par of 97. The page therefore prints **par**,
the median score among neighbours in fitted rate, beside the number and as a marker on the bar.

**Par is deliberately kept outside the score, and that placement is the whole design.** The score
contains **no population data at all**, which is what keeps it a measurement of the pasted symphony
against its own promise, exactly as the owner framed it and consistent with the peer-ranking framing
they rejected 2026-08-28. Par is context printed next to a golf score, not a term inside it. Par is
a **nonparametric sliding median** over a 200-strategy window sampled at 24 points, interpolated
linearly between them and held **flat outside their range rather than extrapolated**: fitting a
curve would put a functional-form assumption underneath the one number the page asks readers to
trust, and an extrapolated par would be an invention at exactly the end of the scale where readers
care most.

**An empirical-null residual was built, tested and rejected as the headline.** Scoring each strategy
against what its cohort actually delivered produces a number that is **+0.928 rank-correlated with
annualized excess return over SPY**, with 80 to 83% tail overlap. It is largely a restatement of
beating the market, and it puts the population back inside the number. Rejected on both counts. The
same +0.93 relationship holds for the shipped score and **is stated in the page's own caveats**,
because a reader is entitled to know the score is not a fundamentally new signal; what it adds is
that it answers the question actually asked rather than a proxy for it, and it separates the two
exactly where the promise was largest.

**Rounding at the ends is a claim, not a formatting choice.** 0 and 100 assert "kept everything" and
"kept nothing". A 99.7 rounded to "100" would print the stronger claim, so scores inside half a
point of either end render with a decimal instead.

**The ceiling: a bigger backtest predicts a better future, up to a point, and then it inverts.**
Restricted to the 2,221 strategies with five or more fitted years so a short noisy window cannot
drive it, median untouched return rises with fitted rate up to about **+239% a year** (peaking at
**+40.3%** delivered) and then collapses. **The top decile, fitted at +551% a year, went on to
deliver +10.3%, which is less than the bottom decile's +12.5% off a fitted +21.9%.** The turning
point is reported as approximate, because it comes from ranking within this same database rather
than from a threshold anyone should tune to.

**Curated strategies are now exempt from the out-of-sample candidate cutoff.** `refresh_oos.py`
selected candidates by Leaderboard score, which asks whether a row could plausibly reach the top of
the board. That is the right question for ranking and the wrong one for the Overfit Check: a curated
strategy gets a hand-written page whatever it scores, and a missing re-run is most conspicuous
there. Measured 2026-09-07, **11 of the 24 visible curated strategies had no re-run for exactly this
reason**, seven of them with over a year of untouched history sitting unused. The exemption raises
candidates from 3,257 to 3,285, roughly a dozen extra API calls a week, and raises visible curated
coverage to 21 of 24.

**A hoisting bug was caught by the render harness and would otherwise have shipped.** The score
block declared `var SD` below the meta line that already read `SD.n`. `var` hoists the declaration
but not the assignment, so the page threw partway through initialisation: the methodology line
rendered blank and **the entire paste-a-symphony lookup was dead**. Nothing about the static page
above it looked wrong. The driver now stands at **53 assertions**, and the ones added here assert
claims rather than presence, per the lesson from the period-confusion bug: that the top ceiling
decile really does deliver less than the bottom one, that the verdict compares the fitted era rather
than the full backtest, and that a 99.7 does not print as 100.

#### Open questions

Three of these four were settled by building Tier 1. Kept with their answers rather than deleted,
because the reasoning is what a later tier will need.

- **Does it accept a symphony absent from the database?** **Settled: yes, as a normal result, not an
  error.** The shipped page names what it could not do and why the population findings above still
  hold, and points at the Database search. It cannot yet say anything Tier 2 would say, because
  Tier 2 does not exist; when it does, this is the branch it slots into.
- **Should the page lead with the population table rather than the pasted symphony?** **Settled
  twice, and the second answer is the shipped one. The paste box leads, by owner decision
  2026-09-07 (v1.76.1), reversing the ruling made earlier the same day.** The original reasoning
  still holds and is why the findings sit immediately below rather than behind anything: the
  population result is true before anyone types, and it survives a reader pasting a symphony the
  database has never seen. What it does not do is answer why the reader came. **Being the more
  important finding is not the same as being the first thing to show**, and the page had been
  ordered by importance rather than by use. Results render between the box and the findings, so a
  reader who pastes never scrolls past the analysis to reach their own answer, and one who does not
  paste meets the findings immediately. The DOM order is now asserted by the render harness, since
  nothing else would catch a later edit quietly restoring it.
- **Can turnover be separated from trading costs?** **Sharpened, not settled.** `total_costs` is
  reported by the same backtest that produced `annualized_rate_of_return`, and
  `refresh_full_database.py` requests it with slippage and both fee flags on, so **the in-sample
  figure is already net of modelled costs**. The turnover result is therefore not the trivial "the
  backtest ignored trading costs". What it cannot rule out is real slippage exceeding the model on
  a high-turnover strategy. The page reports an association and says which two stories fit it.
- **What does the page say about itself?** **Settled: it says it, in the caveats block**, in the
  same words this spec used. Saying so is cheap, so it is said.

---

#### Measurements, in full

Everything measured for this spec on 2026-08-28, kept here so nobody re-runs it. Source is
`data/database.json` (6,669 rows, 6,472 usable) and `data/prices.json` (72 tickers, 4,184 days,
2010-01-04 to 2026-08-21). Reference date 2026-08-23.

**Return concentration across the whole database**, 6,324 rows carrying the field:

| Percentile | Return from best 5% of days | | Other fields, median |
|---|---|---|---|
| 5th | 76.8% | | Best single day: **4.7%** |
| 25th | 108.3% | | Best 10% of days: **209.6%** |
| 50th | **143.0%** | | Kurtosis: **17.0** (95th pct 206.5) |
| 75th | 201.5% | | Tail ratio: 1.169 |
| 95th | 418.8% | | Win rate: 54.9% |

**80.6% of all symphonies get more than 100% of their total return from their best 5% of days**, and
45.8% get more than 150%. The V1.20 item 4 panel finds 25 of 31 for the featured strategies and the
full database agrees almost exactly. **This is why an absolute threshold on the metric is useless
as a flag: it fires on four symphonies in five.** It is also, separately, why the metric fails the
prediction test above. Two independent reasons not to build a verdict on it.

**Backtest length.** Median 3,172 days. **23.2% of the database is backtested on under five years
and 3.4% on under two.**

**Time since the last logic edit**, 6,427 rows with a usable `oos_date`: median **758 days**, 79.3%
at least a year, 53.1% at least two years, 28.0% at least three.

**Predicting the raw out-of-sample outcome rather than the gap.** A second control, run because the
gap is mechanically anti-correlated with the in-sample figure. Spearman rho against the actual
out-of-sample year return, n = 5,095: win rate **+0.232**, in-sample return +0.208, Sharpe +0.171,
backtest length +0.118, turnover **-0.119**, return concentration **-0.126**, Herfindahl -0.069,
tail ratio -0.049, kurtosis -0.046. **Everything is weak in absolute terms**, which is itself the
result: no single stored field comes close to predicting what a symphony will do next year. The
within-decile test in the main spec is the more informative one because it removes the artifact, but
neither should be oversold.

**The diversification confound, recorded so it is not rediscovered as a feature.** Concurrent
holdings appear to improve everything:

| Concurrent holdings | n | Median return from best 5% of days | Median Sharpe | Median win rate | Median backtest days |
|---|---|---|---|---|---|
| 1 | 2,481 | 162.7% | 1.33 | 53.7% | 3,728 |
| 2 to 3 | 1,160 | 159.4% | 1.35 | 54.6% | 3,457 |
| 4 to 7 | 1,014 | 140.3% | 1.50 | 55.1% | 2,942 |
| 8 to 15 | 690 | 123.6% | 1.77 | 55.9% | 2,159 |
| 16 to 31 | 435 | 104.5% | 2.06 | 56.7% | 1,832 |
| 32 or more | 543 | 94.8% | 2.26 | 57.4% | 1,832 |

**Read the last column before believing the rest.** The diversified cohort has roughly **half the
backtest length**, and median Sharpe by window is not monotonic either: 1.36 under two years, 1.60
at two to five, 1.95 at five to ten, back to 1.36 at ten or more. **A tool that rewarded a symphony
for holding more things at once would be scoring the sample period.** Note also that
`active_asset_nodes` is a map of currently active nodes to weights, so its length is today's
diversification and not tree size. **The database has no structural complexity field at all**, which
is exactly why Tier 2 needs the paste rather than a lookup, and why Tier 2 is unvalidated.

**Ticker coverage for Tier 3**, across the 6,661 rows carrying a holdings row:

| | Symphonies | Share |
|---|---|---|
| Every currently held ticker in `prices.json` | 1,112 | **16.7%** |
| Some held tickers covered | 5,179 | 77.8% |
| None covered | 370 | 5.6% |

**3,680 distinct tickers are held across the database and `prices.json` has 72 of them.** The
most-held uncovered names are UPRO (2,271 symphonies), VIXY (1,669), TECS (1,172), UGL (1,057) and
ERX (969). This counts only current holdings, so the reachable universe per symphony is larger and
true coverage is worse than 16.7%.

#### What changed and why

The first version of this spec, written earlier the same day, built the tool on **percentile
ranking against the database**: your symphony's return concentration is worse than 91% of the 6,324
measured. **The owner rejected the framing**, on the grounds that the tool is meant to determine
whether a symphony is overfit by definition, not to rank it against its peers.

**That was correct, and testing it afterwards showed the rejected design was worse than merely
philosophically off.** Percentile ranking on return concentration would have been ranking on a
measure that **does not predict out-of-sample failure** (within-decile rho -0.065, sign unstable).
The tool would have been precise, well presented, and measuring the wrong thing. The definitional
framing survives because it can be checked, and checking it is what exposed both the turnover
finding and the weakness of the metric the tool was originally going to be built on.


---

### V2.5: Documentation Audit and Social Sharing Tags

**Status:** queued 2026-09-07 at the owner's request. Two related pieces of work, specified in full
here and **deliberately not executed at the time of specification**. The owner's instruction was to
add them to the roadmap rather than build them, which is why this section is longer than the work
is far along.

**The external standard this is audited against** lives at
`https://azqato.github.io/prompts/#/documentation`. It is the owner's portable documentation
standard, applied across projects rather than written for this one, and it is the authority for
this item. Read it before starting: the summary below records what it asks for and how this project
already stands against it, but it is a summary and the source can move.

#### Part 1: the documentation audit

**What the standard asks for.** A full read-only crawl of the codebase, then every document in
`/docs` read in full and compared against it, then updated. The rule that matters most is **merge,
do not overwrite**: documentation holds intent and rationale that cannot be reconstructed from code,
so where the code contradicts a document the original text stays and the observed reality is added
beside it as a marked discrepancy for the author to resolve. Code can be wrong as easily as a
document. A second rule sits underneath it: **an existing project rule beats an imported default**,
and where the two differ the difference is flagged rather than silently replaced.

**Where this project already stands.** Better than a cold start, which is worth recording so the
audit is scoped as a gap-check rather than a rewrite:

| The standard asks for | This project has | Gap |
|---|---|---|
| Four documents: `README.md` at root, `PRD.md`, `DESIGN.md`, `PATCHNOTES.md` in `/docs` | Exactly that structure, since V1.3 consolidated 12 files into 4 | **None.** Already conformant |
| `LICENSE.md` at root, all rights reserved, with a NO WAIVER clause and an AI and search carve-out | Exactly that. Added v1.30.4 by owner decision, renamed from `LICENSE` to `LICENSE.md` in v1.31.2 (Section 25, item 26), referenced from `robots.txt`, and carrying all the required sections | **None.** Verified 2026-09-07 rather than assumed: the first draft of this table listed the extension as an open gap, and reading the repository disproved it |
| `robots.txt` at root, fully open, with a comment marking that as deliberate | Exactly that, including the comment and the `Sitemap:` line | **None** |
| `sitemap.xml` at root, or elsewhere if named in `robots.txt` | At root, and named in `robots.txt` | **None** |
| PRD sections: problem, users, goals, non-goals, stories, features, constraints, assumptions, success criteria, tenets, roadmap, metrics, runbook, technical requirements, conventions, writing style, browser testing, verification environment, security, licensing, social sharing, deprecation, doc versus reality, risks, working practice, press release, FAQ | Sections 1 to 27 cover all of these | **Verify rather than assume.** Every section exists by name; whether each is current against the code is the audit's actual job |
| Em dashes prohibited in three forms, swept project-wide with a count reported | Section 19 states the rule; the Unicode character and the entity both measure zero in the docs | **Sweep the rest of the project**, not only `/docs`. Page copy, code comments and commit bodies were never swept as a set |
| Edge for browser testing, never Chrome, with the binary path in the runbook | Section 11 and the harness both state it | **None** |
| Verify locally, never against production | Stated and enforced in practice | **None** |

**So the audit is not a rewrite.** It is a currency check on 27 existing sections plus two specific
sweeps, and the honest expectation is that it finds stale numbers rather than missing structure.
Section 24 already carries 28 rows of exactly that kind, three of them added the day this was
queued, which is the best evidence for what the audit will turn up.

**The one thing to be careful about.** The standard says completeness beats brevity in the PRD, and
this PRD is already past 7,200 lines. That instruction is a licence for more facts, not more words
around the same facts, and it explicitly is not a licence for filler. An audit that grows the
document without adding information has failed on the standard's own terms.

#### Part 2: social sharing tags

**Specified in full in Section 27**, which was written first because the owner asked for the
no-drifting-numbers rule to be recorded before any page was touched. That ordering turned out to
matter: see below.

**Current state, measured 2026-09-07: zero Open Graph and zero Twitter Card tags across all 15 HTML
files.** A link pasted into a chat client renders from whatever the client can scrape unaided,
normally `<title>` and `<meta name="description">`. What ships today is a fallback, not a design.

**The scope when this is built.** Twelve pages get tags, being the twelve in `sitemap.xml`. Three
are deliberately excluded and the exclusions belong in Section 27 so a later reader can tell a
decision from an oversight: `404.html`, because sharing tags make a broken address look legitimate;
`_wf-mockup.html`, an unshipped mockup; and `signal-lab.html`, a `noindex` redirect stub kept only
so old Signal Lab links resolve.

**Four implementation details that are not obvious and cost a rebuild if missed.**

1. **Placement is load-bearing.** Tags go immediately after the viewport meta, above the stylesheet
   and above any inline `<style>`. Some scrapers read only the first few KB of a document, and
   `overfit.html` carries roughly seventy lines of inline CSS in its head. A tag pushed below that
   can fall outside the window a scraper actually fetches, and the failure is indistinguishable
   from having no tags at all.
2. **`og:*` takes `property=`, `twitter:*` takes `name=`.** This is the specification, not a
   preference. A tag written the wrong way validates as HTML, renders nothing, and reports no error.
3. **`og:url` is absolute, per page, and unique.** Copying a head block between pages and forgetting
   to change the URL is the most common failure and the most silent: every card still renders, and
   every one of them links to whichever page was copied from.
   **It is also the extensionless address, and a `<link rel="canonical">` beside it carries the same
   value** (2026-10-18). Cloudflare's default asset HTML handling answers `/page.html` with a 307 to
   `/page`, so `og:url`, the canonical and the sitemap `<loc>` all name `/page` (the homepage is
   `/`). `strategies.html` and `guides.html` repoint both per slug at render time through
   `setPageUrl()` in `js/app.js`, to `/strategies?slug=...` and `/guides?slug=...`. Internal links
   keep `.html`, because the site must also work from `file://`. `scripts/check_social_tags.py`
   asserts `og:url` and the canonical both equal the sitemap entry, and fails, rather than skips, a
   sitemap entry with no file: it silently checked nothing for one commit after the sitemap went
   extensionless.
4. **Escape the attribute.** A stray `&` or a straight quote in a description truncates the tag
   mid-attribute.

**One description per page, not two.** Where a page's existing `<meta name="description">` is
accurate it is reused verbatim as the `og:description` rather than competing with a second one.
Where it is stale it is corrected so both carry the same sentence. Four of the twelve were found
accurate and reusable; the rest need rewriting, three of them because they are wrong rather than
merely thin (Section 24, rows 26 to 28).

**Writing Section 27 before touching a page caught a live violation in the draft.** The prepared
`rsi.html` description read "the 20 ETF tickers", and 20 is read from `data/rsi.json`. It is exactly
the drifting number the section prohibits, in the first batch of tags written after the section was
committed. "10-day RSI" in the same sentence is fine, because the window is a constant of the
indicator rather than a measurement. **This is the argument for keeping the two parts of V2.5 in
this order:** the policy is cheap to write and catches its own violations, and a tag shipped with a
number in it is invisible until it is wrong.

**Compliance is a script, not an argument.** A read-only checker asserting: all six tags present on
every page that should carry them; `og:title` at 70 characters or fewer, `og:description` 200 or
fewer, `og:site_name` 20 or fewer, with the actual count reported for anything over the target
budgets of 60 and 150 so a person can judge the borderline cases; every `og:url` absolute, `https`,
and unique across the site; no `og:title` containing the `og:site_name` string; and where `og:image`
is absent, `twitter:card` set to `summary`. **Whether that checker becomes a sixth deploy gate is an
open question and is not to be decided by whoever writes it.** The precedent is the V1.20 item 10
validator, which was written and deliberately left manual pending an owner ruling. Section 25
carries this as an open question.

**The drifting-numbers rule cannot be checked by a script**, because prose cannot distinguish a
measurement from a constant. It is enforced at review, which is why it is written down at length in
Section 27 rather than encoded.

#### What is deliberately not in scope

**Per-strategy sharing cards.** Strategy pages are addressed as `strategies.html?slug=...` and
resolved in JavaScript. A scraper reads raw HTML and never runs it, so all 25 strategy URLs in the
sitemap would share one identical card no matter what is written. Fixing that means pre-rendered
pages or an edge worker, which is a structural change to how the site is built and not a tagging
change. Recorded here so a later reader does not mistake the single shared card for an oversight.

---

### V3.0: Removed (2026-08-15)

Formerly "Monetization Expansion" (premium strategy tier, newsletter integration, strategy performance alerts). **Removed entirely, not deferred.** The site will not be monetized beyond voluntary reader donations via Buy Me a Coffee, reached through the Support link in the nav and footer, and will not collect user data. See Section 3 (Goals) and Section 4 (Non-Goals). Do not reintroduce ads, paid tiers, email capture, or alert products; if the funding model is ever revisited, that is a fresh product decision, not a resumption of this section.

### V4.0: Signal Discovery & Robustness Tooling (Extreme Future State)

**Status:** Ideation, extreme future state, not near-term. No implementation, forking, or architecture work should begin until V2.x is well underway and this section has been re-scoped with fresh eyes (V3.0 was removed 2026-08-15, so V2.x is now the gate). Documented now (v1.11.5/v1.11.6/v1.11.7) purely so the idea isn't lost.

Five external repos were reviewed as candidate forks: `composer_json_fuzz_tester`, `rsi_search`, `strategy_generation` (private, all owned by GitHub user `VoxMachina1`), `quantstats-js` (public, GitHub user `whsmacon`), and `local-maestro` (public, GitHub user `Gabraham4`). The first three operate on Composer strategy JSON exports and Tiingo price data, entirely outside Composer Atlas today; the latter two are standalone portfolio-analytics/reporting tools. This section documents what each does and how they *could* eventually plug into the site, as a distinct, separately-run "Signal Miner" / analytics capability, not a rewrite of the existing static site.

**⚠️ Adaptation note (applies to all five tools):** None of these repos are drop-in. Every one of them was built as an independent, standalone project with its own assumptions about environment, data format, and output, not against Composer Atlas's actual data layer (`data/database.json`, the Full Database JSON Schema in Section 12) or its existing front-end structure (static HTML/CSS/vanilla JS, no build step, no Node runtime in production, uPlot for charting, see Section 10). Forking any of them means re-authoring the integration points, not just `npm install`-ing or `git clone`-ing and wiring up a call. Treat every item below as "study this, then rebuild the integration surface to fit Atlas," never "paste this in."

**What each tool does:**

1. **`composer_json_fuzz_tester`**: Robustness/fragility auditor for a *single existing* strategy. Walks a strategy's JSON tree, extracts every `IF` condition (RSI thresholds, MA/EMA crosses, cumulative-return and max-drawdown gates, etc.), and re-runs the backtest across a 2D parameter sweep (±30% by default) around each condition's fitted period/threshold. Outputs a self-contained HTML report with heatmaps and a fragility score (coefficient of variation of win rate across the sweep) per condition, color-coded Robust → Very Fragile. Directly answers "is this condition a real edge, or does it only work at one magic number?"
2. **`rsi_search`**: A three-stage pipeline (backtest → filter → insert) that searches for RSI-based "frontrunner" signals, assets that could pre-empt or improve on an existing strategy's decision points, and can automatically insert validated logic back into the strategy JSON at the correct node, ready to re-import into Composer. Filter thresholds are currently hardcoded (win rate > 75%, > 20 trades, benchmark median return < 0).
3. **`strategy_generation`**: The most ambitious and most in-flux of the three Python tools: a from-scratch 15-stage discovery pipeline (data fetch → signal generation → in-sample backtest → out-of-sample walk-forward validation → tail-risk analysis → Composer export). Per its own `VISION.md`, this is the intended long-term convergence point for the other two tools, the fuzz tester's tail-analysis becomes an automated pipeline stage, and the RSI-search insertion logic generalizes to all indicator types and both of the vision doc's two signal archetypes (short-duration "replacement" signals vs. longer-duration "regime/timing" gates). The author's own docs list several pre-requisite bug fixes and note this project is pre-alpha/actively evolving, the least stable of the four to fork against.
4. **`quantstats-js`**: A Node.js/JavaScript port of the popular Python `quantstats` library: 40+ portfolio metrics (Sharpe, Sortino, Calmar, CAGR, VaR/CVaR, Kelly Criterion, Ulcer Index, drawdown-period detail, etc.) plus a "tearsheet" generator that produces a self-contained HTML report with 13+ SVG charts (cumulative returns, rolling Sharpe/Sortino/volatility, monthly heatmap, underwater drawdown plot) from a plain `{values, index}` daily-returns series, with optional benchmark comparison. Unlike the three Python tools, this is pure JavaScript with zero core dependencies, meaningfully more compatible with Atlas's existing static, no-backend, vanilla-JS architecture, since it can in principle run client-side in the browser rather than requiring a Python environment or server compute. Directly relevant to Atlas: it computes a superset of the metrics already tracked per strategy (Section 12's Full Database schema) plus many not currently shown (Sortino, Calmar, Ulcer Index, VaR/CVaR, per-drawdown-period detail, rolling stat charts), and its tearsheet format is a natural candidate for an expanded per-strategy detail view. Its main gap: it needs a daily equity-curve/returns series as input, which Atlas's schema doesn't currently store (see `local-maestro` below for a tool that already solves that data-loading problem).
5. **`local-maestro`**: A local, offline recreation of [MyMaestro.co](https://mymaestro.co): *multi*-strategy portfolio correlation and risk analysis, as opposed to the single-strategy focus of the other four tools. Given a set of strategies' daily equity curves (loaded from CSV, Composer's own `dvm_capital` backtest-cache JSON format, or auto-fetched via the Composer API using a symphony ID), it aligns them to a common date range, simulates a weighted portfolio, and produces an HTML report (Plotly.js charts) across five tabs: Returns, Correlations (including a correlation matrix heatmap and its own **CARP**: Correlation And Risk-adjusted Performance = Sortino ÷ (1 + mean correlation): metric), Volatility, Exposure, and a combined Metrics summary. Validated by its author at ~97–99.9% accuracy against MyMaestro.co across 5 test strategies. Directly relevant to Atlas: this is the "how do these N strategies in my portfolio interact / diversify each other" question, which nothing in Atlas answers today (Atlas shows each strategy's metrics in isolation): a natural fit for a future "build a portfolio from the library and see the correlation/CARP profile" feature. It also already contains a working `data_loader.py` that turns Composer backtest-cache JSON into aligned daily equity-curve series, the same raw-data problem `quantstats-js` has, solved with a different language/library stack (pandas/numpy/Plotly instead of vanilla JS), so if both are ever pursued, that loading logic is worth reviewing side by side to avoid solving it twice, even though it would still need porting to fit Atlas's existing JS-only front end.

**Why fork rather than build from scratch:** The three Python tools already implement the hard, error-prone parts, correct Composer JSON traversal/insertion (node IDs, `if-child` structure, `wt-cash-equal` blocks), zero-lookahead-bias backtesting mechanics, and Tiingo data plumbing with key rotation and freshness caching. Rebuilding this from zero would be substantial duplicated effort; the existing `refresh_full_database.py` pipeline in this repo already solves an adjacent but distinct problem (bulk metric refresh via the Composer API, not local backtesting against raw price data). `quantstats-js` similarly already implements dozens of metric formulas validated against the reference Python library and a full SVG charting layer, reimplementing 40+ statistically fiddly formulas (VaR, CVaR, Ulcer Index, Kelly Criterion, drawdown-period detection, etc.) from scratch would be its own multi-week effort for something this library already gets mathematically right. `local-maestro` similarly already solves cross-strategy alignment, portfolio simulation, and correlation math (validated to ~97–99.9% against a real reference implementation, MyMaestro.co): the kind of numerically fiddly, easy-to-get-subtly-wrong work not worth re-deriving from scratch.

**Major architectural implications (why this is "extreme future state," not a near-term item):**

- Composer Atlas is currently a fully static, browser-only site with **zero server infrastructure** ([Tenet 4](#4-zero-cost-to-operate), Section 15). The three Python signal-discovery tools and `local-maestro` are all local CLI scripts (the latter also offers an optional local web server, `server.py`) requiring a Python environment and non-trivial compute time (parameter sweeps, 15-stage pipelines, and portfolio correlation analysis are not something a static site or GitHub Pages build step can run per-request).
- Any real integration of the Python tools means one of: (a) a scheduled/offline batch job (analogous to `refresh_full_database.py`) that pre-computes fragility/signal/correlation reports for library strategies and publishes static JSON/HTML artifacts the site can serve as-is (cheapest, most consistent with current architecture), or (b) standing up actual server-side compute (serverless function, small backend) if on-demand user-submitted strategy analysis is ever wanted, a real departure from the current zero-cost, static-only posture that would need its own dedicated proposal and cost/security review before any code is written.
- `quantstats-js` is the exception on the compute question (pure JS, could run in-browser) but still needs real adaptation work: it's authored against Node.js conventions (`fs.writeFileSync`, npm/ES module imports, its own bundled MUI-style CSS and SVG chart renderer) rather than Atlas's existing no-build-step `<script>`-tag JS and uPlot-based charting (see Section 10, JS Utility Functions), and it expects a `{values, index}` daily-returns array as input where Atlas's data layer stores pre-computed summary metrics per strategy in `database.json`, not raw daily-return series, feeding it real data would likely require sourcing/storing daily equity-curve series per strategy, which the current schema doesn't capture.
- `local-maestro` has the same "needs daily equity curves, Atlas doesn't store them" gap as `quantstats-js`, plus it's built on pandas/numpy/Plotly.js, a heavier, Python-side dependency stack than a pure-JS port would require, and its interactive server mode (`server.py`) is a genuine local server, not something a static GitHub Pages deploy can host as-is. A user-facing "build a portfolio and see correlations" feature would most realistically need either an offline batch pre-computation (fixed set of curated multi-strategy portfolios, not arbitrary user-built ones) or the server-side compute departure noted above for arbitrary combinations.
- Needs Tiingo (three Python tools) and/or Composer API access (`local-maestro`) with its own rate-limit/cost management, separate from the existing Composer API key and rate-limit handling already documented in Section 13.
- `strategy_generation` is explicitly pre-alpha per its own docs (known bugs, `.planning` scratch docs, no stable public interface yet): forking it today would mean forking a moving target upstream.

**If/when this is revisited, in rough order:**
- [ ] Re-review all five repos for drift against this write-up (upstream is actively developed, especially `strategy_generation`, `quantstats-js`, and `local-maestro`)
- [ ] Decide the batch-artifact-vs-live-backend architecture question above before writing any code
- [ ] Start with `composer_json_fuzz_tester` only (single-strategy robustness report is the most self-contained, lowest-risk fork, no insertion/mutation of strategy JSON, read-only analysis) as a static "Robustness Report" tab per strategy, generated offline and committed like other database artifacts
- [ ] Only after that ships and proves the batch-artifact pattern, evaluate `rsi_search` / `strategy_generation` for a "Signal Miner" / candidate-signal discovery feature feeding V2.3 Community Signals
- [ ] Evaluate `quantstats-js` separately from the Signal Miner track, it's an analytics/reporting upgrade, not a discovery tool. Would require deciding whether to (a) store daily equity-curve series per strategy (schema change) to feed it properly, or (b) adapt just its metric-formula layer against Atlas's existing summary metrics without the full tearsheet/daily-series machinery
- [ ] Evaluate `local-maestro` as a separate "portfolio builder" feature (multi-strategy correlation/CARP analysis) rather than folding it into per-strategy tooling, it answers a different question (how strategies interact) than the other four (is this one strategy robust/improvable). Would share the daily-equity-curve schema gap with `quantstats-js`; worth solving that gap once for both if both are ever pursued
- [ ] Any strategy-JSON mutation (insertion of discovered signals) must be reviewed carefully, these tools write modified strategy JSON meant for re-import into Composer; Atlas has never mutated strategy definitions, only displayed them

### V4.1: Synthetic Backtester (Extreme Future State)

**Status:** ideation. Owner request, 2026-08-30. No implementation work should begin. This sits at
the same distance as V4.0 and shares most of its blockers, plus one of its own that is larger than
anything in V4.0.

**The ask, in the owner's words:** "create synthetic backtester, a tool that allows users to paste in
composer symphonies and run a local backtest according to historical data, substituting popular
tickers for calculated methods."

The reference the request was made against is **Crescendo Suite** (`v4438c863`, released 2026-08-28),
a desktop application, supplied as four screenshots of a run over "zoop's 2026 Wash Sale Master
Symphony". Everything below is read off those screenshots. Nothing was run, and nothing here has
been verified against the application itself or its documentation.

#### What the reference application exposes

**Input surface (Run Backtest tab).** A symphony is added as a row in a *Strategy Input* table with
four columns: `Name`, `Source`, `Symphony ID`, `Version`. The captured row reads
`283m9WIEVV8nP6po2gtF` for the ID and `0o6wSrLXb5uTUe9drOYA` for the version, with `Source` showing
`Checking Latest...`, so the tool resolves a symphony by ID against a live upstream and pins a
**version hash** alongside it. Symphonies can be added by Paste, File, or Browse. Bare tickers can
be added to the same run through a separate `Add Ticker` row, so a strategy and a buy-and-hold
comparison sit in one report. A `Benchmark` is set independently at the top (`QQQ` in the capture).

**Run controls.** `Borrow Rate %` (default `10`) and `Leverage` (default `1`) are explicit numeric
inputs, alongside checkboxes for `Leverage Sweep`, `Unified Report`, `Scrub Report`, and
`Analyze Trade Timing`. Date range is a four-way radio: `Standard`, **`Synthetic`** (selected),
`Default Pathing`, and `Custom` (showing `1987-01-01` to `2026-08-12`), plus an
`Exclude dates/ranges` checkbox with its own picker.

Two of these are worth naming separately. **`Synthetic` is a date-range mode, not a data source
toggle**, which is the whole idea in one word: choosing it does not change what is being tested, it
changes how far back the test is allowed to reach. And **`Exclude dates/ranges` is a robustness
control in disguise**: drop 2020, re-run, and see whether the edge survives its best year. That is
the same question V2.4 Overfit Check asks, asked from the other direction.

**Report surface.** A single self-contained HTML report, headed "Generated with Crescendo v4438c863
(released 2026-08-28) on Aug 30, 2026 for the period from Feb 21, 2006 to Aug 28, 2026". It carries
cumulative returns vs benchmark on a log axis with a difference series, end-of-year returns as
grouped bars, an underwater plot, a **top-drawdowns chart with live `% Threshold` and
`Days Threshold` inputs** and a `Defaults` button, a rolling-CAGR chart against a full-period
reference line, and a monthly-returns heatmap with `Log Scale` and `Relative to Benchmark` toggles.
The right rail holds Returns, Drawdown, Risk-Adjusted, Volatility, Return Distribution, Trade
Activity, End of Year Returns, Worst Drawdowns (Strategy), Worst Drawdowns (Benchmark), Holdings
Breakdown, Contributions Breakdown, and Backtest Limiters, most behind a `Show More` expander.

Metrics shown for the captured run, strategy against `QQQ`: annual return 42.64% vs 15.91%, max
drawdown -38.01% vs -53.4%, longest drawdown 406 days, RoMaD and Calmar both 1.12 vs 0.298, alpha
0.34, beta 0.542, correlation 0.425, R-squared 0.18, information ratio 0.813, Treynor 0.786, risk
free rate 1.69%, Sharpe 1.34 vs 0.705, Sortino 2.2 vs 1, volatility 28.08% vs 21.98%, daily VaR
2.76% vs 2.22%, best year 350.2% vs 53.27%, worst year -20.5% vs -38.22%, time in market 100% vs
100%, win days 55.34% vs 55.67%.

Two structural readings of that block. **Holdings Breakdown lists only `SSO` and `SDS`** (avg 69.46%
and 30.54%, both ranging 20% to 100%, held 4,581 days at 88.7% and 3,566 days at 69.1%), which is a
2x long and a 2x inverse on the same index, held concurrently at varying weights. Time in market of
100% with beta 0.542 and R-squared 0.18 is the signature of a direction-switching overlay rather
than a market exposure. And **the report separates gross contribution from net**: SSO shows 69.56%
of gains and 67.96% of losses for a 76.68% total, SDS 30.44% and 32.04% for 23.32%. Atlas shows no
per-holding attribution of any kind today.

#### The Backtest Limiters table, decoded

This is the most valuable single artifact in the capture, and its meaning is not labelled anywhere
in the UI. It has three columns, `Ticker`, `Available From`, and `Extension`, and reads:

| # | Ticker | Available From | Extension |
|---|--------|----------------|-----------|
| 1 | LABU | 2006-02-21 | 31 days |
| 2 | UVXY | 2006-01-05 | 875 days |
| 3 | SOXL | 2002-07-17 | 519 days |
| 4 | SMH | 2000-06-19 | 3,140 days |
| 5 | KMLM | 1988-01-15 | 6,535 days |
| 6 | IEF | 1962-01-16 | 5,822 days |
| 7 | TQQQ | 1938-10-18 | 180 days |
| 8 | PSQ | 1938-01-31 | 10 days |
| 9 | QQQ | 1938-01-17 | 2,873 days |
| 10 | VTV | 1926-07-16 | 1 day |
| 11-15 | XLY, XLK, FAS, TECL, XLP | 1926-07-15 | 10,077 days |

The rows are sorted by `Available From` descending, which is most-limiting first, and the report
period begins **2006-02-21**, exactly row 1's date. So `Available From` is each ticker's synthetic
inception and the run starts at the latest of them.

`Extension` is not labelled, but the arithmetic identifies it: **it is the number of trading days the
backtest would gain if that one ticker were removed**, which is the gap to the next row down. At 252
trading days per year, row 1 to row 2 is 47 calendar days and 31 is 32; row 2 to row 3 is 3.472
years and 875 is 875.0; row 7 to row 8 is 0.712 years and 180 is 179.4; row 8 to row 9 is 14
calendar days and 10 is 10; row 9 to row 10 is 11.50 years and 2,873 is 2,898; row 10 to row 11 is
one day and the value is 1. Five of the ten gaps land exactly and the rest within about one percent.

That makes the column a **marginal-cost-of-inclusion readout**: it tells the author precisely which
single ticker is costing how much history, ranked. It is a genuinely good idea and it is cheap,
because it is derived entirely from a list of per-ticker start dates.

Two further things follow from the same table, and both matter more than the mechanic itself.

**Limiters include signal-only tickers, not just held ones.** Holdings Breakdown lists two tickers.
Backtest Limiters lists at least fifteen. The other thirteen appear because the symphony *reads*
them in conditions. A ticker used only in an `if RSI(LABU) > x` gate, never bought, still truncates
the whole backtest. Atlas's own strategy pages already separate signals from holdings, so this
distinction maps onto data the project has.

**One recent ticker can make most of the record synthetic.** All three charts carry a vertical
divider labelled `Synthetic | Real Data`, and it sits near 2022, not at any per-ticker inception.
Of the tickers listed, KMLM is the newest in reality (launched late 2020), which is consistent with
the divider marking the point where the *last* input stops being modelled. If that reading is right,
adding a single 2020-vintage ETF to a symphony converts roughly fifteen years of its backtest into
modelled data, and nothing in the metric block distinguishes the two halves.

#### How far the extension actually reaches

Set the synthetic inceptions against the real ones. Real launch dates below are **from memory and
must be verified before being relied on**, but the order of magnitude is not in doubt:

| Ticker | Synthetic from | Real launch (approx) | Modelled years |
|--------|----------------|----------------------|----------------|
| TQQQ | 1938-10-18 | 2010-02 | ~71 |
| PSQ | 1938-01-31 | 2006-06 | ~68 |
| QQQ | 1938-01-17 | 1999-03 | ~61 |
| VTV | 1926-07-16 | 2004-01 | ~77 |
| FAS / TECL | 1926-07-15 | 2008-11 / 2008-12 | ~82 |
| XLK / XLY / XLP | 1926-07-15 | 1998-12 | ~72 |
| IEF | 1962-01-16 | 2002-07 | ~40 |
| KMLM | 1988-01-15 | 2020-12 | ~33 |
| SOXL | 2002-07-17 | 2010-03 | ~8 |
| LABU | 2006-02-21 | 2015-05 | ~9 |

**Inference about the underlying data, clearly marked as inference.** The 1926-07-15 floor shared by
five sector and style funds is the start of the Ken French data library, and 1962 is the
conventional start of the CRSP daily files. That combination suggests sector and style ETFs are
being proxied by Fama-French industry and value portfolios, and bond funds by a separate series
beginning in 1962. The 1938 cluster for the Nasdaq-family tickers does not correspond to either and
is unexplained. **None of this is confirmed**, and if this idea is ever pursued the first task is to
establish what the source actually is, because the answer decides whether the approach is
redistributable at all.

#### The finding that matters most

**In the captured report, every severe drawdown falls in the synthetic era.** Worst Drawdowns
(Strategy) reads -38.01% (2007-07-18 to 2008-10-21, 318 days), -34.88% (2011-07-06 to 2013-02-19,
406 days), -25.08% (2008-10), -25.07% (2015-02 to 2016-05, 311 days), then -18.52%, -17.19%,
-16.7%. The top four are all pre-2016. The real-data era after the 2022 divider contributes nothing
comparable.

So the headline `Max Drawdown -38.01%`, the `Longest DD Days 406`, the Calmar of 1.12, and the
`Worst Year -20.5%` are all **properties of modelled history, not observed history**. The risk half
of the report is almost entirely synthetic while the return half (best year 350.2% in 2020, +152.29%
in 2022 against QQQ's -33.67%) straddles both. A synthetic backtester does not just extend a
backtest; it manufactures most of the evidence a user will use to judge risk, and it presents that
evidence in the same table, same font, same confidence as the measured part.

This is not a reason to reject the idea. It is the requirement the idea has to meet: **anything Atlas
builds here must mark synthetic-derived figures at the point of display, not only on a chart
divider.** A max drawdown computed mostly from proxy data is a different kind of number from one
computed from trades that happened, and the site's existing posture (Section 20, "it cannot claim
the north star") says to admit that rather than paper over it.

#### What Atlas could plausibly do, and what it cannot

**The tractable part is leveraged and inverse ETFs, and only those.** A 2x or 3x daily-reset fund is
reconstructible from its unleveraged parent by well-established arithmetic: multiply the parent's
daily return by the factor, subtract the expense ratio pro rata, and subtract financing on the
borrowed portion at a short rate plus a spread. That needs the parent series and one interest-rate
series, both of which are obtainable, and it covers a large share of what Composer symphonies
actually hold. `UPRO` alone is held by 2,271 symphonies in `database.json`, and the leveraged family
(`TQQQ`, `UPRO`, `SPXL`, `SOXL`, `TECL`, `FAS`, `TNA`, `TMF`, and their inverses) dominates the
library's ticker distribution. The reference app's `Borrow Rate %` input is exactly this financing
assumption made visible, and its default of 10% is high enough that it clearly matters to the
result.

**The intractable part is everything else.** Proxying `XLK` back to 1926 requires licensed academic
data, a mapping from each ETF to a proxy portfolio, and a defence of that mapping. Proxying an
arbitrary single stock is not possible at all. Atlas holds **3,680 distinct tickers**; no proxy
scheme covers that tail.

**The architectural blockers are the V4.0 blockers, unchanged.** Atlas is static and browser-only
with zero server infrastructure ([Tenet 4](#4-zero-cost-to-operate)). `data/prices.json` holds 72
tickers over 4,184 daily closes from 2010 and is already 2.6 MB, and `database.json` at 18.7 MB is a
standing page-weight risk. Daily closes for a few hundred tickers back to 1926 is far outside what a
static site can ship to a browser. Client-side backtesting itself is not the obstacle, Signal Miner
already does it; the obstacle is the data volume the synthetic idea exists to create.

**The realistic shape, if it is ever pursued**, is therefore narrower than the reference app by a
wide margin: a bounded universe of the most-held tickers, synthetic reconstruction limited to
leveraged and inverse funds derived from parents the project already carries, an explicit and
adjustable financing rate, a hard visual and textual separation of modelled from measured, and a
per-ticker limiter readout copied more or less directly from the table above, since that part costs
almost nothing and is the most honest thing in the whole report.

#### Dependencies and open questions

- **Blocked on the same schema gap as V4.0.** Producing any of these charts needs a daily
  equity-curve or returns series per strategy, which `database.json` does not store. That is V1.20
  item 16, and it gates this, `quantstats-js`, and `local-maestro` alike. Solve it once.
- **Blocked on price coverage.** See the HF Data Library entry below. Even 1,391 tickers does not
  reach 3,680, and none of the candidate sources supplies synthetic pre-inception history; that
  would have to be constructed here.
- **Overlaps V2.4 Overfit Check in both directions.** Extending history backwards is an
  out-of-sample test, which is what V2.4 is built on. But synthetic history is *modelled* out of
  sample, so passing it is weaker evidence than surviving a real forward year, and V2.4's
  measurements are built on real forward years. If both are built, V2.4's verdict must not be
  computed from synthetic data, and this needs stating in whichever ships second.
- **Version pinning is separately useful.** The reference app tracks a symphony version hash. Atlas
  currently infers `oos_date` as the last logic edit. If Composer exposes a version identifier,
  edits could be detected exactly rather than inferred, which would sharpen every out-of-sample
  measurement the project makes. That is worth investigating **independently of this item** and is
  much cheaper than it.
- **Benchmark comparison is also separately useful.** The reference app benchmarks everything
  against a settable ticker. Atlas strategy pages show no benchmark at all. Also cheaper than this
  item, and not dependent on it.
- **Redistribution is unresolved.** Publishing derived figures computed from licensed academic or
  vendor price data may not be permitted. This must be answered before any data is ingested, not
  after.
- **Attribution and prior art.** Crescendo Suite is a third party's work. Nothing in it should be
  copied; it is documented here as a description of a problem space and a set of good ideas, in the
  same spirit as the five candidate forks in V4.0.

#### If revisited, in rough order

- [ ] Confirm whether the divider reading is right, that a single recent ticker makes the whole prior
      record synthetic. It is the finding with the largest consequence and it rests on one inference.
- [ ] Measure the library's ticker distribution against the leveraged and inverse families, to size
      how much of the corpus a parent-derived reconstruction would actually cover
- [ ] Resolve the daily-equity-curve schema gap (V1.20 item 16) first, since three separate roadmap
      items are waiting behind it
- [ ] Decide the redistribution question before ingesting anything
- [x] Build the limiter readout on its own (**done v1.33.0**). It needed no synthetic data and it is
      the most honest part of the reference report. **It did not use `prices.json`**: that file's
      2010-01-04 floor makes 48 of its 72 tickers report the file's own start date as their
      inception. `data/ticker_inception.json` was built instead, and it closed V1.20 item 9 outright
      rather than merely improving its wording
- [ ] Only then evaluate leveraged-ETF reconstruction, as an offline batch artifact, never as
      on-demand server compute

### V4.2: Feature Triage Against Comparable Tools

**Status:** triage complete, nothing built. Owner request, 2026-08-30: "add all of these apps to the
roadmap, be sure to name them something different, but they are all features I would eventually like
to see on the site (unless they involve breaking our site's rules such as requiring api key or user
data)."

Two third-party products were supplied as screenshots: **Crescendo Suite** (the desktop application
already described in V4.1, whose tool launcher lists 16 tools across five groups) and **ICDB**, a web
product with a free tier, a free-sign-in tier, and a paid "ICDB Pro" subscription. Everything below
is read off those screenshots. Neither product was run, no code was seen, and nothing here is
verified against either one's documentation.

Every item is renamed. The names below are Atlas's, chosen to describe the thing rather than to echo
a competitor's branding, and none of them are taken from either product.

#### The rules applied

Four project rules decided most of the verdicts, and they are not negotiable by a feature request:

1. **No user accounts, ever, and no collecting, storing, or processing of user data** (Section 4
   Non-Goals, Tenet 7, and the Icebox entry that removed accounts permanently rather than deferring
   them).
2. **Zero server infrastructure** ([Tenet 4](#4-zero-cost-to-operate)). The site is static and
   browser-only. Anything needing per-request compute, a secret, or a live third-party call at query
   time is out unless it can be precomputed offline into a committed artifact.
3. **No monetisation beyond Buy Me a Coffee.** Nothing here becomes a paid tier.
4. **Saved state, where it is wanted at all, is client-side only.** The Icebox is explicit: saved
   strategies "should be solved with client-side-only storage or not at all." `localStorage` with a
   `try`/`catch` and a graceful default already has precedent in Signal Miner's family selection.

#### Triage

Verdicts: **Ship** means it fits the rules and is genuinely new. **Have** means Atlas already does
it. **Trim** means the idea survives only with a part removed. **Reject** means it cannot exist here.

| Their name | Atlas name | Verdict | Effort | Note |
|---|---|---|---|---|
| Custom Themes | **Light Mode** | Ship | half day | `css/main.css` has zero `prefers-color-scheme` and zero `data-theme`: the site is dark-only today. Pure CSS custom properties plus a toggle, no data, no server |
| Symphony Diff / Symphony Diff Checker | **Version Compare** | Ship | 1-2 days | Appears independently in **both** products, which is the strongest single signal in either screenshot. Two pasted symphonies, or two versions of one, rendered side by side. Needs no stored data at all: `converter.html` already parses a symphony into a logic tree, so this is that renderer run twice with a diff between the trees |
| Ticker Returns | **Ticker History** | Ship | 1-2 days | Per-ticker returns over selectable windows. `data/prices.json` already holds 4,184 daily closes; bounded to its 72 tickers, which must be said on the page rather than implied |
| Data (price cache inspector) | **Data Provenance** | Ship | half day | A page stating what each data file covers, when it was refreshed, and what it cannot answer. Atlas surfaces `refreshed_at` in two places today and nowhere explains the 72-ticker or 2010 boundaries. The live-intraday half of their version is rejected: new dependency, no static form |
| AI-Powered Search | **Plain-English Search** | Trim | 2-3 days | The live-LLM form is rejected outright: a query-time model call means a server, a secret, and a per-query cost, breaking rules 1, 2 and 3 at once. **The precomputed form survives and is most of the value**: strategy descriptions and tags are already generated offline (`add_ai_summary.py`), so the same offline pass can emit a keyword and synonym index shipped as a static file and searched in the browser |
| Custom Preferences | **Remembered View** | Trim | 1 day | Remembering filters, column choices and sort order is fine in `localStorage`. **"Syncs across all devices" is rejected**: cross-device sync is an account by another name. The page must not imply otherwise |
| Library / Organize with Folders | **Local Shelf** | Trim | 2-3 days | Saving and grouping symphonies is permitted **only** as `localStorage`, per rule 4. **Their "share public folders" is rejected**: sharing requires a server and an identity. A shelf that silently vanishes when someone clears site data has to say so on the page |
| Watchlists | **Indicator Board** | Trim | 2-3 days | `rsi.html` already ships live 10-day RSI for 20 tickers, refreshed 3x daily by workflow. Extending it to more indicators is in scope. A **user-defined** watchlist is `localStorage` only, never stored server-side |
| Monte Carlo | **Path Spread** | Ship | 1 week | Bootstrap-resample a strategy's daily returns to show the realised equity curve as one draw from a distribution rather than a fact. Directly serves the site's stated posture about backtests. **Blocked on daily returns (V1.20 item 16)** |
| Correlation Matrix | **Correlation Grid** | Ship | 1 week | Atlas shows every strategy in isolation and answers nothing about how two of them interact. This is the same gap `local-maestro` fills in V4.0. **Blocked on item 16** |
| Wash Sale Helper | **Substitute Finder** | Ship | 1 week | Genuinely accountless: paste symphonies, exclude tickers held in a window, rank the remainder by correlation. Sits naturally beside the existing K-1 Lookup, which is already tax-adjacent. **Blocked on item 16**, and it needs a plain "not tax advice" line, not a buried one |
| Portfolio Optimizer | **Blend Weights** | Ship | 2 weeks | Optimise weights across several symphonies. Same territory as `local-maestro` in V4.0. **Blocked on item 16.** Weight optimisation is itself an overfitting machine, so it cannot ship without the V2.4 caveat attached to its output |
| Robustness Lab | **Fragility Report** | Ship | 2 weeks | How much of each condition's edge survives moving the number it was fitted on. This is `composer_json_fuzz_tester`, already V4.0's recommended first fork, and its independent appearance here raises confidence in that choice |
| Signal Check | **Threshold Significance** | Ship | 2 weeks | Sweep a threshold and test the result against a benchmark rather than against zero. Overlaps, and should be merged with, **V2.2 item A (parameter plateau scoring)**, which is the same instinct: judge the neighbourhood, not the peak |
| Signal Lab (multi-indicator) | folds into **Signal Miner** | Ship | 2 weeks | Their tool combines multiple indicators. Atlas's `signal-lab.html` is only a redirect stub to Signal Miner. Note the collision: multi-condition combining is **V2.2's "DEFERRED INDEFINITELY: OR combining"** item, deferred by owner decision. This is a reason to revisit that call, not a reason to override it |
| IOTA / OverGuard | already **V2.4 Overfit Check** | Have | shipped as a plan | See the note below; this is the most important finding in the triage |
| Signal Ladders | **Ladder Builder** | Have (partly) | 1 week to extend | Atlas already builds a Calmar-ordered nested de-risking ladder and has a deploy gate protecting its export shape (`check_composer_ladder.py`). Their bulk-sweep and tier-competition layer is the extension |
| Logic Visualizer | **Symphony Converter** | Have | shipped | `converter.html` already renders a symphony as a readable IF/ELSE tree |
| Advanced Filtering | **Filter Panel / Screener** | Have | shipped | V1.11 and V1.12 |
| Comprehensive Database | **Full Database** | Have | shipped | 6,669 rows. One difference worth noting: ICDB also ingests from a Discord community, which Atlas does not and which would be a sourcing decision, not a feature |
| Run Backtest | already **V4.1** | Have | planned | The synthetic backtester |
| Portfolio (live account) | none | **Reject** | n/a | Live account performance, deposit-adjusted returns, transactions and cash flows. Requires a linked brokerage account and stores a named person's financial history. Breaks rule 1 outright |
| Composer API Integration | none | **Reject** | n/a | Asks the visitor to connect their Composer account. That is a credential plus personal financial data. Breaks rule 1 |
| Ticker Preview (account allocations) | none | **Reject** | n/a | Reads the visitor's current account positions. Breaks rule 1. The adjacent accountless question, "what would this symphony hold tomorrow", is a different feature and is not rejected |
| Sync Across Devices | none | **Reject** | n/a | An account with extra steps |
| Search History & Analytics | none | **Reject** | n/a | Local search history is technically permissible and nearly worthless. The actual product is "trending patterns across the community", which requires collecting and aggregating what every visitor searched for. Breaks rule 1 in the most direct way anything here does |
| Settings (API keys, paths) | none | **Reject** | n/a | Atlas holds no visitor secrets and has no paths to configure. The theme half is Light Mode above |

#### The finding that matters most in this triage

**Three independent products have now converged on the same feature, and Atlas has already measured
it.** Crescendo Suite ships "IOTA", an in-sample versus out-of-sample degradation score. ICDB sells
"OverGuard", described as regime consistency, tail risk, drawdown patterns, performance decay, and
out-of-sample versus in-sample. Atlas designed **V2.4 Overfit Check** independently. Three teams
arriving at the same tool is good evidence the problem is real and the market wants it answered.

**Atlas is not behind here. It is ahead, and it has receipts.** V2.4 is not a sketch: it is built on
a measurement over **5,095 symphonies untouched for at least 365 days**, and that measurement already
ruled out one of the factors the competing products advertise.

- Median backtest annualised return **49.4%** against a median actual out-of-sample year of
  **17.6%**. Only **22.2%** delivered at least their backtest, **39.1%** at least half, **77.9%** were
  merely positive, and **77.8%** degraded.
- Scored **within in-sample-return deciles**, to control for regression to the mean, annualised
  turnover is the strongest flag at a mean rank correlation of **-0.316**, consistent across all ten
  deciles. Backtest length (+0.188) and win rate (+0.185) follow at nine of ten.
- **"Tail anomalies" did not survive.** The contribution of the top 5% of days scored **-0.065 and
  was unstable, positive in 4 of 10 deciles.** OverGuard advertises tail-risk profiling as one of its
  five factors. On this corpus, that factor predicts essentially nothing once in-sample return is
  controlled for, and the whole reason Atlas knows that is that it ran the controlled test rather
  than assuming the intuitive factor works.

So the competitive read is not "build what they built." It is that Atlas should ship V2.4 **with its
measurements published**, because the differentiator is not the feature, it is being able to show
which factors were tested, which failed, and on how large a sample.

#### Two structural observations

**Four of the highest-value ideas here sit behind a paywall, and one behind a login.** ICDB puts
Search History, Folders, OverGuard and Wash Sale Helper in a paid tier, and Preferences, Themes,
Sync and API Integration behind a free sign-in. Of those eight, this triage rejects five on the
account rule and adopts three in trimmed, accountless, free form. That is the rule working as
designed rather than a limitation to route around: **Atlas's answer to "sign in to unlock" is that
there is nothing to unlock**, and any of these that ship here ship free (rule 3).

**Item 16 is now blocking eight separate roadmap entries.** Path Spread, Correlation Grid, Substitute
Finder and Blend Weights all need a daily returns series, joining `quantstats-js` and `local-maestro`
in V4.0, the synthetic backtester in V4.1, and the performance chart in V2.2. It has gone from a
schema nicety to the single highest-leverage item on the roadmap, and it is the one thing here that
is neither hard nor speculative: the refresh pipeline already receives the data.

### External Data and Library Resources

**Status:** reference only. Neither item below is adopted, neither is a roadmap item, and neither
should be integrated without its own proposal. Recorded (v1.30.7) so the options are not lost.

**HF Data Library** (`https://hfdatalibrary.com/pages/ai-prompts`, part of the ElkassabgiData
ecosystem). A hosted historical price dataset, offered as a candidate future source for
`data/prices.json`. What the site states, recorded verbatim so a later reader can tell what was
promised from what was verified:

- **1-minute OHLCV data, 2002 to present**, described as the "entire historical record (~24 years)"
- A **1,391-ticker universe** (examples given: AAPL, NVDA, MSFT, SPY), with prepared bundles
  including "Magnificent 7" and S&P 500
- Columns: `datetime` (Eastern Time, tz-naive), `open`, `high`, `low`, `close`, `volume`, `source`
- Derived timeframes offered: 5-minute, 15-minute, 30-minute, hourly, daily, weekly, monthly
- Formats: Parquet and CSV
- Access: a REST API over curl, plus an MCP server with native Claude, Cursor, ChatGPT and
  Antigravity CLI integration. Non-1-minute timeframes come back through a signed-URL flow
- Free tier: API key described as "Free, instant, 100 downloads/minute". No paid pricing is stated
- Sizes: a single ticker is "roughly 30-80 MB" as compressed parquet, the Mag-7 bundle "~400 MB",
  the full universe "~13 GB"

The linked page is itself a set of ready-made prompts for driving those download workflows, not the
dataset documentation; the figures above come off that page.

**Why this is worth keeping on file.** `data/prices.json` covers **72 tickers** over 4,184 daily
closes from 2010-01-04, while `data/database.json` holds **3,680 distinct tickers** across the
library. That 72-ticker ceiling is already documented as a hard blocker in two places: **V2.4
Overfit Check Tier 3**, where only 1,112 symphonies (16.7%) hold exclusively covered tickers, and
**V1.20 item 9**, which as originally specified had to say "at least" precisely because
`prices.json` cannot see far enough back to assert a date. **That constraint is gone as of v1.33.0**:
`data/ticker_inception.json` holds exact first-trade dates for all 105 featured tickers in 2 KB, so
the readout asserts real dates. The Tier 3 coverage problem below is untouched by it, because
inception dates are not price history. A 1,391-ticker source reaching to 2002
would move both of those, and 2002 predates the whole leveraged-ETF era that the 2010 start was
chosen to cover (see the v1.20.1 note on `START_DATE`).

**Counterweights, recorded honestly so this is not revisited as a solved problem:**

- **1,391 is not 3,680.** It is a large improvement on 72 but it does not close Tier 3; it moves the
  coverage number without removing the coverage caveat. The first thing to measure, before any other
  work, is the intersection of that 1,391-ticker list against the actual held-ticker distribution in
  `database.json`, weighted by how many symphonies hold each one. UPRO alone is held by 2,271
  symphonies, so the answer is decided by a short head of tickers, not by the size of the universe.
- **Granularity is wrong by three orders of magnitude.** Every downstream use in this project is
  daily adjusted closes. 1-minute bars would be downsampled on ingest and the rest discarded.
- **~13 GB has no home here.** The site is static with no server and no build step; `database.json`
  is already 18.7 MB and flagged as a page-weight risk. Any use of this source is strictly offline,
  inside `scripts/refresh_prices.py`, producing the same small committed artifact. Nothing about it
  changes what ships to a browser.
- **It introduces an API-key dependency that price data does not currently have.** `refresh_prices.py`
  runs unauthenticated against Yahoo Finance today. A key means a secret in the weekly Action, a
  new upstream that can revoke access, and a free tier with no stated paid pricing behind it.
- **Adjusted closes are not listed.** The stated columns are raw OHLCV. `prices.json` is built on
  adjusted closes, so splits and distributions would have to be handled somewhere, which is exactly
  the work Yahoo currently does for free.
- **Redistribution terms are unread.** This site publishes derived figures computed from price data.
  Whether that is permitted has not been checked and must be, before any adoption.

**`ranaroussi/quantstats`** (`https://github.com/ranaroussi/quantstats`). The original Python
library that candidate fork 4 above, `quantstats-js`, is a port of. Same metric surface (Sharpe,
Sortino, Calmar, CAGR, VaR/CVaR, Kelly, Ulcer Index, drawdown-period detail) and the same tearsheet
concept, in pandas/numpy/matplotlib rather than zero-dependency JavaScript.

For this project the upstream is the **reference implementation, not the candidate**. The JS port is
the one that could in principle run in the browser and fit the no-build-step architecture; the
Python original could only run offline in a batch job. Its value here is as the authority to check
formulas against, since the port's own claim to correctness is that it validates against this
library.

It shares the port's blocking gap exactly: it needs a **daily equity-curve or returns series** as
input, and `database.json` stores pre-computed summary metrics per strategy, not daily series. That
gap is tracked as **V1.20 item 16** and is the real prerequisite for either one. Until it is closed,
neither library can be fed real data, and which language the library is written in does not matter.

### Icebox

- ~~User accounts / saved strategies~~, **removed permanently 2026-08-15, not iceboxed.** User accounts will never be built. Composer Atlas will not let visitors create accounts and will not collect, store, or process any user data, ever. This is a deliberate, permanent design choice (see Section 4 Non-Goals and Tenet 7), not a scoping decision to revisit when the site is bigger. Any future feature that would require an account, a login, a saved per-user state, or any personal data is out of scope by definition, and "saved strategies" specifically should be solved with client-side-only storage or not at all.
- Portfolio simulator
- Community forum
- Mobile app

---

## 15. Security

Composer Atlas is a fully static, browser-only website with no server infrastructure, no user accounts, no authentication, and no database service. This architecture significantly limits the attack surface.

### Architecture Security Posture

| Concern | Status | Notes |
|---|---|---|
| Server-side vulnerabilities | N/A | No server exists |
| SQL injection | N/A | No database service |
| Authentication bypass | N/A | No auth layer |
| Secret/key exposure | Low risk | No API keys in client code |
| XSS (Cross-Site Scripting) | Managed | See below |
| Supply chain attacks | Low risk | Zero npm dependencies |
| Data exfiltration | N/A | No user data collected |
| HTTPS | Required | Both hosts enforce HTTPS: Cloudflare Pages on the canonical domain, GitHub Pages on the mirror. Originally written when GitHub Pages was the only host |

### Key Security Practices

**No secrets in client code.** No API keys, tokens, or credentials are stored in the repository or rendered in client-side JavaScript. The Composer API endpoints used for data refresh require no authentication. The `symphony_url` values are public by nature.

**JSON data integrity.** `data/strategies.json` is the only data source and is committed to the
public repo.

> **Discrepancy (found 2026-08-24).** True when written, at MVP. There are now nine committed data
> sources under `data/`: `strategies`, `glossary`, `database`, `database_summary`, `prices`, `rsi`
> (each as a `.json` plus a `.js` twin), `symphony_scores.json`, `storage.csv`, `AddSymphony.csv`
> and `Full Database.xlsx`. Everything the sentence goes on to say still holds for all of them:
> committed to a public repo, every change in git history, no PII in any of them. All changes go through GitHub's commit history, a full audit trail. No PII in strategy entries.

**XSS prevention.** All dynamic content rendered from JSON must be escaped before DOM insertion. Do not use `innerHTML` with unsanitized JSON values. Strategy descriptions and names in JSON must not contain HTML tags. The `app.js` render functions use template literals with escaped data.

**Dependency management.** Composer Atlas has zero npm/Node.js dependencies. External resources are limited to Google Fonts CDN (fonts only; no JS). If a CDN dependency is ever added, it must be from an official source with SRI (Subresource Integrity) hash verification.

**External links.** All links to external sites must use `target="_blank"` with `rel="noopener noreferrer"` to prevent tab-napping.

**GitHub repository.** Repository is public, treat all committed content as fully public. Never commit `.env` files, credentials, or PII. Branch protection on `main` is recommended: require PR review before merge.

### Google AdSense (Post-MVP): retired, never implemented

> **Discrepancy (found 2026-08-24), resolved in favour of the newer decision.** This subsection used
> to give guidance for integrating Google AdSense. It contradicted three other places in this
> document: Tenet 7 ("The site is free and unmonetized"), Non-Goals ("No monetization beyond
> voluntary donations", decided 2026-08-15), and Section 14's V3.0 entry, which removed the
> Monetization Expansion plan "entirely, not deferred". The v1.1 roadmap line also marks AdSense as
> dropped. Four statements to one, and the one was the oldest, so it loses.
>
> **AdSense was never integrated and will not be.** No ad script has ever been on the site. The
> original guidance is preserved in the git history of this file and needs no live home. The site's
> only funding channel is voluntary Buy Me a Coffee donations.

### Responsible Disclosure

If you discover a security issue (e.g., malicious content injection via JSON, broken external link pointing to a compromised domain), report it by opening a GitHub Issue tagged `security` or contacting the repository owner directly. Reports acknowledged within 72 hours; confirmed issues addressed in the next available release.

### Out of Scope

- Security of Composer.trade (third-party platform)
- Security of the user's Composer.trade account
- Investment losses from using featured strategies

---

## 16. Tenets

> **Note on the count (2026-08-24).** There are **eight** tenets below. A documentation standard
> applied during the 2026-08-24 audit proposes a maximum of seven, on the reasoning that a list long
> enough to need scanning stops being used in an argument. **The existing eight are kept unchanged.**
> They are load-bearing: several are cited by name elsewhere in this document and in
> `docs/DESIGN.md`, and each has visibly decided a real trade-off in the patch notes. Trimming to
> seven would mean either dropping a live principle or fusing two that are cited separately, both of
> which cost more than the length does. The difference is recorded here rather than silently
> resolved.
>
> If the list is ever trimmed, the two closest to merging are 3 (Simplicity Over Complexity) and 8
> (Open and Maintainable), which argue from different directions toward the same restraint. That is
> an observation, not a recommendation.

These tenets guide every product, design, and technical decision. When trade-offs arise, consult this list. Order matters: higher tenets take precedence over lower ones.

### 1. Transparency Over Hype

Every strategy is presented with its full metrics, including drawdowns and risk figures. We never cherry-pick data to make a strategy look better than it is. Visitors should leave with an accurate picture, not an inflated one.

*If we are tempted to hide a metric because it looks bad, we show it anyway.*

### 2. Education Before Promotion

Composer Atlas exists to teach first. Strategy pages explain the logic, signals, and reasoning behind every symphony. A visitor who understands why a strategy works is more valuable than one who blindly clones it.

*If we cannot explain a strategy in plain English, we do not feature it yet.*

### 3. Simplicity Over Complexity

Every feature should reduce friction, not add it. The site should feel like a well-organized wiki, not a bloated dashboard. When in doubt, remove the element.

*If a feature requires a tutorial to use, reconsider the feature.*

### 4. Zero Cost to Operate

Composer Atlas runs on static hosting (Cloudflare Pages canonically, GitHub Pages as a mirror; it ran on GitHub Pages alone until the Cloudflare move) with no server, no database service, and no paid infrastructure. Every technical decision must be evaluated against this constraint. Complexity that introduces operational cost is rejected at MVP.

*If it requires a server, find a static alternative.*

### 5. Data Is the Product

The strategy database is the most valuable asset of Composer Atlas. Metrics must be accurate, schema must be consistent, and updates must be logged. A strategy with stale or incorrect data should be flagged or removed.

*If the data is wrong, the site is wrong.*

### 6. Design With Intention

Every visual decision should serve the user's ability to understand information. Color is used semantically (green = positive, pink = negative). Typography is used for hierarchy. White space is not wasted. We do not decorate for the sake of decoration.

*If an element does not aid comprehension, remove it.*

### 7. Independence and Integrity

Composer Atlas is not affiliated with Composer.trade. We do not receive compensation for featuring any strategy. Our editorial choices are not for sale. If we ever establish a formal partnership or receive compensation, it will be disclosed prominently.

The site is **free and unmonetized**. Its only funding channel is voluntary reader donations via Buy Me a Coffee, linked as Support in the nav and footer. No ads, no premium tier, no paywalled content, no sponsored placement, and no user data collected or sold (decided 2026-08-15; see Section 4). This is a deliberate stance, not a launch-stage limitation: keeping the site free of commercial pressure is what lets the editorial and data decisions above stay honest.

*If it creates a conflict of interest, disclose it or avoid it.*

### 8. Open and Maintainable

The codebase is public, readable, and maintainable by a single developer. We do not introduce dependencies or patterns that create lock-in or require specialist knowledge to maintain.

*If the next developer cannot understand it in 10 minutes, simplify it.*

---

## 17. FAQ

### User FAQ

**Q: What is Composer Atlas?**
A: A free, independent reference website for people who use Composer.trade. It explains how real
strategies work in plain English, publishes their backtested numbers without cherry-picking, covers
thousands of community symphonies in a searchable database, and provides tools for building
strategies of your own.

**Q: Who is this for?**
A: Self-directed retail investors who use Composer.trade, are considering it, or want to learn about
systematic investing generally. It assumes you are willing to read, not that you have a finance
background. The glossary exists precisely so the strategy pages can use real terms without stranding
anyone.

**Q: Are these strategies financial advice?**
A: No. Everything here is educational and informational. Past backtest performance does not
guarantee future results, and many of the featured strategies use leveraged funds that can lose
value very quickly.

**Q: Can I clone these strategies on Composer.trade?**
A: Yes. Every strategy page links directly to the symphony on Composer.trade.

**Q: Is Composer Atlas free?**
A: Yes, entirely. There is no paid tier, no account, and no ads. If you find it valuable there is a
voluntary donation link at https://azqato.com/support.html.

**Q: Do I need an account?**
A: No, and you never will. Composer Atlas has no accounts and collects no user data. This is a
permanent design decision, not a launch simplification.

**Q: Do you track me?**
A: Not personally. The site itself sets no cookies, stores nothing about you, and has no login. The
host adds a cookieless analytics beacon that reports aggregate page counts and web-vitals timings
and does not identify anyone. Nothing you type into any tool leaves your browser.

**Q: Who curates the strategies?**
A: The site owner selects and maintains the curated library. Every featured strategy is presented
with its full logic and its full metrics, including the bad ones.

**Q: What is the difference between the curated Strategies page and the Database?**
A: The curated library is a small, hand-explained set: each has a written breakdown of its logic, an
AI-authored analysis, tags and a full metrics table. The Database is thousands of community
symphonies gathered from many sources, with metrics and a ranking but no hand-written explanation.
The library is for understanding; the database is for finding.

**Q: How often are metrics updated?**
A: The community database refreshes on an automated weekly schedule, the RSI page several times each
weekday, and the Signal Miner's price history weekly. Curated strategy metrics are refreshed on
demand. Every page that shows data shows when that data was last refreshed.

**Q: How is the Leaderboard score calculated?**
A: Twenty metrics, weighted to a 1,000-point total, scored by percentile rank against every eligible
symphony rather than against a fixed threshold. The full methodology is on the page behind the
Methodology button, and any individual score breaks down metric by metric on click. It is designed
to be argued with.

**Q: Why does a strategy with an enormous return rank below one with a smaller return?**
A: Because return is one of twenty inputs. Drawdown, backtest length, risk-adjusted ratios and how
concentrated the returns are all count. A spectacular two-year record scores worse on longevity than
a good fifteen-year one, which is deliberate.

**Q: Why do some database entries have no metrics?**
A: Because Composer's API could not backtest them. A symphony can be deleted, made private, or built
in a way that cannot be backtested at all. Those rows are flagged and hidden from the default views.

**Q: What does the Signal Miner actually do?**
A: It takes the tickers you pick and brute-forces millions of "if this condition, then hold that"
rules against sixteen years of daily price history, then shows you which ones performed best and
hands them back as pasteable Composer JSON. It runs entirely in your browser, which is why it can
take minutes and warms your machine up.

**Q: Should I trust the Signal Miner's top result?**
A: Treat it as an upper bound, not an expectation. The tool tests millions of candidates and reports
the best number it found, and the best of a very large sample is biased upward by construction.
A rule that only works at exactly one threshold is fitting noise. Robustness testing that would flag
this is designed and not yet built; until it ships, prefer results that still look reasonable when
you nudge the parameters yourself.

**Q: Why does the Signal Miner heat my laptop up?**
A: Because it is doing real work on your CPU, single-threaded, for as long as the run takes. The CPU
load control throttles it, and the levels are deliberately capped below 100% for exactly this
reason. Lower it if the machine gets uncomfortable.

**Q: Why can I only see 100 results?**
A: The table shows the top 100 by the current ranking metric. A large run produces millions of rows,
and ordering all of them would freeze the tab. Change the sort or the filters to look at a different
100.

**Q: Are my Signal Miner settings saved?**
A: Yes, locally in your browser: your ticker selection, your signal families, the section-3 settings
and your last run's top rows. None of it is transmitted anywhere. The Default button resets
everything.

**Q: Is Composer Atlas affiliated with Composer.trade?**
A: No. It is an independent, community-built resource. Composer.trade is a separate company. No
compensation is received for featuring any strategy.

**Q: Can I submit a strategy?**
A: A submission route is planned via an external form. In the meantime the community database is
refreshed from a URL list that grows continuously.

**Q: Something is wrong on the site. How do I report it?**
A: Open an issue on the GitHub repository. That includes broken external links, incorrect strategy
logic, and stale or wrong metrics.

**Q: Is the site open source?**
A: The repository is public and every change is in its commit history. See Section 25 on the
licensing question, which is currently unresolved.

### Internal / Stakeholder FAQ

For the maintainer, and for anyone (human or AI) picking the repository up.

**Q: Why build this as a static site with no framework and no build step?**
A: Zero operating cost, zero maintenance overhead, and nothing that can rot. The project started on
Astro, Tailwind and TypeScript and abandoned all three before launch (v1.0.2) because they required
a Node installation for what is fundamentally a set of documents. Tenets 4 and 8.

**Q: Why JSON files instead of a database?**
A: At this scale a flat file is faster than a query, costs nothing, and is diffable in git. The
community database is 6,669 entries and the site loads a columnar summary of it in about 2.3MB.
A database service would add cost, an availability dependency and an operational surface, in
exchange for nothing the site needs.

**Q: Why does every JSON file have a `.js` twin?**
A: So the site works when opened by double-clicking a file. Browsers block `fetch()` over `file://`.
The twin assigns the same data to a `window.*_DATA` global. Writing one without the other splits the
HTTP site from the local site with no error anywhere, which is why it is in Section 23's never-do
table.

**Q: Why two hosts?**
A: Cloudflare Pages is canonical (`composeratlas.com`); GitHub Pages
(`azqato.github.io/composer/`) predates it and still runs. They do not behave identically: Cloudflare
honours `.assetsignore` and GitHub Pages currently serves the whole repository regardless of the
workflow's exclusion list. See Section 25 risk 1, including the open question of whether the mirror
still earns its keep.

**Q: Why is the Signal Miner one 2,400-line HTML file?**
A: Because there is no build step, so there are no modules to split it into without adding one. The
whole tool is self-contained: markup, styles and logic in one file that can be opened directly. The
cost is that it is a large file to navigate. That trade was made deliberately and holds.

**Q: Why is the leaderboard scoring model in `database.html` rather than in data?**
A: Because the score depends on the pool. Percentile rank is computed across whatever set is
eligible at load time, so it cannot be precomputed and shipped without freezing the pool. It is
recomputed client-side on every load.

**Q: Why does the roadmap have items built out of order?**
A: Because the owner asked for them out of order, repeatedly and deliberately. V1.16 shipped before
V1.11 to V1.15; V2.1 shipped before V1.17. Where it happened, the phase says so. The numbering
describes scope, not sequence.

**Q: Why is so much rejected work written down at length?**
A: Because the reasoning is the expensive part and it does not survive in anyone's head. Several
sections record something that was tried, measured, and found wrong (sqrt-scaling RSI levels, a
uniform two-point level step, the assumption that cross-ticker price comparisons are constant-false).
Without the write-up each of those gets re-proposed as a fresh good idea.

**Q: Why can the north-star metric not be measured?**
A: Because measuring it means following a visitor into their Composer account. See Section 20. The
metric is kept anyway, as a direction for deciding arguments rather than a number on a dashboard.

**Q: What is the biggest unaddressed risk in the product?**
A: The Signal Miner's exposure to overfitting. It searches millions of candidates and reports the
maximum, with no robustness check on the result. Designed, not built. Section 25 risk 6.

**Q: What is the biggest unaddressed risk in the infrastructure?**
A: That GitHub Pages publishes the entire repository while two documents say it does not. Nothing
secret is exposed, but a stated boundary is not being enforced. Section 25 risk 1.

**Q: What should an AI assistant read first?**
A: Section 23 (Working Practice), then Section 25 (Risks and Open Questions), then the part of
Section 14 covering whatever is being changed. Section 23's never-do table exists because most of
its rows describe something that already went wrong once.


### Content Notes

**Strategy building best practice, avoid short lookback periods:**
Do not use RSI or return checks shorter than 10 days (e.g., `1d`). Very short windows make the algorithm extremely twitchy and will not match the backtest in out-of-sample (OOS) performance.

---

## 18. Documentation Process

### The Four-Document Structure

Composer Atlas documentation lives in exactly four files, and has since v1.3.0 (2026-06-14). The
count has not changed. What each file is **for** was revised on 2026-08-24, and the revision is
recorded here in full because it reverses a rule this section previously stated.

| File | Purpose | Audience | Update when |
|---|---|---|---|
| `README.md` (repository root, never inside `/docs`) | The front door. What Composer Atlas is, what it offers, who it is for, where it stands, and where the real documentation lives | **A general reader.** Someone who found the repository or the site and wants to know what this is | The product's shape, offering, or status changes |
| `docs/PRD.md` | The master reference. Everything except design | The maintainer, and any AI assistant working on the repository | Any product, architecture, schema, API, policy, roadmap, metric, convention or process change |
| `docs/DESIGN.md` | The design system: tokens, type, spacing, breakpoints, components, accessibility, motion | Anyone changing how the site looks | Any CSS token, component spec or layout change |
| `docs/PATCHNOTES.md` | The changelog, append-only | Everyone, including future readers reconstructing why something is the way it is | **Every change, without exception, including data-only ones** |

### What Changed About the README, and Why

> **Rule reversal, 2026-08-24, owner instruction.** This section previously described `README.md`
> as a "Developer quick-start: setup, run, deploy, links to /docs", and that is what the README was.
> It carried a tech-stack table, prerequisites, a clone command, two ways to run a local server, an
> environment-variables section, a per-script reference with commands, and build and deploy
> instructions.
>
> **The new rule: the README is written for a general reader and contains no install steps, no
> commands, no ports, no environment variables, no build instructions, no version numbers and no
> dependency lists.** Its required sections are: the project name with a one or two sentence
> description, the live site link, what the site offers, who it is for, current status, and where to
> learn more.
>
> **Why the change is right.** The README is the first thing anyone sees, on GitHub and in any
> listing, and the overwhelming majority of people who see it are not about to clone the repository.
> A quick-start serves the one reader who already knows they want to build, at the cost of the many
> who wanted to know what this is. It also duplicated content that Sections 10 and 11 own, and
> duplicated content drifts: the old README carried both "28 strategies" and "29 strategies" in the
> same file, plus a "Hosting: GitHub Pages" row that stopped being the whole truth when Cloudflare
> became canonical.
>
> **Nothing was lost.** Every operational detail removed from the README already lived in, or was
> merged into, Section 10 (architecture, tech stack, deploy pipeline) and Section 11 (local setup,
> the script reference, the runbook). The README's job is now to point at them.
>
> **The one hard rule: `README.md` is always at the repository root and never inside `/docs`.**

### Where Content Lives

- **New product requirement, feature decision, or policy** goes to `docs/PRD.md` Part A (Sections 1 to 9)
- **Architecture change, new utility, deploy change, hosting change** goes to Section 10
- **New operational workflow or troubleshooting step** goes to Section 11
- **Schema field added or changed** goes to Section 12
- **Composer API observations** go to Section 13
- **Roadmap movement, including deferrals and declines** goes to Section 14
- **Security posture change** goes to Section 15
- **A measurement, target, or reporting change** goes to Section 20
- **A code convention, discovered or decided** goes to Section 21
- **Anything retired, renamed, or given a redirect shim** goes to Section 22
- **A rule about how to work in this repository** goes to Section 23
- **A place where a document and the code disagree** goes to Section 24
- **A known risk or unresolved question** goes to Section 25
- **A colour token or component spec change** goes to `docs/DESIGN.md`
- **Every change** goes to `docs/PATCHNOTES.md`, as a new entry

### What Not to Do

- **Do not create new documentation files.** Four is the whole structure. A fifth file is how the
  twelve-file sprawl that v1.3.0 consolidated got started.
- **Do not let `README.md` drift back into a quick-start.** See the rule reversal above.
- **Do not skip a `docs/PATCHNOTES.md` entry**, even for a data-only update.
- **Do not copy a count forward.** Re-derive every number from the files it describes. Most of the
  drift the 2026-08-24 audit found was a stale count that had been carried through several
  revisions unexamined.
- **Do not resolve a disagreement between a document and the code by deleting the document's text.**
  See the merge rule below.
- **Do not edit `docs/PATCHNOTES.md` history to match later reality.** Append a marked correction.
  See Section 22.

### The Merge Rule

**When code and a document disagree, the document is not simply overwritten.** The original text is
kept, the observed reality is recorded beside it, and the disagreement is marked as a discrepancy
with a stated judgement about which source to trust and why.

**The reason is that code is wrong as often as documentation is.** A document saying `#444444` where
the CSS says `#c0c0c0` might be a stale doc, or might be a change nobody meant to make. Deciding
which requires evidence, and in that specific case the evidence was a patch note recording the
change as a deliberate legibility fix, so the code won. In other cases the code lost: `robots.txt`
advertises a sitemap that does not exist, and the right answer is not "update the docs to say the
sitemap is missing" but to fix one side or the other.

**Where the evidence settles it**, the text is corrected and the correction is stated, so a reader
can see what it used to say and why it changed. **Where it does not**, both readings stay and the
item goes into Section 25 for the owner to resolve. Every such case is registered in Section 24,
including the resolved ones, which are kept rather than deleted so the same question is not
re-litigated in the next audit.

### The Full Documentation Audit

A full documentation audit has now been run three times: v1.1.4 (2026-06-08, twelve files),
v1.5.9 (2026-06-15, a site-wide accuracy pass) and 2026-08-24 (the audit that produced Sections 20
to 26). It is worth running whenever the documents have stopped being trusted, which in practice
means after a long run of releases that each touched only what they needed to.

**The sequence, in order, and the first three steps are strictly read-only:**

1. **Crawl the whole codebase.** Every page, script, workflow, data file and config. Read files
   rather than inferring from their names.
2. **Read every document in `/docs` in full**, one at a time, start to finish. Not a skim, not a
   search. The three self-contradictions the 2026-08-24 audit found were only visible to someone who
   had read the whole file.
3. **Compare each document against the code**, claim by claim. Re-derive every count. Fetch the live
   site and check what it actually serves rather than what the deploy config says it serves; that is
   how the GitHub Pages exposure in Section 25 was found, and it was invisible from inside the
   repository.
4. **Only then write.** Merge rather than overwrite, per the rule above. Mark uncertainty as
   uncertainty rather than resolving it by assertion.
5. **Skip no document.**
6. **Report what changed in each file and why**, including the steps that turned up nothing. An
   audit that reports only its findings is indistinguishable from one that did not look.

**A default is not a rule.** An audit will usually bring an external standard with it. Where this
project already states its own rule, the project's rule wins and the standard is recorded as a
difference rather than applied over the top. The 2026-08-24 audit produced three of these: eight
tenets against a proposed maximum of seven (Section 16), a changelog that uses descriptive headlines
instead of Added/Changed/Fixed/Removed blocks (Section 19 and PATCHNOTES), and a removal policy the
project had already arrived at independently (Section 22). All three kept the existing form.

**The exception is an explicit instruction from the owner**, which outranks both the existing rule
and the default. The README reversal above is exactly that case, and it is documented as a reversal
rather than presented as though the rule had always been this way.

### Going Forward

- Every release updates whichever of the four documents it affects, **in the same commit as the
  code**. A documentation change landing a release later is how drift starts.
- Counts that appear in documentation should be re-derived, not carried forward. See Section 25
  item 20 on whether they should live in exactly one place.
- The discrepancy register in Section 24 is permanent. Resolved rows stay, marked resolved.
- Risks in Section 25 keep their numbers so they can be cited. Closed items stay, marked closed.
- The next audit starts by reading Section 24 and Section 25, then checking whether any of it has
  quietly changed.


### Consolidation History

On 2026-06-14, 12 documentation files were consolidated into the current 4-file structure:

| Old File | Content Moved To |
|---|---|
| `docs/TRD.MD` | `docs/PRD.md` Section 10 |
| `docs/RUNBOOK.MD` | `docs/PRD.md` Section 11 |
| `docs/METRICS.MD` | `docs/PRD.md` Section 12 |
| `docs/GLOSSARY-SCHEMA.MD` | `docs/PRD.md` Section 12 |
| `docs/ComposerAPI.MD` | `docs/PRD.md` Section 13 |
| `docs/ROADMAP.MD` | `docs/PRD.md` Section 14 |
| `docs/SECURITY.MD` | `docs/PRD.md` Section 15 |
| `docs/TENETS.MD` | `docs/PRD.md` Section 16 |
| `docs/PRFAQ.MD` | `docs/PRD.md` Section 17 |
| `docs/PRD.MD` | `docs/PRD.md` Part A |
| `docs/DESIGN.MD` | `docs/DESIGN.md` |
| `docs/PATCHNOTES.MD` | `docs/PATCHNOTES.md` |
| `README.MD` (uppercase) | `README.md` (lowercase) |

---

## 19. Writing Style

### Em-Dash Prohibition

Em-dashes are prohibited in all project files: HTML pages, documentation (.md files), JavaScript, CSS, and JSON data. This applies to both forms:

- **Literal Unicode character** (U+2014): the literal character (cannot be stored in this file)
- **HTML entity**: `: `

A text search for one form will not catch the other. Both must be searched independently when auditing for compliance.

**Why:** Em-dashes read as an AI writing pattern. They are a hallmark of AI-generated prose and undermine the editorial voice of the site.

### Approved Replacements

Choose the replacement that best fits the sentence, in order of preference:

| Replacement | When to use |
|---|---|
| **Comma** | Most natural replacement in most cases; keeps the sentence flowing without drawing attention |
| **Colon** | When introducing a list, explanation, or elaboration after a complete clause |
| **Semicolon** | When connecting two closely related independent clauses that could stand alone as sentences |
| **Parentheses** | For asides or extra information that is supplementary rather than central to the sentence |
| **Period** | Sometimes the cleanest fix is splitting into two sentences; shorter sentences are often clearer |

### Common Patterns and Their Fixes

| Original | Fixed | Rule Used |
|---|---|---|
| `**Label** [em-dash] description` | `**Label**: description` | Colon (label introducing explanation) |
| `` `code` [em-dash] what it does `` | `` `code`: what it does `` | Colon (code label) |
| `### Section [em-dash] Subtitle` | `### Section: Subtitle` | Colon (heading) |
| `Feature [em-dash] works like X` | `Feature, works like X` | Comma (mid-sentence aside) |
| `It loads data [em-dash] no server needed` | `It loads data; no server needed` | Semicolon (two independent clauses) |
| `Signal [em-dash] fires when X` | `Signal: fires when X` | Colon (label introducing condition) |

### Double-Dash Punctuation (`--`)

The `--` character sequence used as a punctuation substitute (e.g., `word--word` or `word -- word`) is also prohibited. Do not confuse this with CSS custom property syntax (`--color-bg`, `--nav-height`), which is valid and must not be changed.

### Audit Process

When auditing for em-dash compliance, run both searches independently:

```bash
# Search for literal em-dash
python -c "
import os
for root, dirs, files in os.walk('.'):
    dirs[:] = [d for d in dirs if d != '.git']
    for f in files:
        if any(f.endswith(e) for e in ['.html','.md','.js','.css','.json']):
            text = open(os.path.join(root,f), encoding='utf-8').read()
            if chr(8212) in text:
                print(f'{f}: {text.count(chr(8212))} em-dashes')
"

# Search for HTML entity (grep)
grep -r ', ' --include='*.html' --include='*.md' .
```

The `scripts/add_ai_summary.py` script contains the canonical AI Summary content. When updating summaries, verify the new text contains no em-dashes before committing.

---

### Audit Result, 2026-08-24

The 2026-08-24 documentation audit swept the whole project for both forms. **304 instances were
found in 13 files**, which is the largest count since the original 696-instance sweep in v1.7.2. The
prohibition had been in force the whole time; what had not been happening was the sweeping.

| File | Literal U+2014 | Entity form | Disposition |
|---|---|---|---|
| `docs/PRD.md` | 167 | 2 | Fixed |
| `docs/PATCHNOTES.md` | 78 | 2 | Fixed |
| `converter.html` | 8 | 0 | 5 fixed, **3 kept**, see below |
| `etf-cloner.html` | 4 | 0 | Fixed |
| `data/strategies.json` | 2 | 0 | Fixed |
| `data/strategies.js` | 2 | 0 | Fixed |
| `signal-miner.html` | 1 | 0 | Fixed |
| `docs/DESIGN.md` | 1 | 0 | Fixed |
| `database.html` | 0 | 1 | Fixed |
| `data/database.json` | 9 | 0 | **Not touched**, see below |
| `data/database.js` | 9 | 0 | **Not touched** |
| `data/database_summary.json` | 9 | 0 | **Not touched** |
| `data/database_summary.js` | 9 | 0 | **Not touched** |

**Replacements followed the approved list above:** a colon after a bold label, an inline-code label, or a
closing parenthesis; a comma for a mid-sentence aside. Two headings took a colon under the heading
rule. Four `U+FFFD` replacement characters in `docs/PRD.md`, mangled em-dashes left by an earlier
sweep, were repaired in the same pass.

**Two categories were deliberately left alone, and both are permanent exceptions.**

**1. Third-party symphony names in the community database (36 instances).** The names in
`data/database.json` and its derivatives were written by thousands of anonymous Composer users. They
are quoted data, not this project's prose. Editing someone's strategy name to satisfy an internal
style rule would misrepresent what they called it, and would break the correspondence between a row
here and the same symphony on Composer.trade. **Never sweep the database files.**

**2. Three em-dashes in `converter.html` used as an empty-value glyph**, at the `field('Name',
sym.name || '<dash>')` calls. These are not punctuation. They are the "no value" placeholder printed
into a table cell where a symphony has no name, no rebalance setting, or no indicators. Replacing a
placeholder glyph with a colon or a comma would produce nonsense on screen. They render, they are
not prose, and they stay.

**Both exceptions mean a raw count will never reach zero.** A future audit should expect **39
surviving instances** across those four data files and that one page, and should investigate any
number other than 39 rather than trying to drive it to nought.


## 20. Metrics

**Read this section together with Tenet 7 and Section 4's Non-Goals before proposing any measurement
change.** Composer Atlas collects no user data, has no accounts, and sets no cookies. That is a
permanent design choice, not a phase. It means most of the metrics a product document normally
specifies **cannot be measured here, and must not be measured by adding the machinery that would
make them measurable.** The honest thing is to say which numbers exist, which are proxies, and which
are simply unavailable, rather than to invent a funnel the site is incapable of observing.

### North Star

**Symphonies a visitor understood well enough to clone.**

Not pageviews and not visits. The whole product thesis in Section 1 is that Composer users clone
strategies they do not understand; the site exists to close that gap. A visitor who reads a strategy
page, follows two glossary links, and then opens the symphony on Composer.trade is the entire
success case in one motion.

**It cannot be measured directly and will not be.** Measuring it end to end would require following
a visitor off-site into their Composer account. That is exactly the tracking this project refuses.
The north star is therefore a **direction, not a dashboard**: it decides arguments, not releases.
When two options are on the table, the one that leaves the visitor better able to explain what a
strategy does wins.

**The closest honest proxy** is outbound clicks on "Open in Composer" links relative to strategy
page views, which Cloudflare Web Analytics can report at the page level without identifying anyone.
It is a proxy, not the thing.

### What Is Actually Measured

| Class | Metric | Source | Cadence |
|---|---|---|---|
| Acquisition | Page views and unique visits per path | Cloudflare Web Analytics | Continuous, reviewed monthly |
| Acquisition | Referrer breakdown (Composer Discord, search, direct) | Cloudflare Web Analytics | Monthly |
| Engagement | Which pages are viewed at all, and their relative share | Cloudflare Web Analytics | Monthly |
| Engagement | Outbound clicks to Composer.trade | Cloudflare Web Analytics | Monthly, the north-star proxy |
| Performance | Core Web Vitals as measured on real visits | Cloudflare Web Analytics | Monthly |
| Performance | Lighthouse Performance, Accessibility, LCP, page weight | Manual run against the live site | Per release that touches page weight |
| Content health | Curated strategy count, glossary concept count, database entry count | Counted from `data/*.json` | Every release that changes them |
| Data health | Share of database entries carrying a `sharpe_ratio` (the "has been refreshed" proxy) | Counted from `data/database.json` | After each weekly refresh |
| Data health | Flag distribution across `null` / `retry` / `caution` / `excluded` / `duplicate` | Counted from `data/database.json` | After each weekly refresh |
| Availability | Every live clean URL returns 200 and matches the committed bytes | `python scripts/check_live.py` | Every deploy |

### What Is Not Measured, and Why

| Normally measured | Status here |
|---|---|
| Retention / returning visitors | **Not measured.** Requires a persistent identifier. Cloudflare Web Analytics deliberately does not set one, and neither will the site |
| Conversion funnel | **Not measured.** There is nothing to convert to. No account, no signup, no purchase |
| Session length, scroll depth, heatmaps | **Not measured.** All require client instrumentation the site refuses to load |
| Individual user journeys | **Not measured, and never will be.** This is the whole point of Tenet 7 |
| Revenue | **Zero, by design.** Buy Me a Coffee donations are the only inflow and are not tracked against site activity |

### Targets

| Metric | Target | Standing |
|---|---|---|
| Lighthouse Performance | 85+ | Set at MVP, Section 10 |
| Lighthouse Accessibility | 90+ | Set at MVP, Section 10 |
| Largest Contentful Paint | Under 2s, desktop | Set at MVP, Section 10 |
| Total page weight, homepage | Under 500KB uncompressed | Set at MVP, Section 10. **Scoped to the homepage only.** V1.16 established this explicitly after the target was mistakenly applied to `database.html`, which loads a multi-megabyte dataset by design |
| Live-URL integrity | 100% of checked URLs pass `check_live.py` | Every deploy. Currently 8 checked, 0 failing |
| Database refresh coverage | Every entry has had at least one real API attempt | Met since V1.15. Maintained by the weekly workflow |

**Deliberately unset.** There is no traffic target, no growth target and no engagement target. Setting
one would create pressure to optimise for it, and the only levers a site like this has for moving a
traffic number are the ones Tenets 1 and 3 exist to prevent. Growth is welcome, not managed.

### Measurement Method

**Cloudflare Web Analytics**, injected by the host at serve time on `composeratlas.com`. It is
cookieless, sets no client-side storage, does not fingerprint, and adds about 359 bytes per page. It
was reviewed against Tenet 7 and **accepted by the owner. That decision is settled and is not to be
re-litigated as a privacy concern in future audits.**

Everything else is counted directly from the repository with Python, or measured by running
Lighthouse by hand against the live site. The data-health numbers in this document should always be
reproducible by someone with a checkout and no credentials, which is the reason they are counted
from files rather than reported by a service.

### Reporting Cadence

| When | What |
|---|---|
| Every deploy | `check_live.py`, plus the five deploy gates (`check_html_js.py`, `check_composer_ladder.py`, `check_database_keys.py`, `check_strategy_extras.py`, `check_asset_sizes.py`) |
| Every release touching counts | Re-count strategies, glossary entries and database rows; update this document and the patch note in the same commit |
| Weekly, after the database refresh | Flag distribution and refresh coverage |
| Monthly | Cloudflare Web Analytics review: paths, referrers, outbound clicks, Core Web Vitals |
| Per audit | A full documentation audit re-derives every count in this document from the files (see Section 18) |

There is no external reporting and no stakeholder deck. The audience for all of this is one
maintainer and whatever AI assistant is working on the repository at the time.

---

## 21. Conventions

**These are derived from the code as it actually stands, not prescribed at it.** Where a form is
dominant it is stated as the convention. Where meaningful deviation exists, the deviants are named,
because an undocumented exception looks like a bug to the next reader and gets "fixed" into an
inconsistency. Counts below were taken on 2026-08-24.

### JavaScript

| Convention | Observed | Deviants |
|---|---|---|
| Declarations | `const` everywhere: **39 of 39** in `js/app.js`. Zero `let`, zero `var` | None. This is the cleanest convention in the codebase |
| Indentation | Two spaces per level | None |
| Quotes | Single quotes dominate (roughly 2:1 over double). Double quotes appear inside HTML attribute strings in template literals, which is correct rather than deviant | None |
| Semicolons | Always terminated | None |
| Function form | Mixed by role: **20 `function` declarations** for top-level named helpers and renderers, **16 arrow functions** for callbacks and short expressions | Not a deviation. The split is consistent: named declarations for anything called by name, arrows for anything passed to something else |
| Strings | Template literals for anything producing HTML; concatenation only inside `u()` path building | None |
| Module system | None. `js/app.js` is a plain script defining globals; the tool pages are single inline `<script>` blocks | Deliberate. See Tenet 8 |
| DOM writes | `innerHTML` with template literals | **Community-sourced text must be escaped first.** `escapeHtml()` exists for exactly this and is mandatory for any value originating in `database.json`, whose `name` field comes from thousands of anonymous authors. Curated content in `strategies.json`/`glossary.json` is author-controlled and is inserted directly. Getting this backwards is an XSS bug; it was one, in v1.9.3 |

### Python

Every script is Python 3, standard library only, no `pip` requirements, and lives in `scripts/`. That
last rule was made explicit in v1.5.5 after two scripts were found loose in the project root.

| Convention | Observed | Deviants |
|---|---|---|
| Shebang `#!/usr/bin/env python3` | 15 of 20 scripts | **Missing on five:** `check_html_js.py`, `check_composer_ladder.py`, `check_live.py`, `measure_throughput.py`, `run_harness.py`. All five are invoked as `python3 script.py`, never executed directly, so nothing is broken. The drift correlated with recency until v1.25.1, when `build_sitemap.py` and `check_database_keys.py` were written back to the majority form deliberately |
| Module docstring stating what the script does and why | Effectively universal, and unusually thorough: several carry multi-paragraph rationale including what was tried and rejected | None |
| `pathlib` for file paths | 14 of 20 | The six without it are the older gate and measurement scripts, which mostly use `os.path`. `build_sitemap.py` and `check_database_keys.py` (v1.25.x) use `pathlib`, following the majority rather than their nearest neighbours |
| Type hints | **0 of 24** (removed v1.32.1) | **The codebase does not use type hints.** This row previously read "4 of 20" and instructed the reader not to restore consistency in either direction, which described the situation accurately and resolved nothing: it made a coin flip into a convention. Resolved by owner ruling 2026-08-30 in favour of removal, matching the 21-script majority and the fact that the project runs no type checker. New scripts should not add them |
| `argparse` | **0 of 20.** Flags are parsed by hand from `sys.argv` | Uniform. Not worth changing for the number of flags in play |
| Data writes | Always write the `.json` and its `.js` twin in the same run | Non-negotiable. See below |

### Data Files

**Every JSON data file has a `.js` twin, and they must be written together.** The twin assigns the
same content to a `window.*_DATA` global so pages work when opened over `file://`, where `fetch()`
is blocked. `strategies` / `glossary` / `database` / `database_summary` / `prices` / `rsi` all follow
this. Any script that writes one and not the other has introduced a silent split-brain: the site
served over HTTP and the site opened by double-click will disagree, and nothing will error.

Generated files carry a banner naming the script that regenerates them, so a maintainer editing one
by hand is told not to. The banner text was corrected across five scripts in v1.24.8 when it began
naming a script that no longer existed.

| Convention | Detail |
|---|---|
| Field order | Stable and meaningful. `database.json` entries end `oos_date`, `refresh_date`, `flag`, `error`, fixed in that order in v1.11.13 |
| Null handling | Every entry always carries every key. Unknown values are explicit `null`, never an omitted key |
| Float precision | `database_summary` rounds to 4 decimal places. These are ratios and percentages; 4 places is already more precision than any UI renders |
| Encoding | UTF-8, no BOM. Working copies are CRLF; `check_live.py` normalises line endings before comparing to what the host serves |

### HTML and CSS

| Convention | Observed |
|---|---|
| Page structure | Flat `.html` files at the repository root. No subdirectories, no router, no build step. A detail view is the same file with `?slug=X` |
| Shared chrome | Nav and footer are rendered by `renderNav()` / `renderFooter()` into `<nav id="nav-root">` and `<footer id="footer-root">`, never hand-written per page |
| Internal links | Always built through `u(path)`. Never hardcode a leading `/`: it breaks on the GitHub Pages project-path mirror and on `file://` |
| External links | Always `target="_blank" rel="noopener noreferrer"` |
| Design tokens | Colours, radii, fonts and layout constants come from the `:root` custom properties in `css/main.css`. Literal hex in a rule is a deviation and needs a stated reason. The one accepted exception is the RSI tier palette in `rsi.html`, documented in DESIGN.md |
| Inline `<style>` | Five tool pages only: `signal-miner.html`, `converter.html`, `etf-cloner.html`, `nodes.html`, `k1.html`. See DESIGN.md Section 8 |

### Naming

- **Files:** lowercase with hyphens (`signal-miner.html`, `etf-cloner.html`). Python uses underscores (`refresh_full_database.py`), matching the language.
- **CSS classes:** page-prefixed for page-local work (`.db-*` for the database page, `.sl-*` for the Signal Miner, `.conv-*`, `.ec-*`), unprefixed for shared components (`.card`, `.tag`, `.badge`).
- **Slugs:** lowercase, hyphen-separated, stable. A slug is a public URL and changing one breaks links, so it is treated as permanent.
- **Storage keys:** namespaced and versioned, `composer-atlas.<tool>.<thing>.v<N>`. Bumping the version is how a stored payload whose shape changed is discarded rather than misread.
- **"zoop" is always lowercase**, including at the start of a sentence and in strategy names. It is a brand name in the style of "iPhone". This holds in prose, in data, and in commit messages.

### Commits and Versioning

Versioning is documented in Section 11 and holds: semantic versioning, and **every change gets a
patch-note entry, including data-only ones**. Commit subjects use a `type: summary (vX.Y.Z)` shape
(`feat:`, `fix:`, `docs:`, `chore:`, `data:`).

**Two files must never be committed:** `strategies.xlsx` and `watched_sanity_check.xlsx`.

---

## 22. Deprecation and Removal

### The Removal Policy

The project already has a rule and has followed it consistently. Stated explicitly for the first
time here, derived from what the code actually does rather than newly invented:

**A public-facing address is never simply deleted. An internal source file is.**

The dividing line is whether the thing has a URL a stranger might hold. If it does, removing it
strands somebody, and a bookmark or a Discord link that 404s is a real cost paid by someone who did
nothing wrong. If it does not, deletion costs nothing and leaving the file costs clarity.

**For a public address, the pattern is a permanent redirect shim.** `signal-lab.html` is the worked
example, from the v1.16.6 rename to Signal Miner. The old file still exists, and it:

- carries `<meta name="robots" content="noindex, nofollow">` so search engines drop it,
- carries a `<meta http-equiv="refresh">` as the no-JavaScript path,
- calls `location.replace()` so the redirect leaves no history entry to trap the back button,
- **preserves the query string**, so a deep link with parameters still lands correctly,
- says in plain text where the page went, for anyone who lands with both mechanisms disabled.

The shim is permanent. There is no scheduled removal date, because the cost of keeping a 1KB HTML
file forever is nil and the cost of breaking a link years later is not.

**For an internal file, deletion is correct**, once it is genuinely finished and nothing references
it. v1.24.8 is the worked example: `import_full_database.py` and `add_original_tag.py` were both
one-shot scripts that had done their one job. Before deleting, three things were checked: that the
work was actually complete and reflected in the committed data, that no other script, workflow or
document referenced them, and that the live site did not depend on them. A generated-file banner
that named one of them was updated in the same commit, because a pointer to a deleted file is worse
than no pointer.

> **Note on the audit default.** The audit specification this section was written under proposes the
> same policy as its default. The project's existing rule and the default agree, so there is nothing
> to reconcile. It is recorded here as the project's own rule, which is what it has been since
> v1.16.6.

### Public Surface, Item by Item

Everything with a URL a stranger could hold. Removing or renaming any of these requires a shim.

| Address | Status | Notes |
|---|---|---|
| `/` (`index.html`) | Stable | Landing page. Redesigned from a strategy grid to a marketing page in v1.14.5; the address never moved |
| `/strategies.html` | Stable | Listing, and detail via `?slug=X` |
| `/strategies.html?slug=<slug>` | Stable | **Every slug is a permanent public address.** Renaming a strategy does not rename its slug |
| `/glossary.html` and `?slug=<slug>` | Stable | Same rule for concept slugs |
| `/database.html` | Stable | Tabs are selected by in-page state, not by URL, so tab links are not deep-linkable and never were |
| `/rsi.html` | Stable | |
| `/rsi-backtest.html` | Stable | |
| `/rsi-backtest-advanced.html` | Stable | |
| `/signal-miner.html` | Stable | |
| `/signal-lab.html` | **Retired, shim kept permanently** | Redirects to `signal-miner.html`, `noindex`, query string preserved |
| `/converter.html` | Stable | Indexable since v1.15.4 |
| `/k1.html` | Stable | New at v1.27.0. The slug is `k1`, not `k-1` or `k1-lookup`: it was specified by the owner, it is what people type, and the one-word form matches the rest of the site |
| `/nodes.html` | Stable | New at v1.26.0. Named `nodes`, not `node-calculator`: the one-word form matches the rest of the site, and nothing is calculated, a tree is counted |
| `/etf-cloner.html` | Stable, **deliberately unlinked from the primary nav** | Reachable from the footer sitemap and the homepage grid. Keeping it out of the nav is an owner decision, not an oversight, and must be preserved |
| `/about.html` | Stable | Out of the primary nav since v1.16.5; still in the footer sitemap |
| `/404.html` | Stable | Served by both hosts for unmatched routes |
| `/robots.txt` | Stable | Allows all crawlers, advertises `/sitemap.xml`. That URL 404'd from the file's creation until v1.25.1 |
| `/sitemap.xml` | Stable, **generated** (v1.25.1), **automated** (v1.26.1) | Written by `scripts/build_sitemap.py`, never hand-edited; re-run by `update-metrics.yml` on every metrics refresh. 42 URLs as of v1.27.0: 11 indexable pages plus 31 curated strategy slugs. See Section 11 |
| `/data/*.json` and `/data/*.js` | Stable, load-bearing | The `.js` twins are fetched by every page. Renaming one is a breaking change; `full_database` to `database` in v1.10.1 is the precedent for doing it properly |

### Compatibility

| Item | Guarantee |
|---|---|
| Strategy and concept slugs | Permanent. Never rename one to fix a typo; the URL is the contract |
| `window.*_DATA` global names | Stable. Renaming one breaks `file://` loading on every page that reads it |
| `localStorage` keys | Versioned, and a bump is the deprecation mechanism. `composer-atlas.signal-miner.lastrun.v3` has been through v1 and v2; each bump silently discarded snapshots whose metric definitions had changed, which is correct, because showing a stale snapshot scored under different arithmetic is worse than showing none |
| Schema fields | Added freely; removed only with a migration that touches every entry, both twins, the summary export and the xlsx exporter. v1.11.9 through v1.11.13 are the worked example |
| Composer API shape | **Not ours, and not guaranteed.** `refresh_full_database.py` captures the API's actual error text on failure rather than assuming a shape, which is what makes an upstream change visible instead of silent |

### Retired Items

| Item | Retired | Disposition |
|---|---|---|
| Signal Lab (the name) | v1.16.6 | Renamed to Signal Miner. Address kept as a permanent shim |
| `scripts/import_full_database.py` | v1.24.8 | Deleted. One-shot xlsx bootstrap, completed at v1.9.0 |
| `scripts/add_original_tag.py` | v1.24.8 | Deleted. One-shot rename and tag pass, completed July 2026 |
| `script_errors` / `data_warnings` fields | v1.11.9 | Consolidated into `flag`, then split into `flag` plus `error` at v1.11.11 |
| `last_updated` / `last_semantic_update_at` fields | v1.11.10 | Renamed to `refresh_date` / `oos_date` across every consumer |
| `data/full_database.json` / `.js` | v1.10.1 | Renamed to `database.json` / `.js`; `window.FULL_DATABASE_DATA` became `window.DATABASE_DATA` |
| Google AdSense integration | Dropped pre-launch; plan removed 2026-08-15 | **Never implemented.** No ad script has ever been on the site |
| V3.0 Monetization Expansion (roadmap) | 2026-08-15 | Removed entirely, not deferred |
| User accounts / saved strategies | 2026-08-15 | **Removed permanently, not iceboxed.** Will never be built |
| Screener's 3-state flag toggle | 2026-07-13 | Removed. Screener is always Working-only |
| Astro / Tailwind / TypeScript stack | v1.0.2 | Abandoned before launch in favour of vanilla HTML/CSS/JS |
| `--color-green-muted` token | v1.1.1 | Removed as unused |
| Curated "zoop's X (2026 Edition)" set | Planned, not applied | 11 replacements and 1 removal are decided and recorded in Section 14 V2.2. Not yet executed |

### Historical Records Are Not Rewritten

`docs/PATCHNOTES.md` is an append-only record of what happened, and entries are **not edited to
match later reality.** A patch note that says "80 tickers" was true when written, and v1.21.2's
entry recording the drop to 72 is the correction. The same applies to superseded roadmap sections:
V1.13's scoring model is left intact above V1.17's, which supersedes it, because the launch record
is worth more than a tidy document.

Two exceptions, both narrow and both used:

1. **A correction may be added inline**, marked as a correction and dated, when a published entry
   was factually wrong rather than merely superseded. v1.24.2 carries a `> **Correction (v1.24.4).**`
   block admitting its throughput figure was wrong by a factor of five. The original text stays.
2. **Mechanical punctuation compliance** may be applied across the whole file, as it was in v1.7.2
   and again in this audit. Replacing an em-dash with a colon changes no fact.

---

## 23. Working Practice

This section is instructions, not description. It is written for whoever picks the repository up
next, including an AI assistant with no memory of the previous session.

### Before You Change Anything

1. **Read the file, do not infer it from its name.** `signal-miner.html` is a single 2,400-line page
   with one inline script; `database.html` is 1,348 lines with the whole leaderboard, screener and
   filter engine inside it. Neither is what its name suggests in size.
2. **Check Section 14 before proposing a feature.** A surprising amount has already been decided,
   built, measured, or explicitly declined with a recorded reason. Re-proposing something the owner
   declined, without acknowledging that they declined it, wastes everyone's time.
3. **Check Section 25 before reporting a problem.** Known open items are listed there with their
   current state.

### Where to Work: Kind of Work to File

| If you are changing... | Open |
|---|---|
| Anything about the Signal Miner: search space, families, throttle, results, export | `signal-miner.html` (one file, one inline script) |
| The leaderboard scoring model, tiers, screener, filter panel, database tables | `database.html`, and `SCORE_METRICS` / `CLAMP_Q` / `TIER_CUTS` inside it |
| Nav, footer, breadcrumbs, tag rendering, shared formatters, `u()` | `js/app.js` |
| Colours, type, spacing, any shared component | `css/main.css` first, then `docs/DESIGN.md` in the same commit |
| A tool page's own look | That page's inline `<style>` block, per DESIGN.md Section 8 |
| Curated strategy content, metrics, tags, AI summaries | `data/strategies.json` **and** `data/strategies.js`, plus `scripts/add_ai_summary.py` if a summary is involved |
| Glossary content | `data/glossary.json` **and** `data/glossary.js` |
| The community database pipeline | `scripts/refresh_full_database.py`, then `scripts/export_summary.py` to regenerate what the site reads, then `scripts/check_database_keys.py` to confirm everything agrees |
| **Adding a symphony to `database.json` by hand** | The row itself, then `scripts/sync_database_to_storage.py` to archive its URL, then `scripts/export_summary.py` so the site can see it, then `scripts/check_database_keys.py`. Skipping either middle step is silent, and both have already happened |
| The Signal Miner's price history or ticker universe | `scripts/refresh_prices.py`, which writes `data/prices.json` and `.js` |
| The RSI page's data | `scripts/refresh_rsi.py` |
| Whether a ticker issues a K-1, or adding tickers to the lookup | `data/k1_seed.txt`, then `scripts/refresh_k1.py`, then commit `data/k1.json` **and** `data/k1.js` together |
| Deploy behaviour or the deploy gates | `.github/workflows/deploy.yml`, `scripts/check_html_js.py`, `scripts/check_composer_ladder.py`, `scripts/check_database_keys.py`, `scripts/check_strategy_extras.py`, `scripts/check_asset_sizes.py` |
| **`data/database.json`, `data/k1.json`, `data/prices.json` (since v1.42.1), or the featured set in `data/strategies.json`** | `scripts/build_strategy_extras.py`, then commit `data/strategy_extras.json` **and** `data/strategy_extras.js`. The strategy pages read that join, not the source files, so a refresh that skips this step leaves the page showing yesterday's numbers with no visible sign. `scripts/check_strategy_extras.py` fails the deploy if it is skipped. **Automated since v1.31.1** for the two workflow-driven inputs (`refresh-full-database.yml` for `database.json`, `update-metrics.yml` for `strategies.json`); the `k1.json` path and manual `database.json` edits are still hand-run |
| Which pages search engines are told about | `scripts/build_sitemap.py`, then re-run it. Never hand-edit `sitemap.xml`. Re-run automatically by `update-metrics.yml` since v1.26.1, so a forgotten run self-corrects within a day |
| What Cloudflare serves publicly | `.assetsignore` (not `deploy.yml`, which governs GitHub Pages only) |
| Product decisions, architecture, schemas, roadmap, policy | `docs/PRD.md`, this file |
| Anything at all | `docs/PATCHNOTES.md`, always, in the same commit |

### How to Verify a Change

**Verification is by running the thing, not by reading the diff.** This project has repeatedly found
that a change which looks obviously correct is not.

**Verify locally, not against the live site.** Owner instruction, 2026-08-27, and it is now the
rule. Run the page from the working copy: `file://` for anything that does not need a real origin,
or `python -m http.server 8731 --bind 127.0.0.1` from the repository root for anything that does.
Once a change is proven locally, it is proven. Do not then sit on `composeratlas.com` waiting for a
deployment to appear, and **do not troubleshoot Cloudflare Pages or GitHub Pages when the local run
is correct**: a page that works locally and is missing from a host is a deployment matter, which is
the owner's to look at, not a defect in the change.

**What still needs a real origin, and why.** `file://` is not an origin, so anything touching
`history.pushState`/`replaceState`, `fetch()` of a local path, `localStorage`, or module scripts
either throws or silently no-ops there. `k1.html`'s URL syncing is the worked example: it is
correct under `file://` precisely because it is wrapped in a `try`/`catch` that swallows the
`SecurityError`, which means `file://` **cannot** prove the feature works, only that its absence
breaks nothing. Serve over `127.0.0.1` for those. `python -m http.server` needs no configuration
because the site has no build step.

**Still test both loading paths for a data-driven page.** `file://` and a local server exercise
different halves of the `.js` twin arrangement described in Section 10: the twin under `file://`,
the `fetch()` fallback over http. A change that breaks one commonly leaves the other working.

| What you changed | How to verify |
|---|---|
| `signal-miner.html` | `python scripts/run_harness.py all`. This runs the four gates: `verify` (spec-count lockstep plus dual-path equality), `live` (an end-to-end run, window and rendering), `settings` (persistence and the Default button), `plateau` (parameter plateau scoring, recomputed independently). All four must pass before pushing. `memory` and `inertness` are measurement tools, not gates |
| Any inline `<script>` on any page | `python scripts/check_html_js.py`. A broken inline script still serves a 200 with its static HTML intact, so a bad publish looks healthy from outside. This is the gate that would have caught v1.22.2 |
| The Composer export shape | `python scripts/check_composer_ladder.py`. Valid JSON in the wrong shape is what shipped in v1.22.0 and was not caught for five releases |
| `k1.html`, or any tool page's behaviour | Run it locally and drive it. `file://` for the `.js` twin path, `python -m http.server 8731 --bind 127.0.0.1` for anything needing a real origin. A headless browser can click the page's own buttons and read back the result, which is how the URL syncing at v1.27.1 was verified across all six of its cases |
| Whether a deploy actually landed | `python scripts/check_live.py`. **Useful, but not a gate and not a blocker.** It reports on the hosts, so a failure here after a correct local run means a deployment did not happen, not that the change is wrong. Report it and move on rather than troubleshooting the host |
| Any JSON data file | `python -c "import json; json.load(open('data/FILE.json', encoding='utf-8'))"`, and confirm the `.js` twin was written in the same run |
| The strategy pages' joined data | `python scripts/check_strategy_extras.py`. Rebuilds the join in memory and demands byte equality with both committed files, so it catches a stale join, a `.json`/`.js` twin that drifted, and a featured strategy with no database row. **The twin check is there because `data/database.js` shipped one entry behind `data/database.json` at v1.27.9 and `check_database_keys.py` passed anyway**, since it checks keys rather than whether the twins match |
| `data/database.json`, by any route | `python scripts/check_database_keys.py`. Asserts `symphony_id` is present and unique, agrees with the URL, that `database_summary.json` holds the same ids in the same order, and that every symphony's URL is archived in `storage.csv`. Every one of those failures is invisible without it, and three of the five have already shipped |
| Anything at all, after deploying | `python scripts/check_live.py`. Fetches each live clean URL, compares byte-for-byte against the committed file, and reports failures. Currently 8 URLs, 0 failing |
| Page appearance or behaviour end to end | Drive it in **headless Edge**. See below |
| Documentation counts | Re-count from the files. Never copy a number forward from a previous revision |

### Browser Testing

**Use Microsoft Edge, never Chrome.** There is no JavaScript runtime on the maintenance machine, so
end-to-end testing is done by driving a headless browser, and Chrome is the owner's day-to-day
browser. Driving it would disturb a live session. Edge runs the same engine and is free to use.

The rig lives in `scripts/harness/`, entered through `scripts/run_harness.py`, and
`scripts/harness/README.md` documents eleven traps that have each cost a debugging session. Read it
before writing a new harness. The most expensive one, Trap 11, is worth repeating here: **a shared
Edge profile directory must not have a fixed name.** A killed or backgrounded harness leaves an
`msedge.exe` holding the directory, the cleanup fails silently, and the next run's Edge exits in a
tenth of a second against a locked profile. That surfaces as "NO HARNESS OUTPUT", which looks
exactly like a broken driver. `run_harness.py` now uses a per-process profile name and says so
explicitly if it cannot clear one.

### What Never to Do, and Why

| Never | Because |
|---|---|
| **Add user accounts, logins, or any user-data collection** | Permanent product decision (Tenet 7, Section 4). Not a phase, not a backlog item, not something to revisit. It was removed from the roadmap permanently on 2026-08-15 |
| **Add ads, a premium tier, affiliate links, or any monetization** | Same decision. Buy Me a Coffee donations only |
| **Raise the Signal Miner's CPU ceilings** (Max ~80%, High ~40%, Medium ~20%, Low ~10%) | They are capped for **heat**, on hardware belonging to whoever opens the page, not because of the memory bug. The memory bug was fixed in v1.22.13 and v1.22.15, which invites the conclusion that the caps can now be lifted. They cannot. Owner decision, reaffirmed 2026-08-20 after the fix |
| **Re-raise the Cloudflare Web Analytics beacon as a privacy concern** | Reviewed and accepted by the owner. It is cookieless, sets no storage, and the decision is settled |
| **Put the ETF Cloner in the primary nav** | Owner decision. It is reachable from the footer sitemap and the homepage grid, and that is where it stays |
| **Build a self-hosted strategy submission form** | Decided 2026-08-15: submissions go through an external Google Form. A self-hosted intake would be an input surface on a site that deliberately has none |
| **Commit `strategies.xlsx` or `watched_sanity_check.xlsx`** | Standing instruction |
| **Write a `.json` without its `.js` twin** | Splits the HTTP site from the `file://` site with no error anywhere |
| **Add a symphony to `database.json` without archiving its URL in `storage.csv`** | `storage.csv` is the long-term record of every symphony ever seen and is meant to never lose one. An approved symphony absent from it cannot even be purged later, since `purge_flagged_entries.py` aborts rather than drop a URL it cannot find. Run `scripts/sync_database_to_storage.py`; check 5 of the gate catches you either way |
| **Deduplicate `database.json` on `symphony_url`** | The URL is not unique per symphony. Composer serves at least `/details` and `/factsheet` for the same one, and keying on the URL is how a duplicate row got in and stayed in. **`symphony_id` is the primary key.** Section 12 |
| **Regenerate `database.json` without regenerating `database_summary.json`** | The site reads the summary. A symphony present in the full file and absent from the summary does not exist as far as any visitor is concerned, and nothing raises an error. This is what hid four symphonies until v1.25.1 |
| **Run `scripts/sync_storage_to_database.py` casually, or to see what it would do** | It has no dry-run mode and writes on every invocation. Worse than the write is what it writes: `storage.csv` deliberately keeps every URL ever seen, including 1,004 symphonies purged as permanently dead in v1.11.14, so a blind run **resurrects dead symphonies into the approved database**. It cannot tell "never processed" from "removed on purpose". This has happened twice, 2026-07-15 and 2026-08-24, both reverted. Promotion is an approval decision, not a sync. Section 12 |
| **Run another script that writes `database.json` while `refresh_full_database.py` is running** | It holds the whole file in memory and overwrites on every checkpoint, so a concurrent writer's changes are silently discarded. This happened once, in v1.11.3, and the rule is in both scripts' docstrings |
| **Insert community-sourced text into `innerHTML` without `escapeHtml()`** | `database.json` names come from thousands of anonymous authors. This was a live XSS hole until v1.9.3 |
| **Use an em-dash, or `--` as punctuation** | Section 19. It reads as machine-written and undermines the site's voice |
| **Capitalise "zoop"** | It is a lowercase brand name, always |
| **Rename a strategy or concept slug** | It is a public URL. See Section 22 |
| **Edit `docs/PATCHNOTES.md` history to match later reality** | Append a correction instead. See Section 22 |
| **Add a build step, an npm dependency, or a server** | Tenets 4 and 8. Every technical decision is evaluated against staying static and dependency-free |
| **Push to `main` without running the gates for what you touched** | The gates exist because each one has already caught a real outage |

### Adding a Release

1. Make the change and verify it by the table above.
2. Update `docs/PRD.md` if any decision, schema, architecture, count or policy moved.
3. Update `docs/DESIGN.md` if any token, component or layout moved.
4. Add a `docs/PATCHNOTES.md` entry: new `## [X.Y.Z] - YYYY-MM-DD` heading at the top, a descriptive
   `###` headline, past-tense prose explaining what changed and why, and a bolded
   **Files changed:** line.
5. Bump the version in the PRD header.
6. Commit with `type: summary (vX.Y.Z)`.
7. Push, wait for the deploy, then run `python scripts/check_live.py`.

---

## 24. Documentation Versus Reality

Every place a document and the code disagreed, found in the full audit of 2026-08-24. **Nothing in
this table was resolved by deleting the original text.** Each entry names which source to trust and
why, and the losing text is either kept in place with a marked discrepancy note beside it, or
corrected with the correction stated.

**The general rule: trust the code, but not automatically.** Code can be wrong as easily as a
document, and three of the rows below are cases where the code was the problem. What decides it is
evidence, usually a patch note recording the change as deliberate.

### Open

| # | Doc said | Reality | Trust | Why |
|---|---|---|---|---|
| 1 | `deploy.yml`'s exclusion list keeps `docs/`, `scripts/`, `README.md` and `symphony_scores.json` off the public web | **All four return HTTP 200 on GitHub Pages**, byte-identical to the working copy. They correctly 404 on Cloudflare | **The docs describe the intent; neither host fully delivers it** | The byte-exact match proves GitHub Pages serves the raw repository rather than the workflow artifact. Leading hypothesis: the repository's Pages source is set to "Deploy from a branch" instead of "GitHub Actions". Unconfirmed, `gh` is not installed. **Owner action required** |
| 2 | `data/symphony_scores.json` is "not served publicly" (README, `update_metrics.py`, Section 10) | **200 on both hosts**, 22.8MB. `.assetsignore` never listed it | **The code**, meaning the file genuinely is public | One-line fix: add it to `.assetsignore`. Also true of `data/database.json` (18.7MB) and `data/Full Database.xlsx` (5.8MB), neither of which any page requests |
| 4 | README stated `## License` / `MIT` | **No `LICENSE` file existed in the repository** | **The code**, meaning the project was unlicensed | **CLOSED 2026-08-28 (v1.30.4), owner decision: all rights reserved, deliberately.** A bare "MIT" line with no licence text was not a grant and was removed at the time. The owner has now confirmed the intent was never MIT, so the default was already correct and an explicit `LICENSE` was added to say so rather than leave it implied |
| 6 | Section 12: "All 8 current tags" | **13 tags in use** across `strategies.json` | **The code** | The 8 were the MVP set. All 13 correctly resolve to a glossary slug, so the rule the section states still holds; only the count went stale. Table kept, framing corrected |
| 7 | Section 6: "6,640 total entries, 6,221 clean, 229 duplicate, 88 excluded, 88 caution, 14 retry" | **6,669 entries; 6,474 unflagged, 69 retry, 94 caution, 32 excluded, 0 duplicate** | **The code** | The v1.11.23 figures were correct on the day. The weekly refresh has been moving them ever since, and moved them again between the audit's measurement and this document being committed. Original kept as the historical record, current figures added beside it, and Section 6 now says plainly that flag counts are readings with dates rather than properties |
| 8 | Section 13: "All 24 Composer Atlas strategies" | The table beneath it has **31 rows**, matching `strategies.json` | **The code, and the table** | Only the heading's count was wrong. Removed rather than re-fixed to a number that will go stale again |
| 9 | Section 15: "`data/strategies.json` is the only data source" | **Nine committed data sources** under `data/` | **The code** | True at MVP. Everything the sentence goes on to assert still holds for all of them |
| 10 | Section 10 directory tree: `glossary.json # 8 glossary concept entries` | **20 entries** | **The code** | Corrected. Section 12's own canonical table already said 20, so the document disagreed with itself |
| 11 | Section 10 directory tree: `prices.json (37 tickers from 2018)` | **72 tickers, from 2010-01-01**, 4,184 trading days | **The code** | Two separate changes landed (v1.18.0 expanded the universe, v1.20.1 extended the history) and this line tracked neither |
| 12 | DESIGN.md: `--color-disabled` is `#444444` | `css/main.css` has **`#c0c0c0`** | **The code** | PATCHNOTES v1.5.4 records the change as a deliberate legibility fix. Doc went stale on 2026-08-15 and stayed that way for two months. Secondary issue flagged: the token's name now reads backwards. **Closed 2026-09-28.** DESIGN.md Section 2 now documents the real value and keeps the misnomer knowingly, with the reason. The deeper cause was that *two* documents held the palette: the `#444444` this row registered was in Section 10 of this file as well, where it survived the v1.82.0 rebuild. That copy is gone; see the currency pass below |
| 26 | `database.html` `<meta name="description">`: "the full 6,500+ symphony database" | **6,816 rows** in `data/database_summary.json` | **The code** | Written once and never revisited. Nothing reads a `<meta>` tag, so no job, gate or test could have caught it; the only reader is a search engine and a link preview. The direct case for Section 27 |
| 27 | `strategies.html` `<meta name="description">`: "Browse **all** Composer.trade strategies" | **24 visible curated strategies.** "All" is `database.html`, which holds thousands | **The code** | Not a stale number but a stale scope: the sentence was true when the curated set was the whole site and became wrong when the Database shipped. Worse than row 26, because a reader who believes it concludes the site has 24 strategies in total |
| 28 | `overfit.html` `<meta name="description">` describes the page as measuring what survives a backtest, with no mention of a score | The page has led with a **0 to 100 Overfit Score** since v1.76.0 | **The code** | The description is not false, it is two versions behind. Shows the second failure mode for hand-written head tags: they go stale on a feature change, not only on a data refresh, and nothing in the deploy path looks at them |
| 13 | DESIGN.md breakpoints list four `min-width` queries | A **`max-width: 640px`** query also exists | **The code** | Added |
| 14 | DESIGN.md documents the shared component set | **Six shared components were undocumented**, plus three tool pages' entire inline stylesheets | **The code** | All six now documented; the three inline sheets are named and scoped in a new DESIGN.md Section 8 |
| 15 | Section 15: HTTPS "GitHub Pages enforces HTTPS", Tenet 4 "runs on GitHub Pages" | Canonical host is **Cloudflare Pages** (`composeratlas.com`); GitHub Pages is a mirror | **The code** | Both statements were written before the Cloudflare move and are still true of the mirror, just no longer the whole picture |

### Resolved in This Audit

Kept, per the practice of not erasing a resolved discrepancy. **Numbers are permanent.** A row that
moves from Open to Resolved keeps the number it was registered under, so anything citing it still
resolves; that is why this table is not in numeric order.

| # | Was | Resolution |
|---|---|---|
| 3 | `robots.txt` advertises `https://composeratlas.com/sitemap.xml`, which 404'd | **Fixed in v1.25.1**, by generating the sitemap rather than dropping the line. `scripts/build_sitemap.py` derives it from the indexable pages plus the curated slugs. The claim that it therefore "does not go stale" was **half true until v1.26.1**: nothing ran the script, so every weekly metrics refresh staledated all 31 strategy entries anyway. Now run by `update-metrics.yml`. See Section 11 |
| 5 | `data/database_summary.json` held 6,665 rows against `database.json`'s 6,669 | **Fixed in v1.25.1.** Export re-run; all 6,669 rows present and in source order, `.js` twin verified identical. `export_summary.py` also hardened against silently dropping a field that only later entries carry |
| 16 | Section 15 carried live Google AdSense integration guidance | Contradicted Tenet 7, Section 4's Non-Goals, and Section 14's V3.0 removal. Four statements against one, and the one was the oldest. Retired with the reason recorded; AdSense was never implemented |
| 17 | Section 17 FAQ: "How does the site make money? A: Google AdSense (post-MVP) and direct user donations" | Same contradiction. Answer rewritten to state the site makes no money |
| 18 | Section 17 FAQ and Section 10: "25 curated strategies" | **31.** Corrected, with the count sourced from the file rather than restated |
| 19 | Section 10: "Analytics: None currently" | Cloudflare Web Analytics has been injected at serve time since the Cloudflare move. Row corrected rather than annotated, because it asserted an absence that is no longer true, and the policy it set (cookieless, no personal data) is satisfied |
| 20 | Section 10 deploy snippet listed `--exclude='strategies.xlsx'` and `--exclude='README.MD'` | Neither matches `deploy.yml`, and no `strategies.xlsx` exists in the repository. Snippet corrected to the real list |
| 21 | Four `U+FFFD` replacement characters in this document | Mangled em-dashes from an earlier sweep, all in the form `(done vX.Y.Z) <FFFD> text`. Repaired to a colon |
| 22 | 304 em-dashes across the project, against Section 19's own prohibition | Swept. See Section 19 for the count and the three deliberate survivors |
| 23 | Section 18 said README's role is "developer quick-start: setup, run, deploy" | Superseded by the owner's 2026-08-24 instruction that the README is a general-reader front door with no install steps, commands, versions or dependency lists. Section 18 rewritten; the removed content was merged into Sections 10 and 11 rather than dropped |
| 24 | PATCHNOTES: `[1.15.5]` and `[1.5.8]` each appear twice; `[1.15.0]` sits above `[1.15.5]` in a newest-first file | Real defects in the changelog. **Annotated in place, not renumbered**, because these version strings appear in commit messages and in cross-references elsewhere. See Section 22 on not rewriting history |
| 25 | Section 12: `symphony_url` is "the true unique key" of `data/database.json` | **Wrong, and it cost data integrity.** Composer serves the same symphony under at least `/details` and `/factsheet`, so a URL is not unique per symphony. `sync_storage_to_database.py` was built on this claim and appended a second row for a symphony it already had. **Owner ruling, v1.25.2: `symphony_id` is the primary key and the file is always deduplicated on it.** Original wording kept in the schema table with the correction beside it, invariant stated in Section 12, gated by `scripts/check_database_keys.py`. This is the third row in this register where the code, not the document, was the problem |

---

### The V2.5 documentation audit, 2026-09-08

**The standard was fetched, not remembered.** `https://azqato.github.io/prompts/#/documentation` is
hash-routed, so a plain fetch returns only the page shell; the readable source is
`prompts/documentation.md` in the `Azqato/prompts` repository. **Recorded because the obvious way to
check this standard silently returns nothing and looks like an empty document rather than a failed
fetch.**

**What the audit found, and what it did about each.**

| Finding | Verified against | Action |
|---|---|---|
| **Licensing had no section of its own.** The posture was real and correct, but a reader had to reconstruct it from a gap table in Section 14 and a closed item in Section 25 | `LICENSE.md`, read in full | **Fixed.** Section 28 now states what the licence grants and refuses, in one place |
| Four documents, `README.md` at root and three in `/docs` | The file system | Conformant, no change |
| `LICENSE.md`, `robots.txt`, `sitemap.xml` all at root | The file system | Conformant. `LICENSE.md` carries all eight required sections, checked individually rather than assumed |
| **Em-dash sweep across the whole project**, which the standard asks for and which had only ever been run over `/docs` | Every `.html`, `.js`, `.py`, `.css`, `.md` outside `data/` | **Three found, all in `converter.html`**, all empty-value placeholders rendered into the UI. Replaced with a single hyphen, which the standard permits. The repository now measures **zero** |
| **Browser Testing and Verification Environment are not top-level sections**, though the standard names them | Sections 23 and 11 | **Not moved.** Both exist as subsections of Working Practice and predate the standard naming them; the standard's own rule is that an existing arrangement beats an imported default. A pointer was added to the table of contents so they can be found |
| All 27 existing sections present by name | The table of contents | Conformant |

**What the audit deliberately did not do.** It did not rewrite sections that were merely long, and it
did not "correct" any document that disagreed with the code without recording both. The standard's
merge rule exists because documentation holds intent that code cannot reconstruct, and the cheapest
way to destroy that is a confident tidy-up.

**The honest limit of this audit.** It was a currency check, not a line-by-line re-derivation of
7,000 lines against the codebase. Sections were checked for existence, for the specific claims the
standard names, and for the discrepancies already tracked in this section. A full re-read of every
section against current code remains undone, and saying so is more useful than implying a
completeness the work did not have.

---

### The currency pass of 2026-09-28 (v1.83.2)

**Prompted by a plain read of the three public documents rather than by an audit.** Four places where
this document described a site that no longer exists, found by reading `README.md`, this file and
`docs/PATCHNOTES.md` end to end and then checking the claims against the file system. All four are
fixed; none required a code change.

| Finding | What was wrong | Fix |
|---|---|---|
| **Section 10 carried a second copy of the design tokens**, and it was the pre-v1.82.0 palette | `--color-bg: #0d0d0d`, `--color-pink: #ff4d8d`, `--color-disabled: #444444`, nineteen days after the palette was rebuilt on a Visual Studio dark base | **Replaced with a pointer to DESIGN.md**, not re-synced. Re-syncing restores the same drift with a later start date. DESIGN.md Sections 2 to 5 already cover every token the block listed |
| **The `deploy.yml` snippet showed two gates**, and the prose beneath it said "Two Python scripts gate the publish" | There are **five**, and have been since v1.43.2. `check_database_keys.py`, `check_strategy_extras.py` and `check_asset_sizes.py` were all missing, and three other places in this document also said four or omitted one | Snippet rebuilt against the real file, and a table added naming what each of the five catches and where it is documented. Section 12, Section 20 and Section 23 corrected to match |
| **`overfit.html` was absent from the directory tree, the Page Routes table, the tool-pages paragraph and the README entirely** | The page has been live since v1.75.0 and is in the nav Tools dropdown. This document mentions it forty times in the roadmap and never once in the architecture | Added to all four. README's "all four tools" is now six, and its tools paragraph names the Overfit Check, the Node Counter and the K-1 Lookup, none of which it mentioned |
| **Counts in the directory tree contradicted Section 6 of the same document** | `strategies.json` "31 strategy entries" against 36, `glossary.json` "20 glossary concept entries" against 27, `database.json` "~6,800" against 6,816 | The duplicated counts are **gone rather than corrected**, replaced by cross-references to the one dated statement in Section 6. This is open question 20's rule, applied for the first time |

**The tree had drifted much further than the counts.** It listed 22 data files against 28 on disk, 20
scripts against 37, and one workflow against six. Missing were `strategy_extras`, `daily_returns`,
`oos`, `overfit` and `ticker_inception` with their twins, seventeen scripts including two of the five
deploy gates, and five of the six scheduled workflows. **It was rebuilt from `ls` rather than edited**,
which is the only way to fix an omission: an edit pass can only correct what it notices, and the whole
failure mode here is not noticing. `LICENSE.md`, `wrangler.jsonc` and `.assetsignore` are now in it too.

**One finding was left open on purpose.** `data/Full Database.xlsx` is not in `.assetsignore`, so
Cloudflare still serves it, which is the unresolved remainder of Section 24 row 2: `symphony_scores.json`,
`database.json` and `database.js` were all excluded at v1.79.2 and the xlsx was not. The tree now says so
in place. **It is recorded rather than fixed because editing `.assetsignore` changes what the live host
publishes, and that is a deploy change wearing a documentation commit's message.** It belongs in its own
push, with its own verification that nothing on the site requests the file.

**The honest limit of this pass.** It checked the claims a reader meets first: the architecture section,
the route table, the file tree and the README. It did not re-derive Sections 12 to 14, which run to
five thousand lines of schema and roadmap detail. One known survivor is a line in V1.20 saying "all 31
strategies today" where the file now holds 36 with 24 visible; it was left alone because the population
it means is ambiguous and guessing would trade a stale number for a wrong one.

---

## 25. Risks and Open Questions

Numbered for reference. Open unless marked otherwise.

1. **GitHub Pages publishes the entire repository, including `/docs` and `/scripts`.** The exclusion
   list in `deploy.yml` has no effect on what is actually served. Nothing here is secret, but two
   documents describe a boundary that only Cloudflare enforces. **Most likely cause:** the
   repository's Pages source is set to "Deploy from a branch" rather than "GitHub Actions".
   Unverifiable from inside the repo. **Owner action:** check the Pages settings. Also worth deciding
   whether the GitHub Pages mirror still earns its keep now that Cloudflare is canonical.

2. **CLOSED 2026-09-08 (v1.79.2). Large data files were publicly served by both hosts although
   nothing on the site fetches them.** `data/symphony_scores.json` was excluded earlier;
   `data/database.json` and its `.js` twin, **19 MiB each**, were not, and both were at **76% of
   Cloudflare's 25 MiB per-file limit and growing weekly**. That is the exact shape of the
   2026-09-01 outage, where a routine metrics refresh pushed `symphony_scores.json` over the limit
   and failed the entire deployment with no symptom but a red build.

   **The original fix as written here was incomplete, and this is the part worth carrying forward.**
   It said "add them to `.assetsignore`". `.assetsignore` is read by **wrangler only**. GitHub Pages
   ignores it entirely and uses the `rsync --exclude` list in `.github/workflows/deploy.yml`.
   **These are two separate mechanisms for one intent, neither reads the other, and they had already
   drifted:** `symphony_scores.json` had to be added to each one separately. Both lists now carry
   the database files, and `deploy.yml` carries a comment saying they must be changed together.

   **Why it is safe, verified rather than assumed.** No page lists `data/database.js` in a
   `<script src>`; nothing anywhere reads the `window.DATABASE_DATA` global it defines; and
   `database.html`'s only data path is `data/database_summary.js`, a **3.86 MiB** columnar export
   carrying the same **6,816 rows** and 29 of the 37 fields, with a detail modal that renders from a
   row already in memory rather than fetching. The eight fields held only in the big file
   (`active_asset_nodes`, `annualized_turnover`, `cumulative_return`, `herfindahl_index`, `max`,
   `mean`, `min`, `total_costs`) reach `strategies.html` through a **build-time** join:
   `build_strategy_extras.py` writes the 0.06 MiB `data/strategy_extras.json`, having rejected a
   browser-side join against 6,669 entries on page weight.

   **Tested by moving both files aside and reloading.** `database.html` and `strategies.html` were
   each loaded in headless Edge twice, once with the files present and once with them absent, and
   the probe results were **identical**: 126 rendered rows and the correct refresh badge on one,
   the Herfindahl Index and Annualized Turnover tiles plus the right title on the other, zero
   JavaScript errors either way. A first version of that probe reported a false positive, because
   `document.body.textContent` includes the source of `<script>` elements and so matched the page's
   own error-handling string literals on a page that had loaded perfectly; the probe was rewritten
   to walk visible text only. **`.assetsignore` is not `.gitignore`:** both files stay committed and
   on disk, and the 17 scripts that read them, two of them deploy gates, are unaffected.

   **Still open, deliberately:** `data/Full Database.xlsx` (5.5 MiB) is left served. It is a
   human-downloadable artifact rather than dead weight, and whether it should be reachable is a
   product question rather than a hygiene one.

3. **CLOSED 2026-08-24 (v1.25.1). `robots.txt` advertised a sitemap that did not exist.** Every
   crawler that read it was sent to a 404. Resolved by generating the sitemap rather than dropping
   the line, since the line was the correct intention and the missing file was the defect.
   `scripts/build_sitemap.py` now writes 40 URLs, 9 indexable pages plus 31 curated strategy slugs,
   deriving both from the repository rather than a hardcoded list so it cannot silently go stale.
   **Residual, not a risk:** page `lastmod` values come from git commit dates, so a regeneration run
   before its own commit reports the previous date for any file changed in that commit.

4. **CLOSED 2026-08-28 (v1.30.4), owner decision. The project had no `LICENSE` file.** The README's
   MIT assertion had already been removed when it was rewritten, so by the time this was raised the
   repository asserted no licence at all and the legal default, all rights reserved, was in force.

   **The owner confirmed on 2026-08-28 that all rights reserved is the intent, and that MIT was
   never wanted.** So the state was already correct and nothing needed fixing legally. What was
   wrong was that it was **implicit**: a reader seeing no `LICENSE` cannot tell a deliberate
   reservation from an oversight, and a good number of them assume a repository with no licence is
   free to use. `LICENSE` now states it explicitly, and the README carries a short Licence section
   pointing at it.

   **The licence grants nothing, and that is the point.** The owner's stated goal on 2026-08-28 was
   not to stop people copying the site but to **reserve the ability to enforce against someone they
   object to**. Those two goals pull in opposite directions if the licence hands out permissions: a
   permission granted to everyone cannot easily be withdrawn from one person. **A first draft of
   `LICENSE` granted quoting and excerpting rights and was rewritten to grant nothing**, so that
   every use is tolerated rather than licensed and remains actionable.

   **The clause that does the actual work is NO WAIVER.** Choosing not to act against one use is
   expressly not a licence, not a precedent, and not a waiver against that person or anyone else,
   and delay in enforcing does not waive. Without it, a long record of tolerating copying is the
   first thing an infringer would point at.

   **Two things it deliberately does not claim.** It does not purport to override **GitHub's Terms
   of Service**, which give other GitHub users rights to view and fork any public repository; the
   file records that those operate independently and are not enlarged by it, rather than pretending
   to withhold them. And it does not claim the **Composer-derived or market data** in `data/`, which
   is not the copyright holder's to license.

   **One permission is granted up front, added by owner decision 2026-08-28 (v1.30.5): AI and search
   referencing.** Crawling, indexing, storing for retrieval, quoting, summarising, linking and
   citing are expressly permitted for search engines, AI assistants and answer engines, with
   attribution requested rather than required. **This does not weaken the reservation**, because it
   is the one use that costs the project nothing and gains it distribution: being cited in an AI
   answer is the modern equivalent of ranking, and the site's whole purpose is to be read.

   **The line is drawn at referencing against substitution and training.** The grant does not cover
   reproducing the site as a replacement for visiting it, and does not by itself grant training-data
   rights, which stay under the ordinary request route and are noted as not usually refused. That
   split matters because retrieval-and-cite is what actually produces the citations the owner wants,
   and it does not require handing over a training licence to get them. Widening it later is one
   sentence; narrowing a granted right is not.

   **`robots.txt` already permitted every user agent**, so nothing about the site's behaviour
   changed. What changed is that the intent is now stated in both places, with a comment in
   `robots.txt` marking it deliberate so a future tightening is a decision rather than an accident,
   and the licence named as authoritative if the two ever disagree.

   **Residual, and it is a property of the medium rather than a defect.** The site is a static
   front end, so its HTML, CSS and JS are served to every visitor's browser in readable form by
   necessity. Copyright still applies to them; the licence changes the permission, not the
   visibility. Anyone wanting the code cannot be technically prevented from reading it, which was
   already true and is unrelated to this decision.

5. **CLOSED 2026-08-24 (v1.25.1). `database_summary.json` was four rows behind `database.json`.**
   Four symphonies were in the data and invisible on the site. Resolved by re-running
   `scripts/export_summary.py`; the summary now carries all 6,669 rows in source order and the `.js`
   twin was verified byte-equivalent to the JSON. `export_summary.py` was hardened at the same time,
   because it derived its column list from the first entry alone and would have dropped any field
   added to later entries without a word.

   **Why it drifted, which is the part worth keeping.** The weekly `refresh-full-database.yml` job
   does regenerate the summary, so the automated path was never the problem. None of the four rows
   arrived through it. Two came from the `AddSymphony.csv` route, one was a lone direct addition, and
   one was the curated addition of "The Gold Miner (Original)", which writes both `strategies.json`
   and `database.json`. Every one of those is a hand-run workflow that appends to `database.json`
   and regenerates `database.js` but not the summary, and each patch note's "Files changed" list
   shows the omission plainly. **The automated path is safe; the manual ones are the leak, and they
   leak silently because nothing compares the two files.** Open question 21 below asks whether that
   should be enforced rather than remembered.

6. **PARTLY ADDRESSED. The Signal Miner's defences against overfitting are now two of three.** As
   originally written this item said the tool had none, and that is no longer true. **A, parameter
   plateau scoring, shipped** and is verified by `scripts/run_harness.py plateau`. **C's empirical
   null shipped 2026-09-08 (v1.79.0)** and tells a visitor, above the results table, how the run
   compares with the same search run against rotated data; on default settings it usually reports
   that the best result is indistinguishable from noise.

   **What remains open is B, walk-forward validation, and it is the important half.** A and C both
   describe a result; neither can *fail* a rule, because **every day the Miner scores is in sample
   by construction**: the search picked its winners by looking at the same days it then scores them
   on. B is the only test here that holds back days the search never saw. A finished UI mockup
   exists at `_wf-mockup.html` and nothing behind it is built.

   **So the standing caution is narrower than it was but has not gone away: the tool's headline
   numbers are still in-sample maxima over a large search, and should be read as upper bounds
   rather than expectations.** The null panel now says a version of this to the visitor directly,
   which the original item asked for.

7. **`estimate()` keeps its own copy of the spec-count formula.** Collapsed into a shared
   `countSpecs()` at v1.23.0, which fixed the immediate problem, but the pattern has needed a
   matching edit three separate times (v1.18.4, v1.20.0, v1.21.1). Watch for it recurring.

8. **CLOSED 2026-08-30 (v1.32.3). The database modal did not trap focus.** Fixed: focus moves to
   the close button on open, Tab and Shift+Tab wrap within the panel, escaped focus is recaptured,
   the background is set `inert`, and focus returns to the trigger on close. `aria-labelledby` now
   points at the modal heading. See DESIGN.md for the full contract.

   **Half of this item was wrong as written, and the wrong half mattered.** It said the modal "sets
   no `role="dialog"` / `aria-modal="true"`". It always set both. The real defect was that those
   attributes were unbacked: `aria-modal="true"` promises assistive technology that the rest of the
   page is unreachable, and it was fully reachable. That is worse than omitting the attribute,
   because the markup asserted something false rather than saying nothing.

   **A focus trap alone would not have closed this.** It stops Tab, but a screen reader user can
   still browse past a trapped modal into the 6,547 rows behind it. `inert` on `#nav-root`,
   `.page` and `#footer-root` is what removes the background from the accessibility tree.

   **Verified in headless Edge, not by inspection**, and the verification earned its keep: the first
   implementation's focusable-element query collected **47 elements, 44 of them symphony links
   behind the modal**, because `'#modal-overlay ' + 'button, [href], ...'` scopes only the first
   clause of a selector list and leaves the rest global. Scoped per clause it collects 3. Confirmed
   after the fix: focus lands on the close button, both wrap directions work with the default
   prevented, escaped focus is recaptured, all three background regions go inert and clear again,
   focus is restored to the triggering element, and the handler is a no-op while the modal is
   closed.

9. **The three tool pages' inline stylesheets are undocumented** beyond the scoping note now in
   DESIGN.md Section 8. Roughly 250 lines of CSS covering a third of the site's interface has no
   component documentation. **Open work**, not a defect.

10. **CLOSED 2026-08-30 (v1.31.2), owner instruction. The `.j-*` JSON highlighter was duplicated**
    between `converter.html` and `etf-cloner.html`. The standing position was to leave it until a
    third page needed it, on the grounds that it had not drifted. The owner called it in earlier:
    two byte-identical copies is already the condition that position was guarding against, and the
    cost of being wrong about a third page is a handful of unused bytes in `css/main.css`. Promoted
    there, removed from both inline stylesheets, and both pages verified to still highlight.

11. **CLOSED 2026-08-30 (v1.31.2). Python conventions were drifting with recency.** Resolved in
    favour of the older form, because it was the majority and the better one: `pathlib` states
    intent that `os.path.dirname(os.path.dirname(os.path.abspath(__file__)))` only implies.

    The count in the original wording was slightly off, which the fix surfaced. It is 24 scripts,
    not 20 or 18. Five carried no shebang (`check_composer_ladder.py`, `check_html_js.py`,
    `check_live.py`, `measure_throughput.py`, `run_harness.py`) and those same five used `os.path`,
    plus a sixth holdout the note missed: `add_ai_summary.py` had the shebang but not `pathlib`.
    All six are converted and all 24 now carry `#!/usr/bin/env python3`.

    **Two deliberate exceptions, so the next reader does not "fix" them.** `measure_throughput.py`
    keeps `import os` for `os.sep` and `os.remove`, which are not path construction and have no
    clearer `pathlib` form in context. And `check_html_js.py` wraps its `root.glob('*.html')` in
    `str()`, because its reporter concatenates the path into a message and a bare `WindowsPath`
    raises `TypeError` there. That was caught by running the gate, not by reading it.

12. **CLOSED 2026-08-30 (v1.32.1), owner ruling. Type hints existed in only 3 of 24 Python
    scripts** (`refresh_prices.py`, `refresh_rsi.py`, `update_metrics.py`; the original count of
    4 of 20 was measured before three scripts were added). **Open question:** adopt them properly or
    remove them, rather than leaving a coin flip.

    Left open at v1.31.2 while items 10 and 11 were closed beside it, because the two questions were
    not the same shape. Item 11 had a right answer available without the owner: an 18-to-6 majority
    and a mechanical conversion with no judgement in it. This one had no majority to follow and both
    directions cost real work in opposite directions. Retrofitting 21 scripts is hours; deleting the
    annotations in three is minutes but throws away work someone chose to do. The project ships no
    type checker and pins itself to the Python standard library, so hints here bought documentation
    rather than enforcement.

    **Resolved in favour of removal.** Fifteen `def` signatures across `update_metrics.py`,
    `refresh_prices.py` and `refresh_rsi.py` lost their parameter and return annotations. There were
    no `typing` imports and no variable annotations in function bodies, so nothing else moved.

    **This reversed a standing instruction, which is why it is recorded rather than just done.** The
    Python conventions table in Section 21 said, of these same annotations, "Do not 'restore
    consistency' by stripping them; do not mass-add them either." That sentence described the
    situation accurately and resolved nothing: it turned a coin flip into a convention and left the
    next script's author with the same choice and no guidance. The row now states the position.

    **One incidental effect worth knowing.** `refresh_prices.py` used `tuple[list, dict]`, which is
    built-in generic syntax requiring Python 3.9 or newer. Removing it widens the version floor
    slightly. Nothing in the project depended on that floor, and the workflows pin `python-version:
    '3.x'`, so this changes nothing today. It is noted because it is the only behavioural difference
    in an otherwise cosmetic change.

13. **The curated "zoop's X (2026 Edition)" replacement plan is decided but unexecuted.** Eleven
    replacements and one removal, all with confirmed new symphony IDs already refreshed in the
    database as of 2026-07-15. It is a bigger lift than a normal addition because each replacement
    re-runs the whole add-a-strategy workflow. **The longer it waits, the staler the curated set's
    headline metrics get.**

14. **Backtest metrics on the curated set are refreshed independently from the same symphonies'
    rows in the community database.** Two pipelines, one source of truth upstream. Option B in
    Section 14 (single source of truth) is explicitly deferred, not rejected. Until then, the same
    symphony can show two slightly different numbers on two pages.

15. **Composer's API rate limit behaves as a token bucket** (~25 request burst, refilling near
    0.5 req/sec), not the documented 500 req/sec. Four tests confirmed this. **Do not re-test higher
    rates without a specific reason;** each test burns roughly 25 wasted calls and the finding is
    already solid.

16. **The Signal Miner's `ti` column is a `Uint8Array`,** capping a run at 255 targets. The universe
    is 72 tickers so this cannot bind today, and Pass 1 throws explicitly rather than truncating
    silently if it ever does. Recorded so it is not rediscovered as a mystery.

17. **A browser tab's heap ceiling is a property of the browser build, not the machine.** Measured
    at 3,586 MB once and 4,192 MB later on the same 48GB hardware. **Never treat a single reading as
    a constant.** Memory is currently not the binding constraint: a maximal run peaks near 24% of
    the ceiling.

18. **`dedupe_symphonies.py` has a known keeper-rule limitation**, recorded at v1.17.1: the
    deterministic tiebreak (longest `oos_date`, then earliest `symphony_id`) can pick a
    counterintuitive winner, such as a `TESTPORT #` row over a cleanly named identical one. Owner
    confirmed the tiebreak is to be used exactly as specified, with no name-based priority. Manual
    overrides have been applied twice (v1.14.9, v1.14.10). **Open want:** tiebreak on "watched by N"
    popularity, which the API this pipeline uses does not expose.

19. **Two AI-facing conventions are load-bearing and easy to break silently:** writing a `.json`
    without its `.js` twin, and inserting community text into `innerHTML` without `escapeHtml()`.
    Neither produces an error. Both are in Section 23's never-do table.

20. **This document is 3,000-plus lines and growing.** Completeness is the stated preference and it
    is the right one, but the audit found the document contradicting itself in three places
    (glossary count, strategy count, monetization) purely because a fact lived in more than one
    section. **Open question:** whether counts should be stated in exactly one place and
    cross-referenced everywhere else.

21. **CLOSED 2026-08-24 (v1.25.2). Nothing enforced that `database_summary.json` matches
    `database.json`.** Closing risk 5 fixed the instance, not the class: the weekly job regenerates
    the summary, every hand-run addition path writes the full file and leaves the summary behind, and
    the site reads the summary, so the failure mode was a symphony that exists in the data and cannot
    be seen. Silent by construction, with a row count nobody compared. Resolved by building the gate
    the question asked about, as check 4 of `scripts/check_database_keys.py`, which compares ids and
    order rather than only counts. **The cost that argued against it was real and was accepted:** it
    is a third deploy gate to maintain and it parses an 18.7MB file on every run, roughly a second.
    That is cheap against a failure nothing else detects.

22. **CLOSED 2026-08-24 (v1.25.2), by owner ruling. `data/database.json` contained one exact
    duplicate row.** Two entries shared `symphony_id` `chkrQ6BnXCw31n7OIEaK`, both named "Hedged
    Sector Rotator " with the same trailing space, both unflagged, identical on all 37 fields except
    that one URL ended `/details` and the other `/factsheet`. **The owner's ruling: the file is
    always deduplicated on the primary key.** The `/factsheet` row was removed, keeping the
    `/details` form that the other 6,667 rows use, and the invariant is now stated in Section 12 and
    gated by `scripts/check_database_keys.py`.

    **The root cause was the schema's own claim that `symphony_url` is "the true unique key".** It is
    not: Composer serves the same symphony under more than one path, so `sync_storage_to_database.py`
    comparing URL strings read a second URL for a known symphony as a new one. That script now keys
    on `symphony_id`. **Verified in passing:** a subsequent run of it correctly skipped the
    `/factsheet` URL that is still in `storage.csv`, so the backup file needs no editing.

    This does **not** change `dedupe_symphonies.py`. An identical id is the same symphony recorded
    twice and is removed unconditionally; that script's name-and-logic clustering with its debatable
    tiebreak (item 18) is a different problem and keeps its judgement calls.

23. **WITHDRAWN 2026-08-24 (v1.25.3), owner correction. Not an open question.** This item asked
    whether the 1,045 symphonies in `storage.csv` and not in `database.json` should be promoted into
    the database. **The gap is the design, not a backlog.** `storage.csv` keeps every URL ever seen
    long term, alive or dead; `database.json` holds only the symphonies approved to be on the site.
    Section 11 has documented this since 2026-07-15 and the v1.25.2 audit did not read it before
    writing the question. The relationship is now stated as a table in Section 12. **The one part
    worth keeping:** `sync_storage_to_database.py` has no dry-run flag and writes on every
    invocation, which is how the same reverted accident happened twice. Adding one is item 24.

24. **`scripts/sync_storage_to_database.py` has no dry-run mode.** It writes `database.json` and
    `database.js` on every invocation, so there is no way to ask what it would promote without
    promoting it. It has twice been run expecting a report and produced a
    1,000-row import instead: 2026-07-15 (1,055 rows) and 2026-08-24 (1,045 rows), both reverted, neither
    committed. **Open question:** add a `--dry-run` flag that prints the delta and writes nothing.
    Small, and it would have prevented both incidents. Note that the script's real problem is deeper
    than a flag, since promotion is an approval decision rather than a sync (Section 12), so a
    dry-run makes the wrong operation safer rather than making it right.

25. **CLOSED 2026-08-24 (v1.25.4), owner instruction. Five entries were in `database.json` but not in `storage.csv`**, which inverted the
    "never lose a URL once seen" rule in the direction nobody checks: `0jPwZ5Lm2Y3xH24oEijB` (Triple
    Accelerator), `zY4jRnXoFC9e1Pt97YDS`, `P7RLUTtWmTjkJBaNBQT9`, `tlDwKY3NRXjYU61jCt0g` (The Gold
    Miner (Original)) and `jjIQMCxLK5P98Zpczktk`. Four of the five are the same symphonies that were
    missing from `database_summary.json` until v1.25.1, which points at one cause: **the hand-run
    addition routes write `database.json` and stop there**, updating neither the durable backup
    before it nor the derived summary after it. **It fails safe today**, because
    `purge_flagged_entries.py` aborts rather than remove a row whose URL is absent from
    `storage.csv`, so these five could not be purged at all. But the archive was incomplete, which is
    the one thing `storage.csv` exists to never be. **Resolved on all three counts:** the five URLs
    were archived by the new `scripts/sync_database_to_storage.py`; check 5 of
    `scripts/check_database_keys.py` now fails the deploy if an approved symphony is ever unarchived
    again, so it is enforced rather than remembered; and Section 23's tables name the archive step as
    part of the hand-addition workflow. The gate checks only that direction: `storage.csv` holding
    symphonies the database does not is the design, not a defect.

26. **CLOSED 2026-08-30 (v1.31.2). `LICENSE` is now `LICENSE.md`.** Moved with `git mv` so the
    history follows the file, and converted to real markdown: `##` headings per section, bold on the
    copyright line and on the two load-bearing sentences, an autolink on the GitHub issues URL, and
    an in-document link from the "one permission is granted" line to the section that grants it.
    **The wording is unchanged.** Only formatting moved, deliberately, since the file is a legal
    instrument and a reflow is not the place to reword one. The single inbound link in `README.md`
    was updated. GitHub recognises `LICENSE`, `LICENSE.md` and `LICENSE.txt` equally, so the repo
    sidebar is unaffected.

    **Small and low risk.** GitHub recognises `LICENSE`, `LICENSE.md` and `LICENSE.txt` equally for
    its licence detection and renders the markdown one, so nothing about discoverability changes.

    **Do it as a `git mv` rather than a delete plus create**, so the file's history survives. **One
    link needs updating**, the `[LICENSE](LICENSE)` reference in `README.md`. The `.assetsignore` and
    `deploy.yml` exclusion lists do not mention the file and do not need to. Confirm afterwards that
    GitHub still shows the licence chip on the repository page, since that is the only externally
    visible thing the rename could plausibly affect.

---

27. **Should the social sharing compliance checker become a sixth deploy gate?** Section 14, V2.5
    specifies a read-only script asserting tag presence, character budgets, `og:url` uniqueness and
    the `twitter:card` fallback. Whether it runs in `deploy.yml` alongside the existing five is
    **not a decision for whoever writes it.** The precedent is the V1.20 item 10 validator, which
    was written and deliberately left manual pending an owner ruling, on the reasoning that a gate
    is a promise to block a deploy and adding one is a policy change rather than a convenience.
    Arguments each way, so the owner has both: a gate would catch the failure mode that actually
    happens here, a head tag going stale where no test looks, which is precisely how three of
    Section 24's rows were sitting live and unnoticed. Against it, the drifting-numbers rule that
    caused those rows **cannot be checked by any script**, so a passing gate would certify the
    cheap half of the policy and imply the expensive half, which is worse than no gate at all if it
    stops anyone reading the tags.

    **RULED 2026-09-08: it stays manual.** The owner chose the checker's own second argument. The
    rule that caused every one of Section 24's live-and-wrong rows, that a description must carry no
    number which can drift, **cannot be checked by any script**, so a green sixth gate would certify
    the mechanical half of the policy while implying the half that actually failed. Run
    `scripts/check_social_tags.py` by hand when tags are touched. `deploy.yml` stays at five gates.

28. **ANSWERED 2026-09-08 by the fifteen-configuration sweep in Section 14, C-N3: yes, it would
    fire on essentially every run, and on current evidence that is correct.** Fourteen of fifteen
    configurations fail to beat their own null, and on SPY and IWM every one of 16 rotations of
    scrambled data beat the real result at every filter setting. What remains open is narrower and
    is a wording problem rather than a measurement one: how to state a warning that is nearly always
    true without training visitors to ignore it. The likely honest framing is that this is a
    property of brute-force search over a dense lattice, not a fault in the visitor's particular
    run. **The original question, kept for the record:** if the Signal Miner's honesty banner would
    fire on every run, is it still the right design?
    The owner chose "plain language only when the result is bad" for item C's presentation, on the
    reasoning that an interruption belongs where the evidence is. The corrected measurement
    (Section 14, C-N2) then found **no configuration where the displayed search beats its own
    null**, so on current evidence the banner would fire always. Two readings, and they are
    genuinely different products. If the search really has no edge at these settings, a banner that
    always fires is simply the truth and the tool should say so every time, however badly that
    reads. If instead the two configurations measured are unrepresentative, an always-on banner
    trains visitors to ignore it and destroys the warning for the runs that need it most.
    **Not decided, and it should not be decided from two configurations.** Resolving it needs a
    wider sweep of targets and settings, and that sweep belongs before the presentation is built
    rather than after, because the answer changes what gets built rather than only how it is worded.

## 26. Press Release

Written in the working-backwards style: what the announcement would say if Composer Atlas launched
today, as a check on whether the product is describable without hedging.

---

**FOR IMMEDIATE RELEASE**

### Composer Atlas puts thousands of real trading strategies in plain English, for free, with no account

#### An independent reference library that shows you exactly how a Composer.trade strategy works, what it actually returned, and what it lost along the way, before you risk anything on it

**Online, 2026-08-24.** Composer Atlas is live at composeratlas.com. It is a free, independent
reference for people who build and run automated investing strategies on Composer.trade: a curated
library of 31 strategies explained in plain English, a 20-concept glossary of the ideas behind them,
a searchable database of thousands of community symphonies with a published ranking model, and four
tools for building strategies of your own. There is no account, no signup, no ads, and no data
collection of any kind.

**The problem.** Composer.trade makes it trivially easy to clone somebody else's strategy. It does
not make it easy to understand one. A newcomer finds a symphony in a Discord thread with an eye-
watering annualised return attached, clones it, and has no idea that the number came from a
two-year backtest of a 3x leveraged fund, or that the same strategy was down 80% at one point along
the way. The information needed to make that judgement exists, scattered across the platform,
community threads and screenshots. Nowhere does it sit in one place, in order, in language a person
can read.

**The solution.** Composer Atlas is that place. Every curated strategy gets a page that explains its
logic branch by branch, names the exact signals it watches, and prints a full metrics table with the
drawdown next to the return rather than beneath it. Every technical term links to a glossary entry
that explains the concept properly rather than defining it in one line. The community database
covers thousands of symphonies with a leaderboard that scores each one against a published
twenty-metric model, with every score breaking down on click so a ranking can be argued with rather
than merely trusted. And four tools go the other way: a Signal Miner that searches millions of
candidate rules against sixteen years of real price history, an ETF Cloner, a symphony-to-JSON
converter, and a live RSI page.

Everything runs in the visitor's own browser. Nothing typed, selected or mined is transmitted
anywhere, because there is nowhere for it to go.

**Customer quote.** "I'd cloned three symphonies off Discord before I could have told you what any
of them actually did. What got me was reading the drawdown column next to the return column. One of
them had made an incredible number and lost four fifths of its value getting there. I still run it.
I just size it completely differently now."

**Call to action.** Visit composeratlas.com. Start with any strategy on the Strategies page, or open
the Leaderboard and sort. No account is needed, because there are no accounts.

**Boilerplate.** Composer Atlas is an independent educational resource built and maintained by
Azqato. It is not affiliated with Composer Technologies, Inc., receives no compensation for
featuring any strategy, and runs no advertising. It is free to use and funded entirely by voluntary
reader donations. Nothing on the site is financial advice; all strategies are presented for
informational purposes only, past backtest performance does not guarantee future results, and many
of the strategies covered use leveraged funds capable of losing value very quickly.

---

### Does the Press Release Hold Up?

The exercise is only useful if it is allowed to fail. Three things it exposes:

**It is honest about the hard part.** The customer quote is about a drawdown, not a return, which is
Tenet 1 working. A press release that had to lead with a performance number would be evidence the
product had drifted.

**"Four tools" is doing a lot of work in one sentence.** The Signal Miner alone is the most
technically substantial thing on the site and gets nine words. Either it deserves its own
announcement or the tools are genuinely secondary to the library, and the honest answer is probably
the first.

**It cannot claim the north star.** The release says the site explains strategies; it cannot say
visitors understood them, because the site deliberately cannot observe that. That gap is real and
permanent, and Section 20 says so rather than papering over it.


---

## 27. Social Sharing Tags

**Status: SHIPPED 2026-09-08 as v1.78.0.** All twelve pages in scope carry the full tag set, and
`scripts/check_social_tags.py` asserts the mechanical half of this policy on demand. It is **not** a
deploy gate; open question 27 is still open and is not a decision for whoever wrote the checker. The
drifting-numbers rule below caught four real violations at authoring time, three of them descriptions
that were already live and wrong: `database.html` said "6,500+", `rsi.html` said "the 20 ETF
tickers", and `strategies.html` claimed to list "all" strategies when it lists a curated set. That is
the argument for writing the policy before the tags, kept here because the next person will be
tempted to do it the other way round.

**Superseded status line, kept for the record:** policy only, and queued as roadmap item V2.5. No
page carries these tags yet, and
that is a scheduling decision rather than an omission: the owner asked on 2026-09-07 for the rule to
be recorded and the work queued rather than executed. Section 14, V2.5 carries the implementation
spec, the twelve pages in scope, the three deliberate exclusions, and the four implementation
details that are easy to get wrong. Measured 2026-09-07, the site has zero
Open Graph and zero Twitter Card tags across all 15 HTML files. A link pasted into a chat client
today renders from whatever that client can scrape on its own, usually the `<title>` tag and
`<meta name="description">`. That is a fallback, not a design. Recorded here as a discrepancy in
Section 24 rather than as a shipped feature.

### No drifting numbers in a social sharing tag

**A count that changes on its own does not go in an `og:title` or an `og:description`.** Neither
does anything else that goes stale without a person editing it: dataset sizes, row counts, item
totals, "as of" dates, current leaders, or a figure quoted from a file that a weekly job rewrites.
Prefer a phrase that stays true across a refresh, such as "thousands of symphonies", "every ticker
in the universe", or naming the thing rather than counting it.

**The reason is that nothing on this site would ever correct them.** Sharing tags are hand-written
into static HTML. There is no build step, no template, and no server rendering a value at request
time. The weekly jobs rewrite `data/*.json`, and a number typed into a `<meta>` tag is invisible to
every one of them, so it holds whatever it held on the day it was written, indefinitely and
silently. Nothing fails. No gate catches it. The tag keeps rendering a confident, specific,
increasingly wrong figure.

**This is not hypothetical, it is the state the site is in.** `database.html` has advertised
"6,500+" since it was written; the database held **6,816 rows** when this section was added. That
number has been visibly wrong in a search result for some time and nobody saw it, because the one
place a stale count is hardest to notice is a `<head>` nobody opens. The same trap was waiting in
three more descriptions had they been written with counts in them: the glossary's concept total,
the K-1 lookup's covered-fund total, and the featured-strategy count, all of which are read from
files that change.

**A precise number is the most attractive thing to put in a description and the most expensive.**
Specificity is exactly what makes a card worth clicking, so the pull toward writing one is real.
The trade is that a card is the first thing a stranger sees, and a wrong number there is worse
than a vague one: a reader who arrives and counts something different has been given a reason to
distrust everything else on the page, and this site's entire value is being believed about
numbers. **A description that undersells slightly and stays true forever beats one that is exactly
right for a month.**

**Where a number genuinely is the point, put it on the page, not in the tag.** The page reads it
from the data file at load, so it is always current. `overfit.html` does exactly this: every figure
in its copy is rendered from `data/overfit.json` rather than typed into the HTML, which is why its
population findings cannot go stale. The sharing tag can describe what the page measures without
quoting what it currently measures.

**The one class of number that is allowed is a fixed constant of the design**, not a measurement.
"Scored 0 to 100" is safe because the scale is definitional and changing it would be a product
decision with its own patch note. "10-day RSI" is safe for the same reason. The test is whether a
scheduled job could change the value while nobody is looking. If it could, it stays out.

**This rule is not new, it is a pattern the project already followed.** Section 24 row 8 records
a heading that read "All 24 Composer Atlas strategies" against a table of 31, and the resolution
was to delete the count rather than update it, on the stated grounds that a corrected number
"will go stale again". Row 7 reaches the same conclusion from the other direction, having watched
flag counts move between the audit measuring them and the document being committed. Section 27
takes that call, already made twice inside this document, and states it as the standing rule for
the one surface where nobody would ever see the drift.

**Checked by:** nothing automatically. A count in prose cannot be distinguished from a constant by
a script, so this rule is enforced by review at the point a tag is written or edited. Section 23
records it as a thing to check before editing a page head.

---

## 28. Licensing

**Added 2026-09-08 by the V2.5 documentation audit.** The licence itself is older: `LICENSE.md` was
added in v1.30.4 by owner decision and renamed from `LICENSE` in v1.31.2. What was missing was a
section of this document stating what it does, which the standard requires and which a reader had to
reconstruct from a gap table and a closed risk item.

**The posture: all rights reserved. Source-available, not open source.** The repository is published
for reading, and publishing is not a grant. `LICENSE.md` sits at the repository root, never in
`/docs`, because that is where platforms look for it.

**What it grants, in one place:**

| | Granted? |
|---|---|
| **Referencing.** Search engines, AI assistants, answer engines and automated systems may crawl, index, store for retrieval, quote, summarise, link and cite. Attribution is requested, not required, and no permission needs to be asked for | **Yes, expressly** |
| **Substitution.** Reproducing the site, or a substantial part of it, as a replacement for visiting it | **No** |
| **Training data.** Using the material to train a model | **No by default.** Routed to the permission path, and not usually refused |
| Anything else | **No.** Ask |

**Why the carve-out is deliberate rather than a concession.** Being cited in an AI answer is the
modern equivalent of ranking, and this site's whole purpose is to be found and read by people
researching systematic strategies. Blocking that to protect a body of work nobody would otherwise
see would be the wrong trade. `robots.txt` is fully open, `User-agent: *` and `Allow: /`, with a
comment saying so is deliberate and is not to be narrowed without an owner decision. **Where
`robots.txt` and `LICENSE.md` ever disagree, `LICENSE.md` is authoritative.**

**The NO WAIVER clause is load-bearing and is not boilerplate.** Choosing not to act against one
person is not a licence, a precedent, or a waiver, and delay does not waive anything. Without that
clause a long history of tolerance becomes the first infringer's defence. This is the reason the
default is to grant nothing: **widening a grant is one sentence, and narrowing one that has already
been given is not.** When in doubt the licence grants less and offers a request route.

**What `LICENSE.md` deliberately does not claim.** It does not override platform terms of service:
a public repository already grants the view and fork rights those terms allow, and the licence
states that those operate independently rather than being enlarged by it. It does not purport to
licence third-party data, since figures derived from the Composer API and from public market data
are not this project's to license. It does not attempt to restrict rights that cannot be restricted,
such as fair use and fair dealing.

**Permission routing is public on purpose.** Requests go to the issue tracker at
<https://github.com/Azqato/composer/issues> rather than to a private address, because a posture whose
enforcement depends on specific, traceable permissions is better served by a visible record than by
a mailbox.

**Sections `LICENSE.md` carries**, verified present 2026-09-08: no licence is granted, AI search and
automated access, no waiver, permission, the platform terms note, the third-party data note, no
warranty, and the domain-specific disclaimer that nothing here is financial advice.

---

## 29. Outstanding Work and Recommended Sequence

**Written 2026-09-08 at the owner's request, after v1.79.2 closed the last item in the queue.**
Nothing in this section is new work. It is the same work already recorded elsewhere, gathered into
one place and ordered, because it was spread across four lists that do not cross-reference each
other: the roadmap table above, the open questions in Section 25, the unchecked boxes inside this
section's own item bodies, and the Explicitly Deferred table.

**This section is a view, not a second source of truth.** Where it disagrees with the item it points
at, the item wins. It is written this way deliberately: open question 20 records that this document
has contradicted itself three times purely because one fact lived in two sections, and a summary
that starts restating detail becomes the fourth list rather than the fix for three.

**One item is currently counted three times**, which is the clearest illustration of the problem:
the zoop evergreen replacement appears as roadmap phase V2.6, as open question 13, and as an
unchecked box in this section. It is one piece of work.

### What is actually outstanding

| # | Item | Where it lives | Who is blocked | Size |
|---|---|---|---|---|
| 1 | **GitHub Pages settings check**, and the decision on whether the Pages mirror still earns its keep now Cloudflare is canonical | Open question 1 | **Owner.** Not verifiable from inside the repository | Minutes for the owner |
| 2 | **`--dry-run` for `sync_storage_to_database.py`** | Open question 24 | Nobody | Small |
| 3 | **V2.6 curated content:** the zoop evergreen replacement (11 replacements, 1 removal) and the Cohort A expansion (7 strategies) | V2.6, open question 13, unchecked box | **Owner.** Held for a dedicated session by ruling, 2026-09-08 | Large, and it decays |
| 4 | **V2.2 item B, walk-forward validation** | Item B, open question 6 | Nobody | Large |
| 5 | **Curated metrics diverge from the same symphonies' database rows** | Open question 14, Deferred "Option B" | Nobody, but it is a design decision | Medium |
| 6 | **State each count in exactly one place** and cross-reference it | Open question 20 | Nobody | Medium |
| 7 | **Document the three tool pages' inline stylesheets**, roughly 250 lines covering a third of the interface | Open question 9 | Nobody | Small |
| 8 | **Cross-link curated strategies and the full database** both ways | Section 14, decided 2026-07-13, never built | Nobody | Medium |
| 9 | **V2.3 community signals:** external Google Form, curator notes, related strategies | V2.3 | Nobody | Medium |
| 10 | **V2.4 Tier 3** | V2.4 | **Hard-blocked.** Only 16.7% of symphonies hold exclusively covered tickers | Blocked |
| 11 | **V4.0, five external forks** | V4.0 | Ideation only, by its own rule not to start until V2.x is well underway | Large |

**Recorded but requiring no action:** open questions 7 (a duplicated formula to watch for), 15
(Composer's rate limit behaviour), 16 (the 255-target cap, which cannot bind at 72 tickers), 17
(browser heap ceilings), 18 (the `dedupe_symphonies.py` tiebreak, whose wanted fix needs an API
field Composer does not expose) and 19 (two AI-facing conventions that are easy to break silently).
These are facts kept so they are not rediscovered as mysteries, not work.

### The recommended sequence, and the reasoning

**The single most useful observation is that items 3 and 4 do not compete for the same resource.**
V2.6 is large but is bottlenecked on owner judgement about which strategies earn a page and what
each one says. Item B is large but is almost entirely implementation against a finished mockup.
Treating them as one queue means the site's biggest product-integrity item waits on calendar time
that has nothing to do with it. **Schedule V2.6 as sessions; use solo time for item B.**

**1. The owner's GitHub Pages check (item 1), first, because it is minutes and it may delete a whole
class of future problem.** v1.79.2 had to update *two* exclusion lists, `.assetsignore` for wrangler
and an `rsync --exclude` list for Pages, which are separate mechanisms that neither read each other
nor stay in step on their own; `symphony_scores.json` had already drifted between them. If the Pages
mirror no longer earns its keep, retiring it removes that duplication permanently rather than
documenting around it. If it stays, the answer to open question 1 at least makes the boundary real
instead of aspirational.

**2. The `--dry-run` flag (item 2), because it is small and the incident already happened twice.**
`sync_storage_to_database.py` has twice been run expecting a report and produced a roughly
1,000-row import instead, on 2026-07-15 and 2026-08-24. Both were reverted and neither was
committed, so the cost so far has been time rather than data. **Carry the caveat already recorded in
open question 24 into the implementation:** promotion is an approval decision rather than a sync, so
a dry-run makes the wrong operation safer without making it the right operation. It is worth doing
anyway, and it is worth not mistaking for a fix.

**3. Book V2.6 (item 3) as dedicated sessions, starting soon, because it is the only item here that
gets worse while it waits.** Open question 13 states the decay directly: the curated set's headline
metrics go staler the longer the eleven replacements wait, and the replacement IDs have been
confirmed and in the database since 2026-07-15. Everything else on this list is stable if ignored.

**4. V2.2 item B, walk-forward validation (item 4), as the main solo build.** It is the only Miner
test that can **fail** a rule rather than caveat it. A and C both describe a result; neither can
reject one, because every day the Miner scores is in sample by construction. `_wf-mockup.html` is a
finished mockup with nothing behind it and is the only artifact describing what the panel should
look like. Completing it closes V2.2 honestly rather than by redefinition.

**5. Then the documentation and consistency work (items 5, 6, 7)**, which is where the value drops
off but does not vanish. Item 5 is the one a visitor can actually see: the same symphony can show
two slightly different numbers on two pages.

**6. Items 8 and 9 are product growth** and should be sequenced on what the site needs next rather
than on this list's order. Item 10 stays blocked and item 11 stays ideation.

### In progress: the visual rebrand (added 2026-09-09)

**Owner-directed, three approved workstreams, one shipped.** Not in the table above because it was
commissioned after that table was written; it is recorded here so the section stays a complete view.

| Part | State | Note |
|---|---|---|
| 1. Design tokens | **Shipped v1.82.0** | Base lifted to Visual Studio dark range; every text/surface pair re-derived and measured |
| 2. Left rail on content pages only | **REVERSED by the owner 2026-09-09, will not be built** | The owner prefers the existing top nav. Superseded before any code was written. The rail's job, seeing the whole structure at once and jumping into it, is done instead by `.wiki-jump`, an in-page anchor strip that scrolls with the page and adds no second column |
| 3. Wiki-style content pages | **In progress.** `glossary.html` listing shipped v1.83.0 | Owner ruling: the homepage keeps its pitch structure and CTAs, which direct into wiki-style content pages |

**On whether anything should replace the rail: deliberately undecided.** The owner's ruling was to
build the content pages with the top nav alone and judge afterwards whether anything is genuinely
hard to find. If a per-page contents sidebar is ever added it will be because a real page proved it
was needed, not because a template had one. `.wiki-jump` exists to make that test fair rather than to
pre-empt it.

**Remaining in part 3:** the glossary *detail* view (`glossary.html?slug=`), `about.html`, and a
decision on `strategies.html`. The recommendation on `strategies.html` is to **keep its cards**: they
carry ARR, Max Drawdown and Sharpe per entry, which is real scannable data rather than chrome, and a
plain row list would lose it. That is the opposite of the glossary's problem and should not get the
same fix.

**The owner's verdict on part 1's first attempt is the useful record here.** That attempt improved
every measured number and the owner, looking at it, could not see any difference. The diagnosis was
that it raised borders past the visibility threshold but left surfaces at 1.10 separation, and
surfaces are most of the page. The second attempt targeted an **external reference the owner named**,
Visual Studio's dark theme, rather than an internal threshold, and was approved from three rendered
candidates.

**The honest limit of part 1: it is a correction, not the rebrand.** Density and structure are what
the owner is actually reacting to, and those are parts 2 and 3.

### What this section deliberately does not do

It does not re-rank the Explicitly Deferred table. Each row there was considered and set aside for a
stated reason, several of them by owner decision, and quietly promoting one into a work queue is how
a declined item becomes a surprise. It also does not assign dates. **The honest limit of this
ordering is that it is an argument about sequence, not a schedule, and the two items at the top of
it are both bottlenecked on the owner rather than on effort.**

---

## Brand Identity

**Opened 2026-09-28.** A complete logo system for Composer Atlas, commissioned because the project
has a fully specified colour and type system and **no owned mark**: the identity is currently a
`🗺️` emoji in a `<text>` element, which renders as a different drawing on every operating system.

**Scope, fixed at commission.** This work lives in `brand/` and in the two `## Brand Identity`
sections of this file and `docs/DESIGN.md`. **It does not change the site.** The favicon is not
relinked, the nav mark is not replaced, and `css/main.css` is not touched. Adoption is a separate
decision the owner takes after seeing the presentation.

**Where the build tooling lives, and why it breaks a rule on purpose.** Section 10 requires every
Python script to sit in `scripts/` and use the standard library only. The brand asset generators sit in
`brand/build/` instead and use Pillow and fontTools. Both departures are deliberate: the rule exists so
the deploy stays dependency-free and the repository root stays clean, and a generator that runs once on
a maintainer's machine to produce committed PNGs is neither in the deploy path nor in the root. Nothing
in CI, in `deploy.yml`, or at serve time imports them.

---

### Brand Brief

Settled with the owner on 2026-09-28. The three fields the documents could not answer were put to
the owner directly and are marked as rulings.

| Field | Value |
|---|---|
| **Brand name** | Composer Atlas |
| **Core value** | **Mapped territory.** Thousands of strategies charted and navigable. **Owner ruling.** |
| **Audience** | Primary: self-directed retail investors already using Composer, who want to understand a strategy before cloning it. Secondary: systematic-investing learners who know what a moving average is but have not built a strategy. Tertiary: quant-curious beginners who do not yet have the vocabulary. From Section 2 |
| **Idea the mark represents** | An atlas of a territory that is real, large and previously uncharted: an automated strategy is legible before money is committed to it. The press release states the specific promise better than the tagline does: *the drawdown printed next to the return rather than beneath it* |
| **Industry to analyse** | Retail systematic-investing research and tooling. Adjacent: investment screeners, portfolio backtesters, financial data terminals, and equity research publishers |
| **Colour constraints** | **`--color-green` `#00e676` is fixed, and so is the dark base `#16191f`. Owner ruling.** The palette was rebuilt at v1.82.0 with every step solved for a measured contrast ratio, three weeks before this work opened, and reopening it would mean redoing that. See `docs/DESIGN.md` Section 2 |
| **Font constraints** | The site runs Inter and JetBrains Mono from Google Fonts. The mono is a brand signal in its own right, since it carries every number on the site. A wordmark may use a third face if it earns its place; it must be open-license and it must sit beside Inter without conflict |
| **Existing brand** | See below. It exists, and it is thin enough that concept D has real room |
| **References** | **None. Owner ruling.** Work from the brief and the competitive analysis alone |

**The existing brand, summarised honestly.**

| Asset | State |
|---|---|
| Logo | **A `🗺️` emoji.** `favicon.svg` is a 32x32 viewBox containing one `<text>` element at `font-size: 28`. The nav uses the same glyph with a font stack of `'Segoe UI Emoji', 'Apple Color Emoji', 'Noto Color Emoji'`, so the mark is whichever drawing the visitor's operating system ships. There is no owned artwork of any kind |
| Wordmark | "Composer Atlas" in Inter, beside the emoji, **hidden below 480px**. So on a phone the entire brand is a system emoji |
| Palette | Complete and measured. Base `#16191f`, surfaces `#2c3038` and `#373c46`, text `#e9edf2` / `#d2d8df` / `#b8bec6`, accents green `#00e676`, pink `#ff82ac`, blue `#68afff`, yellow `#f5c518`, purple `#b39dff` |
| Type | Inter 400/500/600/700 and JetBrains Mono 400/500/700 |
| Style rules | Dark mode only, and a light mode is a standing non-goal. **Colour is semantic and never decorative:** green means a positive value or a primary action, pink means a negative one, blue means interactive, yellow means caution, purple is reserved for momentum. Radii 4 / 8 / 12. Motion capped at 0.2s, no entrance or scroll animation |
| Voice | Plain English, measured, unafraid of a bad number. Em-dashes are prohibited project-wide, and so is `--` as punctuation |

**The one constraint the palette puts on the logo, stated because it is easy to miss.**
`docs/DESIGN.md` Section 2 says green is used **exclusively** for positive values and primary calls
to action, never decoratively. A logo is neither. The resolution taken here is that the mark uses
green as **identity** rather than as data, which is a third role the rule did not anticipate, and that
this is recorded as an addition to the rule rather than an exception to it. A logo that borrowed the
green while the rest of the page used it to mean "up" would be the failure case; the mark therefore
never pairs green with an arrow, a rising line, or anything else that reads as a value.

**The risk the owner accepted in choosing this core value.** "Mapped territory" was presented as the
most literal of the four options and the easiest to make generic, and was chosen anyway. That puts the
whole weight of differentiation on the cliché list below: the obvious executions of "map" are pins,
compass roses, globes, folded paper and contour lines, and every one of them is either a competitor
habit or a stock-icon default. **The brief is therefore only satisfiable by cartographic vocabulary
that is real but unused**, which is what Phase 3 goes looking for.

---

### Competitive Analysis

**Method, stated so it can be discounted.** Eight brands. Positioning and current corporate status
were verified by web search on 2026-09-28, and one material fact changed the picture (below). **The
visual reads are from my own knowledge of these brands rather than from a rendered screenshot of each
one**, because the fetch tool returns markdown and cannot show a logo. Treat the shape and colour
observations as a designer's recollection, accurate in the aggregate and worth re-checking before any
claim is made publicly.

**The finding that reshapes the analysis: Composer is no longer independent.** SoFi acquired Composer
in June 2026 for roughly $70.1 million, and the platform now trades as **"Composer by SoFi"**. This
document and the README still describe Composer Technologies, Inc. as the counterparty. Three
consequences for the brand:

1. **Composer's own visual identity will drift toward SoFi's**, which is a large consumer-fintech
   house style: saturated blue, rounded geometric sans, friendly gradients. Whatever Composer Atlas
   does, it must not read as a SoFi sub-brand, because that would imply exactly the affiliation
   Tenet 7 denies.
2. **An independent reference is worth more, not less, after an acquisition.** A platform owned by a
   lender has commercial reasons to present strategies favourably. A site whose entire proposition is
   the drawdown next to the return now has a sharper reason to exist, and the identity should feel
   institutional enough to carry that.
3. **It is a live documentation discrepancy**, recorded here and left for Section 24 rather than fixed
   inside a brand commit.

| Brand | What it is | Visual language, as recalled |
|---|---|---|
| **Composer by SoFi** | The platform itself. Build and automate strategies in plain language | Was a clean startup identity; now carries SoFi endorsement. Expect SoFi blue and a rounded geometric sans |
| **Allocate Smartly** | The closest analogue in existence: tracks published tactical asset allocation strategies and lets members combine them | Utilitarian and data-first. Blue, a plain sans, effectively no symbol. Credible, and visually almost absent |
| **QuantConnect** | Open-source cloud algorithmic trading platform, founded 2011 | Developer-platform look. Dark UI, a geometric symbol, technical sans. The closest competitor in *tone* to a dark reference site |
| **Portfolio Visualizer** | Backtesting, Monte Carlo, tactical allocation and optimisation tools | Almost unbranded. A plain wordmark and chart colours. Trusted precisely because it looks like a tool |
| **Finviz** | The reference screener. Dense tables and heatmaps | Deliberately plain wordmark; the *heatmap* is the real brand asset. Proof that a data view can be more recognisable than a logo |
| **Koyfin** | Modern retail terminal, charting and fundamentals | Contemporary fintech: a geometric mark, blue and teal, rounded sans, gradients |
| **Morningstar** | The incumbent independent research authority | Institutional. A serif-adjacent wordmark, a constellation-like mark, restrained palette. The credibility benchmark |
| **Seeking Alpha** | Retail equity research and commentary publisher | Editorial publisher: a strong wordmark, a Greek alpha as the mark, orange accent |

**What they share.**

- **Shape:** the upward-right diagonal in some form, whether an arrow, a rising line, a candlestick series or a bar ramp. Geometric marks built from a rounded square or a circle. Node-and-line graphs, increasingly, to signal automation or AI.
- **Colour:** blue, overwhelmingly, because blue is the finance-trust default. Teal and violet as the modern escape from blue. Green used specifically to mean gain.
- **Type:** a rounded geometric sans on the newer products (the Circular and Poppins family of shapes), a neutral grotesque on the older tools, and a serif only where the brand is claiming institutional authority.

**Clichés this logo must avoid.** Each is ruled out because it is either a competitor habit or a
stock-icon default, and several are the *obvious* reading of this brief.

| Cliché | Why it is out |
|---|---|
| **The upward-right arrow, rising line, candlestick or bar ramp** | The single most used device in the category, and it is a performance claim. A site whose first tenet is Transparency Over Hype cannot open with a picture of going up |
| **Blue as the primary** | The category default, and now specifically SoFi's territory |
| **The globe or the orbiting sphere** | The first thing anyone draws for "atlas", and it says "global markets", which this site is not about |
| **The map pin or location marker** | The second thing anyone draws for "atlas". It is a Google Maps component, not a cartographic idea |
| **The compass rose and cardinal points** | The third. Decorative antiquarianism, and it appears on every travel and navigation brand |
| **The folded or perspective-curled paper map** | The fourth, and it is what the `🗺️` emoji already is. Replacing an emoji with a drawing of the same emoji is not an identity |
| **Topographic contour lines as texture** | A 2020s trend, heavily used, and purely decorative. It would also fail the project's own rule that nothing is decorative for its own sake |
| **Node-and-line graphs** | Now reads as "AI product" rather than as a mapped structure |
| **Gradient mesh, glassmorphism, glow** | Trend-dated, and each one fails the Phase 3 test that every effect must have a job |
| **A rounded geometric sans wordmark** | Reads as consumer startup. This is a reference library, and it is competing with Morningstar for credibility, not with a neobank for warmth |
| **An `A` monogram in a rounded square** | The generic app-icon solution, and it discards the one distinctive word in the name |
| **Anything resembling Composer's or SoFi's marks** | Tenet 7. Visual similarity implies the affiliation the site explicitly denies |

**How Composer Atlas stands out while staying credible, in one sentence.**

> Composer Atlas will look like a **reference instrument rather than a growth story**: a precise,
> typographically confident identity built from the measured vocabulary of real cartography, the
> graticule, the neatline and the index cell, rather than from the arrow, the pin and the globe,
> keeping the site's existing green so the mark stays continuous with the product while reading as an
> independent library rather than as a broker or a platform.

**Why that is the credible position and not merely the contrarian one.** Two of the eight brands above
are trusted precisely because they look like instruments: Portfolio Visualizer and Finviz are close to
unbranded, and nobody mistrusts them. One, Morningstar, earns institutional authority through
restraint. The category's *decorated* end, the gradients and the rounded sans, belongs to products
selling a feeling about money. This site sells an accurate picture, so restraint is the honest
expression of the product rather than a style preference imposed on it.


---

### Deliverables Checklist

**Phases 1 to 7 complete, 2026-09-28.** Specifications for everything below are in `docs/DESIGN.md`,
Section 11. This table is the inventory; that section is the reasoning.

| # | Deliverable | State | File |
|---|---|---|---|
| 1 | Horizontal lockup | Done, 4 treatments | `brand/logo/lockup-horizontal-*.svg` |
| 2 | Compact horizontal lockup | Done, 4 treatments | `brand/logo/lockup-horizontal-compact-*.svg` |
| 3 | Stacked lockup | Done, 4 treatments | `brand/logo/lockup-stacked-*.svg` |
| 4 | Symbol only, primary | Done, 4 treatments | `brand/logo/symbol-primary-*.svg` |
| 5 | Symbol only, compact | Done, 4 treatments | `brand/logo/symbol-compact-*.svg` |
| 6 | Wordmark only | Done, 4 treatments | `brand/logo/wordmark-*.svg` |
| 7 | Monochrome black | Done | the `-black` treatment of every vector |
| 8 | Reversed white | Done | the `-white` treatment of every vector |
| 9 | Full colour | Done | the `-color` and `-color-reversed` treatments |
| 10 | `favicon.svg` with a dark-scheme variant | Done | `brand/logo/favicon.svg` |
| 11 | `favicon.ico` at 16, 32 and 48 | Done | `brand/logo/favicon.ico` |
| 12 | Favicon PNGs | Done | `brand/logo/favicon-{16,32,48}.png` |
| 13 | App icons 180, 192, 512, 1024 | Done, opaque | `brand/logo/icon-*.png` |
| 14 | Maskable 192 and 512 | Done, ink inside the central 80% | `brand/logo/maskable-*.png` |
| 15 | Merchandise single colour | Done, verified at 25mm | `brand/logo/merch-single-colour.svg` |
| 16 | Clear space and minimum size rules | Done | `docs/DESIGN.md` Section 11 |
| 17 | Brand kit | Done, 8 files | `brand/kit/` |
| 18 | Presentation and PDF | Done, 15 pages A4 landscape | `brand/presentation.html`, `brand/brand-guidelines.pdf` |
| 19 | Brand Design page | Done, **gitignored and unpublished** | `brand/brand-design.html` |

**36 files, every one judged from a rendered screenshot.** The screenshots are kept in
`brand/checks/` rather than regenerated on demand, because the point of the rule is that a specific
image was looked at and a specific fault was found in it, and a sheet that is rebuilt each time cannot
be cited later.

**Two deliverables required a decision the brief did not anticipate, both recorded in DESIGN.md.**
The compact horizontal lockup is not in the original list: it exists because the primary symbol's 32px
floor silently becomes a 288px floor for the whole lockup, and without a compact version the system
has no answer between 120px and 288px. The raster favicons are opaque rather than transparent, which
the brief did not specify either way, because a transparent favicon bakes one ink and a tab strip can


---

### Holdings Fields: What `last_market_days_holdings` Actually Is

**Settled 2026-10-14, and the answer is not what the field name suggests.**

`last_market_days_holdings` is a map of ticker to position value on the **last market day of the
backtest**, captured at that row's `refresh_date`. It carries **every asset the symphony can hold,
including the ones at `0.0`**. A zero is not padding: it means "this symphony can hold this and was
not holding it that day".

**The key set is the symphony's complete holdable universe.** This was verified against the symphony
tree from `/api/v0.1/symphonies/{id}/score`, not inferred:

| Strategy | Asset-node tickers in the tree | Holdings keys |
|---|---|---|
| zoop's Sometimes TQQQ | `SH, SOXL, TECL, TQQQ, UPRO` | identical |
| zoop's 2026 Frontrunner | `BIL, SOXL, SPXU, TQQQ, UPRO, VXX` | identical |

**Tickers used only as signals are absent, correctly.** A strategy that reads QQQ's RSI to decide
whether to buy TQQQ carries TQQQ as a key and never QQQ, because it cannot hold QQQ. There is
therefore **no field anywhere that lists a symphony's signal tickers**, and building one would mean
parsing every symphony's condition nodes.

Two screener fields read this map, and the distinction is the whole point:

| Field | Tests | `TQQQ` on the live data |
|---|---|---|
| **Currently Holding (Ticker)** | the value, `> 0` | 1,638 rows |
| **All Tickers (Held or Not)** | the key, zeros kept | 3,436 rows |

**Currently Holding is a snapshot and goes stale.** Most rows share a refresh date but a tail does
not, so it compares positions taken on different days. Use All Tickers to ask which strategies trade
a ticker; use Currently Holding to ask what is held right now.

**`active_asset_nodes` is not the universe field it sounds like.** It is keyed by node UUID with
weights (`{'e101f5ef-...': 1.0}`), not by ticker, and `export_summary.py` drops it from the summary
the site actually loads.

**A warning for the next person who checks this.** An earlier pass regexed tickers out of the
curated prose and concluded the key set was missing holdable assets, which implied a 6,817-call pull
to build a real universe field. It was wrong: the "missing" tickers were signals. **Curated prose
names signals and holdings in the same sentence and is not a schema.** One call against the
symphony tree answers this definitively.

### The Referral Page and the First-Visit Banner

**Added 2026-10-14.** `referral.html` explains Composer's referral programme and carries the owner's
code; a nav entry sits left of Azqato Invests, with a footer link and a homepage Explore card.

**The code has exactly one definition**, `REFERRAL_CODE` in `js/app.js`, rendered into every
`[data-referral-code]` element. Four surfaces show it. A literal copied into four files is one that
eventually disagrees with itself, and **this particular failure is silent**: a wrong code does not
break signup, Composer simply applies no credit, and the first sign of trouble is a bonus that never
arrives. Changing the code is a one-line edit in one file, by design.

**The banner is shown only during a visitor's first 30 minutes**, tracked with two `localStorage`
keys (`ca-ref-first`, `ca-ref-dismissed`) written on the visitor's own device. **This does not
breach the no-user-data rule**: nothing is collected, nothing is transmitted, and no account exists.
The honest limits are that it is per browser and per device, that private windows and cleared site
data read as a first visit every time, and that a visitor whose storage predates the feature never
sees it. All three are acceptable; the alternative is accounts, which are permanently ruled out.

**The copy leads with the amount, and the urgency is real rather than manufactured.** Every surface
names **$50** instead of saying "a sign-up bonus", and a CTA block carrying the code sits directly
under the disclosure so a decided reader never scrolls for it. There is deliberately **no countdown,
no "limited time" and no implied expiry**: Composer has announced no deadline, and inventing one on
a site whose whole value is being accurate about numbers is a bad trade. The hook used instead is
true and stronger: **the referral field exists only during signup and cannot be applied afterwards**,
so hesitating genuinely costs the reader the money. The page body stays reference material; the
marketing weight lives in the CTAs and in the section about the bonus.

**Disclosure is on the page, above the fold, not in a footnote.** The author is paid for signups
made with that code and the page says so before it says anything else. The page also instructs
anyone sharing a code publicly to disclose the same, which is what the FTC's endorsement guidance
expects of a material connection.

**A layout trap worth keeping.** The banner first rendered invisibly because `.nav` is
`position: fixed; top: 0`, so the first element in normal flow sits behind it. The DOM probe
reported `visible`, `display: block` and a 54px height, and every one of those was true: the element
was painted and then covered. **Moving it after the nav in the markup fixes nothing**, since a fixed
nav is out of flow entirely. Anything meant to appear below the nav belongs inside `.page`, which
already carries `padding-top: var(--nav-height)`. Geometry could not catch this. The screenshot did.

### The Colour Audit and the Two-Theme Palette

**Done 2026-10-07**, against the owner's own published **Template Interface Color Standard v1.0**
(`wireframe/standards/color/`). Measured in headless Edge across 17 page states per theme, reading
computed styles from the live DOM with every translucent layer composited down the chain.

**Result: 346 text pairs and 190 controls across both themes, zero failures.**

**What the audit found, and what it got wrong.** Two of its own first-pass findings were false and
were discarded before anything was reported: 240 "border failures" came from measuring decorative
borders on filled buttons, which are identified by their fill rather than their outline; and a focus
ring read at 1.08:1 was an artefact of `outline-style: auto`, where the browser paints its own ring
and the computed colour means nothing. A screenshot settled it. **A third artefact appeared later
and was more dangerous**: 56 light-mode failures that did not exist, caused by setting `data-theme`
from the parent frame, which does not force a style recalc inside an iframe under virtual time, so
the probe read stale values. The audit was re-run through the page's real boot script instead. **All
three would have produced confident, wrong remediation.**

**The real findings were three**, and all are fixed: text entry fields had no 3:1 boundary; the
footer's one running-text link was identified by colour alone at 1.60 against its surroundings,
where WCAG G183 wants 3.0; and 54 `rgba()` literals were hardcoded copies of token colours.

**Owner rulings, 2026-10-07, taken after being shown both sides:**

| Question | Ruling |
|---|---|
| Brand green collides with the standard's "green means success only" | **Green serves both accent and positive.** One named deviation, documented rather than designed away |
| Pink for negative values | **Adopt red.** The standard lists pink as a data colour and reserves red for danger |
| Blue for info | **Adopt teal.** Freeing blue means it can never read as both informational and clickable |
| Light mode | **Added, with dark as the default.** Sun and moon button in the nav |

See `docs/DESIGN.md` Section 2 for the role table and Section 9 for the focus ring and control
boundaries.

### The Guides Collection

**Added 2026-10-07.** `guides.html` plus `data/guides.json`, seven guides across three categories,
sharing the glossary's renderer. See `docs/DESIGN.md` Section 7 for the component and the schema.

**What it is for.** The glossary answers "what does this word mean". Nothing on the site answered
"how do I build and test well", and the gap showed: the site had a tool that measures overfitting
(`overfit.html`) and no page explaining why a reader should care.

**Where the content came from, and the ruling on attribution.** The source was a body of posts from
the Composer builder community, supplied by the owner. **Owner ruling, 2026-10-07: write every guide
in the site's own voice with no inline credits, and carry one acknowledgement line on the Guides
index.** The ruling was taken after being shown the argument on both sides. The reasoning recorded
for the future: the general principles in the source material are common knowledge that nobody owns,
inline credits would break the prose for claims that are not really anyone's, and a single quiet
acknowledgement removes the one scenario that could sting, which is a builder recognising a specific
technique on a site whose entire asset is being trusted.

**What was deliberately NOT ingested**, because this matters more than what was:

| Source material | Why it was left out |
|---|---|
| Two full Ray Dalio video transcripts | Verbatim copyrighted text, and macroeconomic history rather than anything a reader can apply to a symphony |
| A full podcast transcript (Tim Masters, Better System Trader) | Verbatim copyrighted text. **The ideas were used**, rewritten in site voice, and they became the strongest guide in the collection |
| A 2022 K-1 ETF ticker list | `data/k1.json` already holds 187 tickers refreshed from etfdb.com. The source was a self-described rough draft from 2022 built off a list its own author called incomplete. **Our data is strictly better**, so ingesting it would have been a downgrade |
| A tip about pasting Composer code into the AI window to expand branches | Dead. The author annotated his own post to say Composer shipped the feature natively |
| A bank CD estate-planning loophole | Off topic and distasteful |
| Composer blog links on momentum | Links rather than content. Candidate for a reading list, not a guide |

**Beta slippage, the mean reversion rubber band and leverage decay were also left out of the guides**,
not because they are weak but because `data/glossary.json` already covers them properly under
`volatility-decay`, `leveraged-etfs` and `mean-reversion`, each with a "building this in Composer"
section. Duplicating them would have created two places to maintain one explanation.

**The wash sale guide shipped the same day**, as the eighth guide, and introduced the optional
`disclaimer` field. It is the only guide that uses it: a page about tax mechanics needs a notice
the reader meets *before* the content, not the standard footer line after it.

**Eight further guides are proposed and prioritised in Section 14, "Guides Content Roadmap"**,
along with the standing rule that the collection is capped at roughly a dozen. The highest-priority
item is a year-end wash sale guide, requested by the owner, whose own technique and the five rule
mechanics the guide must get right are recorded there.

**Open item: the sitemap does not list `glossary.html?slug=` pages.** It now lists
`guides.html?slug=` pages, because `collect_guides()` was added alongside the collection. The 27
glossary detail pages have never been in it. That is a real gap and a separate change, flagged in
`scripts/build_sitemap.py` where someone will meet it.

### How the Brand Work Is Deployed, Which Is To Say It Is Not

**`brand/` is committed and served by neither host.** That was a decision, and without it the
commission's "do not change the site" rule would have been broken by the act of committing the work.

**That rule was superseded by the owner on 2026-09-28, narrowly.** The instruction was to apply the
brand to the site's branding colours and update `docs/DESIGN.md` and the CSS. Acting on it revealed
that the colour part was already done and could not be done again: `brand/kit/tokens.css` is
*generated from* the `:root` block of `css/main.css`, and a diff of all thirteen base colour tokens
returns **zero differences**, because the palette was fixed by owner ruling at the Phase 1 gate and
the brand work introduced no new colour. **So the adoption added meaning, not pigment.**
`css/main.css` gained `--color-brand` (an alias of `--color-green`, distinguishing identity from a
positive value) and `--font-brand` (declared, and deliberately not loaded). Nothing in `brand/`
became served, and the table below still holds in full. **The mark remains unadopted**: the favicon
and nav mark are still the map emoji, and moving them would mean taking files out of the exclusions
below, which is a separate change.

`wrangler.jsonc` sets `assets.directory` to `"."`, so **anything not listed in `.assetsignore` is
published**. A `brand/` directory holding 104 files and 4.6 MB, including a 539 KB PDF and 2.5 MB of
contact sheets that exist only as evidence for a design decision, would have become 104 public URLs on
composeratlas.com the moment it was pushed.

| File | Entry | Governs |
|---|---|---|
| `.assetsignore` | `brand/` | Cloudflare Pages, which is the canonical host |
| `.github/workflows/deploy.yml` | `--exclude='brand'` | The GitHub Pages mirror |
| `.gitignore` | `brand/brand-design.html` | Git itself. That one file is not even committed |

**Both host exclusions were added in the same change on purpose.** Section 24 records that
`.assetsignore` and the rsync excludes in `deploy.yml` do not read each other and have drifted before,
most recently over `data/symphony_scores.json`. Changing one and not the other is how that drift
starts, and the cost is a file that is private on one host and public on the other.

**This is not `.gitignore`.** Everything under `brand/` except the showcase page stays committed, on
disk and in the history. It is versioned and backed up; it is simply not served.

---

### The Brand Design Page, and Why It Is Not Published

**`brand/brand-design.html` exists, and it is deliberately not part of the site.**

The prompt for this work asked for a choice between a gated page and an offline one, decided from the
project rather than from preference. **Offline is the only honest answer here.** Composer Atlas is a
public static site on Cloudflare Pages with no accounts, no sessions and no server that could check
one, and Tenet 3 rules out user accounts permanently. A "gated" page on this stack could only ever be
an obscure URL, and an obscure URL is not a gate, it is a page you have lost track of.

| | |
|---|---|
| **Where it is** | `brand/brand-design.html`, built by `brand/build/build_showcase.py` |
| **How to open it** | From the file system. Double-click it, or open the local path in a browser |
| **Is it in git?** | **No. It is in `.gitignore`**, under a comment saying why |
| **Is it linked?** | No. Nothing on the site references it, and it carries `noindex,nofollow` as a second line of defence in case it is ever copied somewhere served |
| **Does it deploy?** | No. It cannot: an ignored file is never committed, so neither Cloudflare nor the Pages mirror ever sees it |

**What it is for, and why it is not the presentation.** `brand/presentation.html` argues the case and
prints to a PDF; it is the document you send. The Brand Design page is the one you poke at: a size
slider that runs the mark from 12px to 220px and switches from the primary to the compact mark at the
real threshold, a light and dark ground toggle, the four colour treatments side by side, and
click-to-copy tokens. **It shows the responsive substitution happening rather than describing it**,
which is the one claim in this system that is genuinely hard to believe from a written table.

**The consequence of ignoring it, stated plainly.** The file is on the maintainer's disk and nowhere
else. It is not backed up by the repository, and a fresh clone will not have it. That is recoverable,
because `build_showcase.py` **is** committed and regenerates the page in full, and it is the reason
the generator is the deliverable rather than the HTML.

be either colour.

