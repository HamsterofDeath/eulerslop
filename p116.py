#!/usr/bin/env python3

def ways(n, k):
    # k = colored tile length, 1 = grey tile
    dp = [0] * (n + 1)
    dp[0] = 1
    for i in range(1, n + 1):
        dp[i] = dp[i - 1]
        if i >= k:
            dp[i] += dp[i - k]
    return dp[n] - 1  # subtract all-grey

def solve():
    return ways(50, 2) + ways(50, 3) + ways(50, 4)

if __name__ == "__main__":
    print(solve())
