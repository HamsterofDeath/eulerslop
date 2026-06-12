#!/usr/bin/env python3
from collections import defaultdict
from math import gcd

def solve():
    # Crossed ladders: with street width w, the ladders reach heights
    # p = sqrt(x^2 - w^2) and q = sqrt(y^2 - w^2) on the walls, and the
    # crossing height satisfies 1/h = 1/p + 1/q, i.e. h = pq/(p+q).
    # For x, y, h, w all integers, (w, p, x) and (w, q, y) must be Pythagorean
    # triples sharing the leg w.  So: generate every Pythagorean triple with
    # hypotenuse < 10^6, group the "height" legs by the shared leg w, and for
    # each pair of heights p < q on the same w count when (p+q) | pq.
    N = 1000000
    by_leg = defaultdict(list)
    m = 2
    while m * m + 1 < N:
        for n in range(1 + (m & 1), m, 2):  # opposite parity
            z = m * m + n * n
            if z >= N:
                break
            if gcd(m, n) != 1:
                continue
            u, v = m * m - n * n, 2 * m * n
            for k in range(1, (N - 1) // z + 1):
                by_leg[k * u].append(k * v)
                by_leg[k * v].append(k * u)
        m += 1

    count = 0
    for heights in by_leg.values():
        L = len(heights)
        if L < 2:
            continue
        for i in range(L - 1):
            p = heights[i]
            for j in range(i + 1, L):
                q = heights[j]
                if (p * q) % (p + q) == 0:
                    count += 1
    return count

if __name__ == "__main__":
    print(solve())
