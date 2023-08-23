from constants import G, C
from planet import bodies
import numpy as np

class Node:
    def __init__(self, center, size):
        self.center = np.array([0.0, 0.0, 0.0])
        self.mass = 0.0
        self.size = size  # dimensions of the node
        self.children = []  # children nodes
        self.body = None  # if node is a leaf, it contains a body

def build_tree(bodies, center, size):
    node = Node(center, size)

    # Filter bodies inside this node
    bodies_inside = [body for body in bodies if inside(body.pos, node.center, node.size)]

    if len(bodies_inside) == 0:
        return None
    elif len(bodies_inside) == 1:
        node.body = bodies_inside[0]
        node.mass = node.body.mass
        node.center = node.body.pos
    else:
        for i in [-0.5, 0.5]:
            for j in [-0.5, 0.5]:
                for k in [-0.5, 0.5]:
                    child_center = node.center + np.array([i, j, k]) * node.size * 0.5
                    child = build_tree(bodies_inside, child_center, node.size * 0.5)
                    if child:
                        node.children.append(child)
                        node.mass += child.mass
                        node.center += child.center * child.mass

        node.center /= node.mass

    return node

def calculate_force_on_body(node, body, theta):
    if not node:
        return np.array([0.0, 0.0, 0.0])

    r = node.center - body.pos
    r_mag = np.linalg.norm(r)

    if node.body:  # If leaf node
        if node.body != body:  # Exclude self force
            force_mag = G * body.mass * node.mass / r_mag**2
            return force_mag * r / r_mag
        return np.array([0.0, 0.0, 0.0])

    # Check if far enough to treat as a single body
    if node.size / r_mag < theta:
        force_mag = G * body.mass * node.mass / r_mag**2
        return force_mag * r / r_mag

    # Otherwise, traverse children nodes
    force = np.array([0.0, 0.0, 0.0])
    for child in node.children:
        force += calculate_force_on_body(child, body, theta)

    return force

def inside(position, center, size):
    """
    Check if a position is inside a cubic region defined by center and size.

    Parameters:
    - position: np.array, the position to check.
    - center: np.array, the center of the cubic region.
    - size: float, the size (edge length) of the cubic region.

    Returns:
    - bool, True if the position is inside the cubic region, False otherwise.
    """

    half_size = size / 2.0
    lower_bound = center - half_size
    upper_bound = center + half_size

    return np.all(position >= lower_bound) and np.all(position <= upper_bound)

def compute_root_size(bodies):
    min_coords = np.min([body.pos for body in bodies], axis=0)
    max_coords = np.max([body.pos for body in bodies], axis=0)

    dimensions = max_coords - min_coords
    max_dimension = np.max(dimensions)

    padding = 0.1 * max_dimension  # 10% extra

    return max_dimension + padding

def calculate_net_force(target_body, post_newtonian_correction, barnes_hut):
    if barnes_hut:
        root = build_tree(bodies, np.array([0, 0, 0]), compute_root_size(bodies))
        net_force = calculate_force_on_body(root, target_body, 0.5)
    else:
        net_force = np.array([0.0, 0.0, 0.0])
        for body in bodies:
            if body != target_body:
                r = body.pos - target_body.pos
                r_mag = np.linalg.norm(r)
                force_mag = G * target_body.mass * body.mass / r_mag**2

                # 1st post-Newtonian correction from GR
                if post_newtonian_correction:
                    correction_force_mag = (G**2 / C**2) * target_body.mass * body.mass * (target_body.mass + body.mass) / r_mag**3
                    force_mag += correction_force_mag

                force = force_mag * r / r_mag
                net_force += force

    # Here, you can still add any post-Newtonian correction if necessary
    return net_force

def derivatives(body, post_newtonian_correction, barnes_hut):
    net_force = calculate_net_force(body, post_newtonian_correction, barnes_hut)
    acc = net_force / body.mass  # Acceleration = net force / mass
    return body.vel, acc

def euler_integration(body, timescale_seconds, post_newtonian_correction, barnes_hut):
    vel_derivative, acc_derivative = derivatives(body, post_newtonian_correction, barnes_hut)
    body.pos += vel_derivative * timescale_seconds
    body.vel += acc_derivative * timescale_seconds

def midpoint_integration(body, timescale_seconds, post_newtonian_correction, barnes_hut):

    k1_vel, k1_acc = calculate_net_force(body, post_newtonian_correction, barnes_hut)
    k1_pos = k1_vel * timescale_seconds
    k1_acc *= timescale_seconds

    # temporary update to midpoint state
    body.pos += 0.5 * k1_pos
    body.vel += 0.5 * k1_acc

    k2_vel, k2_acc = calculate_net_force(body, post_newtonian_correction, barnes_hut)
    k2_pos = k2_vel * timescale_seconds
    k2_acc *= timescale_seconds

    # Roll back the temporary update
    body.pos -= 0.5 * k1_pos
    body.vel -= 0.5 * k1_acc

    # Do the actual update
    body.pos += k2_pos
    body.vel += k2_acc

def heun_integration(body, timescale_seconds, post_newtonian_correction, barnes_hut):
    k1_vel, k1_acc = derivatives(body, post_newtonian_correction, barnes_hut)
    k1_pos = k1_vel * timescale_seconds
    k1_acc *= timescale_seconds

    # temporary update to predict the end state
    body.pos += k1_pos
    body.vel += k1_acc

    k2_vel, k2_acc = derivatives(body, post_newtonian_correction, barnes_hut)
    k2_pos = k2_vel * timescale_seconds
    k2_acc *= timescale_seconds

    # Roll back the temporary update
    body.pos -= k1_pos
    body.vel -= k1_acc

    # Do the actual update with the average of the initial and predicted end state
    body.pos += 0.5 * (k1_pos + k2_pos)
    body.vel += 0.5 * (k1_acc + k2_acc)

def rk4_integration(body, timescale_seconds, post_newtonian_correction, barnes_hut):
    pos_initial = body.pos.copy()
    vel_initial = body.vel.copy()

    force = calculate_net_force(body, post_newtonian_correction, barnes_hut)
    k1_acc = force / body.mass
    k1_vel = body.vel

    k1_pos = k1_vel * timescale_seconds
    k1_acc *= timescale_seconds

    body.pos = pos_initial + 0.5 * k1_pos
    body.vel = vel_initial + 0.5 * k1_acc

    force = calculate_net_force(body, post_newtonian_correction, barnes_hut)
    k2_acc = force / body.mass
    k2_vel = body.vel

    k2_pos = k2_vel * timescale_seconds
    k2_acc *= timescale_seconds

    body.pos = pos_initial + 0.5 * k2_pos
    body.vel = vel_initial + 0.5 * k2_acc

    force = calculate_net_force(body, post_newtonian_correction, barnes_hut)
    k3_acc = force / body.mass  # Convert force to acceleration
    k3_vel = body.vel  # Use the current velocity of the body

    k3_pos = k3_vel * timescale_seconds
    k3_acc *= timescale_seconds

    body.pos = pos_initial + k3_pos
    body.vel = vel_initial + k3_acc

    force = calculate_net_force(body, post_newtonian_correction, barnes_hut)
    k4_acc = force / body.mass  # Convert force to acceleration
    k4_vel = body.vel  # Use the current velocity of the body

    k4_pos = k4_vel * timescale_seconds
    k4_acc *= timescale_seconds

    # return body's position and velocity to the initial values before applying the final update
    body.pos = pos_initial
    body.vel = vel_initial

    body.pos += (k1_pos + 2 * k2_pos + 2 * k3_pos + k4_pos) / 6
    body.vel += (k1_acc + 2 * k2_acc + 2 * k3_acc + k4_acc) / 6

def verlet_integration(body, timescale_seconds, post_newtonian_correction, barnes_hut):
    # Compute current acceleration
    net_force = calculate_net_force(body, post_newtonian_correction, barnes_hut)
    acceleration = net_force / body.mass

    # Compute new position using current velocity and acceleration
    new_pos = body.pos + body.vel * timescale_seconds + 0.5 * acceleration * timescale_seconds**2

    # Compute new acceleration based on new position
    body.pos = new_pos
    new_net_force = calculate_net_force(body, post_newtonian_correction, barnes_hut)
    new_acceleration = new_net_force / body.mass

    # Compute new velocity using average acceleration
    body.vel += 0.5 * (acceleration + new_acceleration) * timescale_seconds

def leapfrog_integration(body, timescale_seconds, post_newtonian_correction, barnes_hut):
    # Half-step velocity update
    net_force = calculate_net_force(body, post_newtonian_correction, barnes_hut)
    acceleration = net_force / body.mass
    body.vel += 0.5 * acceleration * timescale_seconds

    # Full-step position update
    body.pos += body.vel * timescale_seconds

    # Second half-step velocity update
    net_force = calculate_net_force(body, post_newtonian_correction, barnes_hut)
    acceleration = net_force / body.mass
    body.vel += 0.5 * acceleration * timescale_seconds

def get_integrator(method):
    integrators = {
        # Simple and computationally efficient but can suffer from numerical instability. Often less accurate, especially for stiff systems or long simulations.
        'euler': euler_integration,
        # Similar to Euler but takes the average of the initial and midpoint derivatives, improving accuracy. Still might not be suitable for stiff problems.
        'midpoint': midpoint_integration,
        # A predictor-corrector method that's an improved version of the Euler method. It's more accurate but still simple and efficient.
        'heun': heun_integration,
        # Fourth-order Runge-Kutta method. A well-balanced choice for many problems, offering good accuracy and stability. More computationally expensive than Euler but widely used in various fields.
        'rk4': rk4_integration,
        # Commonly used in molecular dynamics simulations and other physical simulations. It conserves energy over long simulations but may be less accurate in terms of position.
        'verlet': verlet_integration,
        # A time-reversible method often used in gravitational simulations. It conserves momentum and is more accurate than simple methods like Euler for oscillatory problems.
        'leapfrog': leapfrog_integration,

        # Designed for integrating celestial bodies following Kepler's laws. It can be highly accurate for such applications, relying on specific orbital parameters like semi-major axis, eccentricity, etc.
        #'orbital_elements': orbital_elements_integration
    }
    return integrators.get(method)

def run_simulation(timescale_seconds, method, post_newtonian_correction, barnes_hut):
    integrator = get_integrator(method)
    for body in bodies:
        integrator(body, timescale_seconds, post_newtonian_correction, barnes_hut)
        if body.parent:
            calculate_orbital_parameters(body)

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


def calculate_eccentricity(body):
    # The standard gravitational parameter
    mu = G * (body.mass + body.parent.mass)

    # The distance between the body and the focus object
    r = np.linalg.norm(body.pos - body.parent.pos)

    # The speed of the body
    v = np.linalg.norm(body.vel)

    # The specific relative angular momentum
    h = np.linalg.norm(np.cross(body.pos - body.parent.pos, body.vel))

    # The specific orbital energy
    epsilon = v**2 / 2 - mu / r

    # The eccentricity of the orbit
    body.eccentricity = np.sqrt(1 + 2 * epsilon * h**2 / mu**2)

    # Check for orbits that are not elliptical (eccentricity is not less than 1)
    if body.eccentricity >= 1:
        body.parent = None
        print(f"Error: {body.name} has an eccentricity of {body.eccentricity}, indicating a non-elliptical orbit.")

def calculate_semi_minor_axis(body):
    body.semi_minor_axis = body.semi_major_axis * np.sqrt(1 - body.eccentricity**2)

def calculate_argument_of_periapsis(body):
    # Define the reference plane's normal vector (z-axis in this case)
    reference_normal = np.array([0, 0, 1])

    # Calculate the cross product between the reference normal and the relative position vector
    n = np.cross(reference_normal, body.relative_pos)

    # Ensure the dot product argument is within the valid range [-1, 1]
    dot_product_arg = np.clip(np.dot(n, body.relative_pos) / (np.linalg.norm(n) * np.linalg.norm(body.relative_pos)), -1, 1)

    # Calculate the argument of periapsis
    body.argument_of_periapsis = np.arccos(dot_product_arg)

    # Adjust the argument of periapsis for the correct direction (for inclined orbits)
    if body.relative_pos[2] < 0:
        body.argument_of_periapsis = 2 * np.pi - body.argument_of_periapsis

def calculate_mean_anomaly(body):
    E = 2 * np.arctan(np.sqrt((1 - body.eccentricity) / (1 + body.eccentricity)) * np.tan(0.5 * body.true_anomaly))
    body.mean_anomaly = E - body.eccentricity * np.sin(E)

def calculate_true_anomaly(body):
    if body.parent is None:
        return

    r = body.pos - body.parent.pos
    v = body.vel - body.parent.vel
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

def calculate_orbital_parameters(body):
    calculate_relative_vectors(body)
    calculate_energy_and_momentum(body)
    calculate_semi_major_axis(body)
    calculate_semi_minor_axis(body)
    calculate_eccentricity(body)
    calculate_argument_of_periapsis(body)
    calculate_mean_anomaly(body)
    calculate_true_anomaly(body)
