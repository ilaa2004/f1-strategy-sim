# Build Guide — F1 Pit Strategy Monte Carlo Simulation

This is your plan, not a solution — you type every line yourself. Step 1
below is broken into very small numbered pieces (1.1, 1.2, 1.3...), each
just a few lines, each with something to run immediately afterward to
check it worked before you move on. Steps 2–4 are written in a denser
style for now — once you finish Step 1, tell me and I'll rewrite Step 2
the same granular way rather than have you read ahead through something
not yet broken down.

When you're stuck on *how* to write something (not *what* it should do),
tell me exactly where and what happened (the error message, or "nothing
printed") — I'll explain the concept or point at the bug, not hand you
the fixed line, unless you ask outright for the answer.

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

You're basic at coding and want this like-a-baby step by step — good,
that's exactly how this section is written. Don't skip ahead. Do each
numbered step, run the check that follows it, and only move on once it
works. Every step is a handful of lines, never more.

Open `src/tires.py` and `tests/test_tires.py` side by side. Work in
`tires.py`. Use a terminal in the project folder for the checks.

### 1.1 — One fixed number

At the top of `tires.py` (below the `import random` line), write:

```python
SOFT_BASE_LAPTIME = 92.0
```

That's it. This is the time (in seconds) for one lap on a *brand new*
Soft tire, before any wear. Save the file.

**Check:** run `python` in your terminal (this opens an interactive
Python shell — you type code and it runs immediately, line by line, so
you can poke at things as you build). Then type:
```python
from tires import SOFT_BASE_LAPTIME
print(SOFT_BASE_LAPTIME)
```
It should print `92.0`. Type `exit()` to leave the shell. If you get an
error, read it — it will tell you the line and what's wrong (a typo,
usually). Don't move on until this works.

### 1.2 — Turn it into a function

A function lets you compute something instead of just storing one fixed
value. Add this below what you just wrote:

```python
def soft_lap_time():
    return SOFT_BASE_LAPTIME
```

**Check:** back in `python`:
```python
from tires import soft_lap_time
print(soft_lap_time())
```
Should print `92.0` again — same number, but now it comes from calling a
function instead of reading a variable directly. That distinction matters
in a second.

### 1.3 — Make the tire wear out

Right now the function always returns the same number, no matter how old
the tire is — that's not useful yet. A function can take **inputs**
(called parameters) so it can compute something different each time.

Rewrite `soft_lap_time` to take one input — how many laps the tire has
already done — and add a small time penalty for each lap of wear:

```python
def soft_lap_time(tire_age_laps):
    degradation_per_lap = 0.15   # seconds lost per lap of wear — a guess for now
    return SOFT_BASE_LAPTIME + degradation_per_lap * tire_age_laps
```

Read that math left to right: fresh-tire pace, plus (wear-per-lap times
how many laps of wear). At `tire_age_laps = 0` you should get exactly the
base time back.

**Check:**
```python
from tires import soft_lap_time
print(soft_lap_time(0))    # should be 92.0
print(soft_lap_time(10))   # should be higher than 92.0
print(soft_lap_time(20))   # should be higher still
```
If the numbers go *up* as tire age goes up, you've got it. If they don't
move, check you're actually using `tire_age_laps` in the formula.

### 1.4 — Handle three compounds, not just one

Writing a separate function per compound (`soft_lap_time`,
`medium_lap_time`, `hard_lap_time`) would mean repeating the same formula
three times. Instead, group each compound's numbers into a **dictionary**
— a way to store several named values together, like a small labeled box.
You've likely seen these in your CS coursework even if you haven't used
one much:

```python
SOFT = {"name": "Soft", "base_laptime": 92.0, "deg_rate": 0.15}
```

Delete the `SOFT_BASE_LAPTIME` variable and `soft_lap_time` function from
the earlier steps — this replaces them. Now add `MEDIUM` and `HARD` the
same way. Medium should have a slightly slower `base_laptime` than Soft
and a slightly lower `deg_rate` (it wears more slowly) — Hard slower and
lower still. Exact numbers don't matter yet, just the ordering:
Soft fastest-but-wears-fastest, Hard slowest-but-longest-lasting.

Then write **one** function that works for any compound, by reading its
values out of the dictionary with square brackets:

```python
def lap_time(compound, tire_age_laps):
    return compound["base_laptime"] + compound["deg_rate"] * tire_age_laps
```

**Check:**
```python
from tires import SOFT, HARD, lap_time
print(lap_time(SOFT, 0))     # should be SOFT's base_laptime
print(lap_time(HARD, 0))     # should be HARD's base_laptime, and higher than SOFT's
print(lap_time(SOFT, 20))    # should be noticeably higher than lap_time(SOFT, 0)
```

### 1.5 — Add randomness

Real lap times aren't perfectly predictable — there's always some small
variation. This is also the piece that will let us run a *Monte Carlo*
simulation later (many random trials instead of one fixed answer), so
it's worth getting comfortable with `random` now, on something simple.

Try this first in a throwaway Python shell, unrelated to your file, just
to see how it behaves:
```python
import random
rng = random.Random(0)     # a controlled source of randomness, seeded with 0
print(rng.gauss(0, 1))     # a random number centered on 0, "spread" of 1
print(rng.gauss(0, 1))     # a different random number, same shell
```
Run those two `gauss` lines a few times (restart Python between attempts,
same seed `0`) — you'll notice you get the *same sequence* every time you
use seed `0`. That's the point of seeding: reproducible randomness. We
use `random.Random(0)` instead of plain `random.gauss(...)` specifically
so we can control and repeat this later — don't worry about why that
matters yet, Step 3 explains it.

Now update `lap_time` in `tires.py` to accept that `rng` and add a bit of
random noise to the result:

```python
def lap_time(compound, tire_age_laps, rng):
    predictable_part = compound["base_laptime"] + compound["deg_rate"] * tire_age_laps
    noise = rng.gauss(0, 0.1)
    return predictable_part + noise
```

Notice `lap_time` now takes **three** inputs instead of two — you'll need
to pass an `rng` every time you call it from now on.

**Check:**
```python
import random
from tires import SOFT, lap_time
rng = random.Random(0)
print(lap_time(SOFT, 0, rng))
print(lap_time(SOFT, 0, rng))
print(lap_time(SOFT, 0, rng))
```
Same inputs (`SOFT`, age `0`), but three different outputs, each close to
92 but not exactly — that's the noise working.

### 1.6 — One last refinement: shakier tires get noisier

A well-worn tire is less predictable lap-to-lap than a fresh one — real
strategists trust an early pit window more than a late one partly for
this reason. Make the noise grow with tire age instead of always being
`0.1`:

```python
def lap_time(compound, tire_age_laps, rng):
    predictable_part = compound["base_laptime"] + compound["deg_rate"] * tire_age_laps
    noise_size = 0.02 * max(tire_age_laps, 1)
    noise = rng.gauss(0, noise_size)
    return predictable_part + noise
```

(`max(tire_age_laps, 1)` just avoids a noise size of exactly zero at
brand-new tire age — a small technicality, not worth dwelling on.)

### Step 1 final checkpoint

Run the test file that came with the project — it checks the behaviors
above automatically instead of you eyeballing numbers each time:

```bash
pytest tests/test_tires.py -v
```

You should see **3 passed**. If something fails, the test name tells you
which behavior is broken (e.g. `test_softs_start_faster_than_hards` means
go re-check your SOFT vs HARD numbers). Paste me the failure if you're
stuck for more than a few minutes — that's exactly what I'm here for.

Once this passes: **stop and tell me.** I'll walk you through Step 2 the
same way, broken into the same size steps — no need to read ahead in this
guide, Step 2 as currently written is the denser "advanced" version I'll
replace once you get there.

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
