from elf_kingdom import *
from w_location import LocationWrapper as Location


class ElfWrapper:
    """
        this class is a wrapper for elf.
    """

    def __init__(self, elf, role):
        self.elf = elf
        self.role = role

    def get_location(self):
        return Location(self.elf.location)

    def get_x(self):
        return self.get_location().get_x()

    def get_y(self):
        return self.get_location().get_y()

    def move_to(self, location):
        self.elf.move_to(location.location)

    def act_attacker(self, **context):
        pass

    def act_defender(self, **context):
        pass

    def act_portal(self):
        pass

    def act_cannibal(self):
        pass

    def act_reserve(self):
        pass

    def act_destroyer(self):
        pass