import elf_kingdom

GAME_WIDTH = 0
GAME_HEIGHT = 0


class LocationWrapper:
    def __init__(self, location=None, x=0, y=0):
        if location is not None:
            self.location = location
        else:
            self.location = elf_kingdom.Location(x, y)

    def __str__(self):
        return "({},{})".format(self.get_x(), self.get_y())

    def __add__(self, other):
        return LocationWrapper(x=self.get_x() + other.get_x(), y=self.get_y() + other.get_y())

    def get_x(self):
        return self.location.col

    def get_y(self):
        return GAME_HEIGHT - self.location.row

    def distance_to(self, other):
        return self.location.distance(other)
