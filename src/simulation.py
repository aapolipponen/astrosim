from constants import G
from planet import bodies, sun
import numpy as np

def calculate_net_force(target_body):
    net_force = np.array([0.0, 0.0, 0.0])
    for body in bodies:
        if body != target_body:
            r = body.pos - target_body.pos
            r_mag = np.linalg.norm(r)
            force_mag = G * target_body.mass * body.mass / r_mag**2
            force = force_mag * r / r_mag
            net_force += force
    return net_force

def euler_integration(body, timescale_seconds):
    pos_derivative, vel_derivative = derivatives(body, body.pos, body.vel)
    body.pos += pos_derivative * timescale_seconds
    body.vel += vel_derivative * timescale_seconds

def orbital_elements_integration(body, focus_object, timescale_seconds):
    # Retrieve the orbital elements
    a, e, i, omega, w, M = get_orbital_elements(body, focus_object)

    # Update mean anomaly based on mean motion
    n = np.sqrt(G * (body.mass + focus_object.mass) / a**3)
    M += n * timescale_seconds

    # Solve Kepler's equation for eccentric anomaly (E) using M and e
    E = solve_keplers_equation(M, e)

    # Calculate true anomaly (f)
    f = 2 * np.arctan2(np.sqrt(1 + e) * np.tan(E / 2), np.sqrt(1 - e))

    # Calculate r, the distance from the focus object
    r = a * (1 - e * np.cos(E))

    # Update position and velocity using f, r, and other orbital elements
    update_body_state_from_orbital_elements(body, focus_object, r, f, w, omega, i)

    # You can also update the orbital elements if needed for the next step
    update_orbital_elements(body, focus_object)

def midpoint_integration(body, timescale_seconds):
    k1_pos, k1_vel = derivatives(body, body.pos, body.vel)
    k1_pos *= timescale_seconds
    k1_vel *= timescale_seconds

    k2_pos, k2_vel = derivatives(body, body.pos + 0.5 * k1_pos, body.vel + 0.5 * k1_vel)
    k2_pos *= timescale_seconds
    k2_vel *= timescale_seconds

    body.pos += k2_pos
    body.vel += k2_vel

def heun_integration(body, timescale_seconds):
    k1_pos, k1_vel = derivatives(body, body.pos, body.vel)
    k1_pos *= timescale_seconds
    k1_vel *= timescale_seconds

    k2_pos, k2_vel = derivatives(body, body.pos + k1_pos, body.vel + k1_vel)
    k2_pos *= timescale_seconds
    k2_vel *= timescale_seconds

    body.pos += 0.5 * (k1_pos + k2_pos)
    body.vel += 0.5 * (k1_vel + k2_vel)

def rk4_integration(body, timescale_seconds):
    k1_pos, k1_vel = derivatives(body, body.pos, body.vel)
    k1_pos *= timescale_seconds
    k1_vel *= timescale_seconds

    k2_pos, k2_vel = derivatives(body, body.pos + 0.5 * k1_pos, body.vel + 0.5 * k1_vel)
    k2_pos *= timescale_seconds
    k2_vel *= timescale_seconds

    k3_pos, k3_vel = derivatives(body, body.pos + 0.5 * k2_pos, body.vel + 0.5 * k2_vel)
    k3_pos *= timescale_seconds
    k3_vel *= timescale_seconds

    k4_pos, k4_vel = derivatives(body, body.pos + k3_pos, body.vel + k3_vel)
    k4_pos *= timescale_seconds
    k4_vel *= timescale_seconds

    body.pos += (k1_pos + 2 * k2_pos + 2 * k3_pos + k4_pos) / 6
    body.vel += (k1_vel + 2 * k2_vel + 2 * k3_vel + k4_vel) / 6

def verlet_integration(body, timescale_seconds):
    # Compute current acceleration
    net_force = calculate_net_force(body)
    acceleration = net_force / body.mass

    # Compute new position using current velocity and acceleration
    new_pos = body.pos + body.vel * timescale_seconds + 0.5 * acceleration * timescale_seconds**2

    # Compute new acceleration based on new position
    body.pos = new_pos
    new_net_force = calculate_net_force(body)
    new_acceleration = new_net_force / body.mass

    # Compute new velocity using average acceleration
    body.vel += 0.5 * (acceleration + new_acceleration) * timescale_seconds

def leapfrog_integration(body, timescale_seconds):
    # Half-step velocity update
    net_force = calculate_net_force(body)
    acceleration = net_force / body.mass
    body.vel += 0.5 * acceleration * timescale_seconds

    # Full-step position update
    body.pos += body.vel * timescale_seconds

    # Second half-step velocity update
    net_force = calculate_net_force(body)
    acceleration = net_force / body.mass
    body.vel += 0.5 * acceleration * timescale_seconds

def get_integrator(method):
    integrators = {
        'euler': euler_integration, # Simple and computationally efficient but can suffer from numerical instability. Often less accurate, especially for stiff systems or long simulations.
        'midpoint': midpoint_integration, # Similar to Euler but takes the average of the initial and midpoint derivatives, improving accuracy. Still might not be suitable for stiff problems.
        'heun': heun_integration, # A predictor-corrector method that's an improved version of the Euler method. It's more accurate but still simple and efficient.
        'rk4': rk4_integration, # Fourth-order Runge-Kutta method. A well-balanced choice for many problems, offering good accuracy and stability. More computationally expensive than Euler but widely used in various fields.
        'verlet': verlet_integration, # Commonly used in molecular dynamics simulations and other physical simulations. It conserves energy over long simulations but may be less accurate in terms of position.
        'leapfrog': leapfrog_integration, # A time-reversible method often used in gravitational simulations. It conserves momentum and is more accurate than simple methods like Euler for oscillatory problems.
        'orbital_elements': orbital_elements_integration # Designed for integrating celestial bodies following Kepler's laws. It can be highly accurate for such applications, relying on specific orbital parameters like semi-major axis, eccentricity, etc.
    }
    return integrators.get(method, leapfrog_integration) # Default to Leapfrog

def run_simulation(timescale_seconds, method='leapfrog'):
    integrator = get_integrator(method)
    for body in bodies:
        integrator(body, timescale_seconds)
        if body.parent is not None:
            calculate_orbital_parameters(body, body.parent)

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
