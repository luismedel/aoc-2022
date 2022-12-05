
import re

input = open ('input.txt', 'r')

def split(s):
    return tuple(s[i*4:i*4 + 4].strip() for i in range(len(s)//4))

def parse_stacks(input):
    header = []
    for line in input:
        if not line.rstrip():
            break
        header.append(line)
    stack_count = int(header[-1][-3])
    header.pop()

    result = [[] for i in range(stack_count)]
    for line in header:
        parts = tuple('   ' if not c else c for c in split(line))
        for i in range(stack_count):
            c = parts[i].rstrip()
            if c:
                result[i].append(c[1])

    return result

def process_instructions(input, stacks):
    r = re.compile(r'^move (\d+) from (\d+) to (\d+)')
    for s in input:
        m = r.match(s)
        if not m:
            break

        count = int(m.group(1))
        from_ = int(m.group(2)) - 1
        dest = int(m.group(3)) - 1

        items = stacks[from_][0:count]
        stacks[from_] = stacks[from_][count:]
        stacks[dest] = items + stacks[dest]

stacks = parse_stacks(input)
process_instructions(input, stacks)
print(''.join(stack[0] for stack in stacks))
