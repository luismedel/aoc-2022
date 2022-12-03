
input = open ('input.txt', 'r')

def get_line_priority(line):
    get_char_priority = lambda c: (ord(c) - ord('a') + 1) if c >= 'a' else (ord(c) - ord('A') + 27)
    repeated = next((chr for chr in line[:len(line)//2] if chr in line[len(line)//2:]), None)
    return get_char_priority(repeated) if repeated else 0

print(sum(map(get_line_priority, input), 0))
