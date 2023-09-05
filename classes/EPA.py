from time import time

class Epa:
    def __init__(self, name, description, location, duration, mode):
        self.id = int(time() * 1000)
        try:
            self.name = str(name)
            self.description = str(description)
            self.duration = float(duration)
            self.mode = str(mode)
            self.location = str(location)
        except ValueError:
            print("Value error while creating Epa class")

