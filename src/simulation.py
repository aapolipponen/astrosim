from constants import G, C
from planet import bodies
import numpy as np
import integration

class Node:
    def __init__(self, center, size):
        self.center = np.array(center)
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
        node.children = []
        for i in [-0.5, 0.5]:
            for j in [-0.5, 0.5]:
                for k in [-0.5, 0.5]:
                    child_center = node.center + np.array([i, j, k]) * node.size * 0.5
                    child = build_tree(bodies_inside, child_center, node.size * 0.5)
                    if child:
                        node.children.append(child)
                        node.mass += child.mass

        center_of_mass_numerator = np.array([0.0, 0.0, 0.0])
        for child in node.children:
            center_of_mass_numerator += child.center * child.mass
        node.center = center_of_mass_numerator / node.mass if node.mass != 0 else node.center

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
        net_force = calculate_force_on_body(root, target_body, 1)
    else:
        net_force = np.array([0.0, 0.0, 0.0])
        for body in bodies:
            if body != target_body:
                r = body.pos - target_body.pos
                r_mag = np.linalg.norm(r)
                # Avoid computation for extremely close objects (optional)
                if r_mag < 1e-6:
                    continue

                force_mag = G * target_body.mass * body.mass / r_mag**2
                # 1st post-Newtonian correction from GR
                if post_newtonian_correction:
                    correction_force_mag = (G**2 / C**2) * target_body.mass * body.mass * (target_body.mass + body.mass) / r_mag**3
                    force_mag += correction_force_mag
                force = force_mag * r / r_mag
                net_force += force

    # Here, you can still add any post-Newtonian correction if necessary
    return net_force

def get_integrator(method):
    integrators = {
        # Simple and computationally efficient but can suffer from numerical instability. Often less accurate, especially for stiff systems or long simulations.
        'euler': integration.euler_integration,
        # Similar to Euler but takes the average of the initial and midpoint derivatives, improving accuracy. Still might not be suitable for stiff problems.
        'midpoint': integration.midpoint_integration,
        # A predictor-corrector method that's an improved version of the Euler method. It's more accurate but still simple and efficient.
        'heun': integration.heun_integration,
        # Fourth-order Runge-Kutta method. A well-balanced choice for many problems, offering good accuracy and stability. More computationally expensive than Euler but widely used in various fields.
        'rk4': integration.rk4_integration,
        # Commonly used in molecular dynamics simulations and other physical simulations. It conserves energy over long simulations but may be less accurate in terms of position.
        'verlet': integration.verlet_integration,
        # A time-reversible method often used in gravitational simulations. It conserves momentum and is more accurate than simple methods like Euler for oscillatory problems.
        'leapfrog': integration.leapfrog_integration,

        # Designed for integrating celestial bodies following Kepler's laws. It can be highly accurate for such applications, relying on specific orbital parameters like semi-major axis, eccentricity, etc.
        #'orbital_elements': orbital_elements_integration
    }
    return integrators.get(method)

def run_simulation(timescale_seconds, method, post_newtonian_correction, barnes_hut, FULL_ORBITS):
    integrator = get_integrator(method)
    for body in bodies:
        integrator(body, post_newtonian_correction, barnes_hut, calculate_net_force, timescale_seconds)
        if body.parent and FULL_ORBITS:
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
    
    # Use the previously computed e_vector here
    calculate_true_anomaly(body, e_vector)
    calculate_argument_of_periapsis(body, h, e_vector)
    calculate_semi_major_axis(body)
    calculate_semi_minor_axis(body)
    calculate_mean_anomaly(body)