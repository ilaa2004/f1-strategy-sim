"""
compare_strategies.py — entry point: compare candidate pit strategies
=========================================================================

YOUR TASK: wire everything together — run each strategy through Monte
Carlo, print a comparison, and plot the results.

See GUIDE.md "Step 4" before writing this.

Run: python compare_strategies.py
"""

import matplotlib.pyplot as plt

from monte_carlo import run_monte_carlo, summarize
from tracks import TRACKS
import statistics
import time

# TODO: define at least two candidate strategies to compare, e.g. a 1-stop
# and a 2-stop. Make sure the lap counts in each strategy sum to the same
# total (so comparisons are fair) — pick a race distance, e.g. 57 laps.
STRATEGIES = {
     "Kimis start)": [("Medium", 14), ("Hard", 43)],
     "Georges start": [("Hard", 14), ("Medium", 14), ("Hard", 29)],
}

N_SIMULATIONS = 5000


def main():
        stat1_wins = 0
        stat2_wins = 0
   
    #   1. For each strategy: run_monte_carlo(), store results, print
    #      summarize() output.
        chosen_track=TRACKS["Madring"]

        stat1_results = run_monte_carlo(STRATEGIES["Kimis start)"], n_simulations=N_SIMULATIONS, chosen_track=chosen_track, safety_car_probability=0.25, seed=None)
        stat2_results = run_monte_carlo(STRATEGIES["Georges start"], n_simulations=N_SIMULATIONS, chosen_track=chosen_track, safety_car_probability=0.25, seed=None)

        print(summarize('1-stop', stat1_results))
        print(summarize('2-stop', stat2_results))
    #   2. Compute win probability: for each simulation index i, which
    #      strategy had the lowest time at that same index? (GUIDE.md
    #      Step 4 explains why comparing "by index" matters here.)
        for i in range(N_SIMULATIONS):
            if stat1_results[i] < stat2_results[i]:
                stat1_wins += 1
            else:
                stat2_wins += 1

        print(f"Kimis: {stat1_wins}")
        print(f"Georges: {stat2_wins}")    

        Kimis_best = time.strftime("%H:%M:%S", time.gmtime(min(stat1_results)))
        Georges_best = time.strftime("%H:%M:%S", time.gmtime(min(stat2_results)))

        print(f"kimis best time: {Kimis_best}")
        print(f"georges best time: {Georges_best}")    
    #   3. Plot overlapping histograms of each strategy's results with
    #      matplotlib and save to strategy_comparison.png.
        ax = plt.subplot(111)
        ax.hist(stat1_results, bins=50, alpha=0.5, label="Kimis start (Medium/Hard)")
        ax.hist(stat2_results, bins=50, alpha=0.5, label="Georges start (Hard/Medium/Hard)")
        ax.set_xlabel("Race Time (seconds)")
        ax.set_ylabel("Frequency")
        ax.set_title("Race Time Distribution by Strategy")
        ax.legend()
        plt.savefig("strategy_comparison.png") 
       
        


if __name__ == "__main__":
    main()
