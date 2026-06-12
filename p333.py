#!/usr/bin/env python3
import numpy as np

def solve():
    LIMIT = 10 ** 6

    # Parts are 2^i * 3^j.  Two parts (i1,j1), (i2,j2) with i1 < i2 are
    # divisibility-free iff j1 > j2 (equal i is impossible: one would divide
    # the other).  So a valid partition, listed by increasing i, has strictly
    # decreasing j: a "staircase".  DP over i = 0..19 with state = j of the
    # most recently used part (which is the minimum j so far); a new part
    # (i, j) may follow any state j' > j, or the empty partition.
    JMAX = 12  # 3^13 > 10^6
    ways = [np.zeros(LIMIT, dtype=np.int64) for _ in range(JMAX + 1)]
    empty = np.zeros(LIMIT, dtype=np.int64)
    empty[0] = 1

    i = 0
    while (1 << i) < LIMIT:
        # run = empty + sum of ways[j'] for j' > j, built top-down,
        # using the values from before this i (one part per i at most).
        run = empty.copy()
        pend = [None] * (JMAX + 1)
        for j in range(JMAX, -1, -1):
            v = (1 << i) * 3 ** j
            if v < LIMIT:
                pend[j] = run[:LIMIT - v].copy()
            run += ways[j]
        for j in range(JMAX + 1):
            if pend[j] is not None:
                v = (1 << i) * 3 ** j
                ways[j][v:] += pend[j]
        i += 1

    P = np.zeros(LIMIT, dtype=np.int64)
    for j in range(JMAX + 1):
        P += ways[j]
    assert P[11] == 2 and P[17] == 1

    # Sieve primes below 10^6.
    sieve = np.ones(LIMIT, dtype=bool)
    sieve[:2] = False
    for p in range(2, int(LIMIT ** 0.5) + 1):
        if sieve[p]:
            sieve[p * p::p] = False
    primes = np.nonzero(sieve)[0]

    good = primes[P[primes] == 1]
    assert int(good[good < 100].sum()) == 233  # given check
    return int(good.sum())

if __name__ == "__main__":
    print(solve())
