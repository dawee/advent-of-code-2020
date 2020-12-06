import os
import re


INPUT_PATH = os.path.realpath("{0}/../input".format(__loader__.path))


def occurences(iterable, item):
    return len([other for other in iterable if other == item])


def get_group_anyone_yes_answers(group):
    return set([answer for person in group.split("\n") for answer in person])


def get_group_everyone_yes_answers(group):
    answers = [answer for person in group.split("\n") for answer in person]
    answers_at_least_one_yes = get_group_anyone_yes_answers(group)
    persons_count = len(group.split("\n"))

    return [answer for answer in answers_at_least_one_yes if occurences(answers, answer) == persons_count]


with open(INPUT_PATH) as input:
    data = input.read()
    total_anyone_yes_count = sum([len(get_group_anyone_yes_answers(group)) for group in data.split("\n\n")])
    print("solution 1:", total_anyone_yes_count)
    total_everyone_yes_count = sum([len(get_group_everyone_yes_answers(group)) for group in data.split("\n\n")])
    print("solution 2:", total_everyone_yes_count)
