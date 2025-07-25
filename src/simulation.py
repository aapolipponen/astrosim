from constants import G, C
from planet import bodies
import numpy as np
import integration

def calculate_net_force(target_body):
    net_force = np.array([0.0, 0.0, 0.0])
    for body in bodies:
        if body != target_body:
            r = body.pos - target_body.pos
            r_mag = np.linalg.norm(r)
            if r_mag < 1e-6:
                continue
            force_mag = G * target_body.mass * body.mass / r_mag**2
            force = force_mag * r / r_mag
            net_force += force
    return net_force

def bodies_to_arrays(bodies):
    N = len(bodies)
    pos = np.zeros((N, 3))
    vel = np.zeros((N, 3))
    mass = np.zeros(N)
    for i, b in enumerate(bodies):
        pos[i] = b.pos
        vel[i] = b.vel
        mass[i] = b.mass
    return pos, vel, mass

def arrays_to_bodies(pos, vel, bodies):
    for i, b in enumerate(bodies):
        b.pos = pos[i]
        b.vel = vel[i]

def run_simulation_array(timescale_seconds, method, FULL_ORBITS):
    from constants import G
    pos, vel, mass = bodies_to_arrays(bodies)
    if method == 'euler':
        integration.euler_step(pos, vel, mass, timescale_seconds, G)
    elif method == 'verlet':
        integration.verlet_step(pos, vel, mass, timescale_seconds, G)
    elif method == 'leapfrog':
        integration.leapfrog_step(pos, vel, mass, timescale_seconds, G)
    elif method == 'rk4':
        integration.rk4_step(pos, vel, mass, timescale_seconds, G)
    else:
        raise ValueError(f'Unknown integration method: {method}')
    arrays_to_bodies(pos, vel, bodies)
    if FULL_ORBITS:
        for body in bodies:
            if body.parent:
                calculate_orbital_parameters(body)

def get_integrator(method):
    integrators = {
        'euler': run_simulation_array,
        'rk4': run_simulation_array,
        'verlet': run_simulation_array,
        'leapfrog': run_simulation_array,
    }
    return integrators.get(method)

def run_simulation(timescale_seconds, method, FULL_ORBITS):
    integrator = get_integrator(method)
    if integrator is not None:
        integrator(timescale_seconds, method, FULL_ORBITS)
    else:
        raise ValueError(f'Unknown integration method: {method}')

def calculate_orbital_position(body):
    # Get the position of the moon relative to its parent planet
    relative_pos = body.pos - body.parent.pos

    # Calculate the angle in radians
    angle_rad = np.arctan2(relative_pos[1], relative_pos[0])

    # If you want the angle in degrees instead of radians
    angle_deg = np.degrees(angle_rad)

    return angle_rad, angle_deg

def calculate_relative_vectors(body):
    body.relative_pos = body.pos - body.parent.pos
    body.relative_vel = body.vel - body.parent.vel

def calculate_energy_and_momentum(body):
    body.E = 0.5 * np.dot(body.relative_vel, body.relative_vel) - G * body.parent.mass / np.linalg.norm(body.relative_pos)
    body.L = np.linalg.norm(np.cross(body.relative_pos, body.relative_vel))

def calculate_semi_major_axis(body):
    eccentricity_ratio = (1 - body.eccentricity) / (1 + body.eccentricity)

    # Check for non-elliptical orbits (eccentricity_ratio < 0)
    if eccentricity_ratio < 0:
        raise ValueError(f"Non-elliptical orbit for {body.name}. Eccentricity ratio: {eccentricity_ratio}")

    E = 2 * np.arctan(np.sqrt(eccentricity_ratio) * np.tan(0.5 * body.true_anomaly))
    body.semi_major_axis = -G * body.parent.mass / (2 * body.E)

def calculate_semi_minor_axis(body):
    body.semi_minor_axis = body.semi_major_axis * np.sqrt(1 - body.eccentricity**2)

def calculate_mean_anomaly(body):
    E = 2 * np.arctan(np.sqrt((1 - body.eccentricity) / (1 + body.eccentricity)) * np.tan(0.5 * body.true_anomaly))
    body.mean_anomaly = E - body.eccentricity * np.sin(E)

def calculate_eccentricity(body):
    if body.parent == None:
        return
    else: 
        r = body.relative_pos
        v = body.relative_vel
        h = np.cross(r, v)
        mu = G * body.parent.mass
        e_vector = (np.cross(v, h) - mu * r / np.linalg.norm(r)) / mu
        body.eccentricity = np.linalg.norm(e_vector)

        if body.eccentricity >= 1:
            body.parent = None
            print(f"Error: {body.name} has an eccentricity of {body.eccentricity}, indicating a non-elliptical orbit.")
        return e_vector

def calculate_true_anomaly(body, e_vector):
    r = body.relative_pos
    v = body.relative_vel
    nu = np.arccos(np.dot(e_vector, r) / (body.eccentricity * np.linalg.norm(r)))
    if np.dot(r, v) < 0:
        nu = 2 * np.pi - nu
    body.true_anomaly = nu

def calculate_argument_of_periapsis(body, h, e_vector):
    n = np.cross([0, 0, 1], h)
    omega_argument = np.dot(n, e_vector) / (np.linalg.norm(n) * body.eccentricity)
    omega_argument = np.clip(omega_argument, -1, 1)
    omega = np.arccos(omega_argument)
    if e_vector[2] < 0:
        omega = 2 * np.pi - omega
    body.argument_of_periapsis = omega

def calculate_orbital_parameters(body):
    calculate_relative_vectors(body)
    calculate_energy_and_momentum(body)
    h = np.cross(body.relative_pos, body.relative_vel)
    
    # This will give us both the eccentricity vector and set the eccentricity attribute of the body.
    e_vector = calculate_eccentricity(body)

    # Skip further orbital calculations for non-elliptical (e>=1) or detached bodies like probes/escape trajectories.
    if body.parent is None or body.eccentricity is None or body.eccentricity >= 1:
        return
 
    # Use the previously computed e_vector here
    calculate_true_anomaly(body, e_vector)
    calculate_argument_of_periapsis(body, h, e_vector)
    calculate_semi_major_axis(body)
    calculate_semi_minor_axis(body)
    calculate_mean_anomaly(body)