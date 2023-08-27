import pygame
import numpy as np
from planets import bodies
from constants import half_rgb, lighten_rgb_hsl, YEAR, MONTH, DAY, HOUR, MINUTE

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

    years, seconds = divmod(seconds, YEAR)
    months, seconds = divmod(seconds, MONTH)
    days, seconds = divmod(seconds, DAY)
    hours, seconds = divmod(seconds, HOUR)
    minutes, seconds = divmod(seconds, MINUTE)

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
                
def draw_trail(screen, body, body_trails, focus_object, fade_trails, SCALE_DIST):
    focus_pos_pygame = np.array([screen.get_width() // 2, screen.get_height() // 2])

    # Store the scaled position in trail
    body_trails[body.name].append((body.pos[:2] - focus_object.pos[:2]))

    # If not displaying full orbits, remove the oldest position if the trail is too long
    if fade_trails:
        if len(body_trails[body.name]) > 5:
            body_trails[body.name].pop(0)

    # Draw the trail with a fixed color
    for i in range(1, len(body_trails[body.name])):
        if fade_trails:
            # Calculate a fade factor based on the position in the trail
            fade_factor = i / len(body_trails[body.name])
            trail_color = tuple([int(c * fade_factor) for c in body.color])
        
        trail_color = body.color
        trail_start = (body_trails[body.name][i-1] * SCALE_DIST + focus_pos_pygame).astype(int)
        trail_end = (body_trails[body.name][i] * SCALE_DIST + focus_pos_pygame).astype(int)

        pygame.draw.line(screen, trail_color, tuple(trail_start), tuple(trail_end))

def draw_orbit(screen, body, focus_object, SCALE_DIST, _iterations=[0]):
    focus_pos_pygame = np.array([screen.get_width() // 2, screen.get_height() // 2])
    theta = np.linspace(0, 2 * np.pi, 1000)
    
    a = body.semi_major_axis
    e = body.eccentricity
    
    r = a * (1 - e**2) / (1 + e * np.cos(theta))
    x = r * np.cos(theta)
    y = r * np.sin(theta)

    # Rotate the orbit by the argument of periapsis
    rotation_theta = body.argument_of_periapsis

    rotation_matrix = np.array([[np.cos(rotation_theta), -np.sin(rotation_theta)], 
                                [np.sin(rotation_theta),  np.cos(rotation_theta)]])
    
    rotated_coords = np.dot(rotation_matrix, np.vstack([x, y]))
    x, y = rotated_coords[0], rotated_coords[1]
    
    parent_pos_scaled = (body.parent.pos[:2] - focus_object.pos[:2]) * SCALE_DIST
    focus_pos_pygame = (focus_pos_pygame + parent_pos_scaled).astype(int)
    
    x *= SCALE_DIST
    x += focus_pos_pygame[0]
    y *= -SCALE_DIST
    y += focus_pos_pygame[1]

    x_pygame = np.where(np.isnan(x), 0, x).astype(int)
    y_pygame = np.where(np.isnan(y), 0, y).astype(int)
    
    for i in range(1, len(x_pygame)):
        pygame.draw.line(screen, half_rgb(body.color), (x_pygame[i-1], y_pygame[i-1]), (x_pygame[i], y_pygame[i]))
    
    pygame.draw.circle(screen, (255, 0, 0), (x_pygame[np.argmin(r)], y_pygame[np.argmin(r)]), 1)
    pygame.draw.circle(screen, (255, 0, 255), (x_pygame[np.argmax(r)], y_pygame[np.argmax(r)]), 1)

    # Iteration counter and update logic
    update_threshold = 60  # For example, update every 60 calls
    _iterations[0] += 1
    if _iterations[0] >= update_threshold:
        body.update_orbital_elements_from_state_vectors()
        _iterations[0] = 0

def draw_gradual_transparency(screen, center, start_radius, thickness, color):
    a = 255  # Initial transparency
    b = 0.1  # Decay rate. Adjust this value to change the fade speed
    
    for offset in range(thickness):
        radius = start_radius + offset
        alpha = int(a * np.exp(-b * offset))
        temp_surface = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
        pygame.draw.circle(temp_surface, (*color, alpha), center, radius)
        screen.blit(temp_surface, (0, 0))

def draw_objects(focus_object, SCALE_DIST, FULL_ORBITS, draw_trail_for_empty, screen, fade_trails):
    focus_pos_pygame = np.array([screen.get_width() // 2, screen.get_height() // 2])
    screen.fill((0, 0, 0))

    for body in bodies:
        relative_pos = body.pos[:2] - focus_object.pos[:2]
        body_pos_scaled = relative_pos * SCALE_DIST
        body_pos_pygame = focus_pos_pygame + body_pos_scaled

        if FULL_ORBITS and body.parent:
            draw_orbit(screen, body, focus_object, SCALE_DIST)
        elif draw_trail_for_empty:
            draw_trail(screen, body, body_trails, focus_object, fade_trails, SCALE_DIST)

        # Calculate the body's radius in pixels
        body_radius = max(1, int(body.radius * SCALE_DIST))

        # Draw the atmosphere if the body has one
        if hasattr(body, 'atmosphere') and body.atmosphere:
            atmosphere_thickness = int(500 * body.atmosphere.scale_height * SCALE_DIST * 0.1)
            atmosphere_color = lighten_rgb_hsl(body.color)  # Some light blue color without alpha
            
            draw_gradual_transparency(screen, tuple(body_pos_pygame.astype(int)), body_radius, atmosphere_thickness, atmosphere_color)

        # Draw the planet
        pygame.draw.circle(screen, body.color, tuple(body_pos_pygame.astype(int)), body_radius)