#!/usr/bin/env python3
from math import comb


def _sum_int(a, b):
    if b < a:
        return 0
    return (a + b) * (b - a + 1) // 2


def _fix_identity(limit):
    total = 0
    t = 0
    while 6 + 3 * t <= limit:
        m = (limit - 6 - 3 * t) // 2
        total += (1 if t == 0 else 2) * comb(m + 3, 3)
        t += 1
    return total


def _fix_rot60(limit):
    return limit // 6


def _fix_rot120(limit):
    m = limit // 3
    return m * (m - 1) // 2 if m >= 2 else 0


def _fix_rot180(limit):
    m = limit // 2
    return comb(m, 3) if m >= 3 else 0


def _fix_ref_vertex(limit):
    # Side pattern a,b,a,a,b,a has perimeter 4a+2b.
    m = limit // 2
    amax = m // 2
    return amax * m - amax * (amax + 1)


def _fix_ref_edge(limit):
    # Side pattern a,b,c,d,c,b.  Closure gives d=a+b-c, so
    # c < a+b and 2a+3b+c <= limit.
    total = 0
    for b in range(1, (limit - 3) // 3 + 1):
        u = limit - 3 * b
        amax = (u - 1) // 2
        split = (limit - 4 * b + 1) // 3

        left = min(split, amax)
        if left >= 1:
            total += _sum_int(1, left) + (b - 1) * left

        lo = max(1, split + 1)
        if lo <= amax:
            total += u * (amax - lo + 1) - 2 * _sum_int(lo, amax)
    return total


def H(limit):
    # Burnside over D_6 acting on the six side lengths.  Labeled closure is
    # encoded by a-c-d+f = 0 and b+c-e-f = 0 in axial coordinates.
    return (
        _fix_identity(limit)
        + 2 * _fix_rot60(limit)
        + 2 * _fix_rot120(limit)
        + _fix_rot180(limit)
        + 3 * _fix_ref_vertex(limit)
        + 3 * _fix_ref_edge(limit)
    ) // 12


def solve():
    assert H(6) == 1
    assert H(12) == 10
    assert H(100) == 31248
    return H(55106)


if __name__ == "__main__":
    print(solve())
