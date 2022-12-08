
def count_until_false(iterable):
    result = 0
    for test in iterable:
        result += 1
        if not test:
            break
    return result

def score(grid, row, col):
    t = grid[row][col]
    return count_until_false(grid[row][i] < t for i in range(col - 1, -1, -1)) \
         * count_until_false(grid[row][i] < t for i in range(col + 1, len(grid[row]))) \
         * count_until_false(grid[j][col] < t for j in range(row - 1, -1, -1)) \
         * count_until_false(grid[j][col] < t for j in range(row + 1, len(grid)))

grid = tuple(tuple(map(int, line.rstrip())) for line in open('input.txt', 'r'))

max_score = -1
for j, i in ((j,i) for j in range(1, len(grid) - 1) for i in range(1, len(grid[0]) - 1)):
    tree_score = score(grid, j, i)
    if tree_score > max_score:
        max_score = tree_score

print(max_score)