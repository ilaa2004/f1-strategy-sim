"""
race.py — simulate one full race for a given pit strategy
===========================================================

Don't write anything here yet — open GUIDE.md and follow "Step 2" from
the top. Same pattern as tires.py: tiny numbered pieces (2.1, 2.2, 2.3...)
with something to run and check after each.
"""
from tires import COMPOUNDS, lap_time
from tracks import TRACKS

import random

rng = random.Random(0)  # a controlled source of randomness, seeded with 0


FUEL_EFFECT_PER_LAP = 0.05   # seconds faster per lap of fuel already burned

TRAFFIC_WINDOW_FRACTION = (0.35, 0.65) # the fraction of the race where traffic is most likely to occur (e.g. 0.35 = 35% of the way through the
TRAFFIC_PENALTY_MEAN = 3.0 # seconds added to the lap time if traffic occurs
TRAFFIC_PENALTY_STD = 1.5 # standard deviation of the traffic penalty (for randomness)

def simulate_race(strategy, rng, chosen_track, safety_car_lap=None, ):
    total_time = 0.0 # time when the race starrs at 0.0 seconds 
    race_lap = 0 # the lap number of the race, starting at 0

    if chosen_track["pit_loss_mean"] is None:
        pit_loss_mean = 22.0
    else:
        pit_loss_mean = chosen_track["pit_loss_mean"]

    
    traffic_start = chosen_track["laps"] * TRAFFIC_WINDOW_FRACTION[0]
    traffic_end = chosen_track["laps"] * TRAFFIC_WINDOW_FRACTION[1]    
    
    for i, (compound_name, stint_length) in enumerate(strategy): # a for loop to iterate through the strategy list
        compound = COMPOUNDS[compound_name] # a variable that refrences the compound dictionary in tires.py from the tulpe in stratgey 
        for tire_age in range(stint_length): # a for loop to iterate through the stint length of the strategy list
            total_time += lap_time(compound,tire_age, rng) - FUEL_EFFECT_PER_LAP * race_lap #adds the time of each lap to the total time,and subtract it based on the fuel effect per lap and the current race lap number, using
            #using the lap_time function from tires.py
            race_lap += 1 # increments the race lap number

    
        is_last_stint = (i == len(strategy) - 1) # a variable that checks if the current stint is the last stint in the strategy list
        if not is_last_stint: # if the current stint is not the last stint in the strategy list, add a pit stop time to the total time
            if  safety_car_lap is not None and abs(race_lap - safety_car_lap) <= 2: # if the current lap is the same as the safety car lap, add a pit stop time to the total time
                pit_stop_time = rng.gauss(pit_loss_mean / 2, chosen_track["pit_loss_stddev"]) # a variable that generates a random pit stop time using a Gaussian distribution with half the mean and the standard deviation defined above
            else: # if the current lap is not the same as the safety car lap, add a pit stop time to the total time
                pit_stop_time = rng.gauss(pit_loss_mean, chosen_track["pit_loss_stddev"]) # a variable that generates a random pit stop time using a Gaussian distribution with the mean and standard deviation defined above

            if traffic_start <= race_lap <= traffic_end:
                pit_stop_time += rng.gauss(TRAFFIC_PENALTY_MEAN, TRAFFIC_PENALTY_STD)    
            total_time += pit_stop_time # adds the pit stop time to the total time

          
    laps_match = race_lap == chosen_track["laps"]

    if laps_match == False:
        raise ValueError("Error: The total number of laps in the strategy does not match the race distance." )
    else:
        # simulate the race
        return total_time


print(simulate_race([("Hard", 3),("Medium", 25), ("Medium", 25)], rng, TRACKS["Italy"])) # a list of tuples that represent the tire compound and the number of laps to run on that compound
print(simulate_race([("Medium", 3), ("Hard", 50)], rng, TRACKS["Italy"]))


# --- Step 2.5 will wrap that script into a reusable simulate_race()
#     function — that's the only thing this file needs to export.
