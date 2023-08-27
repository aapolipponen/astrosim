from constants import G, C
from planets import bodies
import numpy as np
import integration

def calculate_net_force(target_body, post_newtonian_correction):
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

def run_simulation(timescale_seconds, method, post_newtonian_correction, FULL_ORBITS):
    integrator = get_integrator(method)
    for body in bodies:
        integrator(body, post_newtonian_correction, calculate_net_force, timescale_seconds)