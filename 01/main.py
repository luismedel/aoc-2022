
from typing import List


elves: List[int] = [0]
current: int = 0

with open('input.txt', 'r') as input:
    for s in input:
        s = s.rstrip()
        if not s:
            current += 1
            elves.append(0)
        else:
            elves[current] += int(s)

print(max(elves))
