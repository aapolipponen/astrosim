from body import body

# Planet Class
class Planet(body):
    def __init__(self, Atmosphere=None, *args, **kwargs):
        self.atmosphere = Atmosphere
        
        # Check if the "Atmosphere" keyword argument exists in kwargs and remove it
        if "Atmosphere" in kwargs:
            del kwargs["Atmosphere"]
        
        # Call the parent (body) class's __init__ method
        super().__init__(*args, **kwargs)