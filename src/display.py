import pygame
import numpy as np
from planet import bodies
from constants import half_rgb, year, month, day, hour, minute

def clear_body_trails():
    global body_trails
    body_trails = {body.name: [] for body in bodies}

def init_display(screen_width, screen_height):
    # Initialize Pygame and set up the display window
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
    return screen

def get_body_screen_position(body, focus_object, SCALE_DIST, screen):
    focus_pos_pygame = np.array([screen.get_width() // 2, screen.get_height() // 2])
    body_pos_scaled = (body.pos[:2] - focus_object.pos[:2]) * SCALE_DIST
    body_pos_pygame = focus_pos_pygame + body_pos_scaled
    return body_pos_pygame

def convert_seconds_to_human_readable(seconds, paused):
    if paused:
        return 'PAUSED'
    
    # Determine if input is negative
    is_negative = seconds < 0
    seconds = abs(seconds)  # Use absolute value for calculations

    years, seconds = divmod(seconds, year)
    months, seconds = divmod(seconds, month)
    days, seconds = divmod(seconds, day)
    hours, seconds = divmod(seconds, hour)
    minutes, seconds = divmod(seconds, minute)

    # Create human readable string
    human_readable = ""
    if years > 0:
        human_readable += f"{int(years)} years "
    if months > 0:
        human_readable += f"{int(months)} months "
    if days > 0:
        human_readable += f"{int(days)} days "
    if hours > 0:
        human_readable += f"{int(hours)} hours "
    if minutes > 0:
        human_readable += f"{int(minutes)} minutes "
    if seconds > 0:
        human_readable += f"{int(seconds)} seconds "
        
    # If input was negative, add negative sign to output
    if is_negative:
        human_readable = "-" + human_readable

    # If all values are zero, output should be 'PAUSED'
    if human_readable.strip() == "":
        return 'PAUSED'
    else:
        return human_readable.strip()
        
def display_time(timescale_seconds, screen, paused):
    try:
        human_readable_time = convert_seconds_to_human_readable(timescale_seconds, paused)
        font = pygame.font.Font(None, 36)
        text = font.render("Timestep: " + human_readable_time, 1, (255, 255, 255))
        
        text_rect = text.get_rect()
        screen_rect = screen.get_rect()

        text_rect.bottomleft = screen_rect.bottomleft  # Place the text in the bottom-left corner

        screen.blit(text, text_rect)
    except Exception as e:
        if "termux" in str(e).lower():
            print("Running on Termux, skipping text rendering!")
        else:
            raise e
                
def draw_trail(screen, body, body_trails, focus_object, SCALE_DIST):
    focus_pos_pygame = np.array([screen.get_width() // 2, screen.get_height() // 2])

    # Store the scaled position in trail
    body_trails[body.name].append((body.pos[:2] - focus_object.pos[:2]))

    # If not displaying full orbits, remove the oldest position if the trail is too long
    if len(body_trails[body.name]) > 50:
        body_trails[body.name].pop(0)

    # Draw the trail with a fixed color
    for i in range(1, len(body_trails[body.name])):
        # Calculate a fade factor based on the position in the trail
        fade_factor = i / len(body_trails[body.name])
        trail_color = tuple([int(c * fade_factor) for c in body.color])

        trail_start = (body_trails[body.name][i-1] * SCALE_DIST + focus_pos_pygame).astype(int)
        trail_end = (body_trails[body.name][i] * SCALE_DIST + focus_pos_pygame).astype(int)

        pygame.draw.line(screen, trail_color, tuple(trail_start), tuple(trail_end))

def draw_orbit(screen, body, focus_object, SCALE_DIST):
    body_parent = body.parent

    focus_pos_pygame = np.array([screen.get_width() // 2, screen.get_height() // 2])

    # Generate a set of theta values
    theta = np.linspace(0, 2 * np.pi, 1000)

    # Define fixed values for the semi-major axis (a) and eccentricity (e)
    a = body.semi_major_axis  # Semi-major axis
    e = body.eccentricity  # Eccentricity

    # Calculate the corresponding r values
    r = a * (1 - e**2) / (1 + e * np.cos(theta))

    # Convert polar coordinates to Cartesian coordinates
    x = r * np.cos(theta)
    y = r * np.sin(theta)

    # Adjust for the argument of periapsis
    argument_of_periapsis = body.argument_of_periapsis + np.pi / 2
    rot_matrix = np.array([[np.cos(argument_of_periapsis), -np.sin(argument_of_periapsis)],
                           [np.sin(argument_of_periapsis), np.cos(argument_of_periapsis)]])  # Rotation matrix

    coords = np.vstack((x, y))
    x, y = np.dot(rot_matrix, coords)  # Apply rotation

    parent_pos_scaled =(body_parent.pos[:2] - focus_object.pos[:2]) * SCALE_DIST
    focus_pos_pygame = (focus_pos_pygame + parent_pos_scaled).astype(int)

    # Scale and translate the coordinates
    x_pygame = (x * SCALE_DIST + focus_pos_pygame[0]).astype(int)
    y_pygame = (-y * SCALE_DIST + focus_pos_pygame[1]).astype(int)  # Flip the y-coordinate because of pygame's coordinate system

    # Draw the ellipse
    for i in range(1, len(x_pygame)):
        pygame.draw.line(screen, half_rgb(body.color), (x_pygame[i-1], y_pygame[i-1]), (x_pygame[i], y_pygame[i]))

    # Draw periapsis and apoapsis
    pygame.draw.circle(screen, (255, 0, 0), (x_pygame[np.argmin(r)], y_pygame[np.argmin(r)]), 1)  # Periapsis
    pygame.draw.circle(screen, (255, 0, 255), (x_pygame[np.argmax(r)], y_pygame[np.argmax(r)]), 1)  # Apoapsis
    
def draw_objects(focus_object, SCALE_DIST, FULL_ORBITS, draw_trail_for_empty, screen):
    focus_pos_pygame = np.array([screen.get_width() // 2, screen.get_height() // 2])
    screen.fill((0, 0, 0))

    for body in bodies:
        if FULL_ORBITS and body.parent:
            draw_orbit(screen, body, focus_object, SCALE_DIST)
        elif draw_trail_for_empty:
            draw_trail(screen, body, body_trails, focus_object, SCALE_DIST)

        # Calculate the body's position relative to the focus object
        body_pos_scaled = (body.pos[:2] - focus_object.pos[:2]) * SCALE_DIST
        body_pos_pygame = focus_pos_pygame + body_pos_scaled

        # Calculate the body's radius in pixels
        body_radius = max(1, int(body.radius * SCALE_DIST))

        # Draw the planet
        pygame.draw.circle(screen, body.color, tuple(body_pos_pygame.astype(int)), body_radius)