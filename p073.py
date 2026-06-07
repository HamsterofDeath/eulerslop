#!/usr/bin/env python3
from math import gcd

def solve():
    count = 0
    # Reduced fractions between 1/3 and 1/2 for d <= 12000
    for d in range(2, 12001):
        lo = d // 3 + 1
        hi = (d - 1) // 2
        for n in range(lo, hi + 1):
            if gcd(n, d) == 1:
                count += 1
    return count

if __name__ == "__main__":
    print(solve())
