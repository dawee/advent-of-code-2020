import re
import sys


NORTH, EAST, SOUTH, WEST = range(4)
INSTRUCTION_PATTERN = re.compile(r'(?P<name>\w)(?P<value>\d+)\n?')
CARDINAL_MAP = {'N': NORTH, 'E': EAST, 'S': SOUTH, 'W': WEST}


def is_opposite(cardinal_a, cardinal_b):
    return abs(cardinal_a - cardinal_b) == 2


def is_same_axis(cardinal_a, cardinal_b):
    return cardinal_a == cardinal_b or is_opposite(cardinal_a, cardinal_b)


def move(direction, cardinal_point, value):
    horizontal, vertical = direction

    if cardinal_point == NORTH:
        return (horizontal, vertical + value)
    elif cardinal_point == EAST:
        return (horizontal + value, vertical)
    elif cardinal_point == SOUTH:
        return (horizontal, vertical - value)
    elif cardinal_point == WEST:
        return (horizontal - value, vertical)


def turn(faced_cardinal_point, angle):
    return int((faced_cardinal_point + angle / 90) % 4)

def manhattan_distance(instructions):
    faced_cardinal_point = EAST
    direction = (0 , 0)

    for instruction in instructions:
        if instruction['name'] in CARDINAL_MAP:
            direction = move(direction, CARDINAL_MAP[instruction['name']], instruction['value'])
        elif instruction['name'] == 'F':
            direction = move(direction, faced_cardinal_point, instruction['value'])
        elif instruction['name'] == 'L':
            faced_cardinal_point = turn(faced_cardinal_point, -instruction['value'])
        elif instruction['name'] == 'R':
            faced_cardinal_point = turn(faced_cardinal_point, instruction['value'])
    
    horizontal, vertical = direction
    return abs(horizontal) + abs(vertical)


def move_waypoint(waypoint, cardinal, value):
    for item in waypoint:
        if is_same_axis(item['cardinal'], cardinal):
            item['value'] = value - item['value'] if is_opposite(item['cardinal'], cardinal) else item['value'] + value

            if item['value'] < 0:
                item['value'] = abs(item['value'])
            else:
                item['cardinal'] = cardinal


    return waypoint


def turn_waypoint(waypoint, angle):
    for item in waypoint:
        item['cardinal'] = turn(item['cardinal'], angle)
    
    return waypoint


def move_location(location, waypoint, value):
    for waypoint_item in waypoint:
        for location_item in location:
            if is_same_axis(location_item['cardinal'], waypoint_item['cardinal']):
                multiplied_value = value * waypoint_item['value']
                location_item['value'] = multiplied_value - location_item['value'] \
                        if is_opposite(location_item['cardinal'], waypoint_item['cardinal']) \
                        else location_item['value'] + multiplied_value
                
                if location_item['value'] < 0:
                    location_item['value'] = abs(location_item['value'])
                else:
                    location_item['cardinal'] = waypoint_item['cardinal']

    return location



def manhattan_locations_distance(instructions):
    waypoint = [
        {"cardinal": EAST, "value": 10},
        {"cardinal": NORTH, "value": 1},
    ]

    location = [
        {"cardinal": EAST, "value": 0},
        {"cardinal": NORTH, "value": 0},
    ]


    for instruction in instructions:
        if instruction['name'] in CARDINAL_MAP:
            waypoint = move_waypoint(waypoint, CARDINAL_MAP[instruction['name']], instruction['value'])
        elif instruction['name'] == 'F':
            location = move_location(location, waypoint, instruction['value'])
        elif instruction['name'] == 'L':
            waypoint = turn_waypoint(waypoint, -instruction['value'])
        elif instruction['name'] == 'R':
            waypoint = turn_waypoint(waypoint, instruction['value'])

    return sum([item['value'] for item in location])



raw_instructions = (INSTRUCTION_PATTERN.match(line).groupdict() for line in sys.stdin)
instructions = [{'name': instruction['name'], 'value': int(instruction['value'])} for instruction in raw_instructions]

print('solution 1:', manhattan_distance(instructions))
print('solution 2:', manhattan_locations_distance(instructions))
