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


TRACKS = {

    "Australia": {
        "name": "Albert Park Circuit",
        "length_m": 5278,
        "laps": 58,
        "turns": 14,
        "pit_loss_mean": 19.30,
        "pit_loss_stddev": 1.5
    },

    "China": {
        "name": "Shanghai International Circuit",
        "length_m": 5451,
        "laps": 56,
        "turns": 16,
        "pit_loss_mean": 23.67,
        "pit_loss_stddev": 1.5
    },

    "Japan": {
        "name": "Suzuka Circuit",
        "length_m": 5807,
        "laps": 53,
        "turns": 18,
        "pit_loss_mean": 23.75,
        "pit_loss_stddev": 1.5
    },

    "Miami": {
        "name": "Miami International Autodrome",
        "length_m": 5412,
        "laps": 57,
        "turns": 19,
        "pit_loss_mean": 18.76,
        "pit_loss_stddev": 1.5
    },

    "Canada": {
        "name": "Circuit Gilles-Villeneuve",
        "length_m": 4361,
        "laps": 70,
        "turns": 14,
        "pit_loss_mean": 18.25,
        "pit_loss_stddev": 1.5
    },

    "Monaco": {
        "name": "Circuit de Monaco",
        "length_m": 3337,
        "laps": 78,
        "turns": 19,
        "pit_loss_mean": 19.92,
        "pit_loss_stddev": 1.5
    },

    "Barcelona": {
        "name": "Circuit de Barcelona-Catalunya",
        "length_m": 4657,
        "laps": 66,
        "turns": 14,
        "pit_loss_mean": 22.96,
        "pit_loss_stddev": 1.5
    },

    "Austria": {
        "name": "Red Bull Ring",
        "length_m": 4326,
        "laps": 71,
        "turns": 10,
        "pit_loss_mean": 20.02,
        "pit_loss_stddev": 1.5
    },

    "Great Britain": {
        "name": "Silverstone Circuit",
        "length_m": 5891,
        "laps": 52,
        "turns": 18,
        "pit_loss_mean": 20.00,
        "pit_loss_stddev": 1.5
    },

    "Belgium": {
        "name": "Circuit de Spa-Francorchamps",
        "length_m": 7004,
        "laps": 44,
        "turns": 19,
        "pit_loss_mean": 18.50,
        "pit_loss_stddev": 1.5
    },

    "Hungary": {
        "name": "Hungaroring",
        "length_m": 4381,
        "laps": 70,
        "turns": 14,
        "pit_loss_mean": 20.56,
        "pit_loss_stddev": 1.5
    },

    "Netherlands": {
        "name": "Circuit Zandvoort",
        "length_m": 4259,
        "laps": 72,
        "turns": 14,
        "pit_loss_mean": 18.09,
        "pit_loss_stddev": 1.5
    },

    "Italy": {
        "name": "Monza",
        "length_m": 5793,
        "laps": 53,
        "turns": 11,
        "pit_loss_mean": 24.14,
        "pit_loss_stddev": 1.5
    },

    "Madring": {
        "name": "Madring",
        "length_m": 5414,
        "laps": 57,
        "turns": 22,
        "pit_loss_mean": None,  # Pit loss mean not defined for Madring
        "pit_loss_stddev": 1.5
    },

    "Azerbaijan": {
        "name": "Baku City Circuit",
        "length_m": 6003,
        "laps": 51,
        "turns": 20,
        "pit_loss_mean": 19.70,
        "pit_loss_stddev": 1.5
    },

    "Sepang": {
        "name": "Sepang International Circuit",
        "length_m": 5543,
        "laps": 56,
        "turns": 15,
        "pit_loss_mean": None,  # Pit loss mean not defined for Sepang
        "pit_loss_stddev": 1.5
    },

    "Singapore": {
        "name": "Marina Bay Street Circuit",
        "length_m": 4927,
        "laps": 62,
        "turns": 19,
        "pit_loss_mean": 29.10,
        "pit_loss_stddev": 1.5
    },

    "United States": {
        "name": "Circuit of The Americas",
        "length_m": 5513,
        "laps": 56,
        "turns": 20,
        "pit_loss_mean": 20.60,
        "pit_loss_stddev": 1.5
    },

    "Mexico": {
        "name": "Autodromo Hermanos Rodriguez",
        "length_m": 4304,
        "laps": 71,
        "turns": 17,
        "pit_loss_mean": 21.90,
        "pit_loss_stddev": 1.5
    },

    "Brazil": {
        "name": "Interlagos",
        "length_m": 4309,
        "laps": 71,
        "turns": 15,
        "pit_loss_mean": 20.80,
        "pit_loss_stddev": 1.5
    },

    "Las Vegas": {
        "name": "Las Vegas Strip Circuit",
        "length_m": 6201,
        "laps": 50,
        "turns": 17,
        "pit_loss_mean": 20.00,
        "pit_loss_stddev": 1.5
    },

    "Qatar": {
        "name": "Lusail International Circuit",
        "length_m": 5419,
        "laps": 57,
        "turns": 16,
        "pit_loss_mean": 26.30,
        "pit_loss_stddev": 1.5
    },

    "Abu Dhabi": {
        "name": "Yas Marina Circuit",
        "length_m": 5281,
        "laps": 58,
        "turns": 16,
        "pit_loss_mean": 21.00,
        "pit_loss_stddev": 1.5
    }
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