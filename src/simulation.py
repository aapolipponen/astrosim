from constants import G
from planet import bodies
import numpy as np

def calculate_net_force(target_body, use_post_newtonian=True):
    net_force = np.array([0.0, 0.0, 0.0])
    for body in bodies:
        if body != target_body:
            r = body.pos - target_body.pos
            r_mag = np.linalg.norm(r)
            force_mag = G * target_body.mass * body.mass / r_mag**2
            force = force_mag * r / r_mag

            if use_post_newtonian:
                # First post-Newtonian correction
                c_squared = (3e8)**2  # Speed of light, m/s
                v_squared = np.dot(body.vel, body.vel)
                v_dot_r = np.dot(body.vel, r)
                force_correction = G * target_body.mass * body.mass / (r_mag**2 * c_squared) * \
                                   ((4*G*body.mass/r_mag - v_squared)*r + 4*v_dot_r*body.vel)
                force += force_correction

            net_force += force
    return net_force

def derivatives(body):
    net_force = calculate_net_force(body)
    acc = net_force / body.mass  # Acceleration = net force / mass
    return body.vel, acc

def euler_integration(body, timescale_seconds):
    vel_derivative, acc_derivative = derivatives(body)
    body.pos += vel_derivative * timescale_seconds
    body.vel += acc_derivative * timescale_seconds

def midpoint_integration(body, timescale_seconds):

    k1_vel, k1_acc = derivatives(body)
    k1_pos = k1_vel * timescale_seconds
    k1_acc *= timescale_seconds

    # temporary update to midpoint state
    body.pos += 0.5 * k1_pos
    body.vel += 0.5 * k1_acc

    k2_vel, k2_acc = derivatives(body)
    k2_pos = k2_vel * timescale_seconds
    k2_acc *= timescale_seconds

    # Roll back the temporary update
    body.pos -= 0.5 * k1_pos
    body.vel -= 0.5 * k1_acc

    # Do the actual update
    body.pos += k2_pos
    body.vel += k2_acc

def heun_integration(body, timescale_seconds):
    k1_vel, k1_acc = derivatives(body)
    k1_pos = k1_vel * timescale_seconds
    k1_acc *= timescale_seconds

    # temporary update to predict the end state
    body.pos += k1_pos
    body.vel += k1_acc

    k2_vel, k2_acc = derivatives(body)
    k2_pos = k2_vel * timescale_seconds
    k2_acc *= timescale_seconds

    # Roll back the temporary update
    body.pos -= k1_pos
    body.vel -= k1_acc

    # Do the actual update with the average of the initial and predicted end state
    body.pos += 0.5 * (k1_pos + k2_pos)
    body.vel += 0.5 * (k1_acc + k2_acc)

def rk4_integration(body, timescale_seconds):
    pos_initial = body.pos.copy()
    vel_initial = body.vel.copy()

    k1_vel, k1_acc = derivatives(body)
    k1_pos = k1_vel * timescale_seconds
    k1_acc *= timescale_seconds

    body.pos = pos_initial + 0.5 * k1_pos
    body.vel = vel_initial + 0.5 * k1_acc
    k2_vel, k2_acc = derivatives(body)
    k2_pos = k2_vel * timescale_seconds
    k2_acc *= timescale_seconds

    body.pos = pos_initial + 0.5 * k2_pos
    body.vel = vel_initial + 0.5 * k2_acc
    k3_vel, k3_acc = derivatives(body)
    k3_pos = k3_vel * timescale_seconds
    k3_acc *= timescale_seconds

    body.pos = pos_initial + k3_pos
    body.vel = vel_initial + k3_acc
    k4_vel, k4_acc = derivatives(body)
    k4_pos = k4_vel * timescale_seconds
    k4_acc *= timescale_seconds

    # return body's position and velocity to the initial values before applying the final update
    body.pos = pos_initial
    body.vel = vel_initial

    body.pos += (k1_pos + 2 * k2_pos + 2 * k3_pos + k4_pos) / 6
    body.vel += (k1_acc + 2 * k2_acc + 2 * k3_acc + k4_acc) / 6

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
        #'orbital_elements': orbital_elements_integration # Designed for integrating celestial bodies following Kepler's laws. It can be highly accurate for such applications, relying on specific orbital parameters like semi-major axis, eccentricity, etc.
    }
    return integrators.get(method)

def run_simulation(timescale_seconds, method):
    integrator = get_integrator(method)
    for body in bodies:
        if body.parent is not None:
            calculate_orbital_parameters(body, body.parent)
        integrator(body, timescale_seconds)

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
    eccentricity_ratio = (1 - body.eccentricity) / (1 + body.eccentricity)
    if eccentricity_ratio >= 0:
        E = 2 * np.arctan(np.sqrt(eccentricity_ratio) * np.tan(0.5 * body.true_anomaly))
    else:
        # handle the error, for example by setting E to NaN or raising an exception
        E = np.nan
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

def calculate_inclination(body):
    body.inclination = np.arccos(np.dot(body.relative_pos, np.array([0, 0, 1])) / np.linalg.norm(body.relative_pos))

def calculate_argument_of_periapsis(body):
    n = np.cross(np.array([0, 0, 1]), body.relative_pos)
    e = body.eccentricity
    body.argument_of_periapsis = np.arccos(np.dot(n, body.relative_pos) / (np.linalg.norm(n) * np.linalg.norm(body.relative_pos)))
    if body.relative_pos[2] < 0:
        body.argument_of_periapsis = 2 * np.pi - body.argument_of_periapsis

def calculate_longitude_of_ascending_node(body):
    # The specific relative angular momentum
    h = np.cross(body.relative_pos, body.relative_vel)

    # The x and y components of h
    h_x, h_y = h[0], h[1]

    # Calculate the Longitude of the Ascending Node
    Ω = np.arctan2(h_y, h_x)

    # Convert to degrees and correct for negative angles
    Ω = np.degrees(Ω)
    body.longitude_of_ascending_node = Ω

def calculate_mean_anomaly(body):
    E = 2 * np.arctan(np.sqrt((1 - body.eccentricity) / (1 + body.eccentricity)) * np.tan(0.5 * body.true_anomaly))
    body.mean_anomaly = E - body.eccentricity * np.sin(E)

def calculate_true_anomaly(body, focus_object):
    r = body.pos - focus_object.pos
    v = body.vel - focus_object.vel
    h = np.cross(r, v)
    n = np.cross([0, 0, 1], h)

    norm_n = np.linalg.norm(n)
    norm_r = np.linalg.norm(r)

    epsilon = 1e-10  # Small tolerance value
    if norm_n < epsilon or norm_r < epsilon:
        theta = 0
    else:
        cos_theta = np.dot(n, r) / (norm_n * norm_r)
        cos_theta = np.clip(cos_theta, -1, 1)  # Ensure the value is within the interval [-1,1]
        theta = np.arccos(cos_theta)

    if np.dot(r, v) < 0:
        theta = 2 * np.pi - theta

    body.true_anomaly = theta

def calculate_orbital_parameters(body, focus_object):
    calculate_relative_vectors(body, focus_object)
    calculate_energy_and_momentum(body, focus_object)
    calculate_semi_major_axis(body, focus_object)
    calculate_semi_minor_axis(body)
    calculate_eccentricity(body, focus_object)
    calculate_inclination(body)
    calculate_longitude_of_ascending_node(body)
    calculate_argument_of_periapsis(body)
    calculate_mean_anomaly(body)
    calculate_true_anomaly(body, focus_object)
