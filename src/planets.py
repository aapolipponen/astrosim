from constants import AU, KM_TO_M, SUN_AGE_SECONDS, SOLAR_MASS, π
import numpy as np
from body import body
from star import Star, STAR_COLORS
from planet import Planet
from atmosphere import Atmosphere

sun = Star(
    name="Sun",
    pos=[0.0, 0.0, 0.0],  
    mass=SOLAR_MASS, 
    radius=696342 * KM_TO_M, 
    color=STAR_COLORS["G"],  # Using the dictionary for color
    type="star",
    luminosity=3.828e26, 
    spectral_type="G2V", 
    velocity=[0.0, 0.0, 0.0],
    id=10,
    age=SUN_AGE_SECONDS  # Adding the Sun's age
)

mercury = Planet(
    name="Mercury",
    pos=[0.46669835 * AU, 0.0, 0.0],
    mass=3.3011 * 10**23,
    radius=2439.7 * KM_TO_M,
    color=[245, 245, 220],
    type="planet",
    parent=sun,
    velocity=[0, -38.86 * KM_TO_M, 0],
    id=199,
) 

venus_atmosphere = Atmosphere(
    composition={'CO2': 0.965, 'N2': 0.035},
    pressure_surface=9200000,  # 92 times that of Earth
    temperature_surface=737,   # in Kelvin
    albedo=0.77,
    absorption_coefficients={500: 0.10, 600: 0.08, 700: 0.06}  # Hypothetical values for illustration
)

venus = Planet(
    name="Venus",
    pos=[0.7282313 * AU, 0.0, 0.0],
    mass=4.8675 * 10**24,
    radius=6051.8 * KM_TO_M,
    color=[255, 255, 0],
    type="planet",
    parent=sun,
    velocity=[0, -34.78 * KM_TO_M, 0],
    Atmosphere=venus_atmosphere,
    id=299,
)

earth_atmosphere = Atmosphere(
    composition={'N2': 0.78, 'O2': 0.21, 'Ar': 0.01},
    pressure_surface=101325,  # Standard atmospheric pressure
    temperature_surface=288,  # in Kelvin
    albedo=0.3,
    absorption_coefficients={500: 0.05, 600: 0.03, 700: 0.02}  # Made-up values for illustration
)

earth = Planet(
    name="Earth",                                                 
    pos=[1.01671033 * AU, 0.0, 0.0],
    mass=5.97219 * 10**24,                                       
    radius=6371 * KM_TO_M,                                             
    color=[0, 0, 255],                                           
    type="planet",                                                
    parent=sun,                                              
    velocity=[0, -29.29 * KM_TO_M, 0.0],
    Atmosphere=earth_atmosphere,
    id=399,
)

# Earth's Moon
moon = body(
    name="Moon",
    pos=[earth.pos[0] + 405700 * KM_TO_M, 0.0, 0.0],
    mass=7.342 * 10**22,
    radius=1737.4 * KM_TO_M,
    color=[220, 220, 220],
    type="moon",
    parent=earth,
    velocity=[0, earth.vel[1] - 0.970 * KM_TO_M, 0],
    id=301,
)

mars_atmosphere = Atmosphere(
    composition={"CO2": 0.9503, "N2": 0.027, "Ar": 0.0189, "O2": 0.0013, "CO": 0.00007},
    pressure_surface=610.0,  # Average surface pressure in pascals
    temperature_surface=210,  # Approximate average surface temperature in Kelvin
    albedo=0.25,  # A rough estimate
    absorption_coefficients={500: 0.04, 600: 0.02, 700: 0.01}  # Hypothetical values for illustration
)

mars = Planet(
    name="Mars",
    pos=[1.66599116 * AU, 0.0, 0.0],
    mass=6.4171 * 10**23,
    radius=3389.5 * KM_TO_M,
    color=[255, 0, 0],
    type="planet",
    parent=sun,
    velocity=[0, -21.97 * KM_TO_M, 0],
    Atmosphere=mars_atmosphere,
    id=499,
)

jupiter = Planet(
    name="Jupiter",
    pos=[5.45516759 * AU, 0.0, 0.0],
    mass=1.8982 * 10**27,
    radius=69911 * KM_TO_M,
    color=[255, 165, 0],
    type="planet",
    parent=sun,
    velocity=[0, -12.44 * KM_TO_M, 0],
    id=599,
)

io = body(
    name="Io",
    pos=[jupiter.pos[0] + 421800 * KM_TO_M, 0.0, 0.0],
    mass=8.9319 * 10**22,
    radius=1821.6 * KM_TO_M,
    color=[255, 204, 0],
    type="moon",
    parent=jupiter,
    velocity=[0, jupiter.vel[1] + 17.334 * KM_TO_M, 0],
    id=501,
)

europa = body(
    name="Europa",
    pos=[jupiter.pos[0] + 671100 * KM_TO_M, 0.0, 0.0],
    mass=4.7998 * 10**22,
    radius=1560.8 * KM_TO_M,
    color=[173, 216, 230],
    type="moon",
    parent=jupiter,
    velocity=[0, jupiter.vel[1] + 13.740 * KM_TO_M, 0],
    id=502,
)

ganymede = body(
    name="Ganymede",
    pos=[jupiter.pos[0] + 1070400 * KM_TO_M, 0.0, 0.0],
    mass=1.4819 * 10**23,
    radius=2634.1 * KM_TO_M,
    color=[200, 200, 200],
    type="moon",
    parent=jupiter,
    velocity=[0, jupiter.vel[1] + 10.880 * KM_TO_M, 0],
    id=503,
)

callisto = body(
    name="Callisto",
    pos=[jupiter.pos[0] + 1882700 * KM_TO_M, 0.0, 0.0],
    mass=1.0759 * 10**23,
    radius=2410.3 * KM_TO_M,
    color=[169, 169, 169],
    type="moon",
    parent=jupiter,
    velocity=[0, jupiter.vel[1] + 8.204 * KM_TO_M, 0],
    id=504,
)

saturn = Planet(
    name="Saturn",
    pos=[10.05351 * AU, 0.0, 0.0],
    mass=5.6834 * 10**26,
    radius=58232 * KM_TO_M,
    color=[245, 245, 220],
    type="planet",
    parent=sun,
    velocity=[0, -9.14 * KM_TO_M, 0],
    id=699,
)

titan = body(
    name="Titan",
    pos=[saturn.pos[0] + 1221870 * KM_TO_M, 0.0, 0.0],
    mass=1.3452 * 10**23,
    radius=2574.73 * KM_TO_M,
    color=[255, 228, 196],
    type="moon",
    parent=saturn,
    velocity=[0, saturn.pos[1] + 5.57 * KM_TO_M, 0],
    id=601,
)

dione = body(
    name="Dione",
    pos=[saturn.pos[0] + 377420 * KM_TO_M, 0.0, 0.0],
    mass=1.095452 * 10**21,
    radius=561.4 * KM_TO_M,
    color=[180, 180, 180],
    type="moon",
    parent=saturn,
    velocity=[0, saturn.pos[1] + 10.03 * KM_TO_M, 0],
    id=602,
)

rhea = body(
    name="Rhea",
    pos=[saturn.pos[0] + 527108 * KM_TO_M, 0.0, 0.0],
    mass=2.306518 * 10**21,
    radius=763.8 * KM_TO_M,
    color=[160, 160, 160],
    type="moon",
    parent=saturn,
    velocity=[0, saturn.pos[1] + 8.48 * KM_TO_M, 0],
    id=603,
)

iapetus = body(
    name="Iapetus",
    pos=[saturn.pos[0] + 3560850 * KM_TO_M, 0.0, 0.0],
    mass=1.81 * 10**21,
    radius=735.6 * KM_TO_M,
    color=[100, 100, 100],
    type="moon",
    parent=saturn,
    velocity=[0, saturn.pos[1] + 3.26 * KM_TO_M, 0],
    id=605,
)


tethys = body(
    name="Tethys",
    pos=[saturn.pos[0] + 294619 * KM_TO_M, 0.0, 0.0],
    mass=6.17449 * 10**20,
    radius=531.1 * KM_TO_M,
    color=[140, 140, 140],
    type="moon",
    parent=saturn,
    velocity=[0, saturn.pos[1] + 11.35 * KM_TO_M, 0],
    id=604,
)

uranus = Planet(
    name="Uranus",
    pos=[20.0964719 * AU, 0.0, 0.0],
    mass=8.6810 * 10**25,
    radius=25362 * KM_TO_M,
    color=[0, 255, 255],
    type="planet",
    parent=sun,
    velocity=[0, -6.49 * KM_TO_M, 0],
    id=799,
)

ariel = body(
    name="Ariel",
    pos=[uranus.pos[0] + 191020 * KM_TO_M, 0.0, 0.0],
    mass=1.353 * 10**21,
    radius=578.9 * KM_TO_M,
    color=[100, 100, 100],
    type="moon",
    parent=uranus,
    velocity=[0, uranus.vel[1] + 5.51 * KM_TO_M, 0],
    id=804,
)

titania = body(
    name="Titania",
    pos=[uranus.pos[0] + 435910 * KM_TO_M, 0.0, 0.0],
    mass=3.526 * 10**21,
    radius=788.9 * KM_TO_M,
    color=[80, 80, 80],
    type="moon",
    parent=uranus,
    velocity=[0, uranus.vel[2] + 3.64 * KM_TO_M, 0],
    id=806,
)

neptune = Planet(
    name="Neptune",
    pos=[29.810795 * AU, 0.0, 0.0],
    mass=1.02413 * 10**26,
    radius=24622 * KM_TO_M,
    color=[0, 128, 128],
    type="planet",
    parent=sun,
    velocity=[0, -5.37 * KM_TO_M, 0],
    id=899,
)

triton = body(
    name="Triton",
    pos=[neptune.pos[0] + 354759 * KM_TO_M, 0.0, 0.0],
    mass=2.139 * 10**22,
    radius=1353.4 * KM_TO_M,
    color=[50, 50, 255],
    type="moon",
    parent=neptune,
    velocity=[0, -5.43 * KM_TO_M + 4.39 * KM_TO_M, 0],
    id=902,
)

bodies = [sun, earth]
#bodies = [sun, earth, mars]
#bodies = [sun, earth, mercury, venus, mars, jupiter, saturn, uranus, neptune]
#bodies.extend([moon, io, europa, ganymede, callisto, dione, rhea, iapetus, tethys, triton, ariel, triton])
