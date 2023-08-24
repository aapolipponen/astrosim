def derivatives(body, post_newtonian_correction, barnes_hut, calculate_net_force, timescale_seconds):
    net_force = calculate_net_force(body, post_newtonian_correction, barnes_hut)
    acc = net_force / body.mass  # Acceleration = net force / mass
    return body.vel, acc

def euler_integration(body, post_newtonian_correction, barnes_hut, calculate_net_force, timescale_seconds):
    vel_derivative, acc_derivative = derivatives(body, post_newtonian_correction, barnes_hut, calculate_net_force, timescale_seconds)
    body.pos += vel_derivative * timescale_seconds
    body.vel += acc_derivative * timescale_seconds

def midpoint_integration(body, post_newtonian_correction, barnes_hut, calculate_net_force, timescale_seconds):

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

def heun_integration(body, post_newtonian_correction, barnes_hut, calculate_net_force, timescale_seconds):
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

def rk4_integration(body, post_newtonian_correction, barnes_hut, calculate_net_force, timescale_seconds):
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

def verlet_integration(body, post_newtonian_correction, barnes_hut, calculate_net_force, timescale_seconds):
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

def leapfrog_integration(body, post_newtonian_correction, barnes_hut, calculate_net_force, timescale_seconds):
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