"""
Tests for compare_strategies.py — written to match your actual structure
(everything inside main(), no separate win_probabilities() function).
Since main() doesn't return anything, these check what it actually does:
what it prints, and the plot file it saves.

Run: pytest tests/test_compare_strategies.py -v
"""

import os
import re

import compare_strategies


def test_main_prints_a_summary_for_each_strategy(capsys):
    compare_strategies.main()
    output = capsys.readouterr().out
    assert "1-stop" in output
    assert "2-stop" in output


def test_main_prints_win_counts_that_add_up_to_total_simulations(capsys):
    compare_strategies.main()
    output = capsys.readouterr().out

    stat1_match = re.search(r"1-stop wins:\s*(\d+)", output)
    stat2_match = re.search(r"2-stop wins:\s*(\d+)", output)
    assert stat1_match is not None, "couldn't find '1-stop wins: N' in the output"
    assert stat2_match is not None, "couldn't find '2-stop wins: N' in the output"

    stat1_wins = int(stat1_match.group(1))
    stat2_wins = int(stat2_match.group(1))
    assert stat1_wins + stat2_wins == compare_strategies.N_SIMULATIONS


def test_main_saves_the_comparison_plot():
    if os.path.exists("strategy_comparison.png"):
        os.remove("strategy_comparison.png")

    compare_strategies.main()

    assert os.path.exists("strategy_comparison.png")
