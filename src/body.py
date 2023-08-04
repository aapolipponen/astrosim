import numpy as np

class body:
    def __init__(
        self,
        name,
        mass,
        radius,
        type=None,
        color=None,
        parent=None,
        pos=None,
        velocity=None,
        E=0,
        L=0,
        semi_major_axis=0,
        semi_minor_axis=0,
        eccentricity=0,
        inclination=0,
        longitude_of_ascending_node=0,
        argument_of_periapsis=0,
        true_anomaly=0,
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

        # Orbital elements
        self.semi_major_axis = semi_major_axis
        self.eccentricity = eccentricity
        self.inclination = inclination
        self.longitude_of_ascending_node = longitude_of_ascending_node
        self.argument_of_periapsis = argument_of_periapsis
        self.true_anomaly = true_anomaly

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
