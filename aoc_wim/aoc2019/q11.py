from aocd import data
from aoc_wim.aoc2019 import IntComputer
from aoc_wim.ocr import AOCR
from collections import defaultdict


class Robot:
    def __init__(self, data, colour0=0, position0=0j, direction0=1j):
        self.brain = IntComputer(data)
        self.position = position0
        self.direction = direction0
        self.painted = defaultdict(int, {position0: colour0})

    def paint(self):
        while True:
            self.brain.input.append(self.painted[self.position])
            self.brain.run(until=IntComputer.op_output)
            self.brain.run(until=IntComputer.op_output)
            turn, colour = self.brain.output
            self.brain.output.clear()
            self.painted[self.position] = colour
            self.direction *= [1j, -1j][turn]
            self.position += self.direction

    def paint_until_halt(self):
        try:
            self.paint()
        except IntComputer.Halt:
            return


def part_a(data):
    robot = Robot(data)
    robot.paint_until_halt()
    n_panels = len(robot.painted)
    return n_panels


def part_b(data):
    robot = Robot(data, 1)
    robot.paint_until_halt()
    rego = AOCR[robot.painted]
    return rego


print(part_a(data))
print(part_b(data))