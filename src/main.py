from planet import SpaceObject, BODIES, PLANETS, sun, earth, jupiter, mars
import pygame
from simulation import run_simulation
from display import draw_objects

focus_object = sun

FULL_ORBITS = True

SUN_SCALE_MULTIPLIER = 1
PLANET_SCALE_MULTIPLIER = 1
MOON_SCALE_MULTIPLIER = 1

# Define the initial timescale value in seconds
timescale_seconds = 60 * 60

# Calculate scaling factors for size and distance
SCALE_DIST = 2e-10  # Scale down distance by 1e9 for display (1 meter = 1e-9 pixels)

# Main simulation loop
running = True
while running:
    for SpaceObject in BODIES:
        run_simulation(timescale_seconds)
    draw_objects(focus_object, timescale_seconds, SCALE_DIST, SUN_SCALE_MULTIPLIER, PLANET_SCALE_MULTIPLIER, MOON_SCALE_MULTIPLIER, FULL_ORBITS)

pygame.quit()
