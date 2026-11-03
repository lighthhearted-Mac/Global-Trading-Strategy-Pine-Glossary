# Composer Atlas

Composer Atlas is a free, independent reference library for people who build and run automated
investing strategies on Composer.trade. It explains how real strategies work in plain English,
publishes their backtested numbers without cherry-picking, and gives you tools to search, compare
and build your own.

## Live Site

**https://composeratlas.com**

## What the Site Offers

**A curated strategy library.** Every featured symphony gets its own page with a plain-English
breakdown of its logic, the exact signals it watches, an honest risk profile, and a full metrics
table covering returns, drawdown, Sharpe, Calmar and monthly distribution. Each page links straight
to the symphony on Composer.trade so you can clone it yourself.

**A concept glossary.** Long-form explainers for the ideas the strategies are built from: RSI,
moving averages, momentum, VIX tiers, leveraged and inverse ETFs, managed futures, mean reversion,
volatility decay, and the risk metrics used to judge any of it. Every strategy page cross-links to
the concepts it uses, and every concept links back to the strategies that use it.

**A community strategy database.** Thousands of Composer symphonies gathered from across the
community, in one searchable place, with three ways to work through it:

- **All Strategies**, a dense sortable table of the whole set.
- **Leaderboard**, which scores every eligible symphony against a published twenty-metric model and
  ranks it into tiers. The full methodology is on the page, and each score breaks down on click.
- **Screener**, a bucketed filter grid for narrowing thousands of rows to the handful worth reading.

**Tools that build things, and one that argues with you.** A **Signal Miner** that brute-forces
millions of "if this, then hold that" rules against real price history and hands you the survivors as
pasteable Composer JSON. An **Overfit Check** that takes any symphony and scores it from 0 to 100
against the thousands whose logic has gone a year untouched, so a strategy that only looks good in a
backtest has somewhere to be caught. An **ETF Cloner** that turns any ETF's holdings into a Composer
symphony. A **Converter** that turns any symphony URL into clean, readable JSON. A **Node Counter**
for checking a symphony against Composer's own complexity limits, and a **K-1 Lookup** that answers
whether holding a given ticker means a Schedule K-1 instead of a 1099. Plus a **live RSI page**
tracking the signal universe the popular Frontrunner-style strategies watch, and an **RSI
Backtester** that tests any RSI rule, or a cascade of them, against real price history.

Everything runs in your browser. Nothing you type, select or mine is sent anywhere.

## Who It Is For

Self-directed retail investors who already use Composer.trade, or are considering it, and want to
understand what a strategy actually does before trusting money to it. It assumes you are curious
and willing to read, not that you have a finance background: the glossary exists precisely so the
strategy pages can use real terms without stranding anyone.

It is also useful to anyone studying systematic investing generally. The strategies are real, the
metrics come from live backtests rather than illustrations, and the drawdowns are printed next to
the returns rather than buried.

## What It Is Not

Composer Atlas is not affiliated with Composer.trade, and it is not financial advice. Nothing here
is a recommendation to buy or hold anything. Past backtest performance does not predict future
results, and several of the strategies covered use leveraged funds that can lose value very quickly.

There are no accounts and no sign-up, because the site collects no user data at all and never will.
It runs no ads and sells nothing. If it is useful to you, there is a voluntary donation link.

## Current Status

Live and actively maintained. The curated library, the glossary, the full community database with
its leaderboard and screener, and all the tools are built and public. Strategy metrics and the
community database refresh on an automated schedule, and the RSI page refreshes several times each
weekday.

Work in progress is mostly depth rather than breadth: refreshing the curated set to newer versions
of several strategies, cross-linking the curated pages to their rows in the community database, and
adding robustness testing to the Signal Miner so a mined rule can be judged on whether it survives
having its parameters nudged, not just on the best number it found.

## Where to Learn More

Full documentation lives in [`/docs`](docs/):

| Document | What is in it |
|---|---|
| [`docs/PRD.md`](docs/PRD.md) | The master reference: product requirements, tenets, architecture, runbook, data schemas, API notes, roadmap, metrics, conventions, security, and working practice |
| [`docs/DESIGN.md`](docs/DESIGN.md) | The design system: colour palette, typography, spacing, breakpoints, component patterns, accessibility, and motion |
| [`docs/PATCHNOTES.md`](docs/PATCHNOTES.md) | The changelog, every release since launch |

## Licence

**All rights reserved. No licence is granted.** This repository is source-available, not open
source: it is published so it can be read, and publishing it grants nothing. See
[`LICENSE.md`](LICENSE.md), which also records that not enforcing a right does not waive it, and that the
Composer-derived and market data in `data/` is not the copyright holder's to license.

**One permission is granted up front: referencing.** Search engines, AI assistants and answer
engines may crawl, index, quote, summarise, link to and cite this site freely, with attribution
requested. That is deliberate and encouraged.

Everything else is available on request and is often given. Ask by opening an
[issue](https://github.com/Azqato/composer/issues). Requests and answers are public there on
purpose, so the record of what has been permitted is visible.

Built by [Azqato](https://azqato.com).
