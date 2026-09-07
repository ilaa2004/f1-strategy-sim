"""
tires.py — Tire degradation model
==================================

YOUR TASK: model how lap time changes as a tire wears out.

See GUIDE.md "Step 1" for the concepts and the reasoning behind this file's
design before you write any code.
"""

from dataclasses import dataclass
import random


@dataclass
class TireCompound:
    """
    TODO: what fields does a compound need to describe how it performs?
    At minimum you'll want: a name, a fresh-tire lap time, and something
    describing how quickly it degrades. GUIDE.md Step 1 explains why a
    dataclass is a good fit here.
    """
    pass


# TODO: define SOFT, MEDIUM, HARD as TireCompound instances, and a
# COMPOUNDS dict mapping name -> compound (compare_strategies.py will look
# strategies up by name, e.g. COMPOUNDS["Soft"]).
# Numbers don't need to be "correct" — they need to be internally
# consistent: Soft should start faster than Hard and degrade faster.


def lap_time(compound: TireCompound, tire_age_laps: int, rng: random.Random) -> float:
    """
    Return the time (seconds) for one lap on a tire of the given age.

    TODO — build this in two parts:
      1. A deterministic part: base pace + degradation as a function of
         tire_age_laps (start with something linear).
      2. A random noise part using `rng` (not the global `random` module —
         GUIDE.md Step 1 explains why), representing lap-to-lap variability.
         Consider making the noise grow with tire age.

    Return the sum.
    """
    raise NotImplementedError
