"""
Basic sanity tests for run_monte_carlo() and summarize().
Run: pytest tests/test_monte_carlo.py -v
"""

from monte_carlo import run_monte_carlo, summarize

STRATEGY = [("Medium", 20), ("Hard", 38)]
TRACK = {"laps": 58, "pit_loss_mean": 22.0, "pit_loss_stddev": 1.5}  # matches STRATEGY's total laps


def test_returns_correct_number_of_results():
    results = run_monte_carlo(STRATEGY, TRACK, n_simulations=200, seed=1)
    assert len(results) == 200


def test_same_seed_gives_same_results():
    results1 = run_monte_carlo(STRATEGY, TRACK, n_simulations=50, seed=1)
    results2 = run_monte_carlo(STRATEGY, TRACK, n_simulations=50, seed=1)
    assert results1 == results2


def test_results_are_not_all_identical():
    """Catches the classic bug: creating a new random.Random(seed) inside
    the loop instead of once outside it, which would make every simulated
    race come out exactly the same."""
    results = run_monte_carlo(STRATEGY, TRACK, n_simulations=50, seed=1)
    assert len(set(results)) > 1


def test_summarize_returns_expected_keys():
    results = run_monte_carlo(STRATEGY, TRACK, n_simulations=200, seed=1)
    summary = summarize("test", results)
    for key in ("mean", "median", "std", "p10", "p90"):
        assert key in summary
    assert summary["p10"] <= summary["median"] <= summary["p90"]
