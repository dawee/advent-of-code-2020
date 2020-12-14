import re
import pandas
import os


INPUT_PATH = os.path.realpath("{0}/../input".format(__loader__.path))


def get_char(str, pos):
    real_pos = pos - 1
    return str[real_pos] if 0 <= real_pos < len(str) else None


def is_row_weak_valid(row):
    return row["pos_1"] <= len(re.findall(row["char"], row["password"])) <= row["pos_2"]


def is_row_valid(row):
    positions = (row["pos_1"], row["pos_2"])
    results = (get_char(row["password"], pos) == row["char"]
               for pos in positions)
    matching_results = [result for result in results if result == True]

    return len(matching_results) == 1


with open(INPUT_PATH) as input:
    df = pandas.Series(input, dtype="string").str.extract(
        r"^(?P<pos_1>\d+)\-(?P<pos_2>\d+)\s+(?P<char>\w):\s+(?P<password>\w+)$", expand=True)
    df["pos_1"] = pandas.to_numeric(df["pos_1"])
    df["pos_2"] = pandas.to_numeric(df["pos_2"])


print("solution 1:", len(df[df.apply(is_row_weak_valid, axis=1)]))
print("solution 2:", len(df[df.apply(is_row_valid, axis=1)]))
