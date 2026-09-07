# F1 Pit Strategy — Monte Carlo Simulation

A from-scratch Monte Carlo simulation comparing Formula 1 pit-stop
strategies (1-stop vs 2-stop, different compound choices) by simulating
thousands of randomized races and comparing the resulting distributions
of total race time — not a single predicted outcome.

This is Level 1 of a staged project (see [ROADMAP.md](ROADMAP.md)), built
to develop practical race-strategy analysis skills: modeling tire
degradation, quantifying risk with simulation instead of a point
estimate, and comparing strategies the way a strategist actually has to —
on both expected pace and downside risk.

**Building this?** See [GUIDE.md](GUIDE.md) — a step-by-step plan with the
concepts explained and checkpoints, but no filled-in solutions. The files
in `src/` are currently skeletons with `TODO`s.

## Project structure

```
f1-strategy-sim/
├── GUIDE.md                    # step-by-step build plan (start here)
├── ROADMAP.md                  # how this grows after Level 1
├── src/
│   ├── tires.py                # tire compound definitions + degradation model
│   ├── race.py                 # simulate one race for a given strategy
│   ├── monte_carlo.py          # run N simulated races, summarize the distribution
│   └── compare_strategies.py   # entry point: compare strategies, plot results
├── tests/
│   ├── conftest.py
│   └── test_tires.py           # spec for tires.py — pass these before moving on
└── requirements.txt
```

## Setup

```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
pytest                        # confirms setup works (tests fail until you build tires.py — expected)
```

## Status

- [ ] Step 1 — Tire degradation model (`src/tires.py`)
- [ ] Step 2 — Single-race simulator (`src/race.py`)
- [ ] Step 3 — Monte Carlo runner (`src/monte_carlo.py`)
- [ ] Step 4 — Strategy comparison + plot (`src/compare_strategies.py`)

Check items off as you go — it's a useful commit-history marker too.
