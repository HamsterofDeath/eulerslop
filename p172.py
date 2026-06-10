#!/usr/bin/env python3
"""p172: Count 18-digit numbers with at most 3 occurrences of each digit."""
from math import comb, factorial

def solve():
    # Track counts of each digit 0-9, each 0..3, sum = 18.
    # First digit cannot be 0.
    # Use DP over digit types.
    digits = 10
    max_per_digit = 3
    total_len = 18
    
    # dp[pos][count] = ways for first `pos` digit types, total `count` digits used
    dp = [[0] * (total_len + 1) for _ in range(digits + 1)]
    dp[0][0] = 1
    
    for pos in range(digits):
        for used in range(total_len + 1):
            if dp[pos][used] == 0:
                continue
            for take in range(max_per_digit + 1):
                if used + take > total_len:
                    break
                # ways to choose positions for `take` copies of this digit
                # among the remaining (total_len - used) positions
                ways = comb(total_len - used, take)
                dp[pos + 1][used + take] += dp[pos][used] * ways
    
    total_all = dp[digits][total_len]
    
    # Subtract those with leading zero
    # Fix first position as 0, then distribute remaining 17 among digits 0..9
    # with digit 0 now having at most 2 more (since one already used)
    dp0 = [[0] * (total_len) for _ in range(digits + 1)]
    dp0[0][0] = 1
    for pos in range(digits):
        for used in range(total_len):
            if dp0[pos][used] == 0:
                continue
            max_take = max_per_digit
            if pos == 0:
                max_take = 2  # one 0 already at front
            for take in range(max_take + 1):
                if used + take >= total_len:
                    break
                ways = comb(total_len - 1 - used, take)
                dp0[pos + 1][used + take] += dp0[pos][used] * ways
    
    total_no_lead0 = total_all - dp0[digits][total_len - 1]
    return total_no_lead0

if __name__ == "__main__":
    print(solve())
