
import re
from typing import Any, Tuple

rint = re.compile('\d+')

def compare_ints(left: int, right: int):
    return 0 if left == right else -1 if left < right else 1

def compare(left: Any, right: Any) -> int:
    if isinstance(left, int) and isinstance(right, int):
        return compare_ints(left, right)

    left = [left] if isinstance(left, int) else left
    right = [right] if isinstance(right, int) else right

    len_left = len(left)
    len_right = len(right)
    length = min(len_left, len_right)

    for i in range(length):
        test = compare(left[i], right[i])
        if test != 0:
            return test

    return compare_ints(len_left, len_right)

def parse(line: str, offset: int = 0) -> Tuple[Any, int]:
    global rint

    if line[offset] == '[':
        if line[offset + 1] == ']':
            return [], offset + 2

        item, offset = parse(line, offset + 1)
        result = [item]
        while line[offset] == ',':
            item, offset = parse(line, offset + 1)
            result.append(item)
        assert line[offset] == ']'
        return result, offset + 1
    else:
        m = rint.match(line, offset)
        assert m
        result = m.group(0)
        return int(result), offset + len(result)

indices = []
with open('input.txt', 'r') as input:
    i = 1
    while True:
        left = input.readline().strip()
        if not left:
            break
        left = parse(left)
        right = parse(input.readline().strip())
        if compare(left, right) == -1:
            indices.append(i)
        i += 1
        input.readline()

print(sum(indices))
