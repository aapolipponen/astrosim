# Orbital decay or something visual?
class Atmosphere:
    def __init__(
        self,
        composition=None,  # e.g., {'N2': 0.78, 'O2': 0.21, 'Ar': 0.01}
        pressure_surface=101325,  # surface pressure in Pascals
        temperature_surface=288,  # surface temperature in Kelvin
        scale_height=8000,  # in meters
        albedo=0.3,  # fraction of sunlight reflected by the atmosphere
        absorption_coefficients=None  # could be a dict of wavelengths and coefficients
    ):
        self.composition = composition if composition is not None else {}
        self.pressure_surface = pressure_surface
        self.temperature_surface = temperature_surface
        self.scale_height = scale_height
        self.albedo = albedo
        self.absorption_coefficients = absorption_coefficients if absorption_coefficients is not None else {}

    def optical_properties(self, wavelength):
        """
        Return optical properties at a given wavelength.
        This is a placeholder. In reality, the calculations might be complex.
        """
        absorption = self.absorption_coefficients.get(wavelength, 0)
        scattering = 1 - absorption
        return scattering, absorption