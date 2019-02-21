

class Role:
    """

    """
    role = None

    def __init__(self, role):
        self.role = role


    def set_role(self, role):
        self.role =  role

    def get_role(self):
        return self.role

    def compare(self, roleB):
        return roleB == self.role
    def is_attacker(self):
        return self.role == "Attacker"

    def is_defender(self):
        return self.role == "Defender"

    def is_reserve(self):
        return self.role == "Reserve"

    def is_portal(self):
        return self.role == "Portal"

    def is_cannibal(self):
        return self.role == "Cannibal"

    def is_destroyer(self):
        return self.role == "Destroyer"