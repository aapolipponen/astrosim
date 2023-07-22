from constants import G
from planet import bodies, sun
import numpy as np

def calculate_net_force(target_body, softening = 0):
    net_force = np.array([0.0, 0.0, 0.0])
    for body in bodies:
        if body != target_body:
            r = body.pos - target_body.pos
            r_mag = np.linalg.norm(r) + softening # Added softening here
            force_mag = G * target_body.mass * body.mass / r_mag**2
            force = force_mag * r / r_mag
            net_force += force
    return net_force

def run_simulation(timescale_seconds):
    for body in bodies:
        # Half-step velocity update
        net_force = calculate_net_force(body)
        acceleration = net_force / body.mass
        body.vel += 0.5 * acceleration * timescale_seconds

        # Full-step position update
        body.pos += body.vel * timescale_seconds

        # Calculate orbital parameters relative to parent body
        if body.parent_body is not None:
            calculate_orbital_parameters(body, body.parent_body)

    for body in bodies:
        # Second half-step velocity update
        net_force = calculate_net_force(body)
        acceleration = net_force / body.mass
        body.vel += 0.5 * acceleration * timescale_seconds


def calculate_orbital_position(body, focus_object):
    # Get the position of the body relative to the focus_object
    relative_pos = body.pos[:2] - focus_object.pos[:2]

    # Calculate the angle in radians
    angle_rad = np.arctan2(relative_pos[1], relative_pos[0])

    # If you want the angle in degrees instead of radians
    angle_deg = np.degrees(angle_rad)

    return angle_rad, angle_deg

def calculate_relative_vectors(body, focus_object):
    body.relative_pos = body.pos - focus_object.pos
    body.relative_vel = body.vel - focus_object.vel

def calculate_energy_and_momentum(body, focus_object):
    body.E = 0.5 * np.dot(body.relative_vel, body.relative_vel) - G * focus_object.mass / np.linalg.norm(body.relative_pos)
    body.L = np.linalg.norm(np.cross(body.relative_pos, body.relative_vel))

def calculate_semi_major_axis(body, focus_object):
    body.semi_major_axis = -G * focus_object.mass / (2 * body.E)

def calculate_eccentricity(body, focus_object):
    # The standard gravitational parameter
    mu = G * (body.mass + focus_object.mass)
    
    # The distance between the body and the focus object
    r = np.linalg.norm(body.pos - focus_object.pos)
    
    # The speed of the body
    v = np.linalg.norm(body.vel)
    
    # The specific relative angular momentum
    h = np.linalg.norm(np.cross(body.pos - focus_object.pos, body.vel))
    
    # The specific orbital energy
    epsilon = v**2 / 2 - mu / r
    
    # The eccentricity of the orbit
    body.eccentricity = np.sqrt(1 + 2 * epsilon * h**2 / mu**2)

def calculate_semi_minor_axis(body):
    body.semi_minor_axis = body.semi_major_axis * np.sqrt(1 - body.eccentricity**2)

def calculate_orbital_parameters(body, focus_object):
    calculate_relative_vectors(body, focus_object)
    calculate_energy_and_momentum(body, focus_object)
    calculate_semi_major_axis(body, focus_object)
    calculate_eccentricity(body, focus_object)
    calculate_semi_minor_axis(body)
