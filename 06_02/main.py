
input = open ('input.txt', 'r')
line = input.readline()

def has_unique_chars(s):
    length = len(s)
    for i in range(length):
        c = s[i]
        for j in range(i + 1, length):
            if c == s[j]:
                return False
    return True

for i in range(0, len(line) - 14):
    if has_unique_chars(line[i:i+14]):
        print(i+14)
        break
