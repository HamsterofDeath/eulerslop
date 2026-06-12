#!/usr/bin/env python3
"""Project Euler 448: S(99999999019) mod 999999017.

A(n) = (1/n) sum_{i<=n} lcm(n,i).  Grouping i by g = gcd(n,i) and writing
d = n/g gives sum_{i<=n} lcm(n,i) = (n/2)(1 + sum_{d|n} d*phi(d)), so
    A(n) = (1 + sum_{d|n} d*phi(d)) / 2
    S(N) = (N + sum_{d<=N} d*phi(d) * floor(N/d)) / 2.
Let G(x) = sum_{d<=x} d*phi(d).  From m^2 = sum_{d|m} m*phi(d) (m = k*d):
    sum_{m<=x} m^2 = sum_{k<=x} k * G(floor(x/k)),
giving the Du-sieve recursion
    G(x) = P2(x) - sum_{k=2..x} k * G(floor(x/k)),  P2(x) = x(x+1)(2x+1)/6,
evaluated (mod p) at all quotient points floor(N/d) on top of a numpy
phi-sieve up to L, with the inner k-sums done in quotient blocks via numpy.
"""

from math import isqrt

import numpy as np


def compute_S(N, L, p):
    inv2 = pow(2, -1, p)
    inv6 = pow(6, -1, p)

    # --- sieve phi up to L, then dphi[d] = d*phi(d) mod p and its cumsum ---
    phi = np.arange(L + 1, dtype=np.int64)
    comp = np.zeros(L + 1, dtype=bool)
    for i in range(2, isqrt(L) + 1):
        if not comp[i]:
            comp[i * i:: i] = True
    primes = np.nonzero(~comp)[0][2:]  # skip 0 and 1
    for pr in primes:
        pr = int(pr)
        phi[pr::pr] -= phi[pr::pr] // pr
    dphi = phi * np.arange(L + 1, dtype=np.int64)  # <= L^2, fits int64
    dphi %= p
    cum = np.cumsum(dphi)  # 2e7 values < 1e9: fits int64
    cum %= p

    def P2(x):  # sum of squares up to x, mod p
        xm = x % p
        return xm * (xm + 1) % p * (2 * xm + 1) % p * inv6 % p

    def Tm(y):  # triangular numbers mod p, vectorized
        ym = y % p
        return ym * (ym + 1) % p * inv2 % p

    # big[d] will hold G(N // d) for d = 1..D (quotients above L)
    D = N // (L + 1)
    big = np.zeros(D + 1, dtype=np.int64)

    def lookup(vs):  # G at quotient points of N (array)
        res = np.empty_like(vs)
        sm = vs <= L
        res[sm] = cum[vs[sm]]
        bm = ~sm
        res[bm] = big[N // vs[bm]]
        return res

    for d in range(D, 0, -1):  # ascending x, so dependencies are ready
        x = N // d
        r = isqrt(x)
        # part A: k = 2..r individually
        ks = np.arange(2, r + 1, dtype=np.int64)
        sA = int((ks * lookup(x // ks) % p).sum() % p)
        # part B: blocks of constant q = x//k for k >= r+1
        qs = np.arange(1, x // (r + 1) + 1, dtype=np.int64)
        hi = x // qs
        lo = np.maximum(x // (qs + 1) + 1, r + 1)
        w = (Tm(hi) - Tm(lo - 1)) % p  # sum of k over the block, mod p
        sB = int((w * cum[qs] % p).sum() % p)
        big[d] = (P2(x) - sA - sB) % p

    # --- F = sum_{d<=N} d*phi(d) * floor(N/d), in quotient blocks ---
    r = isqrt(N)
    ds = np.arange(1, r + 1, dtype=np.int64)
    F = int((dphi[1: r + 1] * ((N // ds) % p) % p).sum() % p)
    qs = np.arange(1, N // (r + 1) + 1, dtype=np.int64)
    hi = N // qs
    lo1 = np.maximum(N // (qs + 1), r)  # = lo - 1
    F += int((qs * ((lookup(hi) - lookup(lo1)) % p) % p).sum() % p)
    return (N % p + F) % p * inv2 % p


def solve():
    N = 99999999019
    p = 999999017
    return compute_S(N, 2 * 10 ** 7, p)


if __name__ == "__main__":
    print(solve())
