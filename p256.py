#!/usr/bin/env python3
import numpy as np
from math import isqrt

# Tatami tilings of an a x b room (a <= b, ab even) are extremely rigid: they
# split into k vertical "bands" whose widths are confined between a-1 and a+1.
# Verified by an exhaustive profile DP for all a <= 14, the room is tileable iff
#   a odd : exists k >= 0 with k(a-1) <= b <= k(a+1)        (b is even here)
#   a even: exists k >= 0 with k(a-1)-1 <= b <= k(a+1)+1
# (for even a the bands at the two walls may be one column wider/narrower).
#
# Hence the tatami-free b for a given a form explicit gap intervals between
# consecutive tileable windows (window k ends at k(a+1)(+1), window k+1 starts
# at (k+1)(a-1)(-1)):
#   a odd : even b in [k(a+1)+2, (k+1)(a-1)-2],   1 <= 2k <= a-5
#   a even: all  b in [k(a+1)+2, (k+1)(a-1)-2],   1 <= 2k <= a-5
# The smallest free room is 7x10, consistent with the problem statement.
#
# Sieve: for every a, generate all free b <= S/a, increment T[a*b]; then take
# the smallest s with T(s) == 200.  Free-pair density is ~S/(2a) per a, about
# 1.3e8 increments at S = 1e8, done with vectorised fancy indexing (indices
# within one batch are distinct since b values are distinct for fixed a).


def smallest_with(target, S):
    T = np.zeros(S + 1, dtype=np.int16)
    for a in range(7, isqrt(S) + 1):
        X = S // a            # b <= X
        step = 2 if a % 2 else 1
        pieces = []
        for k in range(1, (a - 5) // 2 + 1):
            lo = k * (a + 1) + 2          # even when a is odd
            if lo > X:
                break
            hi = min((k + 1) * (a - 1) - 2, X)
            if lo <= hi:
                pieces.append(np.arange(lo, hi + 1, step, dtype=np.int64))
        if pieces:
            b = np.concatenate(pieces)
            T[a * b] += 1
    hit = np.flatnonzero(T == target)
    return int(hit[0]) if hit.size else None


def solve():
    S = 100_000_000
    while True:
        s = smallest_with(200, S)
        if s is not None:
            return s
        S *= 2


if __name__ == "__main__":
    print(solve())
