from __future__ import annotations

import math
import sys
from enum import Enum
from itertools import permutations


class Directions(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

class Shape:
    def __init__(self, map: list[list[str]]):
        self.map = map#[["#" if char != "." else "." for char in line ] for line in map]
        self.height = len(self.map)
        self.length = len(self.map[0])
        self.area = self.height * self.length
        self.empty = self.empty_space()
        self.hashes = self.area - self.empty

    def copy(self):
        return Shape(self.map.copy())

    def _rotate(self, map: list[list[str]]) -> list[list[str]]:
        return list(zip(*map))[::-1]

    def rotate(self, direction: int = 1) -> list[list[str]]:
            map = self.map.copy()
            for i in range(direction):
                map = self._rotate(map)
            self.map = map
            self.height = len(self.map)
            self.length = len(self.map[0])
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

class Canvas:
    def __init__(self, shape_1: Shape, shape_2: Shape, v_pad: int, h_pad: int):
        self.height = v_pad + max(shape_1.height, shape_2.height)
        self.width = shape_1.length + shape_2.length
        self.canvas = [
            ["." for _ in range(self.width)]
            for _ in range(self.height)
        ]
        # self.hash_count = 0

    @property
    def hash_count(self):
        count = 0
        for y in self.canvas:
            for x in y:
                if x != ".":
                    count+=1
        return count

    def draw(self, shape: Shape, origin_y: int, origin_x: int, fill: str = "#"):
        for y in range(origin_y, origin_y + shape.height):
            for x in range(origin_x, origin_x + shape.length):
                if shape.map[y - origin_y][x - origin_x] != ".":
                    # if self.canvas[y][x] != ".":
                    #     raise Exception("Drawing on filled tile")
                    self.canvas[y][x] = fill

    def clear(self):
        self.canvas = [
            ["." for _ in range(self.width)]
            for _ in range(self.height)
        ]



def create_canvas(shape_1: Shape, shape_2: Shape, v_pad: int, h_pad: int):
    height = v_pad + max(
        shape_1.height,
        shape_2.height)
    width = shape_2.length + h_pad

    return [
        ["." for _ in range(width)]
        for _ in range(height)
    ]

combine_cache = {}

def combine_shapes(shape_1: Shape, shape_2: Shape, debug=True):
    cache_key_1 = f"{str(hash(str(shape_1.map)))},{hash(str(shape_2.map))}"
    cache_key_2 = f"{hash(str(shape_2.map))},{hash(str(shape_1.map))}"

    if cached:=combine_cache.get(cache_key_1, combine_cache.get(cache_key_2)):
        return cached.copy()

    smallest_shape = None

    for a in range(Directions.LEFT.value + 1):
        if a > 0:
            shape_1.rotate()
        for b in range(Directions.LEFT.value + 1):
            if b > 0:
                shape_2.rotate()

            for v in range(0, shape_2.height):
                for h in range(0, shape_1.length):
                    canvas = Canvas(shape_1, shape_2, abs(v), 0)
                    canvas.draw(shape_1, 0, 0, "A")
                    # try:
                    canvas.draw(shape_2, v, h, "B")
                    new_shape = trim(canvas.canvas, {"A", "B"})
                    if canvas.hash_count == (shape_1.hashes + shape_2.hashes) and (smallest_shape is None or  new_shape.area < smallest_shape.area):
                        smallest_shape = new_shape
                        # potentially exit early

                        if debug:
                            print("-"*20)
                            for line in new_shape.map:
                                print(line)

                    # except Exception:
                    #     continue
    if smallest_shape:
        combine_cache[cache_key_2] = smallest_shape.copy()
        combine_cache[cache_key_1] = smallest_shape.copy()
    else:
        smallest_shape = Shape([[]])
        smallest_shape.height = sys.maxsize
        smallest_shape.length = sys.maxsize
        combine_cache[cache_key_2] = None
        combine_cache[cache_key_1] = None
    return smallest_shape

                # Add shape 1 from origin (v*-1),0
                # Add shape 2 0, h*-1
                # check number of hashes, if correct amount AND area smaller than smallest shape, replace smallest shape
def trim(new_map:list[list[str]], pattern_chars: set[str] = {"#"}):
    def _vertical_slice(map: list[list[str]], index:int, pop=False):
        if pop:
            return [m.pop(index) for m in map]
        return [m[index] for m in map]

    while len(new_map) and not pattern_chars.intersection(set(new_map[0])):
        new_map.pop(0)
    while len(new_map) and not pattern_chars.intersection(set(new_map[-1])):
        new_map.pop()
    while len(new_map[0]) and not pattern_chars.intersection(set( _vertical_slice(new_map, 0, False))):
        _vertical_slice(new_map, 0, True)
    while len(new_map[0]) and  not pattern_chars.intersection(set( _vertical_slice(new_map, -1, False))):
        _vertical_slice(new_map, -1, True)
    return Shape(new_map)

def build_list(presents: list[int]) -> list[Shape]:
    present_list = []
    for i, present_count in enumerate(presents):
        for x in range(present_count):
            present_list.append(shapes[i].copy())
    return present_list

def quick_filter(presents: list[Shape], area_x, area_y) -> bool:
    area = area_x * area_y
    pres_area = 0
    for pres in presents:
        pres_area += pres.hashes
    return pres_area >= area

def can_fit(area_x, area_y, present_list:list[int]) -> bool:
    present_list = build_list(present_list)
    if quick_filter(present_list, area_x, area_y):
        print("QUICK FILTER!")
        return False
    else:
        return True

    for j in permutations(present_list):
        present_a = None
        for i, present in enumerate(j):
            if i == 0:
                present_a = present.copy()
            else:
                present_b = present.copy()
                present_a = combine_shapes(present_a, present_b, True)

            if present_a is None or present_a.length > area_x or present_a.height > area_y:
                break
        if present_a is not None and present_a.length <= area_x and present_a.height <= area_y:
            return True

    if present_a is not None and present_a.length <= area_x and present_a.height <= area_y:
        return True
    return False



# filepath = "day12_example.txt"
filepath = "C:/Users/teddy/IdeaProjects/adventOfCode2025/src/day12/day12.txt"

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
    area_x = int(area_x)
    area_y = int(area_y)
    presents = [int(num) for num in split]

    if can_fit(area_x, area_y, presents):
        print("IT FITS")
        total += 1

print(f"(PART 1) Total is: {total}")