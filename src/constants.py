import numpy as np

# ====== Conversion Factors ======
KM_TO_M = 1e3
M_TO_KM = 1e-3
KG_TO_G = 1e3
G_TO_KG = 1e-3

# ====== Time Units in Seconds ======
SECOND = 1
MINUTE = 60 * SECOND
HOUR = 60 * MINUTE
DAY = 24 * HOUR
WEEK = 7 * DAY
MONTH = 30.4375 * DAY  # Average month length
YEAR = 12 * MONTH
SUN_AGE_SECONDS = 4.6e9 * YEAR

# ====== Physical Constants ======
G = 6.67430e-11  # Gravitational constant, m^3 kg^-1 s^-2
C = 2.998e8  # Speed of light, m/s
H = 6.626e-34  # Planck's constant, Js
K_B = 1.381e-23  # Boltzmann constant, J/K
ELECTRON_CHARGE = -1.602e-19  # Coulombs
PROTON_MASS = 1.673e-27  # kg

# ====== Astronomical Constants & Units ======
AU = 1.496e11  # Astronomical unit, meters
M_TO_AU = 1 / AU
AU_TO_M = AU
KM_TO_AU = KM_TO_M * M_TO_AU
LIGHT_YEAR = 9.461e15  # Distance light travels in a year in meters
PARSEC = 3.086e16  # Parsec in meters
LUNAR_DISTANCE = 3.844e8  # Average distance from Earth to Moon in meters
SOLAR_MASS = 1.989e30  # kg
MU_SUN = G * SOLAR_MASS

R_EARTH = 6.371e6  # Earth radius, meters
M_EARTH = 5.972e24  # Earth mass, kg
R_SUN = 6.9634e8  # Sun radius, meters
M_SUN = 1.989e30  # Sun mass, kg

# ====== Mathematical Constants ======
pi = π = np.pi
DEG_TO_RAD = π / 180
GOLDEN_RATIO = (1 + 5**0.5) / 2
EULERS_NUMBER = np.exp(1)

# ====== Colors ======
YELLOW = [255, 255, 0]
BLUE = [0, 0, 255]
BEIGE = [245, 245, 220]
RED = [255, 0, 0]
ORANGE = [255, 165, 0]
CYAN = [0, 255, 255]
TEAL = [0, 128, 128]

# ====== Utility Functions ======
def deg_to_rad(degree):
    """Converts degrees to radians."""
    return degree * DEG_TO_RAD

def half_rgb(rgb_color):
    """Returns half of the RGB color values."""
    return tuple(max(int(color / 2), 0) for color in rgb_color)

def double_rgb(rgb_color):
    """Returns double of the RGB color values, capped at 255."""
    return tuple(min(int(color * 2), 255) for color in rgb_color)

def rgb_to_hsl(r, g, b):
    r /= 255.0
    g /= 255.0
    b /= 255.0
    max_val = max(r, g, b)
    min_val = min(r, g, b)
    diff = max_val-min_val
    l = (max_val+min_val) / 2.0
    if max_val == min_val:
        h = s = 0
    else:
        if l < 0.5:
            s = diff / (max_val + min_val)
        else:
            s = diff / (2.0 - max_val - min_val)
        if max_val == r:
            h = (g - b) / diff + (g < b) * 6
        elif max_val == g:
            h = (b - r) / diff + 2
        else:
            h = (r - g) / diff + 4
        h /= 6.0
    return h, s, l

def hsl_to_rgb(h, s, l):
    if s == 0:
        r = g = b = l
    else:
        def hue_to_rgb(p, q, t):
            if t < 0:
                t += 1
            if t > 1:
                t -= 1
            if t < 1/6:
                return p + (q - p) * 6 * t
            if t < 1/2:
                return q
            if t < 2/3:
                return p + (q - p) * (2/3 - t) * 6
            return p
        if l < 0.5:
            q = l * (1 + s)
        else:
            q = l + s - l * s
        p = 2 * l - q
        r = hue_to_rgb(p, q, h + 1/3)
        g = hue_to_rgb(p, q, h)
        b = hue_to_rgb(p, q, h - 1/3)
    return int(r * 255), int(g * 255), int(b * 255)

def lighten_rgb_hsl(rgb_color, factor=0.4):
    """Makes the RGB color lighter using HSL, preserving its hue."""
    h, s, l = rgb_to_hsl(*rgb_color)
    l = min(l + factor, 1)  # Increase lightness, but ensure it remains <= 1
    return hsl_to_rgb(h, s, l)

def celsius_to_fahrenheit(temp_c):
    """Convert Celsius to Fahrenheit."""
    return (temp_c * 9/5) + 32

def fahrenheit_to_celsius(temp_f):
    """Convert Fahrenheit to Celsius."""
    return (temp_f - 32) * 5/9

def escape_velocity(mass, radius):
    """Calculate escape velocity given mass (kg) and radius (m) of a celestial body."""
    return np.sqrt(2 * G * mass / radius)

def gravitational_force(m1, m2, r):
    """Calculate gravitational force between two masses (kg) separated by distance r (m)."""
    return G * m1 * m2 / r**2
