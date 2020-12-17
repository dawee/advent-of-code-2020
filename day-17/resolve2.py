import sys


def parse_cubes(input):
    return {
        0: {
            0: {
                y: {
                    x: cube == '#'
                    for x, cube in enumerate(line_stacked_cubes)
                    if cube in ['.', '#']
                }
                for y, line_stacked_cubes in enumerate(input.split('\n'))
            }
        }
    }


def find_active_cubes(abstract_cubes):
    return [
        {'x': x, 'y': y, 'z': z, 'w': w}
        for w, cubes in abstract_cubes.items()
        for z, plane_stacked_cubes in cubes.items()
        for y, line_stacked_cubes in plane_stacked_cubes.items()
        for x, cube in line_stacked_cubes.items()
        if cube == True]


def compute_fov(cubes):
    active_cubes = find_active_cubes(cubes)

    return {
        'x': (min([coord['x'] for coord in active_cubes]), max([coord['x'] for coord in active_cubes])),
        'y': (min([coord['y'] for coord in active_cubes]), max([coord['y'] for coord in active_cubes])),
        'z': (min([coord['z'] for coord in active_cubes]), max([coord['z'] for coord in active_cubes])),
        'w': (min([coord['w'] for coord in active_cubes]), max([coord['w'] for coord in active_cubes])),
    }


def is_active(abstract_cubes, x, y, z, w):
    if not w in abstract_cubes:
        return False

    cubes = abstract_cubes[w]
    return (z in cubes) and (y in cubes[z]) and (x in cubes[z][y]) and (cubes[z][y][x] == True)


def set_active(abstract_cubes, x, y, z, w, active):
    abstract_cubes[w] = abstract_cubes.get(w, {})
    cubes = abstract_cubes[w]
    cubes[z] = cubes.get(z, {})
    cubes[z][y] = cubes[z].get(y, {})
    cubes[z][y][x] = active


def count_active_neighbors(abstract_cubes, x, y, z, w):
    return len([
        True
        for x_gap in range(-1, 2)
        for y_gap in range(-1, 2)
        for z_gap in range(-1, 2)
        for w_gap in range(-1, 2)
        if [x_gap, y_gap, z_gap, w_gap] != [0, 0, 0, 0] and is_active(abstract_cubes, x + x_gap, y + y_gap, z + z_gap, w + w_gap)
    ])


def compute_cube_next_state(abstract_cubes, x, y, z, w):
    return (is_active(abstract_cubes, x, y, z, w) and count_active_neighbors(abstract_cubes, x, y, z, w) in [2, 3]) \
        or ((not is_active(abstract_cubes, x, y, z, w)) and count_active_neighbors(abstract_cubes, x, y, z, w) == 3)


def compute_tasks(abstract_cubes, x, y, z, w):
    tasks = []

    for w_gap in range(-1, 2):
        for z_gap in range(-1, 2):
            for y_gap in range(-1, 2):
                for x_gap in range(-1, 2):
                    next_state = compute_cube_next_state(
                        abstract_cubes, x + x_gap, y + y_gap, z + z_gap, w + w_gap)

                    if is_active(abstract_cubes,  x + x_gap, y + y_gap, z + z_gap, w + w_gap) != next_state:
                        tasks.append({
                            'x': x + x_gap,
                            'y': y + y_gap,
                            'z': z + z_gap,
                            'w': w + w_gap,
                            'state': next_state
                        })
    return tasks


def run_cycles(abstract_cubes, cycles_count):
    for __ in range(cycles_count):
        fov = compute_fov(abstract_cubes)
        tasks = []

        for w in range(fov['w'][0], fov['w'][1] + 1):
            for z in range(fov['z'][0], fov['z'][1] + 1):
                for y in range(fov['y'][0], fov['y'][1] + 1):
                    for x in range(fov['x'][0], fov['x'][1] + 1):
                        tasks += compute_tasks(abstract_cubes, x, y, z, w)

        for task in tasks:
            set_active(abstract_cubes, task['x'], task['y'],
                       task['z'], task['w'], task['state'])


abstract_cubes = parse_cubes(sys.stdin.read())

run_cycles(abstract_cubes, 6)

print(len(find_active_cubes(abstract_cubes)))
