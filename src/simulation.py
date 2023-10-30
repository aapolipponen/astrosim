from schwarzschild_geodesics import schwarzschild_geodesic_equation
from constants import G, C
from planets import bodies
import integration
import numpy as np
from scipy.integrate import solve_ivp

def calculate_net_force(target_body):
    net_force = np.array([0.0, 0.0, 0.0])
    for body in bodies:
        if body != target_body:
            r = body.pos - target_body.pos
            r_mag = np.linalg.norm(r)
            # Avoid computation for extremely close objects (optional)
            if r_mag < 1e-6:
                continue
            force_mag = G * target_body.mass * body.mass / r_mag**2
            force = force_mag * r / r_mag
            net_force += force

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
    }
    return integrators.get(method)

def run_simulation(timescale_seconds, method, apply_schwarzchild=True):
    integrator = get_integrator(method)
    sun = next((body for body in bodies if body.name == "Sun"), None)
    if sun is None:
        raise Exception("No Sun found in bodies list")

    for body in bodies:
        if apply_schwarzchild and body != sun:
            # Convert position to Schwarzschild coordinates
            r = np.linalg.norm(body.pos)
            theta = np.pi / 2  # Assuming body is in the xy-plane
            phi = np.arctan2(body.pos[1], body.pos[0])  # In radians

            # Calculate specific angular momentum
            h = np.linalg.norm(np.cross(body.pos, body.vel))

            # Initial momentum components in Schwarzschild coordinates
            pr = 0
            ptheta = 0
            pphi = h / r

            # Solve the geodesic equations
            sol = solve_ivp(
                schwarzschild_geodesic_equation, 
                [0, timescale_seconds], 
                [r, theta, phi, pr, ptheta, pphi], 
                args=(sun.mass,), 
                t_eval=[timescale_seconds],
                method='Radau', # Consider 'BDF' or 'LSODA'
                rtol=1e-6,
                atol=1e-6,
                max_step=1000.0
            )

            if not sol.success:
                print(f"Solver failed: {sol.message}, {sol.t}, {sol.y}, {sol.y.shape}")

            sol_y_array = np.array(sol.y) if isinstance(sol.y, list) else sol.y

            if sol_y_array.shape[0] >= 3:
                x_relativistic = sol_y_array[0] * np.sin(sol_y_array[1]) * np.cos(sol_y_array[2])
                y_relativistic = sol_y_array[0] * np.sin(sol_y_array[1]) * np.sin(sol_y_array[2])
            else:
                print(f"Insufficient dimensions in sol.y: {sol_y_array.shape}")
                
        else:
            integrator(body, calculate_net_force, timescale_seconds)