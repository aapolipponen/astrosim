from body import Star, Planet, Atmosphere
import json

def load_scenario(filename):
    with open(filename, 'r') as file:
        data = json.load(file)

    bodies = []

    for body_data in data['bodies']:
        body_type = body_data.pop('type')  # 'Star', 'Planet', etc.

        if body_type == "Star":
            body_instance = Star(**body_data)
        elif body_type == "Planet":
            atmosphere_data = body_data.pop('atmosphere', None)
            body_instance = Planet(**body_data)
            if atmosphere_data:
                atmosphere_instance = Atmosphere(**atmosphere_data)
                body_instance.add_atmosphere(atmosphere_instance)
        bodies.append(body_instance)

    return bodies

# Usage
filename = "path_to_your_scenario_file.json"
bodies = load_scenario(filename)
