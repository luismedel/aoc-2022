
input = open ('input.txt', 'r')

def range_overlap(a, b):
    return (b[0] >= a[0] and b[0] <= a[1] and b[1] >= a[0] and b[1] <= a[1]) \
        or (a[0] >= b[0] and a[0] <= b[1] and a[1] >= b[0] and a[1] <= b[1])

total = 0
for line in input:
    parts = line.split(',')
    left = tuple(map(int, parts[0].split('-')))
    right = tuple(map(int, parts[1].split('-')))
    if range_overlap(left, right):
        total += 1

print(total)