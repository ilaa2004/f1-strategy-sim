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

# TODO: define at least two candidate strategies to compare, e.g. a 1-stop
# and a 2-stop. Make sure the lap counts in each strategy sum to the same
# total (so comparisons are fair) — pick a race distance, e.g. 58 laps.
STRATEGIES = {
    # "1-stop (Medium/Hard)": [("Medium", 20), ("Hard", 38)],
}

N_SIMULATIONS = 5000


def main():
    # TODO:
    #   1. For each strategy: run_monte_carlo(), store results, print
    #      summarize() output.
    #   2. Compute win probability: for each simulation index i, which
    #      strategy had the lowest time at that same index? (GUIDE.md
    #      Step 4 explains why comparing "by index" matters here.)
    #   3. Plot overlapping histograms of each strategy's results with
    #      matplotlib and save to strategy_comparison.png.
    raise NotImplementedError


if __name__ == "__main__":
    main()
