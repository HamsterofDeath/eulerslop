#!/usr/bin/env python3
"""p164: Count 20-digit numbers with no three consecutive digits summing > 9."""
def solve():
    # DP: dp[pos][d1][d2] = count of numbers of length pos ending with digits d1,d2
    dp = {}
    for a in range(1, 10):
        for b in range(10):
            if a + b <= 9:
                dp[(a, b)] = 1
    
    for pos in range(3, 21):
        ndp = {}
        for (a, b), cnt in dp.items():
            for c in range(10):
                if a + b + c <= 9:
                    key = (b, c)
                    ndp[key] = ndp.get(key, 0) + cnt
        dp = ndp
    
    return sum(dp.values())

if __name__ == "__main__":
    print(solve())
