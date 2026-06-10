#!/usr/bin/env python3

def solve():
    n = 50
    dp = [0] * (n + 1)
    dp[0] = 1
    for i in range(1, n + 1):
        dp[i] = dp[i - 1]
        for k in [2, 3, 4]:
            if i >= k:
                dp[i] += dp[i - k]
    return dp[n]

if __name__ == "__main__":
    print(solve())
