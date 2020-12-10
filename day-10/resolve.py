
import sys
import pandas


items = [0] + sorted([int(line.strip()) for line in sys.stdin.readlines()])
gaps = [items[index + 1] - item for index, item in enumerate(items[:len(items) - 1])]

print("solution 1:", (len([gap for gap in gaps if gap == 1])) * (len([gap for gap in gaps if gap == 3]) + 1))

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








# while True:
#     next_steps = ({"path": path["path"], "rest": path["rest"], "next": path["rest"][(path["rest"] > path["path"].iloc[-1]) & (path["rest"] <= (path["path"].iloc[-1] + 3))]} for path in paths)
#     paths = [{"path": next_step["path"].append(pandas.Series([next_item])), "rest": next_step["rest"][next_step["rest"] != next_item]} for next_step in next_steps for next_item in next_step["next"] if len(next_step["next"]) > 0]

#     longest = max([len(path["path"]) for path in paths])

#     print(len(series) + 1 - longest)

#     if longest == len(series) + 1:
#         print([path for path in paths if len(path["path"]) == longest][0])
#         break