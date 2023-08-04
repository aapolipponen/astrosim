# constants.py
import numpy as np

# Constants
G = 6.67430e-11  # Gravitational constant, in m^3 kg^-1 s^-2
day = 60 * 60 * 24  # Day in seconds
AU = 1.496e11  # Astronomical unit in meters
deg = np.pi / 180  # Degree in radians
year = 3.154e7  # Year in seconds
hour = 60 * 60
kg = 1  # Kilogram in kilograms (already correct)
km = 1e3  # Kilometer in meters

# Physical constants
c = 2.998e8  # Speed of light in m/s
h = 6.626e-34  # Planck's constant in Js
k_B = 1.381e-23  # Boltzmann constant in J/K

# Astronomical constants
R_earth = 6.371e6  # Earth radius in meters
M_earth = 5.972e24  # Earth mass in kg
R_sun = 6.9634e8  # Sun radius in meters
M_sun = 1.989e30  # Sun mass in kg

# Conversion factors
km_to_m = 1e3  # Kilometers to meters
m_to_km = 1e-3  # Meters to kilometers
AU_to_m = AU  # Astronomical units to meters
m_to_AU = 1/AU  # Meters to astronomical units
kg_to_g = 1e3  # Kilograms to grams
g_to_kg = 1e-3  # Grams to kilograms

# RGB Colors
yellow = [255, 255, 0]
blue = [0, 0, 255]
beige = [245, 245, 220]
red = [255, 0, 0]
orange = [255, 165, 0]
cyan = [0, 255, 255]
teal = [0, 128, 128]

# Functions
def deg(degree):
    return degree * np.pi / 180

def half_rgb(rgb_color):
    return tuple(max(int(color / 2), 0) for color in rgb_color)
