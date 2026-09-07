"""
Basic sanity tests for the tire degradation model.

Run: pytest  (from the project root, with src/ on the path — see conftest.py)
"""

import random

from tires import HARD, SOFT, lap_time


def test_lap_time_degrades_with_tire_age_on_average():
    """Older tires should be slower *on average* — noise means any single
    lap could go either way, so we compare averages over many samples."""
    rng = random.Random(1)
    early_laps = [lap_time(SOFT, 1, rng) for _ in range(500)]
    late_laps = [lap_time(SOFT, 25, rng) for _ in range(500)]

    assert sum(late_laps) / len(late_laps) > sum(early_laps) / len(early_laps)


def test_lap_time_is_always_positive():
    rng = random.Random(2)
    for compound in (SOFT, HARD):
        for age in range(40):
            assert lap_time(compound, age, rng) > 0


def test_softs_start_faster_than_hards():
    """On a fresh tire (age 0), softs should be quicker than hards — that's
    the entire reason softs exist as a strategic option."""
    rng = random.Random(3)
    soft_laps = [lap_time(SOFT, 0, rng) for _ in range(200)]
    hard_laps = [lap_time(HARD, 0, rng) for _ in range(200)]

    assert sum(soft_laps) / len(soft_laps) < sum(hard_laps) / len(hard_laps)
