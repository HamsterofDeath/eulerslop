#!/usr/bin/env python3
from math import comb

def solve():
    return sum(1 for n in range(1, 101) for r in range(1, n + 1) if comb(n, r) > 1_000_000)

if __name__ == "__main__":
    print(solve())
