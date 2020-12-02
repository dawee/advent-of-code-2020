import re
import pandas
import os

INPUT_PATH = os.path.realpath("{0}/../input".format(__loader__.path))
LINE_PATTERN = re.compile(r"^(?P<min>\d+)\-(?P<max>\d+)\s+(?P<char>\w):\s+(?P<password>\w+)$")

def get_char(str, pos):
    real_pos = pos - 1

    return str[real_pos] if 0 <= real_pos < len(str) else None

def is_row_valid(row):
    positions = (row["pos_1"], row["pos_2"])
    results = (get_char(row["password"], pos) == row["char"] for pos in positions)
    matching_results = [result for result in results if result == True]

    return len(matching_results) == 1


with open(INPUT_PATH) as data:
    parsed_lines = (LINE_PATTERN.match(line) for line in data.readlines())
    df = pandas.DataFrame([{
        "min": int(parsed_line.group("min")),
        "max": int(parsed_line.group("max")),
        "char": parsed_line.group("char"),
        "password": parsed_line.group("password")
    } for parsed_line in parsed_lines])

    df["valid"] = df.apply(lambda row: row["min"] <= len(re.findall(row["char"], row["password"])) <= row["max"], axis=1)

    print("solution 1:", len(df.query("valid == True")["valid"].index))

    df["pos_1"] = df["min"]
    df["pos_2"] = df["max"]
    df["valid"] = df.apply(is_row_valid, axis=1)

    print("solution 2:", len(df.query("valid == True")["valid"].index))