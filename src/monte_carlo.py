"""
monte_carlo.py — run many simulated races per strategy and compare outcomes
=============================================================================

YOUR TASK: run simulate_race() many times for one strategy and summarize
the resulting distribution of race times.

See GUIDE.md "Step 3" before writing this — it explains why we do this
(a single simulated race is meaningless on its own) and what stats matter.
"""

import random
import statistics

from race import simulate_race


def run_monte_carlo(strategy, n_simulations=5000, safety_car_probability=0.25, seed=None):
    """
    Run `n_simulations` independent simulated races for one strategy.
    Return the list of total race times.

    TODO:
      1. Create an rng = random.Random(seed) — one rng, reused across all
         simulations (GUIDE.md Step 3 explains why this matters for
         reproducibility).
      2. For each simulation: randomly decide (using safety_car_probability)
         whether a safety car happens this race, and if so on what lap.
      3. Call simulate_race() and collect the result.
    """
    raise NotImplementedError


def summarize(name, results):
    """
    Turn a list of race times into the summary stats a strategist cares
    about: mean, median, std dev, and 10th/90th percentile outcomes.

    TODO: use the `statistics` module. For percentiles, sort the results
    and index into them (GUIDE.md Step 3 shows the formula if you get stuck).
    Return a dict.
    """
    raise NotImplementedError
