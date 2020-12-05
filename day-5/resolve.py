import math
import os

INPUT_PATH = os.path.realpath("{0}/../input".format(__loader__.path))


def get_lower_range(value_range):
    min_value, max_value = value_range
    return (min_value,  min_value + math.floor((max_value - min_value) / 2))

def get_upper_range(value_range):
    min_value, max_value = value_range
    return (min_value + math.ceil((max_value - min_value) / 2), max_value)


def get_seat_id(boarding_pass):
    row_range = (0, 127)
    col_range = (0, 7)

    for char in boarding_pass:
        if char == "F":
            row_range = get_lower_range(row_range)
        elif char == "B":
            row_range = get_upper_range(row_range)
        elif char == "L":
            col_range = get_lower_range(col_range)
        elif char == "R":
            col_range = get_upper_range(col_range)

    min_row, max_row = row_range
    min_col, max_col = col_range

    if not (min_row == max_row) or not (min_col == max_col):
        raise Exception("Failed with " + boarding_pass)

    row = min_row
    col = min_col

    return 8 * row + col


with open(INPUT_PATH) as input:
    seat_ids = sorted([get_seat_id(boarding_pass) for boarding_pass in input.readlines()])
    lower_seat_id, upper_seat_id = seat_ids[0], seat_ids[-1]
    missing_seat = [seat_id for seat_id in range(lower_seat_id + 1, upper_seat_id - 1) if seat_id not in seat_ids][0]
    print("solution 1:", upper_seat_id)
    print("solution 2:", missing_seat)
