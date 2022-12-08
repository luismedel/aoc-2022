
def is_visible(grid, row, col):
    t = grid[row][col]
    return all(grid[row][i] < t for i in range(col - 1, -1, -1)) \
        or all(grid[row][i] < t for i in range(col + 1, len(grid[row]))) \
        or all(grid[j][col] < t for j in range(row - 1, -1, -1)) \
        or all(grid[j][col] < t for j in range(row + 1, len(grid)))

grid = tuple(tuple(map(int, line.rstrip())) for line in open('input.txt', 'r'))

result = sum(1 if is_visible(grid, j, i) else 0 for j,i in
             ((j,i) for j in range(len(grid)) for i in range(len(grid[0]))))
print(result)