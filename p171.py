#!/usr/bin/env python3
"""p171: Sum of all n < 10^20 where sum of squares of digits is a perfect square."""
from math import isqrt

def solve():
    N = 20
    max_sq = 9*9 * N  # 81*20 = 1620
    squares = {i*i for i in range(1, isqrt(max_sq) + 1)}
    
    # dp[len][sum] = (count, sum_of_numbers)
    # Count all numbers with given length and digit-square-sum,
    # including leading zeros (we handle leading zeros via subtraction)
    dp = [[(0, 0) for _ in range(max_sq + 1)] for _ in range(N + 1)]
    dp[0][0] = (1, 0)
    
    for length in range(1, N + 1):
        for s in range(max_sq + 1):
            cnt, total = dp[length - 1][s]
            if cnt == 0:
                continue
            for d in range(10):
                ns = s + d * d
                if ns > max_sq:
                    continue
                prev_cnt, prev_total = dp[length][ns]
                new_cnt = prev_cnt + cnt
                new_total = prev_total + total * 10 + cnt * d
                dp[length][ns] = (new_cnt, new_total)
    
    # Sum over all lengths 1..N, all square sums
    # For n-digit numbers, subtract those with leading zero
    total = 0
    for l in range(1, N + 1):
        for s in squares:
            cnt, val_sum = dp[l][s]
            if cnt == 0:
                continue
            # Remove numbers starting with 0: those = dp[l-1][s] as suffix
            if l > 1:
                cnt0, total0 = dp[l - 1][s]
                cnt -= cnt0
                val_sum -= total0  # leading zero doesn't contribute
            total += val_sum
    
    return total % 10**9

if __name__ == "__main__":
    print(solve())
