import requests
import numpy as np
from datetime import datetime, timedelta
from constants import KM_TO_AU, KM_TO_M
from planet import bodies

def get_pos_vel(body_id, center_id, start_date, end_date, step_size):
    url = "https://ssd.jpl.nasa.gov/api/horizons.api"
    params = {
        "format": "text",
        "COMMAND": f"'{body_id}'",
        "EPHEM_TYPE": "VECTORS",
        "CENTER": f"'500@{center_id}'",
        "START_TIME": f"'{start_date}'",
        "STOP_TIME": f"'{end_date}'",
        "STEP_SIZE": f"'{step_size}'",
        "OUT_UNITS": "'KM-S'",
        "REF_PLANE": "'ECLIPTIC'",
        "REF_SYSTEM": "'J2000'",
        "VEC_CORR": "'NONE'",
        "VEC_LABELS": "YES",
        "CSV_FORMAT": "YES"
    }
    response = requests.get(url, params)
    response.raise_for_status()
    return response.text

def parse_pos_vel(data):
    lines = data.split("\n")
    try:
        start_index = lines.index("$$SOE") + 1
        end_index = lines.index("$$EOE")
    except ValueError:
        return None
    pos_vel = []
    for line in lines[start_index:end_index]:
        fields = line.split(",")
        pos = [float(x) for x in fields[2:5]]
        vel = [float(x) for x in fields[5:8]]
        pos_vel.append((pos, vel))
    return pos_vel

def calculate_distance(pos):
    # Calculate the Euclidean distance from the origin (0,0,0)
    return np.sqrt(sum([p**2 for p in pos]))

# Get current date and time
current_datetime = datetime.now()
# Get datetime one minute ago
one_minute_ago_datetime = current_datetime - timedelta(minutes=1)

# Convert datetime to YYYY-MM-DD HH:MM format
current_datetime_str = current_datetime.strftime("%Y-%m-%d %H:%M")
one_minute_ago_datetime_str = one_minute_ago_datetime.strftime("%Y-%m-%d %H:%M")

def get_body_parameters(body):
    one_minute_ago = datetime.utcnow() - timedelta(minutes=1)
    one_minute_ago_datetime_str = one_minute_ago.strftime("%Y-%m-%d %H:%M")
    current_datetime_str = datetime.utcnow().strftime("%Y-%m-%d %H:%M")

    parent_id = body.parent.id if body.parent else None
    if parent_id != None:
        data = get_pos_vel(body.id, parent_id, one_minute_ago_datetime_str, current_datetime_str, "1m")    
        x,y,z,vx,vy,vz = extract_data(data)
        x,y,z,vx,vy,vz = scale_values(x,y,z,vx,vy,vz)
        
        for body in bodies:
            if body.type != "star":
                body.pos = np.array([x, y, z])
                body.vel = np.array([vx, vy, vz])
    else:
        return
    
def extract_data(data):
    lines = data.split("\n")
    start = lines.index("$$SOE") + 1
    end = lines.index("$$EOE")
    relevant_data = lines[start:end]
    
    last_line = relevant_data[-1]  # only take the last line
    parts = last_line.split(",")
    x, y, z = float(parts[2]), float(parts[3]), float(parts[4])
    vx, vy, vz = float(parts[5]), float(parts[6]), float(parts[7])
    return x,y,z,vx,vy,vz 

def scale_values(x,y,z,vx,vy,vz):
    x *= km
    y *= km
    z *= km

    # Scale velocities
    vx *= km * 1000
    vy *= km * 1000
    vz *= km * 1000
    return x,y,z,vx,vy,vz