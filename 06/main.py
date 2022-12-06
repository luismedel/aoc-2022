
input = open ('input.txt', 'r')
line = input.readline()

def is_header(s):
    length = len(s)
    for i in range(length):
        c = s[i]
        for j in range(i + 1, length):
            if c == s[j]:
                return False
    return True

for i in range(0, len(line) - 4):
    if is_header(line[i:i+4]):
        print(i+4)
        break
