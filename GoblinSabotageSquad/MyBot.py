from elf_kingdom import *
import GoblinSabotageSquad.w_location as w_location
import GoblinSabotageSquad.w_castle as w_castle
import GoblinSabotageSquad.w_portal as w_portal
import GoblinSabotageSquad.w_elf as w_elf
import GoblinSabotageSquad.w_enemy_unit as w_enemy_unit
import GoblinSabotageSquad.w_LavaGiant as w_LavaGiant
import range_utility
import location_calculator
import math

ATTACK_PORTAL_LOCATION_ACCURACY = 20


class LocationCalculator:
    """
        this class is used to calculate some locations, currently the different defensive portals
    """

    def __init__(self, my_castle_location, enemy_castle_location, first_portal_location):
        self.my_castle_location = my_castle_location
        self.enemy_castle_location = enemy_castle_location
        self.first_portal_location = first_portal_location

    def calculate_second_def_portal_location(self):
        q = self.first_portal_location.row - self.my_castle_location.row
        t = self.first_portal_location.col - self.my_castle_location.col
        return Location(self.my_castle_location.row + t, self.my_castle_location.col - abs(q))

    def calculate_third_portal_location(self):
        row = int((self.my_castle_location.row + self.enemy_castle_location.row) / 2)
        col = int((self.my_castle_location.col + self.enemy_castle_location.col) / 2)
        return Location(row=row, col=col)


class TurnHandler:
    def __init__(self):
        self.game = None
        self.enemy_castle = None
        self.my_living_elves = None
        self.my_portals = None
        self.enemy_castle = None
        self.first_portal = None
        self.enemy_portals = None
        self.my_castle = None
        self.my_creatures = None
        self.my_elves_by_id = {}
        self.my_portals_by_id = {}

        self.my_mana = None

        self.my_elves_by_role = {}
        self.defensive_portal_locations_list = []

    def wrap_gameobjects(self, game_objects):
        wrapped_list = []
        for game_object in game_objects:
            if(type(Castle, game_object)):
                wrapped_list.append(w_castle.CastleWrapper(game_object))
            if (type(Elf, game_object)):
                wrapped_list.append(w_elf.ElfWrapper(game_object, None))
            if(type(LavaGiant, game_object)):
                wrapped_list.append(w_LavaGiant.LavaGiant_Wrapper(game_object))
            if(type(Portal, game_object)):
                wrapped_list.append((w_portal.Portal_Wrapper(game_object),None))
        return wrapped_list

    def do_turn(self, game):
        self.enemy_castle = self.wrap_gameobjects(game.get_enemy_castle())
        self.my_living_elves = self.wrap_gameobjects(game.get_my_living_elves())
        self.my_portals = self.wrap_gameobjects(game.get_my_portals())
        self.my_castle = self.wrap_gameobjects(game.get_my_castle())
        self.my_mana = game.get_my_mana()
        self.enemy_portals = self.wrap_gameobjects(game.get_enemy_portals())
        self.enemy_creatures = self.wrap_gameobjects((game.get_enemy_creatures(), game.get_enemy_living_elves()))
        self.enemy_portals = self.wrap_gameobjects(game.get_enemy_portals())
        self.my_creatures = self.wrap_gameobjects(game.get_my_creatures())


handler = TurnHandler()


def do_turn(game):
    global handler
    handler.do_turn(game)
