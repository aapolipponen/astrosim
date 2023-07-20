import requests
import re
from datetime import datetime, timedelta

def get_pos_vel(body_id, start_date, end_date, step_size):
    url = "https://ssd.jpl.nasa.gov/api/horizons.api"
    params = {
        "format": "text",
        "COMMAND": f"'{body_id}'",
        "EPHEM_TYPE": "VECTORS",
        "CENTER": "'500@0'",
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
    response = requests.get(url, params=params)
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

# Get current date in YYYY-MM-DD format
current_date = datetime.now().strftime("%Y-%m-%d")

data = get_pos_vel(499, current_date, current_date, "1d")
pos_vel = parse_pos_vel(data)
if pos_vel is not None:
    for pv in pos_vel:
        print(f"Position (KM): {pv[0]}")
        print(f"Velocity (KM/S): {pv[1]}")
else:
    print("No data found.")
