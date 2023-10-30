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
        momentum=None,
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

        if momentum is None:
            self.momentum = np.zeros(3)
        else:
            self.momentum = np.array(momentum)

    def surface_gravity(self):
        return G * self.mass / (self.radius ** 2)
    
    def update_orbital_elements_from_state_vectors(self):
        if self.parent is None:
            return

        mu = G * self.parent.mass
        r = self.pos - self.parent.pos
        v = self.vel - self.parent.vel

        h = np.cross(r, v)
        k = np.array([0, 0, 1])
        N = np.cross(k, h)

        e_vector = (np.cross(v, h) - mu * r / np.linalg.norm(r)) / mu

        self.eccentricity = np.linalg.norm(e_vector)
        self.semi_major_axis = (np.linalg.norm(h)**2) / (mu * (1 - self.eccentricity**2))

        h_norm = np.linalg.norm(h)
        N_norm = np.linalg.norm(N)

        self.inclination = np.arccos(h[2] / h_norm)

        if N_norm != 0:
            self.longitude_of_ascending_node = np.arccos(N[0] / N_norm)
            self.argument_of_periapsis = np.arccos(np.dot(N, e_vector) / (N_norm * self.eccentricity))
        else:
            # Orbit is planar. The notion of ascending node is meaningless.
            # You could choose to define argument of periapsis directly in this case.
            self.longitude_of_ascending_node = 0
            #self.argument_of_periapsis = np.arctan2(e_vector[1], e_vector[0])
            self.argument_of_periapsis = 0