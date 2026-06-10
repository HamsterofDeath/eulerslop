#!/usr/bin/env python3
import numpy as np


def solve():
    MOD = 10**16

    # Primes below 5000 (the set S).
    limit = 5000
    sieve = np.ones(limit, dtype=bool)
    sieve[:2] = False
    for i in range(2, int(limit**0.5) + 1):
        if sieve[i]:
            sieve[i * i::i] = False
    primes = np.flatnonzero(sieve)

    max_sum = int(primes.sum())

    # counts[s] = number of subsets of S with sum s, modulo 10^16.
    # int64 is safe: values stay < 10^16 and a single addition of two
    # such values is < 2 * 10^16 < 2^63.
    counts = np.zeros(max_sum + 1, dtype=np.int64)
    counts[0] = 1
    reached = 0
    for p in primes:
        p = int(p)
        reached += p
        counts[p:reached + 1] += counts[:reached + 1 - p]
        counts[p:reached + 1] %= MOD

    # Sieve up to max_sum to find which sums are prime.
    big = np.ones(max_sum + 1, dtype=bool)
    big[:2] = False
    for i in range(2, int(max_sum**0.5) + 1):
        if big[i]:
            big[i * i::i] = False

    # Sum with Python ints to avoid int64 overflow in the reduction.
    total = sum(int(c) for c in counts[big]) % MOD
    return total


if __name__ == "__main__":
    print(solve())
