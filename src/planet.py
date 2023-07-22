from constants import G, day, AU, year, kg, deg, km
import numpy as np
import requests
import re
from datetime import datetime

class SpaceObject:
    def __init__(self, name, px, py, pz, mass, radius, color, aphelion=None, type=None):
        self.name = name
        self.px = px
        self.py = py
        self.pz = pz
        self.vel = np.zeros(3)
        self.mass = mass
        self.radius = radius
        self.color = color
        self.aphelion = aphelion
        self.type = type
        self.orbit = []
        self.pos, self.vel = self.get_real_time_data()

    def get_real_time_data(self):
        read = False
        with open("data/planets.txt", "r") as file:
            for line in file:
                if self.name in line:
                    read = True
                    continue
                elif read:
                    pos_line = line.split(",")
                    if len(pos_line) >= 5:
                        pos = np.array([float(pos_line[i]) for i in range(2, 5)]) * km  # Convert to km
                        continue
                    vel_line = line.split(",")
                    if len(vel_line) >= 5:
                        vel = np.array([float(vel_line[i]) for i in range(2, 5)]) * km  # Convert to km
                        read = False
                        return pos, vel
        return np.zeros(3), np.zeros(3)

    def get_horizons_data(self, object_id, start_date, end_date, coords='500@10'):
        """
        Fetches position and velocity data for a celestial object from the
        NASA HORIZONS system.
        """
        # The base URL for the HORIZONS web interface
        url = "https://ssd.jpl.nasa.gov/horizons_batch.cgi?batch=1"

        # The command settings for the HORIZONS request
        command = f'{object_id};CENTER={coords};COMMAND={object_id};' \
                  f'START_TIME="{start_date}";STOP_TIME="{end_date}";' \
                  'STEP_SIZE="1 d";QUANTITIES="2,9,20,23,24";'

        # Send the HTTP request to HORIZONS
        response = requests.get(url, params={'batch': 1, 'MAKE_EPHEM': 'YES', 'COMMAND': command})

        # Raise an exception if the request was unsuccessful
        response.raise_for_status()

        # Return the data as a string
        return response.text

    def position_at(self, t):
        # Get the mean anomaly at time t
        M = self.mean_motion * t

        # Use Newton's method to find the eccentric anomaly
        E = M
        for _ in range(10):
            E = E - (E - self.ecc * np.sin(E) - M) / (1 - self.ecc * np.cos(E))

        # Find the true anomaly
        theta = 2 * np.arctan(np.sqrt((1 + self.ecc) / (1 - self.ecc)) * np.tan(E / 2))

        # Calculate the distance from the parent object
        r = self.sma * (1 - self.ecc**2) / (1 + self.ecc * np.cos(theta))

        # Return the position
        return r * np.array([np.cos(theta), np.sin(theta), 0])

    def velocity_at(self, t):
        # Get the position at time t
        pos = self.position_at(t)

        # Get the magnitude of the velocity
        v = np.sqrt(G * self.parent.mass * (2 / np.linalg.norm(pos) - 1 / self.sma))

        # The velocity is perpendicular to the position vector
        vel = v * np.array([-pos[1], pos[0], 0]) / np.linalg.norm(pos)

        # Return the velocity
        return vel


# Name, Semi-major axis, Eccentricity, Orbital period in earth years, Mass, Radius, Color, Parent, Object type

# Sun
sun = SpaceObject("Sun", 0, 0, 0, 1.989e30, 696340 * km, (255, 255, 0), None, "Star")

# Planets and Moons
mercury = SpaceObject("Mercury", 0.39 * AU, 0.205, 0.24 * year, 3.3011e23, 2439.7 * km, (169, 169, 169), sun, "Planet")
venus = SpaceObject("Venus", 0.72 * AU, 0.007, 0.62 * year, 4.8675e24, 6051.8 * km, (210, 180, 140), sun, "Planet")
earth = SpaceObject("Earth", 1.00 * AU, 0.017, 1.00 * year, 5.97237e24, 6371.0 * km, (0, 0, 255), sun, "Planet")
moon = SpaceObject("Moon", 384400 * km, 0.055, 27.322 * day, 7.342e22, 1737.1 * km, (170, 170, 170), earth, "Moon")
mars = SpaceObject("Mars", 1.52 * AU, 0.093, 1.88 * year, 6.4171e23, 3389.5 * km, (255, 0, 0), sun, "Planet")
phobos = SpaceObject("Phobos", 9376 * km, 0.015, 0.31891 * day, 1.0659e16, 11.1 * km, (150, 150, 150), mars, "Moon")
deimos = SpaceObject("Deimos", 23458 * km, 0.0002, 1.26244 * day, 1.4712e15, 6.2 * km, (150, 150, 150), mars, "Moon")
jupiter = SpaceObject("Jupiter", 5.20 * AU, 0.048, 11.86 * year, 1.8982e27, 69911 * km, (205, 133, 63), sun, "Planet")
ganymede = SpaceObject("Ganymede", 1.07e6 * km, 0.0013, 7.15 * day, 1.4819e23, 2634.1 * km, (102, 102, 102), jupiter, "Moon")
callisto = SpaceObject("Callisto", 1.883e6 * km, 0.0074, 16.69 * day, 1.0759e23, 2410.3 * km, (127, 127, 127), jupiter, "Moon")
europa = SpaceObject("Europa", 6.711e5 * km, 0.0094, 3.55 * day, 4.7998e22, 1560.7 * km, (192, 192, 192), jupiter, "Moon")
io = SpaceObject("Io", 4.22e5 * km, 0.0041, 1.77 * day, 8.9319e22, 1821.6 * km, (255, 165, 0), jupiter, "Moon")
saturn = SpaceObject("Saturn", 9.58 * AU, 0.056, 29.46 * year, 5.6834e26, 58232 * km, (210, 180, 140), sun, "Planet")
titan = SpaceObject("Titan", 1.221e6 * km, 0.0288, 15.95 * day, 1.3452e23, 2575.5 * km, (184, 134, 11), saturn, "Moon")
uranus = SpaceObject("Uranus", 19.18 * AU, 0.046, 84.02 * year, 8.6810e25, 25362 * km, (0, 255, 255), sun, "Planet")
ariel = SpaceObject("Ariel", 1.908e5 * km, 0.0012, 2.520 * day, 1.353e21, 578.9 * km, (192, 192, 192), uranus, "Moon")
umbriel = SpaceObject("Umbriel", 2.66e5 * km, 0.0039, 4.144 * day, 1.172e21, 584.7 * km, (192, 192, 192), uranus, "Moon")
neptune = SpaceObject("Neptune", 30.07 * AU, 0.010, 164.8 * year, 1.02413e26, 24622 * km, (0, 0, 128), sun, "Planet")
triton = SpaceObject("Triton", 3.547e5 * km, 0.0000, -5.877 * day, 2.139e22, 1353.4 * km, (192, 192, 192), neptune, "Moon")

# Debris
ceres = SpaceObject("Ceres", 2.77 * AU, 0.079, 4.60 * year, 9.3835e20, 473 * km, (200, 200, 200), sun, "Debris")
pluto = SpaceObject("Pluto", 39.48 * AU, 0.248, 247.94 * year, 1.303e22, 1188.3 * km, (100, 100, 100), sun, "Debris")

# Planets, Moons and the Sun
BODIES = [
    sun,
    mercury,
    venus,
    earth,
    moon,
    mars,
    phobos,
    deimos,
    jupiter,
    ganymede,
    callisto,
    europa,
    io,
    saturn,
    titan,
    uranus,
    ariel,
    umbriel,
    neptune,
    triton,
    ceres,
    pluto
]

# Sun and Planets only
PLANETS = [
    sun,
    mercury,
    venus,
    earth,
    mars,
    jupiter,
    saturn,
    uranus,
    neptune
]
