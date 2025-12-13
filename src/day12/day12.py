from __future__ import annotations
from enum import Enum

class Directions(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

class Shape:
    def __init__(self, map: list[list[str]]):
        self.map = map
        self.height = len(self.map)
        self.length = len(self.map[0])
        self.area = self.height * self.length
        self.empty = self.empty_space()

    def _rotate(self, map: list[list[str]]) -> list[list[str]]:
        return list(zip(*map))[::-1]

    def rotate(self, direction: Directions):
            map = self.map.copy()
            for i in range(direction):
                map = self._rotate(map)
            return map

    def empty_space(self) -> int:
        empty = 0
        for line in self.map:
            for char in line:
              if char == ".":
                  empty+=1
        return empty

    def combine(self, shape: Shape) -> Shape:
        smallest_shape = None
        # rotate each, figure out what the smallest resulting shape is. Probably need to cache this somehow!
        return shape

# filepath = "day12_example.txt"
filepath = "C:/Users/teddy/IdeaProjects/adventOfCode2025/src/day12/day_12_example.txt"

total = 0
shapes = {}

with open(filepath, "r") as file:
    input = file.readlines()

for i, line in enumerate(input):
    if "x" not in line:
        if ":" not in line:
            continue
        count = line.strip().replace(":",'')
        shape = [[char for char in l.strip()]  for l in input[i+1:i+4]]
        shapes[int(count)] = Shape(shape)
        continue


    split = line.replace(":","").strip().split(" ")

    area_x, area_y = split.pop(0).strip().split("x")
    area = int(area_x) * int(area_y)
    present_area = 0
    for num in split:
        # Figure out smallest area using rotations
        pass

print(f"Total is {total}")

