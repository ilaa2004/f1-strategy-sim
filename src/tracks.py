"""
tracks.py — F1 Track Model
==========================

This file will store track-specific information used by the race simulator.

Don't build everything at once. We will start with one circuit and gradually
expand the model as the simulator becomes more realistic.

Eventually, this file can contain data for multiple F1 circuits and may later
be connected to an external API instead of storing everything manually.
"""

from tires import COMPOUNDS, lap_time  


# --- Step 1.1: Create our first track
#
# Start by representing ONE Formula 1 circuit using a dictionary.
#
# For now, the track only needs four pieces of information:
#
#     name
#     length_m       -> track length in meters
#     laps           -> number of laps in the Grand Prix
#     turns          -> number of turns/corners
#
# Don't worry about APIs yet. Enter the first track manually so we understand
# how the data should be structured before trying to retrieve it automatically.
#
# Choose one circuit to start with.
mardring_circuit = {
    "name": "Mardring Circuit",
    "length_m": 5416,
    "laps": 57,
    "turns": 22
}


# --- Step 1.2: Add another circuit
#
# Once the first track works, create a second track using exactly the same
# structure.
#
# This will let us check that the simulator can work with different tracks
# rather than being hard-coded for one race.

monza_circuit = {
    "name": "Monza Circuit",
    "length_m": 5793,
    "laps": 53,
    "turns": 11
}


# --- Step 1.3: Create a TRACKS collection
#
# Once we have several individual track dictionaries, create one collection
# that lets the program find a track by name.
#
# Think about how COMPOUNDS works in tires.py.
# We can use a similar idea here.

TRACK= {
    "Madrid GP": mardring_circuit,
    "Monza GP": monza_circuit
}

# --- Step 1.4: Connect tracks.py to race.py
#
# At the moment, race.py determines the race distance from the strategy itself.
#
# Eventually we want the selected track to tell the simulator how many laps
# the race should contain.
#
# Example question the program should eventually be able to answer:
#
#     "How many laps should this race have at Monza?"
#
# Don't implement this yet.


# --- Step 1.5: Add simulation-relevant track parameters
#
# Track length, laps, and turns describe the circuit, but they do not yet
# strongly affect race strategy.
#
# Later we can investigate parameters such as:
#
#     pit-lane time loss
#     Safety Car probability
#     tyre degradation multiplier
#     average/base lap time
#     overtaking difficulty
#
# We will decide which of these belong in the model before implementing them.


# --- Step 1.6: External data / API
#
# Once the manual version works, investigate whether reliable F1 circuit data
# can be retrieved from an API.
#
# IMPORTANT:
# Don't connect an API until the local track model works.
#
# The goal is for the rest of the simulator not to care whether track data
# came from:
#
#     tracks.py
#
# or:
#
#     an external API
#
# That separation will make the project easier to maintain and expand.