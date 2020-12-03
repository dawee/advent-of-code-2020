import re
import pandas
import os

OPEN_SQUARE = False
TREE = True
INPUT_PATH = os.path.realpath("{0}/../input".format(__loader__.path))


class AreaMap:
    def __init__(self, input=None, matrix=None):
        self.matrix = [[(TREE if char == '#' else OPEN_SQUARE) for char in line] for line in input] if input else matrix
        self.pointer = (0, 0)

    @property
    def width(self):
        return len(self.matrix[0])

    def reset(self):
        self.pointer = (0, 0)

    def move(self, row_gap, col_gap):
        row, col = self.pointer
        self.pointer = (row + row_gap, col + col_gap)

    def is_tree(self):
        row, col = self.pointer
        return self.matrix[row][col % (self.width - 1)] == TREE

    def is_outside(self):
        row, col = self.pointer
        return row >= len(self.matrix)
    
    def compute_encountered_trees(self, slope):
        self.reset()

        row_gap, col_gap = slope
        encountered_trees = 0

        while not self.is_outside():
            if self.is_tree():
                encountered_trees += 1

            self.move(row_gap, col_gap)

        return encountered_trees


with open(INPUT_PATH) as input:
    area_map = AreaMap(input)


print("solution 1:", area_map.compute_encountered_trees((1, 3)))

product = 1
for slope in [(1, 1), (1, 3), (1, 5), (1, 7), (2, 1)]:
    product *= area_map.compute_encountered_trees(slope)

print("solution 2:", product)