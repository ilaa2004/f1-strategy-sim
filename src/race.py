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

strategy =[("Soft", 9), ("Medium", 20), ("Hard", 38)] # a list of tuples that represent the tire compound and the number of laps to run on that compound

total_time = 0.0 # time when the race starrs at 0.0 seconds 
for compound_name, stint_length in strategy: # a for loop to iterate through the strategy list
    compound = COMPOUNDS[compound_name] # a variable that refrences the compound dictionary in tires.py from the tulpe in stratgey 
    for tire_age in range(stint_length): # a for loop to iterate through the stint length of the strategy list
        total_time += lap_time(compound,tire_age, rng) #adds the time of each lap to the total time,
        #using the lap_time function from tires.py


print(total_time)



# --- Step 2.5 will wrap that script into a reusable simulate_race()
#     function — that's the only thing this file needs to export.
