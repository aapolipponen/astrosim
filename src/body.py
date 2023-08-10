import numpy as np
from constants import G, SOLAR_MASS, year

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
    
# Time periods (in million years) for different evolutionary stages
LOW_MASS_RED_DWARF_AGE = 10e9
MEDIUM_MASS_RED_GIANT_START_AGE = 1e9
MEDIUM_MASS_RED_GIANT_END_AGE = 5e9
HIGH_MASS_SUPERGIANT_START_AGE = 1e6
HIGH_MASS_SUPERGIANT_END_AGE = 10e6

class Star(body):
    def __init__(self, luminosity, spectral_type, age=0, hydrogen_content=100, helium_content=0, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.luminosity = luminosity
        self.spectral_type = spectral_type
        self.age = age
        self.hydrogen_content = hydrogen_content
        self.helium_content = helium_content
        self.stage = "main_sequence"  # Initial stage
        self.has_changed_stage = False  # This will help us track changes in the star's lifecycle stage

        # Additional elements 
        self.carbon_content = 0
        self.oxygen_content = 0
        self.neon_content = 0

        if 'temperature' not in kwargs:
            self.temperature = self._get_temperature_from_spectral_type(spectral_type)

        # Define the main sequence lifetime based on mass 
        self.main_sequence_lifetime = self._get_main_sequence_lifetime()
        
        self.has_evolved = {
            "red_giant": False,
            "white_dwarf": False,
            "red_supergiant": False,
            "supernova": False
        }    
    
    def _update_properties_based_on_age(self):
        # Main Sequence phase adjustments
        if self.stage == "main_sequence":
            # Gradually increase the size and decrease the temperature (make it redder)
            self.radius += (self.age / self.main_sequence_lifetime) * self.radius
            temp_decrease_factor = 1 - (self.age / self.main_sequence_lifetime)
            self.temperature *= temp_decrease_factor

        # Red Giant phase adjustments
        elif self.stage == "red_giant":
            # Drastically increase size and make it cooler and redder
            self.radius *= 100
            self.temperature *= 0.7

        # White Dwarf phase adjustments
        elif self.stage == "white_dwarf":
            # Drastically decrease size and make it hotter
            self.radius *= 0.01
            self.temperature *= 1.5

        self.color = self._get_color_from_temperature()

    def _get_color_from_temperature(self):
        if self.temperature > 20000:
            return [255, 255, 255]  # Pure white
        elif 10000 < self.temperature <= 20000:
            return STAR_COLORS["O"]  # Blue
        elif 7500 < self.temperature <= 10000:
            return STAR_COLORS["B"]  # Blue-white
        elif 6000 < self.temperature <= 7500:
            return STAR_COLORS["A"]
        elif 5000 < self.temperature <= 6000:
            return STAR_COLORS["F"]
        elif 3500 < self.temperature <= 5000:
            return STAR_COLORS["G"]
        else:
            return STAR_COLORS["M"]

    def evolve(self, time_elapsed):
        # Time_elapsed is the time since last evolution check
        self.age += time_elapsed
        if self.mass < 0.5 * 1.989e30:  # Less than 0.5 solar masses
            self._evolve_red_dwarf()
        elif self.mass <= 8 * 1.989e30:  # Between 0.5 to 8 solar masses
            self._evolve_sun_like()
        else:
            self._evolve_massive_star()
        self._update_properties_based_on_age()

    def _get_main_sequence_lifetime(self):
        # Simplified formula: main sequence lifetime is inversely proportional to the cube of the mass.
        solar_mass_lifetime = 10 * 1e9 * 365 * 24 * 3600  # 10 billion years for our sun
        return solar_mass_lifetime / (self.mass / 1.989e30) ** 3

    def burn_hydrogen(self, time_elapsed):
        # Simulate the fusion of hydrogen to helium.
        # This is a VERY simplistic model. Real hydrogen burning would depend on stellar physics, pressure, and temperature.
        if self.hydrogen_content > 0:
            burned_hydrogen = 0.0001 * time_elapsed  # Arbitrary burn rate
            self.hydrogen_content -= burned_hydrogen
            self.helium_content += burned_hydrogen
            
    def _get_temperature_from_spectral_type(self, spectral_type):
        # This is a very basic method to determine temperature from spectral type.
        # In a real system, you'd want a more detailed conversion based on astronomy research.
        spectral_temp_map = {
            "O": 30000,  # O type stars are the hottest
            "B": 10000,
            "A": 7500,
            "F": 6000,
            "G": 5500,  # Our sun is a G type star
            "K": 4000,
            "M": 3000   # M type stars are the coolest
        }
        # Get just the first character from the spectral type
        base_type = spectral_type[0].upper()
        return spectral_temp_map.get(base_type, 5500)  # Default to G type temperature if not found

    def _evolve_red_dwarf(self):
        # Red dwarfs burn slowly and haven't evolved in age of universe yet.
        # No need for drastic changes.
        pass

    def _evolve_sun_like(self):
        if self.age > 10 * 1e9 * 365 * 24 * 3600 and not self.has_evolved["red_giant"]:
            self.become_red_giant()
            self.has_evolved["red_giant"] = True

        if self.age > 12 * 1e9 * 365 * 24 * 3600 and not self.has_evolved["white_dwarf"]:
            self.become_white_dwarf()
            self.has_evolved["white_dwarf"] = True
            
    def _evolve_massive_star(self):
        # Implementing a more complex lifecycle for massive stars can be challenging.
        # For simplicity:
        if self.age >= 5 * 1e6 * 365 * 24 * 3600:  # If age is greater than 5 million years (approx.)
            if self.stage != "red_supergiant":
                self.become_red_supergiant()
        if self.age >= 10 * 1e6 * 365 * 24 * 3600:  # If age is greater than 10 million years (approx.)
            if self.stage != "supernova":
                self.explode_supernova()
                
    def become_red_giant(self):
        self.stage = "red_giant"
        self.has_changed_stage = True
        print(f"{self.name} has become a Red Giant!")

    def become_red_supergiant(self):
        self.stage = "red_supergiant"
        self.has_changed_stage = True
        print(f"{self.name} has become a Red Supergiant!")

    def become_white_dwarf(self):
        self.stage = "white_dwarf"
        self.has_changed_stage = True
        print(f"{self.name} has become a White Dwarf!")

    def explode_supernova(self):
        self.stage = "supernova"
        self.has_changed_stage = True
        print(f"{self.name} has exploded as a Supernova!")
        
# Define a dictionary for star colors based on spectral type.
# These are simplistic and might need adjustment for a visually accurate simulation.
STAR_COLORS = {
    "O": [157, 180, 255],  # Blue
    "B": [170, 191, 255],  # Blue white
    "A": [202, 215, 255],  # White
    "F": [255, 255, 242],  # Whitish yellow
    "G": [255, 244, 234],  # Yellow
    "K": [255, 210, 161],  # Orange
    "M": [255, 204, 111],  # Reddish(Reddish? More like Reddit)-orange (Insert is upvote red or orange debate here)
}