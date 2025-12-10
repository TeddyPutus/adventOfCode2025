import itertools
ON = "#"
OFF = "."

class LightDiagram:
    def __init__(self, lights: list[str]):
        self.target = set([i for i, light in enumerate(lights) if light == ON])

class Button:
    def __init__(self, lights: list[str]):
        self.lights = set([int(light) for light in lights])

    def apply(self, state: set[int]):
        for light in self.lights:
            if light in state:
                state.remove(light)
            else:
                state.add(light)

class Joltage:
    def __init__(self, joltages :list[str]):
        self.joltages = [int(j) for j in joltages]

class Manual:
    def __init__(self, light_diagram: LightDiagram, buttons: list[Button], joltage: Joltage):
        self.light_diagram = light_diagram
        self.buttons = buttons
        self.joltage = joltage
        self.current_state = set()
        self.best_solution = -1

    def solve(self) -> int:
        i = 0
        while self.best_solution == -1:
            for subset in itertools.combinations(self.buttons, i):
                for button in subset:
                    button.apply(self.current_state)
                if i!=0 and  self.current_state == self.light_diagram.target:
                    self.best_solution = i
                self.current_state = set()
            i+=1
        return self.best_solution

filepath = "C:/Users/teddy/IdeaProjects/adventOfCode2025/input_files/day_10.txt"

manuals: list[Manual] = []
total = 0

with open(filepath, "r") as file:
    input = file.readlines()
for index, line in enumerate(input):
    inputs = line.strip().split(" ")
    joltage = inputs.pop().strip().replace("{","").replace("}","").split(",")
    light_diagram = [char for char in inputs.pop(0).strip().replace("[","").replace("]","")]

    buttons = [
        Button(el.strip().replace("(","").replace(")","").split(",")) for el in inputs
    ]

    manual = Manual(
        LightDiagram(light_diagram),
        buttons,
        Joltage(joltage)
    )
    solution = manual.solve()
    print(f"Solution for manual {index} is {solution}")
    total += solution

    manuals.append(
        manual
    )
print(f"Part 1: {total}")
