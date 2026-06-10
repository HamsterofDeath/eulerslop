#!/usr/bin/env python3
from fractions import Fraction

def solve():
    # S_n has vertices at angles (2k-1)*pi/n, so its edge from v_k to v_{k+1}
    # points in direction pi/2 + 2*pi*k/n.  The Minkowski sum of convex
    # polygons has one side per distinct edge direction, so we count the
    # distinct values of k/n (mod 1) over n = 1864..1909, k = 0..n-1
    # (the common pi/2 offset doesn't affect distinctness).
    directions = set()
    for n in range(1864, 1910):
        for k in range(n):
            directions.add(Fraction(k, n))
    return len(directions)

if __name__ == "__main__":
    print(solve())
