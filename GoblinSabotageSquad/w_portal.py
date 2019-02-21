class PortalWrapper:
    """
        this class is a wrapper for portal.
    """

    def __init__(self, portal, role="enemy"):
        self.portal = portal
        self.role = role

    def get_role(self):
        return self.role

    def attack(self, mana_fountains):
        if len(mana_fountains) >= 2 and self.portal.can_summon_lava_giant():
            self.portal.summon_lava_giant()

    def defense(self, enemy_units, my_ice_trolls):
        if len(enemy_units) > len(my_ice_trolls) and self.portal.can_summon_ice_troll():
            self.portal.summon_ice_troll()