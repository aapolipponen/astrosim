import numpy as np
import pygame
from display import clear_body_trails

def is_mouse_over_body(mouse_pos, body, focus_object, SCALE_DIST, screen):
    focus_pos_pygame = np.array([screen.get_width() // 2, screen.get_height() // 2])
    planet_pos_scaled = (body.pos[:2] - focus_object.pos[:2]) * SCALE_DIST
    planet_pos_pygame = focus_pos_pygame + planet_pos_scaled
    
    # Calculate the screen radius of the body
    body_radius_screen = body.radius * SCALE_DIST

    # Calculate the distance between the mouse and the body's screen position
    distance = np.linalg.norm(mouse_pos - planet_pos_pygame)
    
    # Check if the mouse is within the body's screen radius
    if distance < body_radius_screen:
        mouse_over_body = True
    else:
        mouse_over_body = False
    
    return mouse_over_body

def calculate_distance(pos1, pos2):
    return ((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)**0.5

def find_closest_body(pos, bodies, SCALE_DIST, focus_object):
    closest_body = None
    min_distance = float('inf')
    focus_pos_pygame = np.array([pygame.display.get_surface().get_width() // 2, pygame.display.get_surface().get_height() // 2])

    for body in bodies:
        body_pos_scaled = (body.pos[:2] - focus_object.pos[:2]) * SCALE_DIST
        body_pos_pygame = focus_pos_pygame + body_pos_scaled
        distance = calculate_distance(pos, body_pos_pygame)

        if distance < min_distance:
            min_distance = distance
            closest_body = body

    return closest_body

def adjust_timestep(timestep_seconds, adjust_amount, direction):
    if direction == 'up':
        return timestep_seconds + adjust_amount
    else:
        return timestep_seconds - adjust_amount

def change_timestep(timestep_seconds, direction, fine_adjust, integration_method=""):    
    leapfrog = "leapfrog" in integration_method.lower()
    adjust_amount = 60 if fine_adjust else 60*60 # adjust these values as necessary

    if direction == 'up':
        timestep_seconds = adjust_timestep(timestep_seconds, adjust_amount, direction)
    elif direction == 'down':
        # check if adjusting the timestep will result in a negative value
        if not leapfrog and (timestep_seconds - adjust_amount) < 0:
            print("Cannot decrease timestep further as integration method is not reversible")
        else:
            timestep_seconds = adjust_timestep(timestep_seconds, adjust_amount, direction)

    if timestep_seconds > 0:
        print("Time scale increased to", timestep_seconds)
    elif timestep_seconds < 0:
        print("Time scale increased in negative direction to", timestep_seconds)
    elif timestep_seconds == 0:
        print("Timestep is at zero")

    return timestep_seconds

def zoom(SCALE_DIST, ZOOM_FACTOR, direction):
    if direction == 'up':
        SCALE_DIST *= ZOOM_FACTOR
    elif direction == 'down':
        SCALE_DIST /= ZOOM_FACTOR
    return SCALE_DIST

def change_focus(bodies, SCALE_DIST, focus_object):
    pos = pygame.mouse.get_pos()

    # Segregate the bodies into planets, moons, and others (with no type specified)
    planets = [body for body in bodies if body.type == "planet"]
    moons = [body for body in bodies if body.type == "moon"]
    others = [body for body in bodies if not body.type]

    # First, find the closest planet
    closest_planet = find_closest_body(pos, planets, SCALE_DIST, focus_object)

    # If no planet is found, then find the closest moon
    if closest_planet is None:
        closest_moon = find_closest_body(pos, moons, SCALE_DIST, focus_object)

        # If no moon is found, then find the closest other body
        if closest_moon is None:
            closest_other = find_closest_body(pos, others, SCALE_DIST, focus_object)
            if closest_other is not None and closest_other != focus_object:  # Check if focus_object changed
                focus_object = closest_other
                clear_body_trails()

        else:
            if closest_moon != focus_object:  # Check if focus_object changed
                focus_object = closest_moon
                clear_body_trails()

    else:
        if closest_planet != focus_object:  # Check if focus_object changed
            focus_object = closest_planet
            clear_body_trails()

    return focus_object
