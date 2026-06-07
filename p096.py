#!/usr/bin/env python3
import urllib.request

def solve_sudoku(grid):
    # Find empty cell
    for r in range(9):
        for c in range(9):
            if grid[r][c] == 0:
                row_set = set(grid[r])
                col_set = {grid[i][c] for i in range(9)}
                box_set = {grid[3*(r//3)+i][3*(c//3)+j] for i in range(3) for j in range(3)}
                used = row_set | col_set | box_set
                for n in range(1, 10):
                    if n not in used:
                        grid[r][c] = n
                        if solve_sudoku(grid):
                            return True
                        grid[r][c] = 0
                return False
    return True

def solve():
    url = "https://projecteuler.net/project/resources/p096_sudoku.txt"
    with urllib.request.urlopen(url) as f:
        data = f.read().decode("utf-8").strip().split("\n")
    
    total = 0
    grid = []
    for line in data:
        if line.startswith("Grid"):
            if grid:
                solve_sudoku(grid)
                total += 100 * grid[0][0] + 10 * grid[0][1] + grid[0][2]
            grid = []
        else:
            grid.append([int(c) for c in line])
    if grid:
        solve_sudoku(grid)
        total += 100 * grid[0][0] + 10 * grid[0][1] + grid[0][2]
    return total

if __name__ == "__main__":
    print(solve())
