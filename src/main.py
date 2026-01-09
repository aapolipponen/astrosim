import pygame
import numpy as np
import threading
import os
import time

from planet import *
from constants import YEAR, MONTH, WEEK, DAY, HOUR, MINUTE, SECOND
from simulation import run_simulation
from display import draw_objects, display_time, init_display, clear_body_trails
from utilities import zoom, change_focus
from starconsole import custom_repl

# Config
focus_object = Sun
integration_method = "leapfrog"
gravity_enabled = True
FULL_ORBITS = True
display_names = True
gravity_field = True
fade_trails = False
draw_trail_for_empty = True

# Physics
dt_phys = 300.0 # Fixed physics timestep (seconds)
steps_per_frame = 1

adaptive_physics = True

# PID / CPU budget (seconds)
TARGET_PHYSICS_TIME = 0.004
MAX_PHYSICS_TIME = 0.006

MIN_STEPS = 1
MAX_STEPS = 2_000_000
MIN_DT = 1.0
MAX_DT = DAY

# Rendering
SCALE_DIST = 5e-10
ZOOM_SPEED = 1.2
screen_width = 1920
screen_height = 1080

# Tools
starconsole = True
debug = False

# Initialization
screen = init_display(screen_width, screen_height)
clear_body_trails()

paused = False
running = True

# Starconsole context
sim_context = {
    'bodies': bodies,
    'dt_phys': dt_phys,
    'steps_per_frame': steps_per_frame,
    'adaptive_physics': adaptive_physics,
    'integration_method': integration_method,
    'gravity_enabled': gravity_enabled,
    'SCALE_DIST': SCALE_DIST,
    'focus_object': focus_object,
    'paused': paused,
    'running': running,
    'FULL_ORBITS': FULL_ORBITS,
    'display_names': display_names,
    'gravity_field': gravity_field,
    'np': np,
    'pygame': pygame,
}

if starconsole:
    def start_repl():
        custom_repl(sim_context)

    threading.Thread(target=start_repl, daemon=True).start()

# Main loop
clock = pygame.time.Clock()

while running:
    user_changed = set()

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            user_changed.add('running')

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mods = pygame.key.get_mods()

            # Manual time controls
            if not adaptive_physics:

                # steps_per_frame
                if mods & pygame.KMOD_SHIFT and not mods & pygame.KMOD_CTRL:
                    if event.button == 4:
                        steps_per_frame = min(steps_per_frame * 2, MAX_STEPS)
                    elif event.button == 5:
                        steps_per_frame = max(MIN_STEPS, steps_per_frame // 2)
                    user_changed.add('steps_per_frame')

                # dt_phys
                elif mods & pygame.KMOD_CTRL:
                    factor = 1.05 if mods & pygame.KMOD_SHIFT else 1.25
                    if event.button == 4:
                        dt_phys = min(MAX_DT, dt_phys * factor)
                    elif event.button == 5:
                        dt_phys = max(MIN_DT, dt_phys / factor)
                    user_changed.add('dt_phys')

            # Zoom
            elif event.button == 4:
                SCALE_DIST = zoom(SCALE_DIST, ZOOM_SPEED, 'up')
                user_changed.add('SCALE_DIST')
            elif event.button == 5:
                SCALE_DIST = zoom(SCALE_DIST, ZOOM_SPEED, 'down')
                user_changed.add('SCALE_DIST')

            # Focus
            elif event.button == 1:
                focus_object = change_focus(bodies, SCALE_DIST, focus_object)
                user_changed.add('focus_object')

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = not paused
                user_changed.add('paused')

            elif event.key == pygame.K_F12:
                os.makedirs("screenshots", exist_ok=True)
                fname = f"screenshots/screenshot_{pygame.time.get_ticks()}.png"
                pygame.image.save(screen, fname)
                print(f"Saved {fname}")

    # Console sync
    if starconsole:
        if 'dt_phys' not in user_changed:
            dt_phys = sim_context.get('dt_phys', dt_phys)
        if 'steps_per_frame' not in user_changed:
            steps_per_frame = sim_context.get('steps_per_frame', steps_per_frame)
        adaptive_physics = sim_context.get('adaptive_physics', adaptive_physics)
        integration_method = sim_context.get('integration_method', integration_method)
        gravity_enabled = sim_context.get('gravity_enabled', gravity_enabled)

        sim_context.update({
            'dt_phys': dt_phys,
            'steps_per_frame': steps_per_frame,
            'adaptive_physics': adaptive_physics,
            'paused': paused,
            'running': running,
        })

    # Physics
    if not paused:
        start = time.perf_counter()
        steps_done = 0

        while steps_done < steps_per_frame:
            run_simulation(dt_phys, integration_method, FULL_ORBITS, gravity_enabled)
            steps_done += 1

            if adaptive_physics and time.perf_counter() - start > MAX_PHYSICS_TIME:
                break

        physics_time = time.perf_counter() - start

        # Adaptive control
        if adaptive_physics:
            if physics_time > MAX_PHYSICS_TIME:
                steps_per_frame = max(MIN_STEPS, int(steps_per_frame * 0.7))
            elif physics_time < TARGET_PHYSICS_TIME:
                steps_per_frame = min(MAX_STEPS, int(steps_per_frame * 1.1) + 1)

    # Render
    draw_objects(
        focus_object,
        SCALE_DIST,
        FULL_ORBITS,
        draw_trail_for_empty,
        screen,
        fade_trails,
        display_names,
        gravity_field
    )

    simulated_seconds = dt_phys * steps_per_frame
    display_time(simulated_seconds, screen, paused)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
