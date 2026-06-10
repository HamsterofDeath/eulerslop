#!/usr/bin/env python3
# P(n): convex lattice polygons with integer edge lengths, no three vertices
# collinear, perimeter <= n, counted up to translation.
#
# Up to translation, a convex polygon with no three collinear vertices is exactly
# a finite set of edge vectors with pairwise distinct directions summing to zero
# (sort the vectors by angle to reconstruct the polygon uniquely).  An edge vector
# must have integer length, so its direction is a primitive vector (a,b) with
# a^2+b^2 a perfect square: the 4 axis directions or one of the 8 sign/swap
# variants of a primitive Pythagorean triple leg pair.  For each direction at most
# one edge k*(a,b) (k >= 1, k*hyp <= n) may be used.
#
# DP over directions with numpy: state = (perimeter, sum_x, sum_y), counting the
# number of subsets reaching that state.  Answer = subsets with sum zero and
# perimeter in [1, n], minus degenerate subsets of size 2 (pairs {v, -v}); subsets
# of size 0/1 with zero sum other than the empty set cannot occur.

import numpy as np
from math import gcd


def directions(n):
    """All (dx, dy, length) usable primitive directions for perimeter limit n."""
    dirs = [(1, 0, 1), (-1, 0, 1), (0, 1, 1), (0, -1, 1)]
    # primitive Pythagorean triples with hypotenuse <= n
    m = 2
    while m * m + 1 <= n:
        for k in range(1 if m % 2 == 0 else 2, m, 2):
            if gcd(m, k) == 1:
                a, b, c = m * m - k * k, 2 * m * k, m * m + k * k
                if c <= n:
                    for sa in (a, -a):
                        for sb in (b, -b):
                            dirs.append((sa, sb, c))
                            dirs.append((sb, sa, c))
        m += 1
    return dirs


def count(n):
    dirs = directions(n)
    OFF = n  # coordinate offset; any partial sum component lies in [-n, n]
    size = 2 * n + 1
    A = np.zeros((n + 1, size, size), dtype=np.int64)
    A[0, OFF, OFF] = 1

    for dx, dy, L in dirs:
        B = A.copy()
        kmax = n // L
        for k in range(1, kmax + 1):
            sx, sy, sp = k * dx, k * dy, k * L
            # B[p, x, y] += A[p - sp, x - sx, y - sy]
            dstx = slice(max(0, sx), size + min(0, sx))
            srcx = slice(max(0, -sx), size - max(0, sx))
            dsty = slice(max(0, sy), size + min(0, sy))
            srcy = slice(max(0, -sy), size - max(0, sy))
            B[sp:, dstx, dsty] += A[:n + 1 - sp, srcx, srcy]
        A = B

    total = int(A[1:, OFF, OFF].sum())
    # subtract degenerate 2-gons {v, -v}: one per direction pair and multiple k
    degen = sum((n // (2 * L)) for (dx, dy, L) in dirs) // 2
    return total - degen


def solve():
    return count(120)


if __name__ == "__main__":
    print(solve())
