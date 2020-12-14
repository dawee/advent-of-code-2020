import math
import sys
import time

import pandas


def solution_1(bus_ids, departure):
    df = pandas.DataFrame([{int(bus_id): (timestamp % int(bus_id) == 0) for bus_id in bus_ids.split(
        ',') if bus_id != 'x'} for timestamp in range(departure + 120)])
    next_stops = df[df.any(axis=1) & (df.index >= departure)]
    first_stop = next_stops.iloc[0]
    next_time = next_stops.index.tolist()[0]
    next_bus_id = first_stop[first_stop == True].index.tolist()[0]
    delay = next_time - departure

    return delay * next_bus_id


def solution_2(bus_ids, departure):
    buses = {index: int(bus_id) for index, bus_id in enumerate(
        bus_ids.split(',')) if bus_id != 'x'}
    gaps_to_go = list(buses.keys())

    timestamp = 0
    increment = 1
    last_match = None

    while len(gaps_to_go) > 0:
        gap_to_test = gaps_to_go[-1]

        if (timestamp + gap_to_test) % buses[gap_to_test] == 0:
            if len(gaps_to_go) == 1:
                return timestamp
            elif last_match is None:
                last_match = timestamp
            else:
                increment = timestamp - last_match
                last_match = None
                gaps_to_go.pop()

        timestamp += increment


departure_line, bus_ids = sys.stdin.read().split('\n')
departure = int(departure_line)


# print('solution 1:', solution_1(bus_ids, departure))
print('solution 2:', solution_2(bus_ids, departure))
