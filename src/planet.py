from constants import AU, KM_TO_M, SUN_AGE_SECONDS, SOLAR_MASS, G
import numpy as np
from body import body, Star, STAR_COLORS, Planet, Atmosphere

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
    pos=[0.39 * AU, 0.0, 0.0],
    mass=3.3011 * 10**23,
    radius=2439.7 * KM_TO_M,
    color=[245, 245, 220],
    type="planet",
    parent=sun,
    velocity=[0, -47.87 * KM_TO_M, 0],
    id=199,
) 

# Add atmospheres
venus_atmosphere = Atmosphere(
    composition={'CO2': 0.965, 'N2': 0.035},
    pressure_surface=9200000,  # 92 times that of Earth
    temperature_surface=737,   # in Kelvin
    albedo=0.77
)

venus = Planet(
    name="Venus",
    pos=[0.723 * AU, 0.0, 0.0],
    mass=4.8675 * 10**24,
    radius=6051.8 * KM_TO_M,
    color=[255, 255, 0],
    type="planet",
    parent=sun,
    velocity=[0, -35.02 * KM_TO_M, 0],
    Atmosphere=venus_atmosphere,
    id=299,
)

earth_atmosphere = Atmosphere(
    composition={'N2': 0.78, 'O2': 0.21, 'Ar': 0.01},
    pressure_surface=101325,  # Standard atmospheric pressure
    temperature_surface=288,  # in Kelvin
    albedo=0.3
)

earth = Planet(
    name="Earth",                                                 
    pos=[1.0 * AU, 0.0, 0.0],
    mass=5.97219 * 10**24,                                       
    radius=6371 * KM_TO_M,                                             
    color=[0, 0, 255],                                           
    type="planet",                                                
    parent=sun,                                              
    velocity=[0, -29.78 * KM_TO_M, 0.0],
    Atmosphere=earth_atmosphere,
    id=399,
)

# Earth's Moon
moon = body(
    name="Moon",
    pos=[1.0 * AU + 384400 * KM_TO_M, 0.0, 0.0],
    mass=7.342 * 10**22,
    radius=1737.4 * KM_TO_M,
    color=[220, 220, 220],
    type="moon",
    parent=earth,
    velocity=[0, -29.78 * KM_TO_M - 1.022 * KM_TO_M, 0],
    id=301,
)

mars = body(
    name="Mars",
    pos=[1.52 * AU, 0.0, 0.0],
    mass=6.4171 * 10**23,
    radius=3389.5 * KM_TO_M,
    color=[255, 0, 0],
    type="planet",
    parent=sun,
    velocity=[0, -24.07 * KM_TO_M, 0],
    id=499,
)

jupiter = body(
    name="Jupiter",
    pos=[5.20 * AU, 0.0, 0.0],
    mass=1.8982 * 10**27,
    radius=69911 * KM_TO_M,
    color=[255, 165, 0],
    type="planet",
    parent=sun,
    velocity=[0, -13.07 * KM_TO_M, 0],
    id=599,
)

io = body(
    name="Io",
    pos=[5.20 * AU + 421800 * KM_TO_M, 0.0, 0.0],
    mass=8.9319 * 10**22,
    radius=1821.6 * KM_TO_M,
    color=[255, 204, 0],
    type="moon",
    parent=jupiter,
    velocity=[0, -13.07 * KM_TO_M + 17.334 * KM_TO_M, 0],
    id=501,
)

europa = body(
    name="Europa",
    pos=[5.20 * AU + 671100 * KM_TO_M, 0.0, 0.0],
    mass=4.7998 * 10**22,
    radius=1560.8 * KM_TO_M,
    color=[173, 216, 230],
    type="moon",
    parent=jupiter,
    velocity=[0, -13.07 * KM_TO_M + 13.740 * KM_TO_M, 0],
    id=502,
)

ganymede = body(
    name="Ganymede",
    pos=[5.20 * AU + 1070400 * KM_TO_M, 0.0, 0.0],
    mass=1.4819 * 10**23,
    radius=2634.1 * KM_TO_M,
    color=[200, 200, 200],
    type="moon",
    parent=jupiter,
    velocity=[0, -13.07 * KM_TO_M + 10.880 * KM_TO_M, 0],
    id=503,
)

callisto = body(
    name="Callisto",
    pos=[5.20 * AU + 1882700 * KM_TO_M, 0.0, 0.0],
    mass=1.0759 * 10**23,
    radius=2410.3 * KM_TO_M,
    color=[169, 169, 169],
    type="moon",
    parent=jupiter,
    velocity=[0, -13.07 * KM_TO_M + 8.204 * KM_TO_M, 0],
    id=504,
)

saturn = body(
    name="Saturn",
    pos=[9.58 * AU, 0.0, 0.0],
    mass=5.6834 * 10**26,
    radius=58232 * KM_TO_M,
    color=[245, 245, 220],
    type="planet",
    parent=sun,
    velocity=[0, -9.68 * KM_TO_M, 0],
    id=699,
)

titan = body(
    name="Titan",
    pos=[9.58 * AU + 1221870 * KM_TO_M, 0.0, 0.0],
    mass=1.3452 * 10**23,
    radius=2574.73 * KM_TO_M,
    color=[255, 228, 196],
    type="moon",
    parent=saturn,
    velocity=[0, -9.68 * KM_TO_M + 5.57 * KM_TO_M, 0],
    id=601,
)

dione = body(
    name="Dione",
    pos=[9.58 * AU + 377420 * KM_TO_M, 0.0, 0.0],
    mass=1.095452 * 10**21,
    radius=561.4 * KM_TO_M,
    color=[180, 180, 180],
    type="moon",
    parent=saturn,
    velocity=[0, -9.68 * KM_TO_M + 10.03 * KM_TO_M, 0],
    id=602,
)

rhea = body(
    name="Rhea",
    pos=[9.58 * AU + 527108 * KM_TO_M, 0.0, 0.0],
    mass=2.306518 * 10**21,
    radius=763.8 * KM_TO_M,
    color=[160, 160, 160],
    type="moon",
    parent=saturn,
    velocity=[0, -9.68 * KM_TO_M + 8.48 * KM_TO_M, 0],
    id=603,
)

tethys = body(
    name="Tethys",
    pos=[9.58 * AU + 294619 * KM_TO_M, 0.0, 0.0],
    mass=6.17449 * 10**20,
    radius=531.1 * KM_TO_M,
    color=[140, 140, 140],
    type="moon",
    parent=saturn,
    velocity=[0, -9.68 * KM_TO_M + 11.35 * KM_TO_M, 0],
    id=604,
)

uranus = body(
    name="Uranus",
    pos=[19.18 * AU, 0.0, 0.0],
    mass=8.6810 * 10**25,
    radius=25362 * KM_TO_M,
    color=[0, 255, 255],
    type="planet",
    parent=sun,
    velocity=[0, -6.80 * KM_TO_M, 0],
    id=799,
)

neptune = body(
    name="Neptune",
    pos=[30.07 * AU, 0.0, 0.0],
    mass=1.02413 * 10**26,
    radius=24622 * KM_TO_M,
    color=[0, 128, 128],
    type="planet",
    parent=sun,
    velocity=[0, -5.43 * KM_TO_M, 0],
    id=899,
)

triton = body(
    name="Triton",
    pos=[30.07 * AU + 354759 * KM_TO_M, 0.0, 0.0],
    mass=2.139 * 10**22,
    radius=1353.4 * KM_TO_M,
    color=[50, 50, 255],
    type="moon",
    parent=neptune,
    velocity=[0, -5.43 * KM_TO_M + 4.39 * KM_TO_M, 0],
    id=902,
)

#bodies = [sun, earth]
#bodies = [sun, earth, mars]
bodies = [sun, earth, mercury, venus, mars, jupiter, saturn, uranus, neptune]
bodies.extend([moon, io, europa, ganymede, callisto, dione, rhea, tethys, triton])
