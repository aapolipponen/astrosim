import numpy as np
from constants import G

class body:
    def __init__(
        self,
        name,
        mass,
        radius,
        type=None,
        color=None,
        parent=None,
        id=None,
        pos=None,
        velocity=None,
        semi_major_axis=0,
        semi_minor_axis=0,
        eccentricity=0,
        inclination=0,
        longitude_of_ascending_node=0,
        argument_of_periapsis=0,
        true_anomaly=0,
        mean_anomaly = 0,
        eccentric_anomaly=0,
        orbital_period = 0,
        rotational_period=0,
        tilt=0,
        current_rotation_angle=0
    ):
        self.name = name
        self.mass = mass
        self.radius = radius
        self.type = type
        self.color = color
        self.parent = parent
        self.id = id

        # Orbital elements
        self.semi_major_axis = semi_major_axis
        self.semi_minor_axis = semi_minor_axis
        self.eccentricity = eccentricity
        self.inclination = inclination
        self.longitude_of_ascending_node = longitude_of_ascending_node
        self.argument_of_periapsis = argument_of_periapsis
        self.true_anomaly = true_anomaly
        self.mean_anomaly = mean_anomaly
        self.eccentric_anomaly = eccentric_anomaly
        self.orbital_period = orbital_period

        # Rotational elements
        self.rotational_period = rotational_period
        self.tilt = tilt
        self.current_rotation_angle = current_rotation_angle

        # Position and velocity
        if pos is None:
            self.pos = np.zeros(3)
        else:
            self.pos = np.array(pos)

        if velocity is None:
            self.vel = np.zeros(3)
        else:
            self.vel = np.array(velocity)

    def surface_gravity(self):
        return G * self.mass / (self.radius ** 2)
    
    def update_orbital_elements_from_state_vectors(self):
        # Ensure that a parent body is defined for relative motion
        if self.parent is None:
            return

        mu = G * self.parent.mass  # Gravitational parameter of the central body

        r = self.pos - self.parent.pos  # Relative position vector
        v = self.vel - self.parent.vel  # Relative velocity vector

        # Angular Momentum
        h = np.cross(r, v)

        # Node Vector
        k = np.array([0, 0, 1])
        N = np.cross(k, h)

        # Eccentricity Vector
        e_vector = (1/mu) * ((np.cross(v, h)) - (mu * r/np.linalg.norm(r)))

        # Update attributes
        self.eccentricity = np.linalg.norm(e_vector)
        self.semi_major_axis = (np.linalg.norm(h)**2) / (mu * (1 - self.eccentricity**2))
        self.inclination = np.arccos(h[2] / np.linalg.norm(h))
        self.longitude_of_ascending_node = np.arccos(N[0] / np.linalg.norm(N))
        self.argument_of_periapsis = np.arccos(np.dot(N, e_vector) / (np.linalg.norm(N) * self.eccentricity))

        # True Anomaly (careful of quadrant)
        dot_product = np.dot(e_vector, r)
        if dot_product >= 0:
            self.true_anomaly = np.arccos(dot_product / (self.eccentricity * np.linalg.norm(r)))
        else:
            self.true_anomaly = 2 * np.pi - np.arccos(dot_product / (self.eccentricity * np.linalg.norm(r)))

        # Adjust angles for correct quadrants
        if N[1] < 0:
            self.longitude_of_ascending_node = 2 * np.pi - self.longitude_of_ascending_node

        if e_vector[2] < 0:
            self.argument_of_periapsis = 2 * np.pi - self.argument_of_periapsis