
from functools import cmp_to_key
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

sep2 = parse('[[2]]')
sep6 = parse('[[6]]')

packets = []
packets.append(sep2)
packets.append(sep6)

for line in open('input.txt', 'r'):
    line = line.strip()
    if not line:
        continue
    packets.append(parse(line))

packets = sorted(packets, key=cmp_to_key(compare))

print((packets.index(sep2) + 1) * (packets.index(sep6) + 1))
