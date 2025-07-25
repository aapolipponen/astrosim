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