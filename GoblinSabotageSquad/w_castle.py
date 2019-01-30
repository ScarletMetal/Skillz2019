from w_location import LocationWrapper


class CastleWrapper:
    """
        this class is a wrapper for castle.
    """

    def __init__(self, castle):
        self.castle = castle

    def get_location(self):
        return LocationWrapper(self.castle.location)

    def get_x(self):
        return self.get_location().get_x()

    def get_y(self):
        return self.get_location().get_y()
