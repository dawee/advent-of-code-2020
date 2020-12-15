import sys


def compute_number_at(initial_numbers, goal):
    numbers = {(index + 1): number for index,
               number in enumerate(initial_numbers)}
    indexes = {number: (index + 1) for index,
               number in enumerate(initial_numbers)}

    for index in range(len(numbers) + 1, goal + 1):
        last_value = numbers[index - 1]
        numbers[index] = (index - 1) - \
            indexes[last_value] if last_value in indexes else 0
        indexes[last_value] = index - 1

    return numbers[goal]


initial_numbers = [int(n) for n in sys.stdin.read().split(',')]

print('solution 1:', compute_number_at(initial_numbers, 2020))
print('solution 2:', compute_number_at(initial_numbers, 30000000))
