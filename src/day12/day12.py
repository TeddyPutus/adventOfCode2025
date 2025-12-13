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
        self.hashes = self.area - self.empty

    def copy(self):
        return Shape(self.map.copy())

    def _rotate(self, map: list[list[str]]) -> list[list[str]]:
        return list(zip(*map))[::-1]

    def rotate(self, direction: int) -> list[list[str]]:
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

    @staticmethod
    def _pad(map_1: list[list[str]], map_2: list[list[str]], v_shift: int, h_shift: int):
        blank_line = [".", ".", "."]
        h_pad = ["." for i in range(h_shift + 1)]
        for i in range(v_shift):
            map_1.insert(0, blank_line)
            map_2.append(blank_line)
        for i in range(len(map_1)):
            map_1[i] = h_pad + list(map_1[i])
            map_2[i] = list(map_2[i]) + h_pad
        return map_1, map_2

    @staticmethod
    def _combine(shape_1: Shape, shape_2: Shape, v_shift: int, h_shift: int) -> Shape | None:
        def _vertical_slice(map: list[list[str]], index:int, pop=False):
            if pop:
                return [m.pop(index) for m in map]
            return [m[index] for m in map]


        map_1, map_2 = Shape._pad(shape_1.map.copy(), shape_2.map.copy(), v_shift, h_shift)

        new_map = []
        hash_count = 0
        hash_target = shape_1.hashes + shape_2.hashes
        for y in range(len(map_1)):
            new_line = []
            for x in range(len(map_1[0])):
                if map_1[y][x] == "#" or map_2[y][x] == "#":
                    new_line.append("#")
                    hash_count += 1
                else:
                    new_line.append(".")
            new_map.append(new_line)
        if hash_count != hash_target:
            return None

        print("Shapes don't overlap")
        # Trim rows and columns containing only dots
        while len(new_map) and "#" not in new_map[0]:
            new_map.pop(0)
        while len(new_map) and "#" not in new_map[-1]:
            new_map.pop()
        while len(new_map[0]) and "#" not in _vertical_slice(new_map, 0, False):
            _vertical_slice(new_map, 0, True)
        while len(new_map[0]) and "#" not in _vertical_slice(new_map, -1, False):
            _vertical_slice(new_map, -1, True)
        return Shape(new_map)

    def combine(self, shape: Shape) -> Shape:
        smallest_shape = None
        # rotate each, figure out what the smallest resulting shape is. Probably need to cache this somehow!
        for a in range(Directions.LEFT.value + 1):
            self.map = self.rotate(a)

            if self.map != shape.map:
                print("MAPS DIFFER")
                for line in self.map:
                    print(line)
                print("MAPS DIFFER")
                for line in shape.map:
                    print(line)
            # for b in range(Directions.LEFT.value + 1):
                # shape.map = shape.rotate(b)
            for x in range(0, 4):
                for y in range (0, 4):
                    new_shape = Shape._combine(self, shape, x, y)
                    if new_shape is not None:
                        print("-"*10)
                        for line in new_shape.map:
                            print(line)

                    if smallest_shape == None or (new_shape is not None and smallest_shape.area > new_shape.area):
                        smallest_shape = new_shape
        return smallest_shape

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
new_shape = shapes[4].copy().combine(shapes[4].copy())
print("-"*20)
for line in new_shape.map:
    print(line)

