#!/usr/bin/env python3
import urllib.request

def solve():
    url = "https://projecteuler.net/project/resources/p081_matrix.txt"
    with urllib.request.urlopen(url) as f:
        data = f.read().decode("utf-8")
    grid = [[int(n) for n in line.split(",")] for line in data.strip().split("\n")]
    size = len(grid)
    for i in range(1, size):
        grid[i][0] += grid[i - 1][0]
        grid[0][i] += grid[0][i - 1]
    for r in range(1, size):
        for c in range(1, size):
            grid[r][c] += min(grid[r - 1][c], grid[r][c - 1])
    return grid[size - 1][size - 1]

if __name__ == "__main__":
    print(solve())
