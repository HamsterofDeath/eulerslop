#!/usr/bin/env python3
"""p181: Grouping objects

Find the number of ways sixty black objects B and forty white objects W
can be grouped (i.e. partitioned into non-empty multisets).
This is solved using 2D knapsack DP.
"""

def solve():
    # We want to partition the multiset {60*B, 40*W}
    # Denominations are (b, w) where 0 <= b <= 60, 0 <= w <= 40, b + w >= 1.
    # dp[i][j] is the number of ways to partition {i*B, j*W} using the first k denominations.
    
    max_b = 60
    max_w = 40
    
    dp = [[0] * (max_w + 1) for _ in range(max_b + 1)]
    dp[0][0] = 1
    
    # We loop over all denominations in lexicographical order
    for b in range(max_b + 1):
        for w in range(max_w + 1):
            if b == 0 and w == 0:
                continue
                
            # Update DP table using this denomination
            for i in range(b, max_b + 1):
                for j in range(w, max_w + 1):
                    dp[i][j] += dp[i - b][j - w]
                    
    return dp[max_b][max_w]

if __name__ == "__main__":
    print(solve())
