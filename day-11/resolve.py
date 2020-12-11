import sys


def build_first_matrix(data):
    matrix = dict([
            [row, dict([[col, {"taken": False, "adjacent": [], "row": row, "col": col}] for col, char in enumerate(line) if char == 'L'])]
            for row, line in enumerate(data.split("\n"))])

    for row, seats in matrix.items():
        for col, seat in seats.items():
            seat["adjacent"] = [matrix[row + row_gap][col + col_gap]
                                    for row_gap in range(-1, 2)
                                    for col_gap in range(-1, 2)
                                    if (col_gap != 0 or row_gap != 0) and (col + col_gap) in matrix.get(row + row_gap, {})]

    return matrix


def compute_first_solution(data):
    adjancent_taken_seat = lambda seat: [other for other in seat["adjacent"] if other["taken"]]
    seats = lambda matrix: (seat for row, seats in matrix.items() for col, seat in seats.items())
    matrix = build_first_matrix(data)


    while True:
        seats_to_take = [seat for seat in seats(matrix) if not seat["taken"] and len(adjancent_taken_seat(seat)) == 0]
        seats_to_leave = [seat for seat in seats(matrix) if seat["taken"] and len(adjancent_taken_seat(seat)) >= 4]

        if len(seats_to_take) == 0 and len(seats_to_leave) == 0:
            return len([seat for seat in seats(matrix) if seat["taken"]])

        for seat in seats_to_take:
            seat["taken"] = True
        
        for seat in seats_to_leave:
            seat["taken"] = False


data = sys.stdin.read()

print("solution 1:", compute_first_solution(data))
