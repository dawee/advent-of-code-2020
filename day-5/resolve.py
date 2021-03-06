import math
import os


INPUT_PATH = os.path.realpath("{0}/../input".format(__loader__.path))


def split_range(value_range):
    min_value, max_value = value_range
    return (min_value,  min_value + math.floor((max_value - min_value) / 2)), (min_value + math.ceil((max_value - min_value) / 2), max_value)


def get_seat_id(boarding_pass):
    row_range = (0, 127)
    col_range = (0, 7)

    for char in boarding_pass:
        if char in ["F", "B"]:
            lower_row_range, upper_row_range = split_range(row_range)
            row_range = lower_row_range if char == "F" else upper_row_range
        elif char in ["L", "R"]:
            lower_col_range, upper_col_range = split_range(col_range)
            col_range = lower_col_range if char == "L" else upper_col_range

    row, __ = row_range
    col, __ = col_range

    return 8 * row + col


with open(INPUT_PATH) as input:
    seat_ids = sorted([get_seat_id(boarding_pass) for boarding_pass in input])
    lower_seat_id, upper_seat_id = seat_ids[0], seat_ids[-1]
    missing_seat = [seat_id for seat_id in range(
        lower_seat_id + 1, upper_seat_id - 1) if seat_id not in seat_ids][0]
    print("solution 1:", upper_seat_id)
    print("solution 2:", missing_seat)
