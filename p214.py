#!/usr/bin/env python3
import numpy as np

def solve():
    limit = 40000000
    target_len = 25

    # Sieve of Euler's totient: phi[n] starts as n; for each prime p,
    # multiply every multiple by (1 - 1/p) via phi -= phi // p.
    phi = np.arange(limit, dtype=np.int32)
    for p in range(2, limit):
        if phi[p] == p:  # p is prime (untouched so far)
            phi[p::p] -= phi[p::p] // p

    # chain[n] = length of the totient chain n, phi(n), ..., 1.
    # chain[n] = chain[phi[n]] + 1 with phi[n] < n, so process blocks in
    # increasing order; within a block iterate until all values resolve
    # (dependency depth inside a block is tiny: phi(odd) is even and
    # phi(even m) <= m/2).
    chain = np.zeros(limit, dtype=np.int8)
    chain[1] = 1
    block = 1 << 20
    for lo in range(2, limit, block):
        hi = min(lo + block, limit)
        f = phi[lo:hi]
        sub = chain[lo:hi]
        while True:
            c = chain[f]
            mask = (sub == 0) & (c > 0)
            if not mask.any():
                break
            sub[mask] = c[mask] + 1

    # Primes p satisfy phi[p] == p - 1.
    candidates = np.flatnonzero(chain == target_len)
    is_prime = phi[candidates] == candidates - 1
    return int(candidates[is_prime].sum(dtype=np.int64))

if __name__ == "__main__":
    print(solve())
