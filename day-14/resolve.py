import re
import sys
from itertools import combinations


MASK_PATTERN = re.compile(r'mask = ([01X]{36})')
MEMSET_PATTERN = re.compile(r'mem\[(?P<address>\d+)\] = (?P<value>\d+)')


def sum_mem_values(lines, version=1):
    mem = {}

    for line in lines:
        mask_match = MASK_PATTERN.match(line)

        if mask_match:
            mask_expression = mask_match[1]
            or_mask = int(mask_expression.replace('X', '0'), 2)
            and_mask = int(mask_expression.replace('0', '1').replace('X', '0')
                           if version == 2 else mask_expression.replace('X', '1'), 2)
            floating_increment_parts = [2 ** (len(line) - index - 2)
                                        for index, char in enumerate(line) if char == 'X']
            floating_increments = [0] + sorted([sum(combination)
                                                for length in range(1, len(floating_increment_parts) + 1)
                                                for combination in combinations(floating_increment_parts, length)])
        else:
            instruction = MEMSET_PATTERN.match(line).groupdict()
            value = int(instruction['value'])
            address = int(instruction['address'])

            if version == 1:
                mem[address] = (value | or_mask) & and_mask
            elif version == 2:
                base_address = (address | or_mask) & and_mask

                for floating_increment in floating_increments:
                    mem[base_address + floating_increment] = value

    return sum(mem.values())


lines = sys.stdin.read().split('\n')

print('solution 1:', sum_mem_values(lines))
print('solution 2:', sum_mem_values(lines, version=2))
