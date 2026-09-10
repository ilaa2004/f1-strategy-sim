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
   
       stimulate_result = simulate_race(strategy, rng, safety_car_lap)
       result.append(stimulate_result)   # call simulate

   return result


def summarize(name, results):

   mean_time = statistics.mean(results)
   median_time = statistics.median(results)
   stdev_time = statistics.stdev(results)  

   tenth_percentile = sorted(results)[int(0.10 * len(results))]  # 10th percentile
   ninetieth_percentile = sorted(results)[int(0.90 * len(results))]  # 90th percentile
   return {
       "name": name,
       "mean": mean_time,
       "median": median_time,
       "stdev": stdev_time,
       "10th_percentile": tenth_percentile,
       "90th_percentile": ninetieth_percentile
   }
