from elf_kingdom import *
from w_location import LocationWrapper


class IceTrollWrapper:
    def __init__(self, troll):
        self.troll = troll

    def get_location(self):
        return LocationWrapper(self.troll.location)

    def get_x(self):
        return self.get_location().get_x()

    def get_y(self):
        return self.get_location().get_y()
