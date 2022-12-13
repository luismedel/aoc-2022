
from ast import List, Tuple
from collections import deque, namedtuple
from typing import Any, Dict, Iterable


GridPos = namedtuple('GridPos', ('row', 'col'))
SearchNode = namedtuple('SearchNode', ('pos', 'prev_node', 'cost'))

def inc_pos(pos: GridPos, row_col_delta: Tuple(int, int)) -> GridPos:
    return GridPos(pos.row + row_col_delta[0], pos.col + row_col_delta[1])

class Terrain:
    def __init__(self):
        self.S = GridPos(0,0)
        self.grid: List[List[int]] = None

    def load_from_file(self, path):
        with open(path, 'r') as input:
            self.grid = tuple(list(map(ord, line.strip())) for line in input.readlines())

        for j in range(len(self.grid)):
            row = self.grid[j]
            for i in range(len(row)):
                if row[i] == ord('S'):
                    row[i] = ord('a')
                elif row[i] == ord('E'):
                    row[i] = ord('z')
                    self.S = GridPos(j, i)

    def value_at(self, pos: GridPos) -> int:
        if pos.row < 0 or pos.row >= len(self.grid) or pos.col < 0 or pos.col >= len(self.grid[0]):
            return -1
        return self.grid[pos.row][pos.col]

def search_paths(terrain: Terrain) -> Iterable[Iterable[GridPos]]:
    start = SearchNode(terrain.S, None, 0)

    dq = deque((start,))
    costs = [[999999 for j in range(len(terrain.grid[0]))]
                      for i in range(len(terrain.grid))]

    result: List[int] = []

    def visit(node: SearchNode):
        current = terrain.value_at(node.pos)
        if current == ord('a'):
            terrain.grid[node.pos.row][node.pos.col] == ' '
            result.append(node.cost)
            return

        if costs[node.pos.row][node.pos.col] <= node.cost:
            return

        costs[node.pos.row][node.pos.col] = node.cost

        for delta in ((-1, 0), (1, 0), (0, 1), (0, -1)):
            pos = inc_pos(node.pos, delta)
            v = terrain.value_at(pos)
            if v and (current - v < 2):
                dq.append(SearchNode(pos, node, node.cost + 1))

    while dq:
        visit(dq.pop())

    return result

terrain = Terrain()
terrain.load_from_file('input.txt')
solutions = sorted(set(search_paths(terrain)))
print(solutions[0], solutions[-1])
