from constants import G, day, AU, year, kg, deg, km, R_earth, M_earth, M_sun, R_sun, deg, yellow, blue, beige, teal, red, orange, cyan
import numpy as np
from body import body

sun = body(
    name="Sun",
    mass=1.989 * 10**30,
    radius=696342 * km,
    color=[255, 223, 0],
    type="star",
    id=10,
)

mercury = body(
    name="Mercury",
    pos=[0.39 * AU, 0.0, 0.0],
    mass=3.3011 * 10**23,
    radius=2439.7 * km,
    color=[245, 245, 220],
    type="planet",
    parent=sun,
    velocity=[0, -47.87 * km, 0],
    id=199,
) 

venus = body(
    name="Venus",
    pos=[0.723 * AU, 0.0, 0.0],
    mass=4.8675 * 10**24,
    radius=6051.8 * km,
    color=[255, 255, 0],
    type="planet",
    parent=sun,
    velocity=[0, -35.02 * km, 0],
    id=299,
)

earth = body(
    name="Earth",                                                 
    pos=[1.0 * AU, 0.0, 0.0],
    mass=5.97219 * 10**24,                                       
    radius=6371 * km,                                             
    color=[0, 0, 255],                                           
    type="planet",                                                
    parent=sun,                                              
    velocity=[0, -29.78 * km, 0.0],
    id=399,
)

# Earth's Moon
moon = body(
    name="Moon",
    pos=[1.0 * AU + 384400 * km, 0.0, 0.0],
    mass=7.342 * 10**22,
    radius=1737.4 * km,
    color=[220, 220, 220],
    type="moon",
    parent=earth,
    velocity=[0, -29.78 * km - 1.022 * km, 0],
    id=301,
)

mars = body(
    name="Mars",
    pos=[1.52 * AU, 0.0, 0.0],
    mass=6.4171 * 10**23,
    radius=3389.5 * km,
    color=[255, 0, 0],
    type="planet",
    parent=sun,
    velocity=[0, -24.07 * km, 0],
    id=499,
)

jupiter = body(
    name="Jupiter",
    pos=[5.20 * AU, 0.0, 0.0],
    mass=1.8982 * 10**27,
    radius=69911 * km,
    color=[255, 165, 0],
    type="planet",
    parent=sun,
    velocity=[0, -13.07 * km, 0],
    id=599,
)

io = body(
    name="Io",
    pos=[5.20 * AU + 421800 * km, 0.0, 0.0],
    mass=8.9319 * 10**22,
    radius=1821.6 * km,
    color=[255, 204, 0],
    type="moon",
    parent=jupiter,
    velocity=[0, -13.07 * km + 17.334 * km, 0],
    id=501,
)

europa = body(
    name="Europa",
    pos=[5.20 * AU + 671100 * km, 0.0, 0.0],
    mass=4.7998 * 10**22,
    radius=1560.8 * km,
    color=[173, 216, 230],
    type="moon",
    parent=jupiter,
    velocity=[0, -13.07 * km + 13.740 * km, 0],
    id=502,
)

ganymede = body(
    name="Ganymede",
    pos=[5.20 * AU + 1070400 * km, 0.0, 0.0],
    mass=1.4819 * 10**23,
    radius=2634.1 * km,
    color=[200, 200, 200],
    type="moon",
    parent=jupiter,
    velocity=[0, -13.07 * km + 10.880 * km, 0],
    id=503,
)

callisto = body(
    name="Callisto",
    pos=[5.20 * AU + 1882700 * km, 0.0, 0.0],
    mass=1.0759 * 10**23,
    radius=2410.3 * km,
    color=[169, 169, 169],
    type="moon",
    parent=jupiter,
    velocity=[0, -13.07 * km + 8.204 * km, 0],
    id=504,
)

saturn = body(
    name="Saturn",
    pos=[9.58 * AU, 0.0, 0.0],
    mass=5.6834 * 10**26,
    radius=58232 * km,
    color=[245, 245, 220],
    type="planet",
    parent=sun,
    velocity=[0, -9.68 * km, 0],
    id=699,
)

titan = body(
    name="Titan",
    pos=[9.58 * AU + 1221870 * km, 0.0, 0.0],
    mass=1.3452 * 10**23,
    radius=2574.73 * km,
    color=[255, 228, 196],
    type="moon",
    parent=saturn,
    velocity=[0, -9.68 * km + 5.57 * km, 0],
    id=601,
)

dione = body(
    name="Dione",
    pos=[9.58 * AU + 377420 * km, 0.0, 0.0],
    mass=1.095452 * 10**21,
    radius=561.4 * km,
    color=[180, 180, 180],
    type="moon",
    parent=saturn,
    velocity=[0, -9.68 * km + 10.03 * km, 0],
    id=602,
)

rhea = body(
    name="Rhea",
    pos=[9.58 * AU + 527108 * km, 0.0, 0.0],
    mass=2.306518 * 10**21,
    radius=763.8 * km,
    color=[160, 160, 160],
    type="moon",
    parent=saturn,
    velocity=[0, -9.68 * km + 8.48 * km, 0],
    id=603,
)

tethys = body(
    name="Tethys",
    pos=[9.58 * AU + 294619 * km, 0.0, 0.0],
    mass=6.17449 * 10**20,
    radius=531.1 * km,
    color=[140, 140, 140],
    type="moon",
    parent=saturn,
    velocity=[0, -9.68 * km + 11.35 * km, 0],
    id=604,
)

uranus = body(
    name="Uranus",
    pos=[19.18 * AU, 0.0, 0.0],
    mass=8.6810 * 10**25,
    radius=25362 * km,
    color=[0, 255, 255],
    type="planet",
    parent=sun,
    velocity=[0, -6.80 * km, 0],
    id=799,
)

neptune = body(
    name="Neptune",
    pos=[30.07 * AU, 0.0, 0.0],
    mass=1.02413 * 10**26,
    radius=24622 * km,
    color=[0, 128, 128],
    type="planet",
    parent=sun,
    velocity=[0, -5.43 * km, 0],
    id=899,
)

triton = body(
    name="Triton",
    pos=[30.07 * AU + 354759 * km, 0.0, 0.0],
    mass=2.139 * 10**22,
    radius=1353.4 * km,
    color=[50, 50, 255],
    type="moon",
    parent=neptune,
    velocity=[0, -5.43 * km + 4.39 * km, 0],
    id=902,
)

bodies = [sun, earth, mercury, venus, mars, jupiter, saturn, uranus, neptune]
bodies.extend([moon, io, europa, ganymede, callisto, dione, rhea, tethys, triton])
