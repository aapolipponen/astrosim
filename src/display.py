import pygame
import numpy as np
from planet import bodies
from constants import half_rgb, YEAR, MONTH, DAY, HOUR, MINUTE, G

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

def draw_orbit(screen, body, focus_object, SCALE_DIST):
    focus_pos_pygame = np.array([screen.get_width() // 2, screen.get_height() // 2])
    theta = np.linspace(0, 2 * np.pi, 1000)
    a = body.semi_major_axis
    e = body.eccentricity
    if a == 0:
        return  # Skip bodies without computed orbital parameters yet

    r = a * (1 - e**2) / (1 + e * np.cos(theta))

    # Base ellipse (periapsis along +x direction)
    x = r * np.cos(theta)
    y = r * np.sin(theta)

    # -------------------------------------------------------------
    # Determine orientation of the ellipse in the inertial frame.
    # Instead of relying solely on argument_of_periapsis (which may
    # be referenced to the ascending node), compute the angle of the
    # eccentricity vector projected onto the XY-plane. The
    # eccentricity vector points towards periapsis, so its azimuth
    # directly gives the required rotation.
    # -------------------------------------------------------------
    try:
        # Current position and velocity relative to parent (3-D)
        rel_pos = body.pos - body.parent.pos
        rel_vel = body.vel - body.parent.vel

        # Specific angular momentum
        h_vec = np.cross(rel_pos, rel_vel)
        mu = G * body.parent.mass
        e_vec = (np.cross(rel_vel, h_vec) - mu * rel_pos / np.linalg.norm(rel_pos)) / mu
        # Store for debugging if desired
        body.e_vector = e_vec

        # In-plane projection (XY)
        omega = np.arctan2(e_vec[1], e_vec[0])
    except Exception:
        omega = getattr(body, "argument_of_periapsis", 0)

    cos_om = np.cos(omega)
    sin_om = np.sin(omega)
    x_rot = x * cos_om - y * sin_om
    y_rot = x * sin_om + y * cos_om
 
    parent_pos_scaled = (body.parent.pos[:2] - focus_object.pos[:2]) * SCALE_DIST
    focus_pos_pygame = (focus_pos_pygame + parent_pos_scaled).astype(int)
    x_pygame = (x_rot * SCALE_DIST + focus_pos_pygame[0]).astype(int)
    y_pygame = (y_rot * SCALE_DIST + focus_pos_pygame[1]).astype(int)
 
    for i in range(1, len(x_pygame)):
        pygame.draw.line(screen, half_rgb(body.color), (x_pygame[i-1], y_pygame[i-1]), (x_pygame[i], y_pygame[i]))
 
    # Draw periapsis (closest point) and apoapsis (farthest point)
    pygame.draw.circle(screen, (255, 0, 0), (x_pygame[np.argmin(r)], y_pygame[np.argmin(r)]), 1)
    pygame.draw.circle(screen, (255, 0, 255), (x_pygame[np.argmax(r)], y_pygame[np.argmax(r)]), 1)
                                
def draw_gravity_field(screen, body, focus_object, SCALE_DIST, gravity_multiplier=10, smooth=False):
    focus_pos_pygame = np.array([screen.get_width() // 2, screen.get_height() // 2])
    body_pos_scaled = (body.pos[:2] - focus_object.pos[:2]) * SCALE_DIST
    body_pos_pygame = focus_pos_pygame + body_pos_scaled

    # Define the area around the body to visualize the gravity field
    field_radius = int(body.radius * SCALE_DIST * 30)  # Increase the multiplier for a larger field
    grid_size = 50  # Fewer points for faster calculation, interpolate to smooth

    # Create grid coordinates relative to the body's position
    x = np.linspace(-field_radius, field_radius, grid_size)
    y = np.linspace(-field_radius, field_radius, grid_size)
    xv, yv = np.meshgrid(x, y)

    # Calculate distance from the body
    distances = np.sqrt(xv**2 + yv**2) / SCALE_DIST

    # Calculate gravity strength, adding a small constant to avoid division by zero
    with np.errstate(divide='ignore', invalid='ignore'):
        gravity_field = gravity_multiplier * (G * body.mass) / (distances**2 + 1e-10)

    # Handle NaN and infinite values
    gravity_field = np.nan_to_num(gravity_field, nan=0.0, posinf=0.0, neginf=0.0)

    # Normalize the gravity field to [0, 1]
    max_gravity = np.max(gravity_field)
    if max_gravity > 0:
        gravity_field /= max_gravity

    if smooth:
        # Interpolated smooth color transitions
        for i in range(grid_size - 1):
            for j in range(grid_size - 1):
                color_intensity = int(255 * gravity_field[i, j])
                color = (color_intensity, color_intensity, 0)  # Yellowish color for gravity

                # Four corners of each grid cell
                points = [
                    body_pos_pygame + np.array([xv[i, j], yv[i, j]]),
                    body_pos_pygame + np.array([xv[i + 1, j], yv[i + 1, j]]),
                    body_pos_pygame + np.array([xv[i, j + 1], yv[i, j + 1]]),
                    body_pos_pygame + np.array([xv[i + 1, j + 1], yv[i + 1, j + 1]]),
                ]
                pygame.draw.polygon(screen, color, points)
    else:
        # Draw dots
        for i in range(grid_size):
            for j in range(grid_size):
                color_intensity = int(255 * gravity_field[i, j])
                color = (color_intensity, color_intensity, 0)  # Yellowish color for gravity

                # Position on the screen
                field_pos_pygame = body_pos_pygame + np.array([xv[i, j], yv[i, j]])
                screen.set_at(tuple(field_pos_pygame.astype(int)), color)
                
def draw_objects(focus_object, SCALE_DIST, FULL_ORBITS, draw_trail_for_empty, screen, fade_trails, display_names, gravity_field=False):
    focus_pos_pygame = np.array([screen.get_width() // 2, screen.get_height() // 2])
    screen.fill((0, 0, 0))

    for body in bodies:
        relative_pos = body.pos[:2] - focus_object.pos[:2]
        body_pos_scaled = relative_pos * SCALE_DIST
        body_pos_pygame = focus_pos_pygame + body_pos_scaled

        # Draw the gravity field around each body
        if gravity_field:
            draw_gravity_field(screen, body, focus_object, SCALE_DIST, gravity_multiplier=10)

        if FULL_ORBITS and body.parent:
            draw_orbit(screen, body, focus_object, SCALE_DIST)
        elif draw_trail_for_empty:
            draw_trail(screen, body, body_trails, focus_object, fade_trails, SCALE_DIST)

        # Calculate the body's radius in pixels
        body_radius = max(1, int(body.radius * SCALE_DIST))

        # Draw the planet
        pygame.draw.circle(screen, body.color, tuple(body_pos_pygame.astype(int)), body_radius)
        
        # Draw the planet's name if display_names is True
        if display_names:
            font = pygame.font.Font(None, 24)
            text = font.render(body.name, True, (255, 255, 255))
            text_rect = text.get_rect(center=(body_pos_pygame[0], body_pos_pygame[1] - body_radius - 10))
            screen.blit(text, text_rect)