import pygame
import numpy as np
from planet import SpaceObject, BODIES

# Initialize Pygame and set up the display window
pygame.init()

screen = pygame.display.set_mode((800, 800), pygame.RESIZABLE)

# Dictionary to hold planet trails
planet_trails = {planet.name: [] for planet in BODIES}

def draw_trail(screen, planet, planet_trails, focus_object, SCALE_DIST, FULL_ORBITS):
    focus_pos_pygame = np.array([screen.get_width() // 2, screen.get_height() // 2])

    # Store the scaled position in trail
    planet_trails[planet.name].append((planet.pos[:2] - focus_object.pos[:2]))

    # If not displaying full orbits, remove the oldest position if the trail is too long
    if not FULL_ORBITS and len(planet_trails[planet.name]) > 100:
        planet_trails[planet.name].pop(0)

    # Draw the trail with a fixed color
    for i in range(1, len(planet_trails[planet.name])):
        trail_color = planet.color
        trail_start = (planet_trails[planet.name][i-1] * SCALE_DIST + focus_pos_pygame).astype(int)
        trail_end = (planet_trails[planet.name][i] * SCALE_DIST + focus_pos_pygame).astype(int)
        pygame.draw.line(screen, trail_color, tuple(trail_start), tuple(trail_end))

def draw_objects(focus_object, timescale_seconds, SCALE_DIST, SUN_SCALE_MULTIPLIER, PLANET_SCALE_MULTIPLIER, MOON_SCALE_MULTIPLIER, FULL_ORBITS):
    focus_pos_pygame = np.array([screen.get_width() // 2, screen.get_height() // 2])
    screen.fill((0, 0, 0))

    for planet in BODIES:
        draw_trail(screen, planet, planet_trails, focus_object, SCALE_DIST, FULL_ORBITS)

        # Calculate the planet's position relative to the focus object
        planet_pos_scaled = (planet.pos[:2] - focus_object.pos[:2]) * SCALE_DIST         
        planet_pos_pygame = focus_pos_pygame + planet_pos_scaled

        # Draw the trail for the planet
        draw_trail(screen, planet, planet_trails, focus_object, SCALE_DIST, FULL_ORBITS)

        # Choose the size multiplier based on the object type
        if planet.object_type == 'sun':
            size_multiplier = SUN_SIZE_MULTIPLIER
        elif planet.object_type == 'planet':
            size_multiplier = PLANET_SIZE_MULTIPLIER
        elif planet.object_type == 'moon':
            size_multiplier = MOON_SIZE_MULTIPLIER
        else:
            size_multiplier = 1  # Default multiplier

        # Calculate the planet's radius in pixels
        planet_radius = max(1, int(planet.radius * SCALE_DIST * size_multiplier)) 

        # Draw the planet
        pygame.draw.circle(screen, planet.color, tuple(planet_pos_pygame.astype(int)), planet_radius)

    pygame.display.flip()
    pygame.time.wait(10)
