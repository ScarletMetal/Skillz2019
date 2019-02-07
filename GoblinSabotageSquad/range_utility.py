
import math


def enemy_units_in_range(target, rng, enemy_units):
    return filter(lambda unit: unit.distance(target) < rng, enemy_units)


def get_closest_to(source, targets):
    closest = targets[0]
    for target in targets:
        if source.distance(target) < source.distance(closest):
            closest = target
    return closest


def enemy_units_between_range(target, rng1, rng2, enemy_units):
    return filter(lambda unit: rng1 < unit.distance(target) < rng2, enemy_units)


def enemy_units_above_range(target, rng, enemy_units):
    return filter(lambda unit: unit.distance(target) > rng, enemy_units)


def sort_by_range(map_objects, target):
    return sorted(map_objects, key=lambda map_object: map_object.distance(target))


def range_from_line(location1, line_func):
    return (math.fabs(line_func[1] * location1.get_x + -1 * location1.get_y + line_func[2])) / math.sqrt(
        line_func[1]
        ^ 2 + 1)


def sum_of_distance_to_line(line, map_objects):
    sum = 0
    for map_object in map_objects:
        sum += range_from_line(location1=map_object.get_location(), line_func=line)
    return sum


def is_closest_enemy_building_castle(self, offensive_portal_location):
    closest_building = self.enemy_castle
    for Portal in self.enemy_portals:
        if Portal.distance(offensive_portal_location) < closest_building.distance(offensive_portal_location):
            return False
    return True
