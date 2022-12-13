
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
        self.E = GridPos(0,0)
        self.grid: List[List[int]] = None

    def load_from_file(self, path):
        with open(path, 'r') as input:
            self.grid = tuple(list(map(ord, line.strip())) for line in input.readlines())

        for j in range(len(self.grid)):
            row = self.grid[j]
            for i in range(len(row)):
                if row[i] == ord('S'):
                    row[i] = ord('a')
                    self.S = GridPos(j, i)
                elif row[i] == ord('E'):
                    row[i] = ord('z')
                    self.E = GridPos(j, i)

    def value_at(self, pos: GridPos) -> int:
        if pos.row < 0 or pos.row >= len(self.grid) or pos.col < 0 or pos.col >= len(self.grid[0]):
            return -1
        return self.grid[pos.row][pos.col]

def search_paths(terrain: Terrain) -> Iterable[Iterable[GridPos]]:
    start = SearchNode(terrain.S, None, 0)

    dq = deque((start,))
    visited = set()
    costs = [[999999 for j in range(len(terrain.grid[0]))]
                      for i in range(len(terrain.grid))]

    result: List[List[GridPos]] = []

    def visit(node: SearchNode):
        if node.pos == terrain.E:
            path: List[SearchNode] = []
            n = node
            while n:
                path.append(n)
                n = n.prev_node
            result.append(path)
            return

        if costs[node.pos.row][node.pos.col] <= node.cost:
            return

        costs[node.pos.row][node.pos.col] = node.cost
        current = terrain.value_at(node.pos)

        for delta in ((-1, 0), (1, 0), (0, 1), (0, -1)):
            pos = inc_pos(node.pos, delta)
            if 0 <= terrain.value_at(pos) <= current + 1:
                dq.append(SearchNode(pos, node, node.cost + 1))

    while dq:
        visit(dq.pop())

    return result

terrain = Terrain()
terrain.load_from_file('input.txt')
paths = sorted(map(len, search_paths(terrain)))
print(paths[0] - 1, paths[-1] - 1)

