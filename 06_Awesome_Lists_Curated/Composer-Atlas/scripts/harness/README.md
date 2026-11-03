# Signal Miner headless harnesses

The Signal Miner has no build step and no JS runtime available in this
environment, so there is no `npm test`. What exists instead is a set of
drivers that run the real page end to end in **headless Microsoft Edge** and
report from inside it. They are the reason the numbers in `docs/PRD.md` are
measured rather than asserted.

Run them from the repository root:

```
python scripts/run_harness.py verify      # spec lockstep + dual-path equality
python scripts/run_harness.py live        # end-to-end run, window, rendering
python scripts/run_harness.py settings    # persistence and the Default button
python scripts/run_harness.py plateau     # parameter plateau scoring
python scripts/run_harness.py inertness   # cross-ticker operand degeneracy
python scripts/run_harness.py memory      # peak heap and throughput
python scripts/run_harness.py all         # the four gates
```

`verify`, `live`, `settings` and `plateau` gate any change to
`signal-miner.html`. The other two are measurement tools: run them when a
figure in the PRD needs re-establishing, not on every edit.

## Use Edge, never Chrome

Every harness launches Edge deliberately, so the owner's Chrome session stays
untouched. `EDGE_PATH` overrides the executable if it lives somewhere unusual.

## The traps

All four are encoded once in `_edge.py`. They are documented here because each
one cost real time to find and every one of them fails *silently* or with a
misleading error.

**1. The page is an IIFE.** `signal-miner.html` wraps its whole script in
`(function () { ... })();`. Nothing inside is reachable from an injected
sibling `<script>`, and the symptom is `WINDOWS is not defined`. The fix is to
splice a `window.__t = { ... }` hook in before the trailing `})();` in the
test copy of the page.

**2. Bind by getter, not by value.** `targets`, `compares`, `sigCache`, `PD`,
`N` and `DATES` are all reassigned after load. A hook that captures the value
at parse time holds a stale reference forever. This one is nasty because it
does not throw: two harness cases silently run the same selection and report
identical numbers, which reads as a suspiciously stable result rather than a
bug. Always use `get x() { return x; }`.

**3. The CPU throttle feeds back on itself under virtual time.** Pass 1 sleeps
`busy * FACTOR` between batches, which interacts badly with
`--virtual-time-budget`; a run can crawl or appear to hang. Neutralise it in
the **test copy only** by forcing `FACTOR` to 0 at `cpu === 'max'`, and do it
identically on both sides of any A/B comparison.

**4. Read the dumped DOM as bytes.** `--dump-dom` emits UTF-8. Letting Python
decode it as the console codepage dies on the first non-ASCII byte, and the
page uses a middot as a separator, so this happens immediately. Take
`subprocess` stdout as bytes and `.decode('utf-8', 'replace')`.

## Trap 5: wall-clock deadlines are meaningless inside a driver

Under `--virtual-time-budget` the page clock races ahead whenever the
renderer is idle, so a `Date.now()` deadline inside a driver expires long
before a long compute has finished. The first version of the memory harness
reported "timeout" on all three cases at an 82 MB peak, which is Pass 1 not
having meaningfully started. It reads as a hang or a crash, not as a broken
timeout. Count **polls**, not milliseconds, and let the `subprocess` timeout
in `run_harness.py` be the real guard.

## Trap 6: the browser profile

`_edge.py` gives every invocation a **fresh** `--user-data-dir` under the
system temp directory, and that is deliberate. A single shared profile fails
in two directions, and both look like a hang or a crash in the page:

- a killed run leaves `msedge.exe` holding the profile lock, so the next run
  blocks on the lock rather than on anything the harness is doing;
- deleting the directory races with Edge's shutdown, which still holds file
  handles for a moment. The result is a half-deleted profile, and the driver
  then throws before it can report, surfacing as `NO HARNESS OUTPUT`.

Cleanup is best effort and some leftovers stay in temp. That is the right
trade. Pass an explicit `profile=` name only when a harness genuinely needs
state to survive between two Edge invocations, which today means a
`localStorage` round trip and nothing else.

If something still looks stuck, check for stray `msedge.exe` processes:
`taskkill /F /IM msedge.exe`.

## Traps 7 and 8, cheaper but just as silent

`window.confirm` **auto-dismisses** under `--headless=new`, so a run that
trips the large-batch confirm silently does nothing. `_edge.py` stubs it to
return true.

And when a driver asserts on rendered output: `renderResults()` is debounced
through `requestRender()`, so `#sl-results-panel` becomes visible *before*
`#sl-body` is filled. Wait on the row count, not on the panel, or the check is
an intermittent race.

## Traps 9 and 10: why timing lives outside this directory

**Trap 9: under virtual time, the page clock is not a clock.** This is the
trap that cost the most, because it fails by producing plausible numbers.
`--virtual-time-budget` is what makes `--dump-dom` wait for asynchronous work
instead of dumping at the load event, and every harness here depends on it. The
price is that the page clock is *paused* during synchronous compute and
*fast-forwarded* through idle gaps. Measured, with one driver and two run sizes:

| Run | Real duration | `performance.now()` elapsed | Summed `busyMs` |
|---|---|---|---|
| 4 tickers | 3.68s | 1,154 ms | 63 ms |
| 8 tickers | 9.44s | 4,095,136 ms | 70 ms |

Neither column measures anything, and the fast-forwarding is not even monotone
in the work. At 16 tickers the accumulated virtual time crossed the 2e9 ms
budget, Edge shut the browser down mid-run, and the harness reported
`NO HARNESS OUTPUT` with no other symptom. The budget cannot simply be raised:
2e9 is already close to the largest value the flag accepts.

A wrong throughput figure derived this way (4.5 ns per spec-target-day, five
times too fast) reached production in code comments, the patch notes and the
PRD before it was caught. **Never quote a duration measured inside this rig.**
Timing lives in `scripts/measure_throughput.py`, which runs Edge without
virtual time and without `--dump-dom`, and reads results off stderr through
`console.info` so the parent process can timestamp them.

**Trap 10: a real-time headless run needs four more flags.** Dropping virtual
time introduces two problems that virtual time was hiding:

- A headless tab counts as **hidden**, and a hidden tab has its timers clamped
  to roughly one per second. Pass 1 yields through `setTimeout` between
  batches, so without `--disable-background-timer-throttling`,
  `--disable-backgrounding-occluded-windows` and
  `--disable-renderer-backgrounding` a run does about one batch per second and
  what you measure is the clamp.
- **A fresh `--user-data-dir` is not a clean browser.** Edge still loads the
  machine's extensions, which log continuously into the same stderr channel the
  result is being read from, and open network tabs of their own. Pass
  `--disable-extensions --no-first-run --no-default-browser-check`.

## The two-invocation pattern (`settings`)

Most harnesses run once on a throwaway profile. `settings` cannot: it tests
whether the section-3 controls survive a refresh, and a single page load has no
way to observe one. So `run_harness.py` drives `settings.js` **twice** over one
shared `--user-data-dir`, selecting the half to run with `config={'phase': N}`:

- it **deletes the profile directory first**, so phase 1 is genuinely a browser
  that has never seen the page and the shipped defaults can be asserted;
- phase 1 checks the HTML attributes against `DEFAULT_SETTINGS`, changes every
  control, and lets the change listeners persist;
- phase 2 is a **new browser process** over the same profile. It asserts the
  controls came back changed, clicks Default, and asserts everything reset and
  wrote through to storage.

Two things to know if you write another one. Reloading from inside the driver
is not a substitute: `window.__cfg` is re-injected on every load, so a
self-reload loops forever. And a two-phase harness must pass **both** phases, so
`run_harness.py` counts `ALL CHECKS PASSED` twice rather than looking for it
once.

`localStorage` works on `file://` in headless Edge, and the test copy is written
to the same path every time, so both invocations share an origin.

**Trap 11: a shared profile name must not be a fixed one.** The profile the two
phases share is named `settings-<pid>`, not `settings`. A killed or backgrounded
harness leaves an `msedge.exe` holding its profile directory, `shutil.rmtree`
then fails silently under `ignore_errors=True`, and the next run's Edge exits
against the locked directory in about a tenth of a second. What you see is
`NO HARNESS OUTPUT` on both phases with no JavaScript error anywhere, which
reads exactly like a driver that hangs, and costs an hour of instrumenting a
driver that was fine. A per-invocation name cannot collide with a leftover, and
`run_settings` now says so explicitly if the directory survives the delete.

If you do hit a locked profile, list the offenders before killing anything:

```powershell
Get-CimInstance Win32_Process -Filter "Name='msedge.exe'" |
  Where-Object { $_.CommandLine -like '*composer-harness*' }
```

Filter on `composer-harness` rather than killing `msedge.exe` wholesale, so the
browser session you are actually using is left alone.

## Trap 13: a second launch over a populated profile hangs

`--disable-sync --disable-component-update`, in `_edge.py`'s `argv`. Without
them the **second** Edge invocation of a two-phase harness hangs until the
wall-clock timeout: no JavaScript error, no partial output, just
`TimeoutExpired` after 900 seconds.

What makes this one expensive is that **phase 1 always passes**. An empty
profile has nothing to reconcile, so the first launch is clean and the second
is not, which reads as a bug in whatever the page changed since the last green
run. It was found while trying to ship an unrelated feature and was reproduced
against an **unmodified** page and an unmodified hook, which is the only thing
that ruled the feature out.

Measured 2026-09-03: `settings` phase 2 hung in **2 of 3** baseline runs and
passed **6 of 6** with the flags. Either flag alone was enough in testing; both
are passed because the failure is intermittent and neither costs anything.

The mechanism is trap 9 wearing a different hat. Edge schedules sync and
component-update work at startup once a profile has state, and under
`--virtual-time-budget` the tab never reaches the idle point that `--dump-dom`
waits for.

**If a harness ever hangs with no output, check this before reading a single
line of page code.** The intermittency is the trap: a green run proves nothing.

## Trap 12: a default-settings sample can be a sample of one

`plateau` asserts across the rows on screen, and its first version reported
100 rows of which **one** was a single signal. At the shipped pairing setting
the top 100 by Calmar is 99 combined AND rows, so every single-row assertion
was resting on one row and proving very little, while still printing a
comforting `ok`. The driver now turns pairing off for the main pass and back on
for the combined-row case, and asserts a **minimum sample size** rather than
merely a non-zero one.

The general lesson: when a driver asserts over "whatever is on screen", assert
how much is on screen too. A shipped default that makes the interesting
population rare is not a bug in the page and it will not announce itself.

**And there is a second half to this trap that cost a shipped bug.** The same
sentence, "100 rows, 1 single, 99 combined", was read as a statement about the
*test* when it was equally a statement about the *product*: the feature scored
singles only, so on the default view it rendered a wall of dashes. Turning
pairing off in the driver made the test honest and made the product bug
invisible at the same time.

So a driver that changes a setting to get a better sample owes a second pass at
the **shipped default**, asserting what a visitor who touches nothing actually
sees. `plateau` now does exactly that, and the assertion is one line: zero empty
cells. Adjusting settings for a good sample is right; adjusting settings and
never looking back at the default is how a feature ships invisible.

## What `plateau` proves

The plateau columns are pure diagnosis. Nothing downstream reads them, so a
wrong number has no second symptom and could sit there for months. The driver
therefore **recomputes everything independently** rather than re-reading what
the page decided:

- **every row on screen is scored at the shipped pairing default, combined AND
  rows included, and no cell renders empty.** This is a regression test with a
  history: see trap 12;
- a row perturbed by **zero** steps reproduces the metric the results table
  already holds for it. If that drifts, every neighbour around it is being
  compared against a different backtest than the row itself;
- each plateau endpoint really scores inside the band, and the step just past
  it really does not, checked with the driver's own boolean pass and backtest
  rather than with `plateauScore`. For a combined row the driver rebuilds the
  other condition's boolean array itself and re-ANDs, so it is not borrowing the
  page's idea of what the partner is either;
- the neighbourhood median reproduces exactly, over the same pool;
- no neighbour violates the canonical `p1 < p2` rule `pushCmpSpecs` enforces on
  same-ticker comparisons, so the ring never scores a spec the run itself would
  refuse to build;
- window neighbours come from the run's **active** grid. The driver runs at a
  min period of 12 specifically so that 5, 7 and 10 are absent and this check
  cannot pass by accident;
- the ring is proved to **evaluate rather than look up**: it scores specs at
  the extreme ends of a level grid, which never fire and therefore have a total
  of exactly zero, and which the Pass 1 store consequently never kept.

It also prints a plateau-width distribution. That is a measurement, not an
assertion, and it is there because the roadmap entry for this item says to look
at what real runs produce before deciding whether to re-rank on the
neighbourhood or which band widths to mine.

## Writing a new harness

Drop a `.js` driver in this directory, register it in `run_harness.py`, and
have it append its output to a `<pre id="HARNESS">` element. Print
`ALL CHECKS PASSED` when every assertion holds (the runner greps for it), or
`DONE` for a measurement harness that has nothing to assert.
