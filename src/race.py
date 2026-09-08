"""
race.py — simulate one full race for a given pit strategy
===========================================================

Don't write anything here yet — open GUIDE.md and follow "Step 2" from
the top. Same pattern as tires.py: tiny numbered pieces (2.1, 2.2, 2.3...)
with something to run and check after each.
"""
from tires import COMPOUNDS, lap_time

import random



# --- Step 2.2 will import COMPOUNDS and lap_time from tires.py here.

# --- Step 2.2-2.4 will build up a throwaway script below the import.

rng = random.Random(0)  # a controlled source of randomness, seeded with 0

print(simulate_race([("Medium", 3), ("Hard", 25), ("Medium", 25)], rng)) # a list of tuples that represent the tire compound and the number of laps to run on that compound
print(simulate_race([("Medium", 3), ("Hard", 50)], rng))

PIT_STOP_MEAN = 22.0 #the average time it takes to make a pit stop, in seconds

PIT_STOP_STDDEV = 1.5 #the standard deviation of the pit stop time, in seconds

def simulate_race(strategy, rng):
    total_time = 0.0 # time when the race starrs at 0.0 seconds 
    for i, (compound_name, stint_length) in enumerate(strategy): # a for loop to iterate through the strategy list
        compound = COMPOUNDS[compound_name] # a variable that refrences the compound dictionary in tires.py from the tulpe in stratgey 
        for tire_age in range(stint_length): # a for loop to iterate through the stint length of the strategy list
            total_time += lap_time(compound,tire_age, rng) #adds the time of each lap to the total time,
            #using the lap_time function from tires.py
        
        is_last_stint = (i == len(strategy) - 1) # a variable that checks if the current stint is the last stint in the strategy list
        if not is_last_stint: # if the current stint is not the last stint in the strategy list, add a pit stop time to the total time
            pit_stop_time = rng.gauss(PIT_STOP_MEAN, PIT_STOP_STDDEV) # a variable that generates a random pit stop time using a Gaussian distribution with the mean and standard deviation defined above
            total_time += pit_stop_time # adds the pit stop time to the total time

    return total_time



# --- Step 2.5 will wrap that script into a reusable simulate_race()
#     function — that's the only thing this file needs to export.
