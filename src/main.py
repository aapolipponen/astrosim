import pygame
import numpy as np
#from load_scenario import load_scenario
from planet import *
from constants import YEAR, MONTH, WEEK, DAY, HOUR, MINUTE, SECOND
from simulation import run_simulation
from query import get_body_parameters
from display import draw_objects, display_time, init_display, clear_body_trails
#from request import get_body_parameters
from utilities import is_mouse_over_body, change_timestep, zoom, change_focus
from starconsole import custom_repl
import cProfile
import threading
import os

focus_object = Sun

debug = False
debug_2 = True
profile_simulation = False
starconsole = True  # Enable console by default

integration_method = 'rk4'

get_real_parameters = True # Get real time body positions with 1 minute accuracy positions for objects from the Nasa Horizons API

post_newtonian_correction = False
barnes_hut = False

fade_trails = False
draw_trail_for_empty = True
FULL_ORBITS = False
display_names = True
gravity_field = False  # Gravity field visualization

timestep_seconds = HOUR / 8 # Define the initial timestep value in seconds
SCALE_DIST = 5e-10 # Calculate scaling factors for size and distance
ZOOM_SPEED = 1.2  # Adjust this value to increase/decrease the zoom speed
screen_width = 1920
screen_height = 1080
gravity_enabled = True  # Default gravity state

if get_real_parameters:
    from query import get_body_parameters

    for body in bodies:
        get_body_parameters(body)
        if debug:
            print(f"Updated {body.name}: Position = {body.pos}, Velocity = {body.vel}")

if debug:
    for body in bodies:
        print(body.name, body.pos, body.vel)

screen = init_display(screen_width, screen_height)

clear_body_trails()

hovered_body_name = None
mouse_pos = pygame.mouse.get_pos()  # get the current mouse position

"""# Button properties
button_color = (255, 0, 0)  # Red color
button_hover_color = (200, 0, 0)  # Darker red when hovered
button_rect = pygame.Rect(10, 10, 100, 50)  # Button rectangle

def draw_button(screen, button_rect, button_color):
    pygame.draw.rect(screen, button_color, button_rect)
    font = pygame.font.Font(None, 36)
    text_surface = font.render("POISTA AURINKO", True, (255, 255, 255))  # White text
    screen.blit(text_surface, (button_rect.x + 10, button_rect.y + 10))"""

if profile_simulation:
    def profile(profile_x_times):
        for i in range(profile_x_times):
            run_simulation(timestep_seconds, integration_method, FULL_ORBITS, gravity_enabled)
            profile_x_times-=1

    cProfile.run('profile(500)')
    exit()

# Create a context dictionary that will be updated with simulation state
sim_context = {
    'bodies': bodies,
    'timestep_seconds': timestep_seconds,
    'SCALE_DIST': SCALE_DIST,
    'focus_object': focus_object,
    'paused': False,
    'running': True,
    'gravity_enabled': gravity_enabled,
    'integration_method': integration_method,
    'FULL_ORBITS': FULL_ORBITS,
    'display_names': display_names,
    'fade_trails': fade_trails,
    'draw_trail_for_empty': draw_trail_for_empty,
    'gravity_field': gravity_field,
    'Sun': Sun,
    'Earth': Earth,
    'Mercury': Mercury,
    'Venus': Venus,
    'Mars': Mars,
    'Jupiter': Jupiter,
    'Saturn': Saturn,
    'Uranus': Uranus,
    'Neptune': Neptune,
    'Moon': Moon,
    'Voyager1': Voyager1,
    'Voyager2': Voyager2,
    # Add utility functions
    'change_timestep': change_timestep,
    'zoom': zoom,
    'change_focus': change_focus,
    'clear_body_trails': clear_body_trails,
    # Add common imports for convenience
    'np': np,
    'numpy': np,
    'pygame': pygame,
}

if starconsole:
    def start_repl():
        # Update context with current locals
        sim_context.update(locals())
        custom_repl(sim_context)
        
    # Start the REPL on a separate thread
    repl_thread = threading.Thread(target=start_repl, daemon=True)
    repl_thread.start()

# Main simulation loop
running = True
paused = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            """if button_rect.collidepoint(event.pos):
                bodies.remove(aurinko)"""
            if pygame.key.get_pressed()[pygame.K_LSHIFT] or pygame.key.get_pressed()[pygame.K_RSHIFT] or pygame.key.get_mods() & pygame.KMOD_CTRL:  # shift is pressed
                fine_adjust_enabled = pygame.key.get_mods() & pygame.KMOD_CTRL
                if event.button == 4:  # scroll up
                    timestep_seconds = change_timestep(timestep_seconds, 'up', fine_adjust_enabled, debug, integration_method)
                elif event.button == 5:  # scroll down
                    timestep_seconds = change_timestep(timestep_seconds, 'down', fine_adjust_enabled, debug, integration_method)
            elif event.button == 4:  # scroll up
                SCALE_DIST = zoom(SCALE_DIST, ZOOM_SPEED, 'up')
            elif event.button == 5:  # scroll down
                SCALE_DIST = zoom(SCALE_DIST, ZOOM_SPEED, 'down')
            elif event.button == 1:
                focus_object = change_focus(bodies, SCALE_DIST, focus_object)
        elif event.type == pygame.KEYDOWN:
            # Space key pauses the game
            if event.key == pygame.K_SPACE:
                paused = not paused  # Toggle paused state
            elif event.key == pygame.K_F12:
                # Create a folder if it doesn't exist
                if debug_2:
                    print("Screenshot key pressed")
                if not os.path.exists("screenshots"):
                    os.mkdir("screenshots")
                screenshot_folder = "screenshots"
                screenshot_name = os.path.join(screenshot_folder, "screenshot.png")

                if os.path.exists(screenshot_name):
                    index = 1
                    while os.path.exists(os.path.join(screenshot_folder, f"screenshot_{index}.png")):
                        index += 1
                    screenshot_name = os.path.join(screenshot_folder, f"screenshot_{index}.png")

                pygame.image.save(screen, screenshot_name)
                
                if debug_2:
                    print("Took screnshot")
            # Zoom controls with keyboard
            elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS or event.key == pygame.K_KP_PLUS:
                # Zoom in: +, =, or numpad +
                SCALE_DIST = zoom(SCALE_DIST, ZOOM_SPEED, 'up')
            elif event.key == pygame.K_MINUS or event.key == pygame.K_KP_MINUS:
                # Zoom out: - or numpad -
                SCALE_DIST = zoom(SCALE_DIST, ZOOM_SPEED, 'down')
            elif event.key == pygame.K_i:
                # Zoom in: i key
                SCALE_DIST = zoom(SCALE_DIST, ZOOM_SPEED, 'up')
            elif event.key == pygame.K_o:
                # Zoom out: o key
                SCALE_DIST = zoom(SCALE_DIST, ZOOM_SPEED, 'down')
            elif event.key == pygame.K_PAGEUP:
                # Zoom in: Page Up
                SCALE_DIST = zoom(SCALE_DIST, ZOOM_SPEED, 'up')
            elif event.key == pygame.K_PAGEDOWN:
                # Zoom out: Page Down
                SCALE_DIST = zoom(SCALE_DIST, ZOOM_SPEED, 'down')

    # Sync with console: read console changes first, then update context
    if starconsole:
        # Read console-modified values first (before overwriting)
        timestep_seconds = sim_context.get('timestep_seconds', timestep_seconds)
        SCALE_DIST = sim_context.get('SCALE_DIST', SCALE_DIST)
        focus_object = sim_context.get('focus_object', focus_object)
        paused = sim_context.get('paused', paused)
        running = sim_context.get('running', running)
        gravity_enabled = sim_context.get('gravity_enabled', gravity_enabled)
        FULL_ORBITS = sim_context.get('FULL_ORBITS', FULL_ORBITS)
        fade_trails = sim_context.get('fade_trails', fade_trails)
        draw_trail_for_empty = sim_context.get('draw_trail_for_empty', draw_trail_for_empty)
        display_names = sim_context.get('display_names', display_names)
        gravity_field = sim_context.get('gravity_field', gravity_field)
        
        # Now update context with current simulation state (for console to read)
        sim_context.update({
            'bodies': bodies,
            'timestep_seconds': timestep_seconds,
            'SCALE_DIST': SCALE_DIST,
            'focus_object': focus_object,
            'paused': paused,
            'running': running,
            'gravity_enabled': gravity_enabled,
            'FULL_ORBITS': FULL_ORBITS,
            'fade_trails': fade_trails,
            'draw_trail_for_empty': draw_trail_for_empty,
            'display_names': display_names,
            'gravity_field': gravity_field,
        })
    
    if not paused:
        for body in bodies:
            run_simulation(timestep_seconds, integration_method, FULL_ORBITS, gravity_enabled)
        if debug:
            for body in bodies:
                print(body.name, body.pos, body.vel)

    # Draw everything
    draw_objects(focus_object, SCALE_DIST, FULL_ORBITS, draw_trail_for_empty, screen, fade_trails, display_names, gravity_field)
    display_time(timestep_seconds, screen, paused)
    
    """# Draw the button
    mouse_pos = pygame.mouse.get_pos()
    if button_rect.collidepoint(mouse_pos):
        current_button_color = button_hover_color
    else:
        current_button_color = button_color
    draw_button(screen, button_rect, current_button_color)"""
    
    pygame.display.flip()
    pygame.time.wait(10)

pygame.quit()