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

    def get_optimal_attack_portal_location(self):
        pass

    """
        runs this function on the first turn on combat,
        this function calculates the locations of the defensive portals
    """

    def do_on_first_turn(self):
        self.first_portal = self.my_portals[0]
        calc = LocationCalculator(self.my_castle.location,
                                  self.enemy_castle.location,
                                  self.first_portal.location)
        self.defensive_portal_locations_list.append(calc.calculate_second_def_portal_location())
        self.defensive_portal_locations_list.append(calc.calculate_third_portal_location())
        # self.defensive_portal_locations_list.reverse()
        print "size of queue is ", len(self.defensive_portal_locations_list)

        self.my_elves_by_role[self.my_living_elves[0].id] = self.handle_attacker_elf
        self.my_elves_by_role[self.my_living_elves[1].id] = self.handle_defender_elf

    """
        runs this function every turn
    """

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
        self.enemy_castle = game.get_my_castle()
        self.my_living_elves = game.get_my_living_elves()
        self.my_portals = game.get_my_portals()
        self.my_castle = game.get_my_castle()
        self.my_mana = game.get_my_mana()
        self.enemy_portals = game.get_enemy_portals()
        self.enemy_creatures = game.get_enemy_creatures() + game.get_enemy_living_elves()
        self.enemy_portals = game.get_enemy_portals()
        self.my_creatures = game.get_my_creatures()
        self.enemy_structures = self.enemy_portals + [self.enemy_castle]

        for elf in self.my_living_elves:
            self.my_elves_by_id[elf.id] = elf

        for portal in self.my_portals:
            self.my_portals_by_id[portal.id] = portal

        # runs the function on the first turn
        if game.turn == 1:
            self.do_on_first_turn()

        if self.my_portals != []:
            self.portal_roles()
        self.handle_elves()

    def portal_roles(self):
        defensive_portals = range_utility.enemy_units_in_range(self.my_castle, 2500, self.my_portals)
        for portal in defensive_portals:
            self.defensive_portal(portal)
        middle_portals = range_utility.enemy_units_between_range(self.my_castle, 2500, 4000, self.my_portals)
        for portal in middle_portals:
            self.defensive_portal(portal)
            if not portal.already_acted:
                self.offensive_portal(portal)
        offensive_portals = range_utility.enemy_units_above_range(self.my_castle, 4000, self.my_portals)
        for portal in offensive_portals:
            self.offensive_portal(portal)

    """
        handles elves
    """

    def handle_elves(self):
        for elf in self.my_living_elves:
            self.my_elves_by_role[elf.id](elf)

    """
        handles portals
    """

    """
        finds units in range
    """

    def handle_attacker_elf(self, elf):
        portal_location = self.choose_offensive_portal_location()
        for portal in self.my_portals:
            if portal.location.distance(portal_location) < 100:
                if not elf.in_attack_range(range_utility.sort_by_range(self.enemy_portals, elf)[0]):
                    elf.move_to(range_utility.sort_by_range(self.enemy_portals, elf)[0])
                    break
                else:
                    elf.attack(range_utility.sort_by_range(self.enemy_portals, elf)[0])
                    break
            else:
                if elf.location == portal_location:
                    if elf.can_build_portal():
                        elf.build_portal()
                        break
                else:
                    elf.move_to(portal_location)
                    break

    def handle_defender_elf(self, elf):
        if len(self.defensive_portal_locations_list) != 0:
            target = self.defensive_portal_locations_list.pop()
            if not elf.location.in_range(target, 3):
                elf.move_to(target)
                self.defensive_portal_locations_list.append(target)

            else:
                if elf.can_build_portal():
                    elf.build_portal()
                else:
                    self.defensive_portal_locations_list.append(target)
        else:
            if len(self.enemy_structures) != 0:
                closest_structure = range_utility.get_closest_to(elf, self.enemy_structures)
                if elf.in_attack_range(closest_structure):
                    elf.attack(closest_structure)

                else:
                    elf.move_to(closest_structure)

    def defensive_portal(self, portal):
        if len(range_utility.enemy_units_in_range(self.my_castle, 3000, self.enemy_creatures)) > len(
                range_utility.enemy_units_in_range(self.my_castle, 3000,
                                                   self.my_creatures)) and portal.can_summon_ice_troll():
            portal.summon_ice_troll()

    def offensive_portal(self, portal):
        if portal.can_summon_lava_giant() and self.my_mana - 40 > 60:
            portal.summon_lava_giant()


handler = TurnHandler()


def do_turn(game):
    global handler
    handler.do_turn(game)
