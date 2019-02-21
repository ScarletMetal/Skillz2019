from w_castle import CastleWrapper
from w_elf import ElfWrapper
from w_ice_troll import IceTrollWrapper
from w_lava_giant import LavaGiantWrapper
from w_portal import PortalWrapper

ATTACK_PORTAL_LOCATION_ACCURACY = 20


class TurnHandler:
    def __init__(self):
        self.game = None
        self.enemy_castle = None
        self.enemy_portals = None
        self.my_portals = None
        self.my_living_elves = None
        self.my_ice_trolls = None
        self.my_lava_giants = None
        self.my_castle = None
        self.my_creatures = None
        self.my_mana = None

        self.attacker_elves = []
        self.defender_elves = []

    def wrap_game_data(self, game):
        self.game = game

        self.enemy_castle = CastleWrapper(game.get_enemy_castle())
        self.enemy_portals = map(lambda portal: PortalWrapper(portal), game.get_enemy_portals())

        self.my_portals = map(lambda portal: PortalWrapper(portal, "none"), game.get_my_portals())
        self.my_living_elves = map(lambda elf: ElfWrapper(elf, "none"), game.get_my_living_elves())
        self.my_castle = CastleWrapper(game.get_my_castle())
        self.my_lava_giants = map(lambda giant: LavaGiantWrapper(giant), game.get_my_lava_giants())
        self.my_ice_trolls = map(lambda troll: IceTrollWrapper(troll), game.get_my_ice_trolls())
        self.my_creatures = self.my_lava_giants + self.my_ice_trolls + self.my_living_elves
        self.my_mana = game.get_my_mana()

    def do_turn(self, game):
        self.wrap_game_data(game)

    def attack_elf_exists(self):
        return len(filter(lambda elf: elf.role == "attacker", self.my_living_elves)) > 0

    def attack_portal_exists(self):
        return len(filter(lambda portal: portal.role == "attacker", self.my_portals)) > 0

    def handle_elves(self):
        self.allocate_elves()

        map(lambda elf: elf.act_defender(), self.defender_elves)
        map(lambda elf: elf.act_attacker(), self.attacker_elves)

    def allocate_elves(self):

        for elf in self.my_living_elves:
            if not self.attack_elf_exists() and not self.attack_portal_exists():
                elf.role = "attacker"



handler = TurnHandler()


def do_turn(game):
    global handler
    handler.do_turn(game)
