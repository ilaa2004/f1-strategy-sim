# Roadmap

This project is deliberately staged: get a small, correct, well-tested
simulation working first, then add complexity one layer at a time. Each
level below is a real, scoped chunk of work — good commit-sized (or
few-commits-sized) milestones for the GitHub history.

## Level 1 — Single-car pit strategy (done)

- Linear tire degradation + noise, per compound.
- Randomized pit-stop time loss.
- Optional random safety car event with cheaper pit stops.
- Monte Carlo comparison of 1-stop vs 2-stop strategies: mean, median,
  spread, percentile outcomes, and head-to-head win probability.

## Level 2 — More realistic single-car model

Ideas, in roughly increasing difficulty:
- **Non-linear degradation**: replace the linear model with a curve that
  has a "cliff" past some tire age (piecewise or quadratic).
- **Fuel effect**: lap time should improve slightly each lap as fuel burns
  off — currently ignored, but real and directional.
- **Track-specific parameters**: pull base lap time, pit loss, and safety
  car probability out into a per-track config (e.g. Monaco vs Monza have
  very different pit-loss and overtaking characteristics).
- **Track position / traffic**: a pit stop that drops you into traffic
  costs more than the raw pit-lane time — model an approximate "traffic
  penalty" based on where the stop lands relative to other cars.

## Level 3 — Real data

- Pull real session data with the [FastF1](https://docs.fastf1.dev/)
  Python package (lap times, tire compounds, stint lengths, actual pit
  loss for a given circuit) and fit `tires.py`'s parameters to it instead
  of hand-picked numbers.
- Validate the model: does it predict something close to the strategies
  teams actually ran in a real race?
- This is the point where the project stops being "illustrative" and
  starts being backed by real telemetry — a strong thing to point to in
  an interview.

## Level 4 — Multi-car race simulation

- Simulate a full grid, not just one car: relative pace, overtaking
  probability as a function of pace delta and track (some tracks are much
  harder to pass on), and how a pit stop changes track position and
  therefore who you're racing.
- This is where "strategy" starts to mean something closer to what a real
  strategist does — decisions depend on what *other* cars are doing, not
  just your own tire model in isolation.

## Level 5 — Strategy optimization

- Instead of comparing a handful of hand-picked strategies, search the
  space of possible stint-length / compound combinations to find the one
  that maximizes win probability (or minimizes expected time, or some
  risk-adjusted objective) — a simple grid search first, then something
  smarter (Bayesian optimization, or a learned model) if there's appetite.
- This is also a natural point to add **live re-strategizing**: given a
  safety car that just appeared, what's now the best remaining strategy?

## Nice-to-haves along the way

- A small CLI or notebook to define a strategy and see its distribution
  without editing `compare_strategies.py` directly.
- Docstring/type-hint pass once the model stabilizes, and a
  `pyproject.toml` if this becomes an installable package.
- CI (GitHub Actions) running `pytest` on push — cheap, and it's an
  expected signal on a portfolio repo.
