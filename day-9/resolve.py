import sys


sum_combinations = lambda numbers: [number + other for index, number in enumerate(numbers) for other in numbers[:index]]


def find_weakness(numbers, preamble):
    for index, number in enumerate(numbers):
        if index >= preamble and not number in sum_combinations(numbers[index - preamble:index]):
            return number


def find_encryption_weakness(numbers, weakness):
    for left_index, number in enumerate(numbers):
        contiguous_sum = 0
        right_index = left_index + 1

        while contiguous_sum < weakness:
            contiguous_numbers = numbers[left_index:right_index + 1]
            contiguous_sum = sum(contiguous_numbers)

            if len(contiguous_numbers) > 1 and contiguous_sum == weakness:
                return min(contiguous_numbers) + max(contiguous_numbers)

            right_index += 1


input_numbers = [int(line.strip()) for line in sys.stdin.readlines()]
weakness = find_weakness(input_numbers, int(sys.argv[1]))

print("solution 1:", weakness)
print("solution 2:", find_encryption_weakness(input_numbers, weakness))
