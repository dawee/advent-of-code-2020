
import sys
import pandas


items = [0] + sorted([int(line.strip()) for line in sys.stdin.readlines()])
gaps = [items[index + 1] - item for index,
        item in enumerate(items[:len(items) - 1])]

print("solution 1:", (len([gap for gap in gaps if gap == 1]))
      * (len([gap for gap in gaps if gap == 3]) + 1))

weak_refs = {
    1: 1,
    2: 2,
    3: 4,
    4: 7
}

combinations = 1
left_index = None

for index, gap in enumerate(gaps + [3]):
    if gap == 1 and left_index is None:
        left_index = index
    elif gap == 3 and left_index is not None:
        combinations *= weak_refs[index - left_index]
        left_index = None

print("solution 2:", combinations)
