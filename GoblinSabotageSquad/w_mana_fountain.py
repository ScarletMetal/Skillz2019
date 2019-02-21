from w_location import LocationWrapper


class ManaFountainWrapper:
    def __init__(self, mana_fountain):
        self.mana_fountain = mana_fountain

    def get_location(self):
        return LocationWrapper(self.mana_fountain.location)

    def get_x(self):
        return self.get_location().get_x()

    def get_y(self):
        return self.get_location().get_y()
