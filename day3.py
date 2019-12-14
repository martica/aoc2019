import collections

def calc_positions(x, y, move):
    """Convert a position and a move into a series of intermediate positions and a destinations."""

    direction = move[0]
    distance = move[1]

    if direction == 'R':
        offset = (distance, 0)
        positions = [(new_x, y) for new_x in range(x+1, x+distance+1)]
    elif direction == 'L':
        offset = (-distance, 0)
        positions = reversed([(new_x, y) for new_x in range(x-distance, x)])
    elif direction == 'U':
        offset = (0, distance)
        positions = [(x, new_y) for new_y in range(y+1, y+distance+1)]
    elif direction == 'D':
        offset = (0, -distance)
        positions = reversed([(x, new_y) for new_y in range(y-distance, y)])

    return x + offset[0], y + offset[1], positions

f = open("day3.txt")

wire_one = [(x[0], int(x[1:])) for x in next(f).strip().split(",")]
wire_two = [(x[0], int(x[1:])) for x in next(f).strip().split(",")]

locations = dict()

x = 0
y = 0
distance = 0

for move in wire_one:
    x, y, positions = calc_positions(x, y, move)
    for position in positions:
        distance = distance + 1
        if position not in locations:
            locations[position] = distance

print(len(locations))

x = 0
y = 0
distance = 0

intersections = dict()

for move in wire_two:
    x, y, positions = calc_positions(x, y, move)
    for position in positions:
        distance = distance + 1
        if position in locations and position not in intersections:
            intersections[position] = locations[position] + distance

print(sorted(intersections.items(), key=lambda item: item[1]))
#distances = [abs(p[0]) + abs(p[1]) for p in intersections]
#print(sorted(distances))


