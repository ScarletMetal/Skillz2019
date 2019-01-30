from elf_kingdom import *


class Portal_Wrapper(Portal):
    """
        this class is a wrapper for portal.
    """

    def __init__(self, portal, role):
        self.portal = portal
        self.role = role