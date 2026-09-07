"""
race.py — simulate one full race for a given pit strategy
===========================================================

YOUR TASK: given a strategy (a sequence of stints) simulate the total race
time, including pit stop losses.

See GUIDE.md "Step 2" before writing this.
"""

import random

from tires import COMPOUNDS, lap_time

# TODO: pick reasonable constants for pit stop time loss (mean + std dev).
PIT_STOP_MEAN = None
PIT_STOP_STD = None


def simulate_race(strategy, rng: random.Random, safety_car_lap: int | None = None) -> float:
    """
    Return total race time in seconds for one strategy, for one simulated
    (random) race.

    strategy: list of (compound_name, stint_length) tuples,
              e.g. [("Medium", 20), ("Hard", 38)]
    safety_car_lap: optional lap number a safety car appears on — pitting
                    near this lap should be cheaper than normal (GUIDE.md
                    Step 2 explains why this matters for real strategy).

    TODO:
      1. Loop over each stint in `strategy`.
      2. Within a stint, loop over each lap of tire age and add up lap_time().
      3. After every stint except the last, add a randomized pit stop cost.
         If a safety_car_lap is given and you're pitting near it, reduce
         the cost.
      4. Return the total.
    """
    raise NotImplementedError
