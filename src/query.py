import json
import os
from astroquery.jplhorizons import Horizons
import numpy as np
from astropy.time import Time
from constants import AU, DAY

# Define the cache file path
CACHE_FILE = 'planet_cache.json'
CACHE_TIME_THRESHOLD = 1  # Maximum cache age in days

# Load the cache from a file if it exists
if os.path.exists(CACHE_FILE):
    with open(CACHE_FILE, 'r') as f:
        cache = json.load(f)
else:
    cache = {}

def save_cache():
    """Saves the current cache to a file."""
    with open(CACHE_FILE, 'w') as f:
        json.dump(cache, f)

def get_body_parameters(body):
    """
    Fetches the position and velocity of a specific body and updates the body object.

    Parameters:
    - body: A planet object with attributes `id`, `pos`, and `vel`.
    """
    if body.id is None:
        print(f"No Horizons ID available for {body.name}")
        return

    current_time = Time.now().jd
    cache_key = str(body.id)

    if cache_key in cache:
        cached_time, cached_data = cache[cache_key]
        time_difference = current_time - cached_time

        if time_difference <= CACHE_TIME_THRESHOLD:
            print(f"Using cached data for {body.name} (Julian Date {cached_time})")
            body.pos, body.vel = np.array(cached_data[0]), np.array(cached_data[1])
            return
        else:
            print(f"Cached data for {body.name} is outdated (Julian Date {cached_time}), fetching new data...")

    obj = Horizons(id=body.id, location='500@10', epochs=current_time, id_type=None)
    eph = obj.vectors(refplane='ecliptic')
    
    # Update the body's position and velocity in the simulation
    pos = np.array([eph['x'][0], eph['y'][0], eph['z'][0]]) * AU  # Convert from AU to meters
    vel = np.array([eph['vx'][0], eph['vy'][0], eph['vz'][0]]) * AU / DAY  # Convert from AU/day to m/s

    # Update the body and store in the cache
    body.pos = pos
    body.vel = vel
    cache[cache_key] = (current_time, (pos.tolist(), vel.tolist()))

    # Save the updated cache to a file
    save_cache()