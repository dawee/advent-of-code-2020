import os

INPUT_PATH = os.path.realpath("{0}/../input".format(__loader__.path))

def exists(expenses, expense):
    try:
        return expenses.index(expense) and True
    except:
        return False



with open(INPUT_PATH) as data:
    expenses = [int(line) for line in data.readlines()]

    for expense in expenses:
        complement = 2020 - expense

        if exists(expenses, complement):
            print("solution 1:", expense * complement)
            break

    solution_2_found = False

    for expense in expenses:
        rest = 2020 - expense

        for sub_expense in expenses:
            complement = rest - sub_expense

            if exists(expenses, complement):
                print("solution 2:", expense * sub_expense * complement)
                solution_2_found = True
                break

        if solution_2_found:
            break