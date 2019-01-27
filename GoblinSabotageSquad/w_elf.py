from elf_kingdom import *
from w_location import LocationWrapper as Location
class ElfWrapper:
    """
        this class is a wrapper for elf.
    """

    def __init__(self, elf):
        self.elf = elf

    def get_location(self):
        return Location(self.elf.location)

    def get_x(self):
        return self.get_location().get_x()

    def get_y(self):
        return self.get_location().get_y()