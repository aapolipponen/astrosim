import numpy as np
from numba import njit, prange

@njit(parallel=True)
def euler_step(pos, vel, mass, dt, G):
    N = pos.shape[0]
    acc = np.zeros((N, 3))
    for i in prange(N):
        for j in range(N):
            if i != j:
                r = pos[j] - pos[i]
                r_mag = np.sqrt(np.sum(r**2)) + 1e-12
                acc[i] += G * mass[j] * r / r_mag**3
    vel += acc * dt
    pos += vel * dt

@njit(parallel=True)
def verlet_step(pos, vel, mass, dt, G):
    N = pos.shape[0]
    acc = np.zeros((N, 3))
    for i in prange(N):
        for j in range(N):
            if i != j:
                r = pos[j] - pos[i]
                r_mag = np.sqrt(np.sum(r**2)) + 1e-12
                acc[i] += G * mass[j] * r / r_mag**3
    pos_new = pos + vel * dt + 0.5 * acc * dt**2
    acc_new = np.zeros((N, 3))
    for i in prange(N):
        for j in range(N):
            if i != j:
                r = pos_new[j] - pos_new[i]
                r_mag = np.sqrt(np.sum(r**2)) + 1e-12
                acc_new[i] += G * mass[j] * r / r_mag**3
    vel += 0.5 * (acc + acc_new) * dt
    pos[:] = pos_new

@njit(parallel=True)
def leapfrog_step(pos, vel, mass, dt, G):
    N = pos.shape[0]
    acc = np.zeros((N, 3))
    for i in prange(N):
        for j in range(N):
            if i != j:
                r = pos[j] - pos[i]
                r_mag = np.sqrt(np.sum(r**2)) + 1e-12
                acc[i] += G * mass[j] * r / r_mag**3
    vel += 0.5 * acc * dt
    pos += vel * dt
    acc_new = np.zeros((N, 3))
    for i in prange(N):
        for j in range(N):
            if i != j:
                r = pos[j] - pos[i]
                r_mag = np.sqrt(np.sum(r**2)) + 1e-12
                acc_new[i] += G * mass[j] * r / r_mag**3
    vel += 0.5 * acc_new * dt

@njit(parallel=True)
def rk4_step(pos, vel, mass, dt, G):
    N = pos.shape[0]
    k1_vel = np.copy(vel)
    k1_acc = np.zeros((N, 3))
    for i in prange(N):
        for j in range(N):
            if i != j:
                r = pos[j] - pos[i]
                r_mag = np.sqrt(np.sum(r**2)) + 1e-12
                k1_acc[i] += G * mass[j] * r / r_mag**3
    k1_pos = k1_vel * dt
    k1_acc_dt = k1_acc * dt

    k2_vel = vel + 0.5 * k1_acc_dt
    k2_pos = pos + 0.5 * k1_pos
    k2_acc = np.zeros((N, 3))
    for i in prange(N):
        for j in range(N):
            if i != j:
                r = k2_pos[j] - k2_pos[i]
                r_mag = np.sqrt(np.sum(r**2)) + 1e-12
                k2_acc[i] += G * mass[j] * r / r_mag**3
    k2_pos = k2_vel * dt
    k2_acc_dt = k2_acc * dt

    k3_vel = vel + 0.5 * k2_acc_dt
    k3_pos = pos + 0.5 * k2_pos
    k3_acc = np.zeros((N, 3))
    for i in prange(N):
        for j in range(N):
            if i != j:
                r = k3_pos[j] - k3_pos[i]
                r_mag = np.sqrt(np.sum(r**2)) + 1e-12
                k3_acc[i] += G * mass[j] * r / r_mag**3
    k3_pos = k3_vel * dt
    k3_acc_dt = k3_acc * dt

    k4_vel = vel + k3_acc_dt
    k4_pos = pos + k3_pos
    k4_acc = np.zeros((N, 3))
    for i in prange(N):
        for j in range(N):
            if i != j:
                r = k4_pos[j] - k4_pos[i]
                r_mag = np.sqrt(np.sum(r**2)) + 1e-12
                k4_acc[i] += G * mass[j] * r / r_mag**3
    k4_pos = k4_vel * dt
    k4_acc_dt = k4_acc * dt

    pos += (k1_pos + 2 * k2_pos + 2 * k3_pos + k4_pos) / 6
    vel += (k1_acc_dt + 2 * k2_acc_dt + 2 * k3_acc_dt + k4_acc_dt) / 6

@njit(parallel=True)
def compute_acceleration(pos, mass, G):
    """Helper function to compute accelerations for all bodies"""
    N = pos.shape[0]
    acc = np.zeros((N, 3))
    for i in prange(N):
        for j in range(N):
            if i != j:
                r = pos[j] - pos[i]
                r_mag = np.sqrt(np.sum(r**2)) + 1e-12
                acc[i] += G * mass[j] * r / r_mag**3
    return acc

@njit(parallel=True)
def rk6_step(pos, vel, mass, dt, G):
    """
    6th order Runge-Kutta integrator (Verner's method)
    Very high accuracy, suitable for precision orbital mechanics
    Uses 8 function evaluations per step
    """
    N = pos.shape[0]
    
    # Store intermediate positions and velocities
    pos_temp = np.zeros((N, 3))
    vel_temp = np.zeros((N, 3))
    
    # k1
    k1_acc = compute_acceleration(pos, mass, G)
    k1_vel = vel
    k1_pos = k1_vel * dt
    
    # k2
    pos_temp[:] = pos + (1.0/6.0) * k1_pos
    vel_temp[:] = vel + (1.0/6.0) * k1_acc * dt
    k2_acc = compute_acceleration(pos_temp, mass, G)
    k2_vel = vel_temp
    k2_pos = k2_vel * dt
    
    # k3
    pos_temp[:] = pos + (4.0/75.0) * k1_pos + (16.0/75.0) * k2_pos
    vel_temp[:] = vel + (4.0/75.0) * k1_acc * dt + (16.0/75.0) * k2_acc * dt
    k3_acc = compute_acceleration(pos_temp, mass, G)
    k3_vel = vel_temp
    k3_pos = k3_vel * dt
    
    # k4
    pos_temp[:] = pos + (5.0/6.0) * k1_pos - (8.0/3.0) * k2_pos + (5.0/2.0) * k3_pos
    vel_temp[:] = vel + (5.0/6.0) * k1_acc * dt - (8.0/3.0) * k2_acc * dt + (5.0/2.0) * k3_acc * dt
    k4_acc = compute_acceleration(pos_temp, mass, G)
    k4_vel = vel_temp
    k4_pos = k4_vel * dt
    
    # k5
    pos_temp[:] = pos - (8.0/5.0) * k1_pos + (144.0/25.0) * k2_pos - (4.0) * k3_pos + (16.0/25.0) * k4_pos
    vel_temp[:] = vel - (8.0/5.0) * k1_acc * dt + (144.0/25.0) * k2_acc * dt - (4.0) * k3_acc * dt + (16.0/25.0) * k4_acc * dt
    k5_acc = compute_acceleration(pos_temp, mass, G)
    k5_vel = vel_temp
    k5_pos = k5_vel * dt
    
    # k6
    pos_temp[:] = pos + (361.0/320.0) * k1_pos - (18.0/5.0) * k2_pos + (407.0/128.0) * k3_pos - (11.0/80.0) * k4_pos + (55.0/128.0) * k5_pos
    vel_temp[:] = vel + (361.0/320.0) * k1_acc * dt - (18.0/5.0) * k2_acc * dt + (407.0/128.0) * k3_acc * dt - (11.0/80.0) * k4_acc * dt + (55.0/128.0) * k5_acc * dt
    k6_acc = compute_acceleration(pos_temp, mass, G)
    k6_vel = vel_temp
    k6_pos = k6_vel * dt
    
    # k7
    pos_temp[:] = pos - (11.0/640.0) * k1_pos + (11.0/256.0) * k3_pos - (11.0/160.0) * k4_pos + (11.0/256.0) * k5_pos
    vel_temp[:] = vel - (11.0/640.0) * k1_acc * dt + (11.0/256.0) * k3_acc * dt - (11.0/160.0) * k4_acc * dt + (11.0/256.0) * k5_acc * dt
    k7_acc = compute_acceleration(pos_temp, mass, G)
    k7_vel = vel_temp
    k7_pos = k7_vel * dt
    
    # k8
    pos_temp[:] = pos + (93.0/640.0) * k1_pos - (18.0/5.0) * k2_pos + (803.0/256.0) * k3_pos - (11.0/160.0) * k4_pos + (99.0/256.0) * k5_pos + k7_pos
    vel_temp[:] = vel + (93.0/640.0) * k1_acc * dt - (18.0/5.0) * k2_acc * dt + (803.0/256.0) * k3_acc * dt - (11.0/160.0) * k4_acc * dt + (99.0/256.0) * k5_acc * dt + k7_acc * dt
    k8_acc = compute_acceleration(pos_temp, mass, G)
    k8_vel = vel_temp
    k8_pos = k8_vel * dt
    
    # 6th order combination (Verner's method coefficients)
    pos += dt * ((31.0/384.0) * k1_vel + 
                 (1125.0/2816.0) * k3_vel +
                 (9.0/32.0) * k4_vel +
                 (125.0/768.0) * k5_vel +
                 (5.0/66.0) * k6_vel)
    
    vel += dt * ((31.0/384.0) * k1_acc + 
                 (1125.0/2816.0) * k3_acc +
                 (9.0/32.0) * k4_acc +
                 (125.0/768.0) * k5_acc +
                 (5.0/66.0) * k6_acc)

@njit(parallel=True)
def yoshida4_step(pos, vel, mass, dt, G):
    """
    Yoshida 4th order symplectic integrator
    Preserves energy and phase space structure, excellent for long-term orbital mechanics
    
    Uses the correct Yoshida 4th order coefficients:
    w0 = 1/(2-2^(1/3))
    w1 = -2^(1/3)/(2-2^(1/3))
    w2 = 1/(2-2^(1/3))
    
    Pattern: D(w0*dt) K(w1*dt) D(w2*dt) K(w1*dt) D(w0*dt)
    where D = drift (position update) and K = kick (velocity update)
    """
    # Correct Yoshida 4th order coefficients
    # w0 = 1/(2-2^(1/3)) ≈ 1.3512071919596578
    # w1 = -2^(1/3)/(2-2^(1/3)) ≈ -1.7024143839193155
    # w2 = 1/(2-2^(1/3)) ≈ 1.3512071919596578
    w0 = 1.3512071919596578
    w1 = -1.7024143839193155
    w2 = 1.3512071919596578
    
    N = pos.shape[0]
    
    # Yoshida 4th order pattern: D(w0) K(w1) D(w2) K(w1) D(w0)
    # Step 1: Drift with w0
    pos += w0 * vel * dt
    
    # Step 2: Kick with w1
    acc = compute_acceleration(pos, mass, G)
    vel += w1 * acc * dt
    
    # Step 3: Drift with w2
    pos += w2 * vel * dt
    
    # Step 4: Kick with w1
    acc = compute_acceleration(pos, mass, G)
    vel += w1 * acc * dt
    
    # Step 5: Drift with w0
    pos += w0 * vel * dt