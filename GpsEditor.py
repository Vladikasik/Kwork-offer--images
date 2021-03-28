import random

class GPS:

    # coordinates be like [(43.03, 32.78, 32.43), (43.03, 32.78, 32.43)]
    def __init__(self, coordinates, edit_to):

        self.lat = coordinates[0]
        self.long = coordinates[1]

        self.met = edit_to

    def _edit(metres):
        return None