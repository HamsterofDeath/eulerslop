#!/usr/bin/env python3
import sys
import numpy as np


def solve(limit=10**8):
    # By the de Bruijn-Tengbergen-Kruyswijk theorem the divisor lattice of n
    # (a product of chains of lengths e_i) has its maximum antichain at the
    # middle rank: N(n) = #{d | n : Omega(d) = floor(E/2)}, E = sum of the
    # exponents e_i of n.  So N(n) = [x^(E//2)] prod_i (1 + x + ... + x^e_i),
    # which depends only on the multiset of exponents (the prime signature).
    #
    # Enumerate all n <= limit by DFS over primes in increasing order with
    # their exponents.  A state only needs to branch on primes p with
    # p^2 <= limit/value or p*nextprime(p) <= limit/value; all larger primes
    # can only appear once, as the final factor, and are counted in bulk via
    # the prime counting function pi.

    sieve = np.ones(limit + 1, dtype=bool)
    sieve[:2] = False
    for i in range(2, int(limit**0.5) + 1):
        if sieve[i]:
            sieve[i * i::i] = False

    # primes needed for explicit branching: up to sqrt(limit) (plus one more
    # for the nextprime lookahead)
    primes = [int(p) for p in np.nonzero(sieve[: int(limit**0.5) + 1000])[0]]

    # blocked prefix sums for pi(x) queries
    BLK = 1 << 15
    nblk = (limit + BLK) // BLK
    padded = np.zeros(nblk * BLK, dtype=bool)
    padded[: limit + 1] = sieve
    blocks = padded.reshape(nblk, BLK).sum(axis=1)
    pre = np.concatenate(([0], np.cumsum(blocks)))  # primes below b*BLK

    def pi(x):
        b = x >> 15
        return int(pre[b]) + int(np.count_nonzero(padded[b << 15: x + 1]))

    # N(signature): coefficient of x^(E//2) in prod (1 + ... + x^e)
    memo = {}

    def nval(sig):
        v = memo.get(sig)
        if v is None:
            poly = [1]
            for e in sig:
                new = [0] * (len(poly) + e)
                for i, c in enumerate(poly):
                    for j in range(e + 1):
                        new[i + j] += c
                poly = new
            v = poly[sum(sig) // 2]
            memo[sig] = v
        return v

    sys.setrecursionlimit(10000)

    def rec(value, t0, sig):
        # contribution of n = value plus all n = value * (primes with index
        # >= t0, each larger than any prime already in value)
        res = nval(sig)
        hi = limit // value
        t = t0
        while True:
            p = primes[t]
            if p > hi:
                break
            if p * p > hi and p * primes[t + 1] > hi:
                # every prime q with p <= q <= hi yields the leaf n = value*q
                # (exponent 1, no further extension possible): bulk count
                c = pi(hi) - t
                if c > 0:
                    res += c * nval(tuple(sorted(sig + (1,))))
                break
            v = value * p
            e = 1
            while v <= limit:
                res += rec(v, t + 1, tuple(sorted(sig + (e,))))
                v *= p
                e += 1
            t += 1
        return res

    return rec(1, 0, ())


if __name__ == "__main__":
    print(solve())
