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
   rng= random.Random(seed)  # a controlled source of randomness, seeded with seed
   result = []

   for n in range(n_simulations):
       safety_car_happens = rng.random() < safety_car_probability
       if safety_car_happens:
           safety_car_lap = rng.randint(1, 53)  # randomly choose a lap for the safety car
       else:
           safety_car_lap = None  # no safety car
   
       stimulate_result = simulate_race(strategy, rng)
       result.append(stimulate_result)   # call simulate

   return result


def summarize(name, results):
    """
    Turn a list of race times into the summary stats a strategist cares
    about: mean, median, std dev, and 10th/90th percentile outcomes.

    TODO: use the `statistics` module. For percentiles, sort the results
    and index into them (GUIDE.md Step 3 shows the formula if you get stuck).
    Return a dict.
    """
    raise NotImplementedError
