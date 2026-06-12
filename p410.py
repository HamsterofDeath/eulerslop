#!/usr/bin/env python3
# Project Euler 410: circle tangents through P(a,b), Q(-a,c).
#
# Tangency of line PQ to x^2+y^2=r^2 gives a^2(b+c)^2 = r^2((b-c)^2 + 4a^2).
# With s=b+c, d=b-c (s=d mod 2), g=gcd(a,r), a=g*alpha, r=g*rho (coprime),
# coprimality forces s=rho*sigma, d=alpha*delta, reducing to sigma^2-delta^2=4g^2,
# i.e. factorizations m*n=g^2 via sigma=m+n, delta=n-m.  Counting solutions with
# the parity constraint rho*sigma = alpha*delta (mod 2) gives per-(a,r) counts:
#   alpha,rho both odd:        2*tau(g^2)
#   mixed parity, g odd:       2*tau(g^2)
#   mixed parity, g even:      2*tau((g/2)^2)
# Summing over a<=X, r<=R and collapsing the gcd/Moebius double sums via
# Dirichlet convolution (tau(g^2) conv mu = 2^omega) yields, with Odd(t)=ceil(t/2):
#   F(R,X) = 2*sum_{m odd} 2^omega(m) (R//m)(X//m)
#          + 4*sum_{v>=2} sum_{m odd} 2^omega(m) (R//(2^v m))(X//(2^v m))
#          + 4*sum_{v>=1} sum_{m odd} 2^omega(m) Odd(R//(2^v m)) Odd(X//(2^v m))
# Validated against brute force for F(1,5)=10, F(2,10)=52, F(10,100)=3384.

import numpy as np
from math import isqrt


def omega_odd(M):
    # w[i] = number of distinct prime factors of m = 2i+1, for odd m <= M
    n = (M + 1) // 2
    sieve = np.ones(n, dtype=bool)
    sieve[0] = False
    for i in range(1, (isqrt(M) + 1) // 2 + 1):
        if sieve[i]:
            p = 2 * i + 1
            sieve[(p * p) // 2::p] = False
    primes = 2 * np.flatnonzero(sieve).astype(np.int64) + 1
    del sieve
    w = np.zeros(n, dtype=np.uint8)
    KMAX = 64
    cut = M // (2 * KMAX + 1)
    for p in primes[primes <= cut].tolist():
        w[(p - 1) // 2::p] += 1  # odd multiples of p sit at index (p-1)/2 step p
    for k in range(1, KMAX + 1):
        # primes with exactly k odd multiples <= M: p in (M/(2k+1), M/(2k-1)]
        ps = primes[(primes > max(M // (2 * k + 1), cut)) & (primes <= M // (2 * k - 1))]
        if len(ps) == 0:
            continue
        base = (ps - 1) // 2
        for j in range(k):
            w[base + j * ps] += 1  # indices unique for fixed j
    return w


CHUNK = 1 << 22


def T(A, B, w, oddq):
    # sum over odd m <= min(A,B) of 2^omega(m) * f(A//m) * f(B//m),
    # f = identity or Odd(t) = (t+1)//2
    n = (min(A, B) + 1) // 2
    total = 0
    for i0 in range(0, n, CHUNK):
        i1 = min(i0 + CHUNK, n)
        m = (np.arange(i0, i1, dtype=np.int64) << 1) + 1
        qa = A // m
        qb = B // m
        if oddq:
            qa += 1; qa >>= 1
            qb += 1; qb >>= 1
        wt = np.int64(1) << w[i0:i1].astype(np.int64)
        total += int((wt * qa * qb).sum())
    return total


def F(R, X, w):
    total = 2 * T(R, X, w, False)
    v = 2
    while (R >> v) and (X >> v):
        total += 4 * T(R >> v, X >> v, w, False)
        v += 1
    v = 1
    while (R >> v) and (X >> v):
        total += 4 * T(R >> v, X >> v, w, True)
        v += 1
    return total


def solve():
    w = omega_odd(10**8)
    assert F(1, 5, w) == 10 and F(2, 10, w) == 52 and F(10, 100, w) == 3384
    return F(10**8, 10**9, w) + F(10**9, 10**8, w)


if __name__ == "__main__":
    print(solve())
