"""
tires.py — Tire degradation model
==================================

Don't write anything here yet — open GUIDE.md and follow "Step 1" from the
top. It walks through this file one tiny piece at a time (1.1, 1.2, 1.3...)
and tells you exactly what to type at each point. This file will fill in
gradually as you go — it's normal for it to stay broken/incomplete for a
while.
"""

# --- Step 1.1 will define a plain number here for the Soft compound's
#     fresh-tire lap time. Nothing to do yet — see GUIDE.md.

#SOFT_BASE_LAPTIME = 92.0 #time in seconds for a fresh soft tire


# --- Step 1.2 will turn that into a function.
# --- Step 1.3 will add tire wear (degradation) to the function.
#def soft_lap_time(tire_age_laps):
    #degradtion_per_lap = 0.15 # seconds per lap of degradation
    # u get the performance of the tire by adding the base lap time 
    # to the degradation per lap multiplied by the age of the tire in laps
   #return SOFT_BASE_LAPTIME + degradtion_per_lap * tire_age_laps

# --- Step 1.4 will generalize it to handle Soft/Medium/Hard instead of
#     just one compound.
# --- Step 1.5 will add randomness (this is the part that makes it a
#     "Monte Carlo" simulation later).
SOFT = {"name": "Soft", "base_lap_time": 92.0, "degradation_per_lap": 0.15}
MEDIUM = {"name": "Medium", "base_lap_time": 93.0, "degradation_per_lap": 0.10}
HARD = {"name": "Hard", "base_lap_time": 94.0, "degradation_per_lap": 0.05}

def lap_time(compound, tire_age_laps, rng):
    predictable_part = compound["base_lap_time"] + compound["degradation_per_lap"] * tire_age_laps
    noise_size = 0.02 * max(tire_age_laps, 1) # Standard deviation of the noise
    noise = rng.gauss(0, noise_size)  # Generate random noise
    return predictable_part + noise  # Add noise to the predictable part
    #first perameter refrence back to the dictionary for the 
    #base lap time and degrataion, and lap age is written by the user to determine 
    #how many laps the tire has been used for.


#rng = random.Random(0)  
#a controlled source of randomness, seeded with 0
#print(rng.gauss(0, 1))
#a random number centered on 0, "spread" of 1

