from constants import G
from planet import SpaceObject, BODIES
import numpy as np

def calculate_net_force(target_body, softening = 0):
    net_force = np.array([0.0, 0.0, 0.0])
    for body in BODIES:
        if body != target_body:
            r = body.pos - target_body.pos
            r_mag = np.linalg.norm(r) + softening # Added softening here
            force_mag = G * target_body.mass * body.mass / r_mag**2
            force = force_mag * r / r_mag
            net_force += force
    return net_force

def run_simulation(timescale_seconds):
    for body in BODIES:
        # Half-step velocity update
        net_force = calculate_net_force(body)
        acceleration = net_force / body.mass
        body.vel += 0.5 * acceleration * timescale_seconds

        # Full-step position update
        body.pos += body.vel * timescale_seconds

    for body in BODIES:
        # Second half-step velocity update
        net_force = calculate_net_force(body)
        acceleration = net_force / body.mass
        body.vel += 0.5 * acceleration * timescale_seconds
