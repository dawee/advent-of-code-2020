import re
import pandas
import os

INPUT_PATH = os.path.realpath("{0}/../input".format(__loader__.path))

with open(INPUT_PATH) as input:
    df = pandas.DataFrame([
        dict([[pair.group("key"), pair.group("value")] for pair in re.finditer(r"\b(?P<key>\w{3}):(?P<value>[^\s]+)\b", line)])
        for line in (line.replace("\n", " ") for line in input.read().split("\n\n"))
    ])

    valid_df = df[
        df["byr"].notnull() &
        df["iyr"].notnull() &
        df["eyr"].notnull() &
        df["hgt"].notnull() &
        df["hcl"].notnull() &
        df["ecl"].notnull() &
        df["pid"].notnull()]

    print("solution 1:", len(valid_df))

    strict_valid_df = valid_df[
        (valid_df["byr"].str.match("^[0-9]{4}$").astype(bool)) & (valid_df["byr"].astype(int) >= 1920) & (valid_df["byr"].astype(int) <= 2002) &
        (valid_df["iyr"].str.match("^[0-9]{4}$").astype(bool)) & (valid_df["iyr"].astype(int) >= 2010) & (valid_df["iyr"].astype(int) <= 2020) &
        (valid_df["eyr"].str.match("^[0-9]{4}$").astype(bool)) & (valid_df["eyr"].astype(int) >= 2020) & (valid_df["eyr"].astype(int) <= 2030) &
        ( # sizes
            ( # cm
                (valid_df["hgt"].str.extract(r"(?P<size>[0-9]+)cm")["size"].astype("float").astype("Int64") >= 150) &
                (valid_df["hgt"].str.extract(r"(?P<size>[0-9]+)cm")["size"].astype("float").astype("Int64") <= 193)
            ) |
            ( # inches
                (valid_df["hgt"].str.extract(r"(?P<size>[0-9]+)in")["size"].astype("float").astype("Int64") >= 59) &
                (valid_df["hgt"].str.extract(r"(?P<size>[0-9]+)in")["size"].astype("float").astype("Int64") <= 76)
            )
        ) &
        valid_df["hcl"].str.match("^#[0-9a-f]{6}$").astype(bool) &
        valid_df["ecl"].isin(["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]) &
        valid_df["pid"].str.match("^[0-9]{9}$").astype(bool)
    ]

    print("solution 2:", len(strict_valid_df))
