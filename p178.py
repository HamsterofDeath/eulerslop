#!/usr/bin/env python3
"""p178: Pandigital step numbers < 10^40.
Adjacent digits differ by exactly 1, must contain 0-9 at least once."""
def solve():
    MAX_LEN = 40
    FULL_MASK = (1 << 10) - 1
    
    # dp[length][last_digit][mask] = count
    # Use list of dicts for sparse representation
    dp = [{} for _ in range(MAX_LEN + 1)]
    
    # length 1: single digit, no leading zero restriction yet
    for d in range(1, 10):
        dp[1][(d, 1 << d)] = 1
    
    for l in range(1, MAX_LEN):
        for (last, mask), cnt in dp[l].items():
            for nd in (last - 1, last + 1):
                if 0 <= nd <= 9:
                    nmask = mask | (1 << nd)
                    key = (nd, nmask)
                    dp[l + 1][key] = dp[l + 1].get(key, 0) + cnt
    
    total = 0
    for l in range(1, MAX_LEN + 1):
        for (last, mask), cnt in dp[l].items():
            if mask == FULL_MASK:
                total += cnt
    
    return total

if __name__ == "__main__":
    print(solve())
