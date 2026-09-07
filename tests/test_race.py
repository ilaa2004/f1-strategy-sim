"""
Basic sanity tests for simulate_race(). Run: pytest tests/test_race.py -v
"""

import random

from race import simulate_race


def test_same_seed_gives_same_result():
    """Determinism: identical seed -> identical simulated race. This is
    what makes fair strategy comparisons possible later (GUIDE.md Step 4)."""
    strategy = [("Medium", 20), ("Hard", 38)]

    rng1 = random.Random(1)
    rng2 = random.Random(1)

    assert simulate_race(strategy, rng1) == simulate_race(strategy, rng2)


def test_more_laps_takes_more_time():
    short_strategy = [("Medium", 10)]
    long_strategy = [("Medium", 30)]

    short_time = simulate_race(short_strategy, random.Random(1))
    long_time = simulate_race(long_strategy, random.Random(1))

    assert long_time > short_time


def test_pit_stop_adds_time():
    """Two 1-lap stints (one pit stop) vs one 2-lap stint (no pit stop).
    Laps are kept tiny on purpose so tire degradation barely differs
    between the two — almost the whole gap should be the pit stop itself."""
    no_pit = [("Medium", 2)]
    one_pit = [("Medium", 1), ("Medium", 1)]

    no_pit_time = simulate_race(no_pit, random.Random(1))
    one_pit_time = simulate_race(one_pit, random.Random(1))

    assert one_pit_time > no_pit_time
