
input = open ('input.txt', 'r')

def range_partial_overlap(a, b):
    return (a[0] <= b[0] <= a[1]) or (a[0] <= b[1] <= a[1]) or \
           (b[0] <= a[0] <= b[1]) or (b[0] <= a[1] <= b[1])

total = 0
for line in input:
    parts = line.split(',')
    left = list(map(int, parts[0].split('-')))
    right = list(map(int, parts[1].split('-')))

    if range_partial_overlap(left, right):
        total += 1

print(total)