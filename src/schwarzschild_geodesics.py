from constants import G, C
import numpy as np

def schwarzschild_geodesic_equation(t, y, M):
    # Schwarzschild radius (in your units)
    rs = 2 * G * M

    r, theta, phi, pr, ptheta, pphi = y
    
    # Avoid division by zero
    if r == rs or r == 0 or np.sin(theta) == 0:
        return [0]*6
    
    dpr = - ((rs - r) / (r * (r - rs))) * pr**2 + ((r - rs) / r**3) - (2 / (r**2 * np.sin(theta)**2)) * pphi**2 - (2 / r**3) * ptheta**2
    dptheta = 2 * pr * ptheta / r - 2 * pphi**2 * np.sin(theta) * np.cos(theta) / np.sin(theta)**2
    dpphi = 2 * pr * pphi / r + 2 * pphi * ptheta * np.cos(theta) / np.sin(theta)

    return [pr, ptheta, pphi, dpr, dptheta, dpphi]
