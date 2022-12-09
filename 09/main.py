
from collections import namedtuple

Pos = namedtuple('Pos', ('row', 'col'))

ACTIONS = { 'U': (-1, 0), 'D': (1, 0), 'L': (0, -1), 'R':(0, 1) }

H = Pos(0, 0)
T = Pos(0, 0)

visits = {}

def add_visit():
    global T
    if T in visits:
        visits[T] += 1
    else:
        visits[T] = 1

def move_T():
    global T
    if T.row - 1 <= H.row <= T.row + 1 \
    and T.col - 1 <= H.col <= T.col + 1:
        return
    T = Pos(T.row + (-1 if T.row > H.row else 1 if T.row < H.row else 0), \
            T.col + (-1 if T.col > H.col else 1 if T.col < H.col else 0))

for line in open('input.txt', 'r'):
    action, count = line.rstrip().split(' ', maxsplit=1)
    for i in range(int(count)):
        H = Pos(H.row + ACTIONS[action][0], H.col + ACTIONS[action][1])
        move_T()
        add_visit()

print(len(visits.keys()))