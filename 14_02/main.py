
from collections import namedtuple
from typing import Set

Point = namedtuple('Point', ('x', 'y'))

mkpt = lambda s: Point(*(map(int, s.split(','))))

class Cascade:
    def __init__(self):
        self.grid: Set[Point] = set()
        self._left: int = 999999
        self._right: int = -1
        self._top: int = 999999
        self._bottom: int = -1

    def put(self, pt: Point):
        self.grid.add(pt)

    def set_bounds(self):
        self._left = min(pt.x for pt in self.grid)
        self._right = max(pt.x for pt in self.grid)
        self._top = min(pt.y for pt in self.grid)
        self._bottom = max(pt.y for pt in self.grid) + 2

    def is_free(self, pt: Point):
        if pt.y == self._bottom:
            return False
        return pt not in self.grid

    def run(self, grain: Point) -> bool:
        while True:
            place = True
            for dx, dy in ((0, 1), (-1, 1), (1, 1)):
                next = Point(grain.x + dx, grain.y + dy)
                if self.is_free(next):
                    grain = next
                    place = False
                    break
            if place:
                self.put(grain)
                return True

    def put_line(self, from_: Point, to_: Point):
        dx = 0 if from_.x == to_.x else -1 if to_.x < from_.x else 1
        dy = 0 if from_.y == to_.y else -1 if to_.y < from_.y else 1
        while from_ != to_:
            c.put(from_)
            from_ = Point(from_.x + dx, from_.y + dy)
        c.put(to_)

    def print(self):
        width = self._right - self._left + 1
        height = self._bottom - self._top + 1
        grid = [['.'] * width for _ in range(height)]
        for pt in self.grid:
            grid[pt.y - self._top][pt.x - self._left] = 'x'
        for line in grid:
            print(''.join(line))


c = Cascade()

for line in open('input.txt', 'r'):
    points = [mkpt(pt) for pt in line.split('->')]
    for i in range(0, len(points) - 1):
        c.put_line(points[i], points[i + 1])
c.set_bounds()

grains = 0
source = Point(500, 0)
while c.is_free(source):
    c.run(source)
    grains += 1

print(grains)