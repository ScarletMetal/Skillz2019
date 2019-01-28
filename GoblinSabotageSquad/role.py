from elf_kingdom import *


class Role:
    """

    """
    global role
    role = None

    def __init__(self, role):
        self.role = role


    def setRole(self, role):
        self.role =  role

    def getRole(self):
        return self.role

    def compare(self, roleB):
        if (roleB == self):
            return True
        else:
            return False

    def isAttacker(self):
        global role
        if(role == "Attacker"):
            return True
        return False

    def isDefender(self):
        global role
        if(role == "Defender"):
            return True
        return False

    def isReserve(self):
        global role
        if(role == "Reserve"):
            return True
        return False

    def isPortal(self):
        global role
        if(role == "Portal"):
            return True
        return False

    def isCannibal(self):
        global role
        if(role == "Cannibal"):
            return True
        return False

    def isDestroyer(self):
        global role
        if(role == "Destroyer"):
            return True
        return False