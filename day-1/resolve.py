import os


INPUT_PATH = os.path.realpath("{0}/../input".format(__loader__.path))


def exists(expenses, expense):
    try:
        return expenses.index(expense) and True
    except:
        return False


def get_complement_product(expenses, expected_sum):
    for expense in expenses:
        complement = expected_sum - expense

        if exists(expenses, complement):
            return expense * complement


with open(INPUT_PATH) as data:
    expenses = [int(line) for line in data.readlines()]
    print("solution 1:", get_complement_product(expenses, 2020))

    for expense in expenses:
        rest_product = get_complement_product(expenses, 2020 - expense)

        if rest_product:
            print("solution 2:", expense * rest_product)
            break
