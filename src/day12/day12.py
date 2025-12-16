from __future__ import annotations

import sys

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

    for a in range(4):
        if a > 0:
            shape_1.rotate()
        for b in range(4):
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