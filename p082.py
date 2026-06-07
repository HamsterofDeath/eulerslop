#!/usr/bin/env python3
import urllib.request

def solve():
    url = "https://projecteuler.net/project/resources/p082_matrix.txt"
    with urllib.request.urlopen(url) as f:
        data = f.read().decode("utf-8")
    grid = [[int(n) for n in line.split(",")] for line in data.strip().split("\n")]
    size = len(grid)

    # Dynamic programming column by column
    dp = [row[0] for row in grid]
    for c in range(1, size):
        # Move right from previous column
        new_dp = [dp[r] + grid[r][c] for r in range(size)]
        # Allow up/down moves
        for _ in range(size):
            changed = False
            for r in range(1, size):
                if new_dp[r - 1] + grid[r][c] < new_dp[r]:
                    new_dp[r] = new_dp[r - 1] + grid[r][c]
                    changed = True
            for r in range(size - 2, -1, -1):
                if new_dp[r + 1] + grid[r][c] < new_dp[r]:
                    new_dp[r] = new_dp[r + 1] + grid[r][c]
                    changed = True
            if not changed:
                break
        dp = new_dp
    return min(dp)

if __name__ == "__main__":
    print(solve())
