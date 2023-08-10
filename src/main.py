import pygame
import numpy as np
from planet import bodies, sun, mercury, venus, earth, mars, jupiter, saturn, uranus, neptune
from constants import year, month, week ,day, hour, minute, second, AU
from simulation import run_simulation
from display import draw_objects, display_time, init_display, clear_body_trails
from request import get_body_parameters
from utilities import is_mouse_over_body, change_timestep, zoom, change_focus
import cProfile
import threading

def custom_repl(context):
    """
    Custom REPL for interactive star management.
    
    Parameters:
    - context: Dictionary containing the local context in which to execute commands.
    """
    while True:
        try:
            # Read
            cmd = input("StarConsole >>> ")
            
            if cmd.strip() == "exit":
                print("Exiting StarConsole.")
                break

            # Evaluate (for commands that return a value like variable access)
            try:
                result = eval(cmd, context)
                if result is not None:
                    print(result)
            except:
                # If evaluation failed, then try exec (for statements that don't return a value)
                exec(cmd, context)
        
        except Exception as e:
            print(f"Error: {e}")

debug = False
profile_simulation = False

focus_object = sun

integration_method = 'rk4'

get_real_parameters = False # Get real time body positions with 1 minute accuracy positions for objects from the Nasa Horizons API

post_newtonian_correction = True

use_barnes_hut = True

FULL_ORBITS = True
draw_trail_for_empty = False

timestep_seconds = hour # Define the initial timestep value in seconds

SCALE_DIST = 1e-10 # Calculate scaling factors for size and distance

ZOOM_SPEED = 1.1  # Adjust this value to increase/decrease the zoom speed

screen_width = 800
screen_height = 800

if get_real_parameters:
    for body in bodies:
        get_body_parameters(body)

if debug:
    for body in bodies:
        print(body.name, body.pos, body.vel)
        
screen = init_display(screen_width, screen_height)

clear_body_trails()

hovered_body_name = None
mouse_pos = pygame.mouse.get_pos()  # get the current mouse position

if profile_simulation:
    def profile(profile_x_times):
        for i in range(profile_x_times):
            run_simulation(timestep_seconds, integration_method, post_newtonian_correction)
            profile_x_times-=1

    cProfile.run('profile(500)')
    exit()

def start_repl():
    custom_repl(locals())

# Start the REPL on a separate thread
repl_thread = threading.Thread(target=start_repl)
repl_thread.start()

# Main simulation loop
running = True
paused = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.key.get_pressed()[pygame.K_LSHIFT] or pygame.key.get_pressed()[pygame.K_RSHIFT] or pygame.key.get_mods() & pygame.KMOD_CTRL:  # shift is pressed
                fine_adjust_enabled = pygame.key.get_mods() & pygame.KMOD_CTRL
                if event.button == 4:  # scroll up
                    timestep_seconds = change_timestep(timestep_seconds, 'up', fine_adjust_enabled, integration_method)
                elif event.button == 5:  # scroll down
                    timestep_seconds = change_timestep(timestep_seconds, 'down', fine_adjust_enabled, integration_method)
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
    
    if not paused:        
        for body in bodies:
            run_simulation(timestep_seconds, integration_method, post_newtonian_correction)
        if debug:
            for body in bodies:
                print(body.name, body.pos, body.vel)
    
    mouse_pos = np.array(pygame.mouse.get_pos())  # Convert to numpy array for compatibility with our function

    for body in bodies:
        if is_mouse_over_body(mouse_pos, body, focus_object, SCALE_DIST, screen):
            font = pygame.font.Font(None, 36)
            text_surface = font.render(body.name, True, (255, 255, 255))  # White color, adjust as needed
            screen.blit(text_surface, (mouse_pos[0] + 10, mouse_pos[1] + 10))  # Offset a bit for better visibility    

    draw_objects(focus_object, SCALE_DIST, FULL_ORBITS, draw_trail_for_empty, screen)
    display_time(timestep_seconds, screen, paused)
    
    pygame.display.flip()
    pygame.time.wait(10)
     
pygame.quit()
