

class Role:
    """

    """
    role = None

    def __init__(self, role):
        self.role = role


    def setRole(self, role):
        self.role =  role

    def getRole(self):
        return self.role

    def compare(self, roleB):
        return roleB == self.role
    def isAttacker(self):
        return self.role == "Attacker"

    def isDefender(self):
        return self.role == "Defender"

    def isReserve(self):
        return self.role == "Reserve"

    def isPortal(self):
        return self.role == "Portal"

    def isCannibal(self):
        return self.role == "Cannibal"

    def isDestroyer(self):
        return self.role == "Destroyer"