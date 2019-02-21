import math

import range_utility
from w_location import LocationWrapper as Location

LOCATION_CALC_ACCURACY = 20


def get_location_on_castle_circle_by_x(castle, radius, x):
    # Finds x for  R^2=(y-b)^2+*(x-a)^2, where (a,b) is the center
    # Circle function

    if x > radius or x < 0:
        return None

    y1 = math.sqrt(radius * radius - x * x + 2 *
                   castle.get_location().get_x() * x - castle.get_location().get_x() *
                   castle.get_location().get_x()) + castle.get_location().get_y()

    y2 = -(math.sqrt(radius * radius - x * x + 2 *
                     castle.get_location().get_x() * x - castle.get_location().get_x() *
                     castle.get_location().get_x()) + castle.get_location().get_y())

    if (y2 < 0):
        return [Location(x, y1)]
    elif (y1 < 0):
        return [Location(x, y2)]
    else:
        return None


def create_line_by_locations(location1, location2):
    m = (location1.get_y() - location2.get_y()) / (location1.get_x() - location2.get_x())
    c = location1.get_y() - m * location1.get_x
    return [m, c]


def find_intersections_line_circle(radius, castle, line):
    m = line[0]
    c = line[1]
    a = castle.get_location().get_x()
    b = castle.get_location().get_y()
    x1 = (m * c - b * m + math.sqrt(
        radius ^ 2 * m ^ 2 - a ^ 2 * m ^ 2 + 2 * a * b * m - 2 * a * m * c
        + 2 * b * c + radius ^ 2 - b ^ 2 - c ^ 2) - a) / (
             -1 - m ^ 2)
    x2 = -((m * c - b * m + math.sqrt(
        radius ^ 2 * m ^ 2 - a ^ 2 * m ^ 2 + 2 * a * b * m - 2 * a * m * c
        + 2 * b * c + radius ^ 2 - b ^ 2 - c ^ 2) + a) / (
               -1 - m ^ 2))
    return [Location(x1, m * x1 + c), Location(x2, m * x2 + c)]


def calc_attack_portal_location(radius, castle, enemy_portals):
    attack_portal_possible_locations = []
    if castle.get_location().get_x() - radius < 0:
        x = 0
    else:
        x = castle.get_location().get_x() - radius
    while x < 2 * radius:
        if get_location_on_castle_circle_by_x(castle, radius, x) != None:
            attack_portal_possible_locations.append(
                get_location_on_castle_circle_by_x(castle, radius, x))
        x += LOCATION_CALC_ACCURACY

    max_sum = 0
    for locations in attack_portal_possible_locations:
        for location1 in locations:
            sum = range_utility.sum_of_distance_to_line(
                create_line_by_locations(location1,
                                         castle.get_location()),
                enemy_portals)
            if sum > max_sum:
                return location1

    if max_sum <= 0:
        return None
        # INSERT DEFAULT LOCATION HERE


def calc_defense_portal_location(radius, castle, enemy_portals, managens):
    defense_portal_possible_locations = []
    if castle.get_location().get_x() - radius < 0:
        x = 50
    else:
        x = castle.get_location().get_x() - radius
    while x < 2 * radius:
        if get_location_on_castle_circle_by_x(castle, radius, x) != None:
            defense_portal_possible_locations.append(
                get_location_on_castle_circle_by_x(castle, radius, x))
        x += LOCATION_CALC_ACCURACY

    min_sum = 0
    for locations in defense_portal_possible_locations:
        for location1 in locations:
            sum = range_utility.sum_of_distance_to_line(
                create_line_by_locations(location1,
                                         castle.get_location()),
                enemy_portals) + range_utility.sum_of_distance_to_line(
                create_line_by_locations(location1,
                                         castle.get_location()),
                managens)
            if sum < min_sum:
                return location1

    if min_sum <= 0:
        return None


def calc_managen_location(radius, castle, enemy_castle, managens):
    managen_possible_locations = []
    if castle.get_location().get_x() - radius < 0:
        x = castle.get_location().get_x() - radius
        while x < 0:
            x = x + 1
    else:
        x = castle.get_location().get_x() - radius
    while x < 2 * radius:
        if get_location_on_castle_circle_by_x(castle, radius, x) != None:
            managen_possible_locations.append(
                get_location_on_castle_circle_by_x(castle, radius, x))
        x += LOCATION_CALC_ACCURACY

    max_sum = 0
    for locations in managen_possible_locations:
        for location1 in locations:
            sum = range_utility.sum_of_distance_to_line(
                create_line_by_locations(location1,
                                         castle.get_location()),
                enemy_castle+managens)
            if sum > max_sum:
                return location1

    if max_sum <= 0:
        return None