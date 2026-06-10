#!/usr/bin/env python3

def F(m, n):
    dp = [0] * (n + 1)
    dp[0] = 1
    for i in range(1, n + 1):
        dp[i] = dp[i - 1]
        for k in range(m, i + 1):
            dp[i] += dp[i - k - 1] if i - k - 1 >= 0 else (1 if k == i else 0)
    return dp[n]

def solve():
    m = 50
    n = m
    while True:
        if F(m, n) > 1_000_000:
            return n
        n += 1

if __name__ == "__main__":
    print(solve())
