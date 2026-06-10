#!/usr/bin/env python3
"""p179: Count n < 10^7 with equal divisor count as n+1."""
def solve():
    LIMIT = 10_000_000
    # Use sieve to compute divisor count
    div = [0] * (LIMIT + 1)
    for i in range(1, LIMIT + 1):
        for j in range(i, LIMIT + 1, i):
            div[j] += 1
    
    count = 0
    for n in range(2, LIMIT):
        if div[n] == div[n + 1]:
            count += 1
    return count

if __name__ == "__main__":
    print(solve())
