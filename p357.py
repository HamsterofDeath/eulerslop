#!/usr/bin/env python3
from math import isqrt

import numpy as np


def solve():
    # For every divisor d of n, d + n/d must be prime.  Divisor pairs (d, n/d)
    # give the same sum, so it suffices to check all d <= sqrt(n).  The pair
    # d = 1 forces n + 1 prime, so candidates are n = p - 1 for primes p.
    # The remaining checks are vectorized: for each d = 2..sqrt(N), among the
    # surviving candidates divisible by d (with d <= sqrt(n)), keep only those
    # where d + n/d is prime.  Each check eliminates ~all multiples of d, so
    # the candidate array collapses quickly (d = 2 alone kills ~94%).
    N = 10 ** 8

    sieve = np.ones(N + 2, dtype=bool)
    sieve[:2] = False
    for i in range(2, isqrt(N + 1) + 1):
        if sieve[i]:
            sieve[i * i:: i] = False

    cand = np.flatnonzero(sieve).astype(np.int64) - 1  # n with n + 1 prime

    for d in range(2, isqrt(N) + 1):
        idx = np.flatnonzero((cand % d == 0) & (cand >= d * d))
        if idx.size:
            bad = idx[~sieve[cand[idx] // d + d]]
            if bad.size:
                keep = np.ones(cand.size, dtype=bool)
                keep[bad] = False
                cand = cand[keep]

    return int(cand.sum())


if __name__ == "__main__":
    print(solve())
