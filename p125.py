#!/usr/bin/env python3
from math import isqrt

def is_pal(n):
    s = str(n)
    return s == s[::-1]

def solve():
    limit = 10 ** 8
    seen = set()
    # Sum of consecutive squares from a^2 to b^2 inclusive
    # precompute prefix sums of squares
    max_a = int(isqrt(limit)) + 1
    
    for a in range(1, max_a):
        s = a * a
        for b in range(a + 1, max_a):
            s += b * b
            if s >= limit:
                break
            if is_pal(s):
                seen.add(s)
    return sum(seen)

if __name__ == "__main__":
    print(solve())
