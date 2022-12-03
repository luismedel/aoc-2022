
input = open ('input.txt', 'r')

def get_group_priority(a, b, c):
    get_char_priority = lambda c: (ord(c) - ord('a') + 1) if c >= 'a' else (ord(c) - ord('A') + 27)
    group = (a, b, c) if len(a) > len(b) and len(a) > len(c) else ((b, a, c) if len(b) > len(a) and len(b) > len(c) else (c, a, b))
    repeated = next((chr for chr in group[0] if chr in group[1] and chr in group[2]), None)
    return get_char_priority(repeated) if repeated else 0

total = 0
while a:= next(input, None):
    total += get_group_priority(a.rstrip(), next(input).rstrip(), next(input).rstrip())

print(total)