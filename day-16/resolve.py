from functools import reduce
import re
import sys


RANGE_PATTERN = re.compile(
    r'^(?P<name>[\w\ ]+): (?P<range_1>\d+\-\d+) or (?P<range_2>\d+\-\d+)$')


def parse_category_ranges(ranges_block):
    range_matches = (RANGE_PATTERN.match(range_line).groupdict()
                     for range_line in ranges_block.split('\n'))

    return {
        group['name']: [
            [int(part) for part in range_expression.split('-')]
            for range_expression in (group['range_1'], group['range_2'])
        ] for group in range_matches
    }


def parse_tickets(tickets_expression):
    return [
        [int(value) for value in line.split(',')]
        for line in tickets_expression.split('\n')[1:]
    ]


def parse_input(input):
    ranges_block, my_ticket_block, nearby_tickets_block = \
        input.replace('\r\n', '\n').split('\n\n')

    return {
        "categories_ranges": parse_category_ranges(ranges_block),
        "my_ticket": parse_tickets(my_ticket_block)[0],
        "nearby_tickets": parse_tickets(nearby_tickets_block),
    }


def value_in_category_ranges(value, category_ranges):
    return any((min_value <= value <= max_value for min_value, max_value in category_ranges))


def is_value_valid(value, categories_ranges):
    return any((value_in_category_ranges(value, category_ranges) for category_ranges in categories_ranges.values()))


def is_ticket_valid(ticket, categories_ranges):
    return all((is_value_valid(value, categories_ranges) for value in ticket))


def filter_valid_tickets(tickets, categories_ranges):
    return [ticket for ticket in tickets if is_ticket_valid(ticket, categories_ranges)]


def map_all_values_by_index(tickets):
    return {index: [ticket[index] for ticket in tickets] for index, __ in enumerate(tickets[0])}


def sum_invalid_values(nearby_tickets, categories_ranges):
    return sum([
        value
        for ticket in nearby_tickets
        for value in ticket if not is_value_valid(value, categories_ranges)
    ])


def identify_possible_categories(values, categories_ranges):
    return [
        category_name
        for category_name, category_ranges in categories_ranges.items()
        if all((value_in_category_ranges(value, category_ranges) for value in values))
    ]


def filter_index_categories(filtered_index_categories, unpicked_categories, all_values_by_index):
    return {
        index: (
            filtered_index_categories[index]
            if index in filtered_index_categories and len(filtered_index_categories[index]) == 1
            else identify_possible_categories(values, unpicked_categories)
        )
        for index, values in all_values_by_index.items()
    }


def find_unpicked_categories(unpicked_categories, filtered_index_categories):
    unpicked_names = [
        category_names[0]
        for category_names in filtered_index_categories.values()
        if len(category_names) == 1 and category_names[0] in unpicked_categories
    ]

    return {name: ranges for name, ranges in unpicked_categories.items() if name not in unpicked_names}


def identify_categories(categories_ranges, all_values_by_index):
    unpicked_categories = {**categories_ranges}
    filtered_index_categories = {}

    while len(unpicked_categories) > 0:
        filtered_index_categories = filter_index_categories(
            filtered_index_categories, unpicked_categories, all_values_by_index)

        unpicked_categories = find_unpicked_categories(
            unpicked_categories, filtered_index_categories)

    return {category_names[0]: index for index, category_names in filtered_index_categories.items()}


def my_ticket_product(nearby_tickets, categories_ranges, my_ticket):
    valid_tickets = filter_valid_tickets(nearby_tickets, categories_ranges)
    all_values_by_index = map_all_values_by_index(valid_tickets)

    departure_categories_indexes = (
        index
        for name, index in identify_categories(categories_ranges, all_values_by_index).items()
        if 'departure' in name
    )

    departure_values = (
        my_ticket[index]
        for index in departure_categories_indexes
    )

    return reduce(lambda memo, value: memo * value, departure_values, 1)


spec = parse_input(sys.stdin.read())

print('solution 1:', sum_invalid_values(
    spec['nearby_tickets'], spec['categories_ranges']))

print('solution 2:', my_ticket_product(**spec))
