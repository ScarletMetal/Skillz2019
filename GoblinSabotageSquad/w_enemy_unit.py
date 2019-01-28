from w_location import LocationWrapper as Location


class EnemyUnitWrapper:
    def __init__(self, unit, unit_type):
        self.unit = unit
        self.unit_type = unit_type

    def get_location(self):
        return Location(self.unit.location)

    def get_x(self):
        return self.get_location().get_x()

    def get_y(self):
        return self.get_location().get_y()
