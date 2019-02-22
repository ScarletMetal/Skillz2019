from elf_kingdom import *
from w_castle import CastleWrapper
from w_elf import ElfWrapper
from w_ice_troll import IceTrollWrapper
from w_lava_giant import LavaGiantWrapper
from w_portal import PortalWrapper
from w_mana_fountain import ManaFountainWrapper

ATTACK_PORTAL_LOCATION_ACCURACY = 20


class TurnHandler:
    def __init__(self):
        self.game = None
        self.enemy_castle = None
        self.enemy_portals = None
        self.enemy_units = None
        self.enemy_elves = None
        self.enemy_ice_trolls = None
        self.enemy_lava_giant = None
        self.my_portals = None
        self.my_living_elves = None
        self.my_ice_trolls = None
        self.my_lava_giants = None
        self.my_castle = None
        self.my_creatures = None
        self.my_mana = None
        self.my_mana_fountains = []

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
        self.my_mana_fountains = map(lambda fountain: ManaFountainWrapper(fountain), game.get_my_mana_fountains())
        self.my_mana = game.get_my_mana()
        self.enemy_ice_trolls = map(lambda ice_troll: IceTrollWrapper(ice_troll), game.get_enemy_ice_trolls())
        self.enemy_lava_giant = map(lambda lava_giant: LavaGiantWrapper(lava_giant), game.get_enemy_lava_giants())
        self.enemy_elves = map(lambda elf: ElfWrapper(elf, None), game.get_enemy_living_elves())
        self.enemy_units = self.enemy_elves + self.enemy_ice_trolls + self.enemy_lava_giant

    def do_turn(self, game):
        self.wrap_game_data(game)
        self.handle_elves()
        self.handle_portals()

    def attack_elf_exists(self):
        return len(filter(lambda elf: elf.role == "attacker", self.my_living_elves)) > 0

    def attack_portal_exists(self):
        return len(filter(lambda portal: portal.role == "attacker", self.my_portals)) > 0

    def defender_elf_exists(self):
        return len(filter(lambda elf: elf.role == "defender", self.my_living_elves)) > 0

    def defender_portal_exists(self):
        return len(filter(lambda portal: portal.role == "defender", self.my_portals)) > 0

    def mana_fountain_exists(self):
        return len(self.my_mana_fountains) > 0

    def mana_fountain_elf_exists(self):
        return len(filter(lambda elf: elf.role == "mana_fountain", self.my_mana_fountains)) > 0

    def handle_elves(self):
        self.allocate_elves()
        for elf in self.my_living_elves:
            if elf.role == "mana_fountain":
                elf.act_mana_fountain(self.my_castle, self.enemy_castle, self.my_mana_fountains)
            if elf.role == "attacker":
                elf.act_attacker(self.enemy_castle, self.enemy_portals)
            if elf.role == "defender":
                elf.act_defender(self.my_castle, self.enemy_portals, self.my_mana_fountains)

    def allocate_elves(self):
        for elf in self.my_living_elves:
            if self.my_castle.current_health() >= self.enemy_castle.current_health():
                if not self.mana_fountain_exists() and not self.mana_fountain_exists():
                    elf.role = "mana_fountain"
                if not self.attack_elf_exists() and not self.attack_portal_exists():
                    elf.role = "attacker"
                if not self.defender_elf_exists() and not self.defender_elf_exists():
                    elf.role = "defender"
            else:
                if not self.mana_fountain_exists() and not self.mana_fountain_exists():
                    elf.role = "mana_fountain"
                if not self.defender_elf_exists() and not self.defender_elf_exists():
                    elf.role = "defender"
                if not self.attack_elf_exists() and not self.attack_portal_exists():
                    elf.role = "attacker"

    def allocate_portals(self):
        for portal in self.my_portals:
            if portal.get_location().distance_to(self.enemy_castle) < 2000:
                portal.role = "attack"
            if portal.get_location().distance_to(self.my_castle) < 3000:
                portal.role = "defense"

    def handle_portals(self):
        self.allocate_portals()
        for portal in self.my_portals:
            if portal.role == "attack":
                portal.attack(self, self.my_mana_fountains)
            if portal.role == "defense":
                portal.defense(self, self.enemy_units, self.my_ice_trolls)


handler = TurnHandler()


def do_turn(game):
    global handler
    handler.do_turn(game)
