from elf_kingdom import *
import GoblinSabotageSquad.w_location as location
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

    def get_location_on_lava_castle_circle_by_x(self, castle, radius, x):
        # Finds x for  R^2=(y-b)^2+*(x-a)^2, where (a,b) is the center
        # Circle function

        if x > radius or x < 0:
            return Location(None, None)
        return [Location(x, math.sqrt(radius * radius - x * x + 2 *
                                      castle.get_location().get_x() * x - castle.get_location().get_x() *
                                      castle.get_location().get_x()) + castle.get_location().get_y()),
                Location(x,
                         -(math.sqrt(radius * radius - x * x + 2 *
                                     castle.get_location().get_x() * x - castle.get_location().get_x() *
                                     castle.get_location().get_x()) + castle.get_location().get_y()))]

    def create_line_by_locations(self, location1, location2):
        m = (location1.col - location2.col) / (location1.row - location2.row)
        c = location1.col - m * location1.row
        return [lambda x: m * x + c, m, c]


class RangeUtills:

    def __init__(self):
        pass;

    def enemy_units_in_range(self, target, rng, enemy_units):
        return filter(lambda unit: unit.distance(target) < rng, enemy_units)

    def get_closest_to(self, source, targets):
        closest = targets[0]
        for target in targets:
            if source.distance(target) < source.distance(closest):
                closest = target
        return closest

    def enemy_units_between_range(self, target, rng1, rng2, enemy_units):
        return filter(lambda unit: rng1 < unit.distance(target) < rng2, enemy_units)

    def enemy_units_above_range(self, target, rng, enemy_units):
        return filter(lambda unit: unit.distance(target) > rng, enemy_units)

    def sort_by_range(self, map_objects, target):
        return sorted(map_objects, key=lambda map_object: map_object.distance(target))

    def range_from_line(self, location1, line_func):
        return (math.fabs(line_func[1] * location1.get_x + -1 * location1.get_y + line_func[2])) / math.sqrt(
            line_func[1]
            ^ 2 + 1)

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

    def do_turn(self, game):
        self.enemy_castle = game.get_enemy_castle()
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
        defensive_portals = RangeUtills.enemy_units_in_range(self.my_castle, 2500, self.my_portals)
        for portal in defensive_portals:
            self.defensive_portal(portal)
        middle_portals = RangeUtills.enemy_units_between_range(self.my_castle, 2500, 4000, self.my_portals)
        for portal in middle_portals:
            self.defensive_portal(portal)
            if not portal.already_acted:
                self.offensive_portal(portal)
        offensive_portals = RangeUtills.enemy_units_above_range(self.my_castle, 4000, self.my_portals)
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
                if not elf.in_attack_range(RangeUtills.sort_by_range(self.enemy_portals, elf)[0]):
                    elf.move_to(RangeUtills.sort_by_range(self.enemy_portals, elf)[0])
                    break
                else:
                    elf.attack(RangeUtills.sort_by_range(self.enemy_portals, elf)[0])
                    break
            else:
                if elf.location == portal_location:
                    if elf.can_build_portal():
                        elf.build_portal()
                        break
                else:
                    elf.move_to(portal_location)
                    break

    def is_closest_enemy_building_castle(self, offensive_portal_location):
        closest_building = self.enemy_castle
        for Portal in self.enemy_portals:
            if Portal.distance(offensive_portal_location) < closest_building.distance(offensive_portal_location):
                return False

        return True

    def choose_offensive_portal_location(self):
        radius = 1700
        potential_locations = []
        average_distance = 0
        optimal_location = Location(1000, 1000)

        opt_x = self.enemy_castle.location.col
        while opt_x < self.enemy_castle.location.col + radius:
            location = Location(opt_x, math.sqrt(
                -opt_x ^ 2 - 2 * opt_x * self.enemy_castle.location.row - self.enemy_castle.location.row ^ 2 + radius ^ 2) + self.enemy_castle.location.col)
            if self.is_closest_enemy_building_castle(location):
                potential_locations.append(location)
            opt_x += 1
        opt_location_distance_average = 0
        if potential_locations.__len__() != 0:
            optimal_location = potential_locations[0]
        for opt_location in potential_locations:
            for enemy_portal in self.enemy_portals:
                average_distance += opt_location.distance(enemy_portal)
            if self.enemy_portals.__len__() != 0:
                average_distance /= self.enemy_portals.__len__()
            if average_distance < opt_location_distance_average:
                opt_location_distance_average = average_distance
                optimal_location = opt_location

        return optimal_location

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
                closest_structure = RangeUtills.get_closest_to(elf, self.enemy_structures)
                if elf.in_attack_range(closest_structure):
                    elf.attack(closest_structure)

                else:
                    elf.move_to(closest_structure)

    def defensive_portal(self, portal):
        if len(RangeUtills.enemy_units_in_range(self.my_castle, 3000, self.enemy_creatures)) > len(
                RangeUtills.enemy_units_in_range(self.my_castle, 3000,
                                                 self.my_creatures)) and portal.can_summon_ice_troll():
            portal.summon_ice_troll()

    def offensive_portal(self, portal):
        if portal.can_summon_lava_giant() and self.my_mana - 40 > 60:
            portal.summon_lava_giant()


handler = TurnHandler()


def do_turn(game):
    global handler
    handler.do_turn(game)
