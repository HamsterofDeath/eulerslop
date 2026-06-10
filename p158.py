#!/usr/bin/env python3
"""p158: Maximum p(n) for n<=26, where p(n) = C(26,n) * A(n,1).
A(n,1) = number of permutations of n with exactly 1 ascent = 2^n - n - 1."""
from math import comb

def solve():
    best = 0
    for n in range(1, 27):
        euler_1 = (1 << n) - n - 1  # 2^n - n - 1
        p = comb(26, n) * euler_1
        if p > best:
            best = p
    return best

if __name__ == "__main__":
    print(solve())
