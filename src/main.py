from planet import sun, earth, bodies
from constants import day, hour
import pygame
from simulation import run_simulation
from display import draw_objects

focus_object = sun

FULL_ORBITS = True

star_size_multiplier = 1
planet_size_multiplier = 1
moon_size_multiplier = 1

# Define the initial timescale value in seconds
timescale_seconds = day

# Calculate scaling factors for size and distance
SCALE_DIST = 2e-10  # Scale down distance by 1e9 for display (1 meter = 1e-9 pixels)

# Main simulation loop
running = True
while running:
    for body in bodies:
        run_simulation(timescale_seconds)
    draw_objects(focus_object, timescale_seconds, SCALE_DIST, star_size_multiplier, planet_size_multiplier, moon_size_multiplier, FULL_ORBITS)

pygame.quit()
