import sys


def parse_cubes(input):
    return {
        0: {
            y: {
                x: cube == '#'
                for x, cube in enumerate(line_stacked_cubes)
                if cube in ['.', '#']
            }
            for y, line_stacked_cubes in enumerate(input.split('\n'))
        }
    }


def find_active_cubes(cubes):
    return [
        {'x': x, 'y': y, 'z': z}
        for z, plane_stacked_cubes in cubes.items()
        for y, line_stacked_cubes in plane_stacked_cubes.items()
        for x, cube in line_stacked_cubes.items()
        if cube == True]


def compute_fov(cubes):
    active_cubes = find_active_cubes(cubes)

    return {
        'x': (min([coord['x'] for coord in active_cubes]), max([coord['x'] for coord in active_cubes])),
        'y': (min([coord['y'] for coord in active_cubes]), max([coord['y'] for coord in active_cubes])),
        'z': (min([coord['z'] for coord in active_cubes]), max([coord['z'] for coord in active_cubes]))
    }


def is_active(cubes, x, y, z):
    return (z in cubes) and (y in cubes[z]) and (x in cubes[z][y]) and (cubes[z][y][x] == True)


def set_active(cubes, x, y, z, active):
    cubes[z] = cubes.get(z, {})
    cubes[z][y] = cubes[z].get(y, {})
    cubes[z][y][x] = active


def count_active_neighbors(cubes, x, y, z):
    return len([
        (x + x_gap, y + y_gap, z + z_gap, True)
        for x_gap in range(-1, 2)
        for y_gap in range(-1, 2)
        for z_gap in range(-1, 2)
        if [x_gap, y_gap, z_gap] != [0, 0, 0] and is_active(cubes, x + x_gap, y + y_gap, z + z_gap)
    ])


def compute_cube_next_state(cubes, x, y, z):
    return (is_active(cubes, x, y, z) and count_active_neighbors(cubes, x, y, z) in [2, 3]) \
        or ((not is_active(cubes, x, y, z)) and count_active_neighbors(cubes, x, y, z) == 3)


def compute_tasks(cubes, x, y, z):
    tasks = []

    for z_gap in range(-1, 2):
        for y_gap in range(-1, 2):
            for x_gap in range(-1, 2):
                next_state = compute_cube_next_state(
                    cubes, x + x_gap, y + y_gap, z + z_gap)

                if is_active(cubes,  x + x_gap, y + y_gap, z + z_gap) != next_state:
                    tasks.append({
                        'x': x + x_gap,
                        'y': y + y_gap,
                        'z': z + z_gap,
                        'state': next_state
                    })
    return tasks


def run_cycles(cubes, cycles_count):
    for __ in range(cycles_count):
        fov = compute_fov(cubes)
        tasks = []

        for z in range(fov['z'][0], fov['z'][1] + 1):
            for y in range(fov['y'][0], fov['y'][1] + 1):
                for x in range(fov['x'][0], fov['x'][1] + 1):
                    tasks += compute_tasks(cubes, x, y, z)

        for task in tasks:
            set_active(cubes, task['x'], task['y'], task['z'], task['state'])


cubes = parse_cubes(sys.stdin.read())

run_cycles(cubes, 6)

print(len(find_active_cubes(cubes)))
