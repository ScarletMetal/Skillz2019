class PortalWrapper:
    """
        this class is a wrapper for portal.
    """

    def __init__(self, portal, role="enemy"):
        self.portal = portal
        self.role = role

    def get_role(self):
        return self.role

    def attack(self):
        pass
