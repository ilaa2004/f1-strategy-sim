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
import time

from race import simulate_race
from tracks import TRACKS

def run_monte_carlo(strategy, chosen_track, n_simulations=5000, safety_car_probability=0.25, seed=None):
    rng = random.Random(seed)
    result = []

    for n in range(n_simulations):
        safety_car_happens = rng.random() < safety_car_probability
        if safety_car_happens:
            safety_car_lap = rng.randint(1, chosen_track["laps"] - 1)
        else:
            safety_car_lap = None

        stimulate_result = simulate_race(strategy, rng, chosen_track, safety_car_lap)
        result.append(stimulate_result)

    return result


def summarize(name, results):

   mean_time = statistics.mean(results)
   median_time = statistics.median(results)
   std_time = statistics.stdev(results)  


   time_string = time.strftime("%H:%M:%S", time.gmtime(min(results)))

   p10 = sorted(results)[int(0.10 * len(results))]  # 10th percentile
   p90 = sorted(results)[int(0.90 * len(results))]  # 90th percentile
   percentile_range = p90 / p10
   return {
       "name": name,
       "mean": mean_time,
       "median": median_time,
       "std": std_time,
       "p10": p10,
       "p90": p90,
       "percentile": percentile_range,
       "best": time_string

      
   }



choosen_track = TRACKS["Madring"]
Startegy = [("Hard", 14), ("Medium", 14), ("Hard", 29)]
stop1 = run_monte_carlo(Startegy, choosen_track, n_simulations=10, safety_car_probability=0.25, seed=None)
print(len(stop1))
print(summarize('1-stop', stop1))


