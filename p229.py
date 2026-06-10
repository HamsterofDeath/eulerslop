#!/usr/bin/env python3
import math

import numpy as np

N = 2_000_000_000


def mark_form(k, n):
    """Return bool array m of size n+1 where m[i] iff i = a^2 + k*b^2, a,b >= 1."""
    cur = np.zeros(n + 1, dtype=bool)
    max_b = math.isqrt((n - 1) // k)
    b = np.arange(1, max_b + 1, dtype=np.int64)
    kb2 = (k * b * b).astype(np.int32)
    a = 1
    while a * a + k <= n:
        a2 = a * a
        m = math.isqrt((n - a2) // k)  # number of valid b for this a
        cur[kb2[:m] + np.int32(a2)] = True
        a += 1
    return cur


def solve(n=N):
    acc = None
    for k in (1, 2, 3, 7):
        cur = mark_form(k, n)
        if acc is None:
            acc = cur
        else:
            acc &= cur
            del cur
    return int(np.count_nonzero(acc))


if __name__ == "__main__":
    print(solve())
