from functools import lru_cache as memoized
import sys


def build_first_matrix(data):
    lines = data.split("\n")
    matrix = dict([
            [row, dict([[col, {"taken": False, "adjacent": [], "row": row, "col": col}] for col, char in enumerate(line) if char == 'L'])]
            for row, line in enumerate(lines)])

    for row, seats in matrix.items():
        for col, seat in seats.items():
            seat["adjacent_positions"] = [{"row": row + row_gap, "col": col + col_gap}
                                            for row_gap in range(-1, 2)
                                            for col_gap in range(-1, 2)
                                            if (col_gap != 0 or row_gap != 0)]

            seat["adjacent"] = [matrix[adjacent_position["row"]][adjacent_position["col"]]
                                    for adjacent_position in seat["adjacent_positions"]
                                    if adjacent_position["col"] in matrix.get(adjacent_position["row"], {})]

    return matrix, len(lines), len(lines[0])

seats = lambda matrix: (seat for row, seats in matrix.items() for col, seat in seats.items())

def compute_first_solution(data):
    matrix, __, __ = build_first_matrix(data)

    while True:
        adjancent_taken_seat = lambda seat: [other for other in seat["adjacent"] if other["taken"]]
        seats_to_take = [seat for seat in seats(matrix) if not seat["taken"] and len(adjancent_taken_seat(seat)) == 0]
        seats_to_leave = [seat for seat in seats(matrix) if seat["taken"] and len(adjancent_taken_seat(seat)) >= 4]

        if len(seats_to_take) == 0 and len(seats_to_leave) == 0:
            return len([seat for seat in seats(matrix) if seat["taken"]])

        for seat in seats_to_take:
            seat["taken"] = True
        
        for seat in seats_to_leave:
            seat["taken"] = False


def compute_second_solution(data):
    matrix, rows_count, cols_count = build_first_matrix(data)

    while True:
        @memoized()
        def taken(row, col, row_dir, col_dir):
            if not (0 <= row < rows_count) or not (0 <= col < cols_count):
                return False
            elif row in matrix and col in matrix[row]:
                return matrix[row][col]["taken"]
            else:
                return taken(row + row_dir, col + col_dir, row_dir, col_dir)

        adjancent_taken_seat = lambda seat: [
            other_position for other_position in seat["adjacent_positions"]
            if taken(other_position["row"], other_position["col"], other_position["row"] - seat["row"], other_position["col"] - seat["col"])]
        
        seats_to_take = [seat for seat in seats(matrix) if not seat["taken"] and len(adjancent_taken_seat(seat)) == 0]
        seats_to_leave = [seat for seat in seats(matrix) if seat["taken"] and len(adjancent_taken_seat(seat)) >= 5]

        if len(seats_to_take) == 0 and len(seats_to_leave) == 0:
            return len([seat for seat in seats(matrix) if seat["taken"]])

        for seat in seats_to_take:
            seat["taken"] = True
        
        for seat in seats_to_leave:
            seat["taken"] = False



data = sys.stdin.read()

print("solution 1:", compute_first_solution(data))
print("solution 2:", compute_second_solution(data))


