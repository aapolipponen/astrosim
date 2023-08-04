from constants import G, day, AU, year, kg, deg, km, R_earth, M_earth, M_sun, R_sun, deg, yellow, blue, beige, teal, red, orange, cyan
import numpy as np
import requests
import re
from datetime import datetime
from body import body

# Planets' data estimated or taken from NASA fact sheets

sun = body(
    name="Sun",
    pos=[0.0, 0.0, 0.0],
    mass=1.989 * 10**30,
    radius=696342 * km,
    color=[255, 223, 0],
    type="star",
    parent=None,
)

earth = body(
    name="Earth",                                                 
    pos=[1.0 * AU, 0.0, 0.0],
    mass=5.97219 * 10**24,                                       
    radius=6371 * km,                                             
    color=[0, 0, 255],                                           
    type="planet",                                                
    parent=sun,                                              
    velocity=[0, -29.78 * km, 0]
)

mercury = body(
    name="Mercury",
    pos=[0.39 * AU, 0.0, 0.0],
    mass=3.3011 * 10**23,
    radius=2439.7 * km,
    color=[245, 245, 220],
    type="planet",
    parent=sun,
    velocity=[0, -47.87 * km, 0]
) 

venus = body(
    name="Venus",
    pos=[0.723 * AU, 0.0, 0.0],
    mass=4.8675 * 10**24,
    radius=6051.8 * km,
    color=[255, 255, 0],
    type="planet",
    parent=sun,
    velocity=[0, -35.02 * km, 0]
)

mars = body(
    name="Mars",
    pos=[1.52 * AU, 0.0, 0.0],
    mass=6.4171 * 10**23,
    radius=3389.5 * km,
    color=[255, 0, 0],
    type="planet",
    parent=sun,
    velocity=[0, -24.07 * km, 0]
)

jupiter = body(
    name="Jupiter",
    pos=[5.20 * AU, 0.0, 0.0],
    mass=1.8982 * 10**27,
    radius=69911 * km,
    color=[255, 165, 0],
    type="planet",
    parent=sun,
    velocity=[0, -13.07 * km, 0]
)

saturn = body(
    name="Saturn",
    pos=[9.58 * AU, 0.0, 0.0],
    mass=5.6834 * 10**26,
    radius=58232 * km,
    color=[245, 245, 220],
    type="planet",
    parent=sun,
    velocity=[0, -9.68 * km, 0]
)

uranus = body(
    name="Uranus",
    pos=[19.18 * AU, 0.0, 0.0],
    mass=8.6810 * 10**25,
    radius=25362 * km,
    color=[0, 255, 255],
    type="planet",
    parent=sun,
    velocity=[0, -6.80 * km, 0]
)

neptune = body(
    name="Neptune",
    pos=[30.07 * AU, 0.0, 0.0],
    mass=1.02413 * 10**26,
    radius=24622 * km,
    color=[0, 128, 128],
    type="planet",
    parent=sun,
    velocity=[0, -5.43 * km, 0]
)


bodies = [sun, earth, mercury, venus, mars, jupiter, saturn, uranus, neptune]
