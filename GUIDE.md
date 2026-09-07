# Build Guide — F1 Pit Strategy Monte Carlo Simulation

This is your plan, not a solution. Each step explains the concept, tells
you what the file needs to do, and gives you a checkpoint to confirm it
works — but you write the code. The `TODO`s in `src/*.py` mark exactly
where your work goes. When you're stuck on *how* to write something (not
*what* it should do), ask me and I'll explain the technique or point you
at the relevant Python feature — I won't fill in the logic for you unless
you explicitly ask for the answer.

Work through the steps in order. Each one only needs what came before it.

---

## Step 0 — Setup

```bash
cd f1-strategy-sim
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Confirm it's wired up:
```bash
pytest
```
You'll see failures — that's expected, `tires.py` is empty (`raise
NotImplementedError`). Those tests are your spec for Step 1: they tell you
exactly what `lap_time()` needs to do without telling you how.

---

## Step 1 — Tire degradation (`src/tires.py`)

### The concept

A strategist's whole job comes down to one trade-off: soft tires are fast
when fresh but wear out quickly; hard tires are slower but last. You need
a function that, given a compound and how many laps it's been used, tells
you how long a lap takes.

**Why a `dataclass`?** You need a small bundle of related values (name,
base pace, degradation rate) with no real behavior of its own — that's
exactly what `@dataclass` is for: it gives you a clean constructor and
readable repr for free, instead of a bare class with a hand-written
`__init__`. If you haven't used one, read the first example in the
[dataclasses docs](https://docs.python.org/3/library/dataclasses.html) —
don't copy the fields, just the pattern.

**Why pass an `rng` object instead of calling `random.gauss()` directly?**
Python's `random` module has a global random state, shared by your whole
program. If every function pulls from that global state, you can't
reproduce a specific run — which matters a lot once you're comparing
strategies (Step 4) and want "strategy A vs strategy B, same random
conditions" to be a fair comparison. A `random.Random(seed)` instance is
an independent random stream you control explicitly. Get used to threading
it through function calls now — it'll matter more later.

**Why should noise grow with tire age?** A fresh tire is predictable; a
worn one is not — a strategist trusts an early pit window more than a
late one for exactly this reason. Encoding that (noise scales with age)
is a small modeling choice that makes the simulation's behavior match
real intuition, and it's worth being able to explain *why* you made it,
not just that you did.

### What to build

1. Fill in `TireCompound` — name, base lap time, degradation rate, and a
   term controlling how much noise grows with age.
2. Define `SOFT`, `MEDIUM`, `HARD` and a `COMPOUNDS` dict.
3. Write `lap_time(compound, tire_age_laps, rng)`: deterministic
   base-pace-plus-degradation, plus `rng.gauss(0, some_std_dev)` noise.
   Start with **linear** degradation (`deg_rate * tire_age_laps`) — that's
   deliberate, see `ROADMAP.md` Level 2 for why we upgrade it later.

### Checkpoint

```bash
pytest tests/test_tires.py -v
```
All three tests should pass. If `test_softs_start_faster_than_hards`
fails, check your SOFT/HARD numbers. If
`test_lap_time_degrades_with_tire_age_on_average` fails, check your
degradation term's sign.

Also sanity-check it by eye — in a Python shell:
```python
import random
from tires import SOFT, lap_time
rng = random.Random(0)
for age in [0, 10, 20, 30]:
    print(age, lap_time(SOFT, age, rng))
```
The numbers should trend upward as age increases, with some jitter.

---

## Step 2 — Simulate one race (`src/race.py`)

### The concept

A **strategy** is a sequence of stints: `[("Medium", 20), ("Hard", 38)]`
means 20 laps on Mediums, pit, then 38 laps on Hards. This is a **1-stop**
strategy — one pit stop. `[("Soft", 15), ("Soft", 15), ("Hard", 28)]` is a
**2-stop**.

Two real F1 terms worth knowing, because they explain why pit timing
itself is strategic, not just tire-driven:
- **Undercut**: pitting *before* a rival, so your fresh tires are faster
  than their old ones for the laps immediately after — you gain track
  position without passing on-track.
- **Overcut**: the opposite — staying out longer than a rival, banking
  faster laps than they can on their newly-fresh-but-not-yet-quick tires
  right after a stop.
This simulation (Level 1) doesn't model rival cars yet, so it can't
capture undercut/overcut directly — that's Level 4 in `ROADMAP.md`. But
it's worth knowing the terms now since they're exactly what a real
strategist means by "pit strategy."

**Why randomize the pit stop cost?** A real pit stop varies — crew
execution, timing precision. Modeling it as fixed would hide a real
source of risk that strategists have to weigh (a strategy needing more
stops is more exposed to a bad one).

**Why does a safety car make pitting cheaper?** Under a safety car the
whole field slows down, so the *relative* time you lose by diving into
the pits is much smaller than under green-flag racing. This is why real
strategists react live to a safety car rather than only planning
pre-race — it can flip the optimal strategy instantly.

### What to build

`simulate_race(strategy, rng, safety_car_lap=None) -> float`:
1. Loop over each `(compound_name, stint_length)` in `strategy`.
2. For each lap of that stint (tire age `0` to `stint_length - 1`), add
   `lap_time(...)` to a running total.
3. After every stint *except the last*, add a pit stop cost:
   `rng.gauss(PIT_STOP_MEAN, PIT_STOP_STD)`. If `safety_car_lap` is set
   and the current lap is close to it, reduce the cost (e.g. multiply by
   something less than 1).
4. Return the total.

Pick your own `PIT_STOP_MEAN` / `PIT_STOP_STD` — real F1 stops (including
pit lane transit) lose roughly 20–25 seconds; exact realism matters less
right now than having a value that makes strategies with more stops
visibly cost more.

### Checkpoint

In a Python shell:
```python
import random
from race import simulate_race
rng = random.Random(0)
print(simulate_race([("Medium", 20), ("Hard", 38)], rng))
```
Should return a single float in the low thousands of seconds (58 laps ×
~90s/lap + one pit stop ≈ 5300s). Run it a few times with different seeds
— you should see it vary, but stay in a plausible range. If it's wildly
off, check you're summing correctly and not double-counting the pit stop.

---

## Step 3 — Monte Carlo runner (`src/monte_carlo.py`)

### The concept

One call to `simulate_race()` is one random draw — noise in tire wear,
maybe a safety car, pit stop variance. On its own it tells you almost
nothing about how good a strategy *is*. Monte Carlo simulation means:
run that random process thousands of times and look at the **distribution**
of results, not any single one.

This is the core statistical idea of the whole project, so it's worth
being able to explain in an interview: with enough independent samples,
the distribution of outcomes converges toward the strategy's true
behavior (this convergence is the **law of large numbers** — worth
knowing the name). More samples = a more reliable picture of the
distribution, at the cost of more compute. 5,000 is a reasonable default
for this scale; try 100 vs 5,000 side by side later and watch how much
noisier the summary stats are with fewer samples.

**Why percentiles, not just the mean?** The mean tells you the expected
outcome. It doesn't tell you what a *bad* race looks like for this
strategy. A strategist cares about both — "what's typical" and "how bad
can it realistically get." The 10th percentile (`p10`) is roughly "an
unlucky race for this strategy"; the 90th (`p90`) is roughly "a lucky
one." Two strategies with the same mean can have very different p10s —
that's a real risk difference a single average hides.

### What to build

1. `run_monte_carlo(strategy, n_simulations, safety_car_probability, seed)`:
   create one `random.Random(seed)`, then loop `n_simulations` times,
   each time deciding (using `safety_car_probability`) whether a safety
   car happens and on what lap, then calling `simulate_race()`. Collect
   and return the list of results.
2. `summarize(name, results)`: compute `mean`, `median`, `std` (the
   `statistics` module has all three), plus `p10`/`p90`. For a percentile
   by hand: sort the results, then index at `int(percentile * len(results))`
   — e.g. `sorted(results)[int(0.10 * len(results))]` for p10.

### Checkpoint

```python
from monte_carlo import run_monte_carlo, summarize
results = run_monte_carlo([("Medium", 20), ("Hard", 38)], n_simulations=2000, seed=1)
print(summarize("test", results))
print(len(results))  # should be 2000
```
`std` should be a modest number (tens of seconds, not thousands) — if
it's huge, revisit your noise terms in `tires.py`/`race.py`.

---

## Step 4 — Compare strategies (`src/compare_strategies.py`)

### The concept

**Fair comparison trick:** if you run strategy A's 5,000 simulations with
seed 1 and strategy B's with seed 2, differences between them are a mix
of "real strategy difference" and "which strategy happened to get luckier
random draws." To separate those, run every strategy with **the same
seed**, so simulation #37 for strategy A and simulation #37 for strategy
B experience the *same* underlying randomness (up to what differs
structurally between the strategies, like when pit stops fall). Then you
can meaningfully ask "in simulation #37's conditions, which strategy
won?" and count across all 5,000 — that's your **win probability**. This
is a standard variance-reduction idea in simulation (worth knowing that
term too); it's why the plan has you loop `for i in range(n_simulations)`
and compare `results_A[i]` to `results_B[i]`, not just compare the two
lists' overall means.

### What to build

1. Define 2–3 `STRATEGIES` (lap counts must sum to the same total per
   strategy — pick a race distance, e.g. 58 laps, and stick to it).
2. For each strategy: run Monte Carlo, print `summarize()`.
3. Compute win probability: for each index `i`, find which strategy had
   the lowest `results[i]`; tally and print as a percentage.
4. Plot: overlapping `ax.hist(...)` per strategy on the same axes
   (`alpha=0.5` so they're visible through each other, `density=True` so
   different sample counts are still comparable), save to a PNG.

### Checkpoint

```bash
python compare_strategies.py
```
You should get printed stats for each strategy, win probabilities that
sum to \~100%, and a saved `strategy_comparison.png`. Open the image —
the histograms should visibly overlap but have different centers/spreads
depending on your strategies' compound choices.

**Interpretation check** (this is the actual point of the project): does
the 2-stop strategy with more Soft-tire laps show a lower mean but wider
spread than the 1-stop? Does that match the real-world intuition that
more pit stops = more speed but more risk exposure? If your numbers say
the opposite, that's worth digging into — it usually means a constant in
`tires.py` or `race.py` needs adjusting.

---

## Step 5 — Tests

`tests/test_tires.py` already covers Step 1. As you build `race.py` and
`monte_carlo.py`, add your own tests for them the same way — one behavior
per test, named for what it checks. A couple worth writing yourself as
practice:
- A 2-stop strategy's `simulate_race()` result should include (roughly)
  one more pit stop's worth of time than a 1-stop over the same laps.
- `run_monte_carlo()` with the same `seed` twice should return identical
  results (this is what makes Step 4's win-probability comparison valid —
  worth actually proving to yourself).

---

## Step 6 — Push to your GitHub repo

You said the repo already exists and is basically empty. From inside
`f1-strategy-sim/`:

```bash
git add -A
git commit -m "Scaffold F1 pit strategy Monte Carlo project"
git remote add origin <your-repo-url>
git branch -M main
git push -u origin main
```

Commit as you finish each step rather than all at once at the end — a
commit history showing the project built up in stages (tire model → race
sim → Monte Carlo → comparison) is itself a small piece of evidence, in a
portfolio repo, that you understand how the pieces fit together.

---

## When you're stuck

Tell me which step and what you've tried — a specific error, or "my
degradation test fails and I don't see why," gets you a much more useful
answer than "it doesn't work." I'll point at the concept or the bug, not
rewrite the function. If you genuinely want to see a working version of
one piece to compare against your own after you've had a real attempt,
ask directly and I'll show you just that piece.

Once Step 4 is solid, `ROADMAP.md` has the next stages (non-linear
degradation, real telemetry via FastF1, multi-car races, strategy
optimization) — good material for talking about where this project is
headed in an interview, even before you've built them.
