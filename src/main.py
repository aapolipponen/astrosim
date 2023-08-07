from planet import sun, earth, bodies
from constants import day, hour
import pygame
from pygame.locals import MOUSEBUTTONDOWN, MOUSEWHEEL
from simulation import run_simulation
from display import draw_objects, init_display, get_body_screen_position
import numpy as np

def is_mouse_over_object(mouse_pos, body, focus_object, SCALE_DIST, screen, click_multiplier=5):
    body_pos_pygame = get_body_screen_position(body, focus_object, SCALE_DIST, screen)

    # Calculate approximate radius on screen using the provided multiplier
    body_radius_screen = body.radius * SCALE_DIST * click_multiplier

    # Check if mouse position is within the bounding box of the body
    return (body_pos_pygame[0] - body_radius_screen <= mouse_pos[0] <= body_pos_pygame[0] + body_radius_screen) and \
           (body_pos_pygame[1] - body_radius_screen <= mouse_pos[1] <= body_pos_pygame[1] + body_radius_screen)

def change_timestep(event, timestep_seconds, integration_method):
    adjust_amount = 1.4  # This can be changed according to how large of an adjustment you want each time
    fine_adjust_amount = 1.1  # This can be changed to how fine of an adjustment you want each time
    pause_threshold = 0.005  # The threshold for pause; timescale within (-pause_threshold, pause_threshold) means pause

    if pygame.key.get_mods() & pygame.KMOD_CTRL:  # Check if CTRL key is held down
        adjust_amount = fine_adjust_amount  # Use finer adjustment if CTRL is held down

    if pygame.key.get_mods() & pygame.KMOD_SHIFT:
        if event.y > 0:  # Scroll up
            if timestep_seconds < 0:
                timestep_seconds /= adjust_amount  # Decrease absolute value of negative timescale (going towards zero)
                if -pause_threshold < timestep_seconds < 0:
                    timestep_seconds = 0  # Stop time if within pause threshold
                    print("Time paused (from negative to zero)")
            else:
                if timestep_seconds != 0:
                    timestep_seconds *= adjust_amount  # Increase timescale
                    print("Time scale increased to", timestep_seconds)
                else:
                    timestep_seconds = pause_threshold  # Start time forward if paused
                    print("Time started moving forward from pause")

        elif event.y < 0:  # Scroll down
            if "leapfrog" in integration_method.lower():
                if timestep_seconds > 0:
                    timestep_seconds /= adjust_amount  # Decrease timescale (going towards zero)
                    if 0 < timestep_seconds < pause_threshold:
                        timestep_seconds = 0  # Stop time if within pause threshold
                        print("Time paused (from positive to zero)")
                else:
                    if timestep_seconds != 0:
                        timestep_seconds *= adjust_amount  # Increase absolute value of negative timescale (going more backwards)
                        print("Time scale increased in negative direction to", timestep_seconds)
                    else:
                        timestep_seconds = -pause_threshold  # Start time backwards if paused
                        print("Time started moving backwards from pause")

    return timestep_seconds

focus_object = sun
integration_method = 'rk4'
FULL_ORBITS = True

screen_width = 800
screen_height = 800

star_size_multiplier = 1
planet_size_multiplier = 100
moon_size_multiplier = 1

# Define the initial / default timestep value in seconds
timestep_seconds = day

zoom_factor = 1.2

# Calculate scaling factors for size and distance
SCALE_DIST = 7.5e-11  # Scale (1 meter = SCALE_DIST pixels)

screen = init_display(screen_width, screen_height)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == MOUSEWHEEL:
            if not (pygame.key.get_mods() & pygame.KMOD_SHIFT):
                if event.y > 0:  # Scroll up
                    SCALE_DIST *= zoom_factor  # Zoom in
                elif event.y < 0:  # Scroll down
                    SCALE_DIST /= zoom_factor  # Zoom out
            else:
                # Update timescale using function
                timestep_seconds = change_timestep(event, timestep_seconds, integration_method)
        elif event.type == MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            clicked_body = None

            # Print all bodies' Pygame screen positions
            for body in bodies:
                body_pygame_pos = get_body_screen_position(body, focus_object, SCALE_DIST, screen)
                print(f"{body.name}'s Pygame position: {body_pygame_pos}")

            for body in bodies:
                if is_mouse_over_object(mouse_pos, body, focus_object, SCALE_DIST, screen):
                    focus_object = body
                    clicked_body = body.name
                    break

            # Debug message
            if clicked_body:
                print(f"Clicked at {mouse_pos}. Focus changed to: {clicked_body}.")
            else:
                print(f"Clicked at {mouse_pos}. No body selected.")

            for body in bodies:
                run_simulation(timestep_seconds, integration_method)

    draw_objects(focus_object, SCALE_DIST, star_size_multiplier, planet_size_multiplier, moon_size_multiplier, FULL_ORBITS, screen)

pygame.quit()
