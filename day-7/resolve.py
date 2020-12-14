import os
import re


INPUT_PATH = os.path.realpath("{0}/../input".format(__loader__.path))
SENTENCE_PATTERN = re.compile(
    r'(?P<subject>[\w ]+) bags contain (?P<objects>[\w\, ]+).\n?')
OBJECT_PATTERN = re.compile(r'(?P<count>\d+) (?P<name>[\w ]+) bag')
NO_OTHER_BAGS = re.compile(r'no other bags\n?')


def count_children_by_name(node, child_name):
    return sum(child["count"] for child in node["children"] if child["name"] == child_name) \
        + sum(count_children_by_name(child["node"], child_name)
              for child in node["children"])


def count_all_children(node):
    return sum([child["count"] * (1 + count_all_children(child["node"])) for child in node["children"]])


with open(INPUT_PATH) as input:
    tree = {}

    for sentence in input:
        sentence_dict = SENTENCE_PATTERN.match(sentence).groupdict()
        tree[sentence_dict["subject"]] = tree.get(sentence_dict["subject"], {
            "children": []
        })

        if not NO_OTHER_BAGS.match(sentence_dict["objects"]):
            for sentence_object in sentence_dict["objects"].split(", "):
                sentence_object_dict = OBJECT_PATTERN.match(
                    sentence_object).groupdict()
                tree[sentence_object_dict["name"]] = tree.get(sentence_object_dict["name"], {
                    "children": []
                })

                tree[sentence_dict["subject"]]["children"].append({
                    "name": sentence_object_dict["name"],
                    "count": int(sentence_object_dict["count"]),
                    "node": tree[sentence_object_dict["name"]]
                })

counts = (count_children_by_name(node, "shiny gold") for node in tree.values())
print("solution 1:", len([count for count in counts if count > 0]))

print("solution 2:", count_all_children(tree["shiny gold"]))
