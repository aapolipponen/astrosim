from body import Star, Planet, Atmosphere
import json

def load_scenario(scenario_filename):
    with open(scenario_filename, 'r') as file:
        data = json.load(file)
    return data

def process_body(body_data):
    # Here we'll determine the type of body (Star, Planet, etc.)
    # and instantiate an appropriate object.
    
    if body_data["type"] == "star":
        return Star(
            name=body_data["name"],
            mass=body_data["mass"],
            radius=body_data["radius"],
            color=body_data["color"],
            pos=body_data["pos"],
            velocity=body_data["velocity"],
            id=body_data["id"],
            luminosity=body_data["luminosity"],
            spectral_type=body_data["spectral_type"],
            age=body_data["age"]
            # You can add more fields if needed
        )
    elif body_data["type"] == "planet":
        return Planet(
            name=body_data["name"],
            mass=body_data["mass"],
            radius=body_data["radius"],
            color=body_data["color"],
            pos=body_data["pos"],
            velocity=body_data["velocity"],
            id=body_data["id"]
            # Again, add more fields if they exist and are needed
        )
    # Implement other body types similarly
    else:
        return None

def load_scenario(scenario_filename):
    with open(scenario_filename, 'r') as file:
        data = json.load(file)
    
    bodies = [process_body(body_data) for body_data in data["bodies"]]
    
    return bodies