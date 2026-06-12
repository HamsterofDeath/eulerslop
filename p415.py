#!/usr/bin/env python3
"""Project Euler 415: Titanic sets, T(10^11) mod 10^8.

A set is titanic iff some line passes through exactly two of its points.
By Sylvester-Gallai every finite non-collinear set has an ordinary line,
and every 2-point set is titanic, so the NON-titanic sets are exactly:
the empty set, the singletons, and collinear sets of size >= 3.  With
M = (N+1)^2 grid points and f(k) = 2^k - 1 - k - k(k-1)/2,

    T(N) = 2^M - 1 - M - sum over lines L of f(#points on L).

Grouping maximal segments by primitive direction (a,b), a,b>=1 coprime,
a line with k points contributes via second differences h(k)=2^{k-2}-1,
and with d = k-1 the diagonal-line total is 2 * sum_d (2^{d-1}-1) * W(d),
W(d) = sum over coprime a,b with da,db<=N of (N+1-da)(N+1-db).  The map
(d,a,b) -> (x,y)=(da,db) is a bijection onto pairs with d = gcd(x,y), so

    sum_lines f = 2(N+1) f(N+1) + 2*(G - U1),
    U1 = (N(N+1)/2)^2,
    G  = sum_{1<=x,y<=N} (N+1-x)(N+1-y) 2^{gcd(x,y)-1}
       = sum_{t<=N} h(t) S(t)^2,   h = mu * (d -> 2^{d-1}) (Dirichlet),
    S(t) = sum_{a<=N//t} (N+1-ta) = q(N+1) - t*q(q+1)/2,  q = N//t.

S(t)^2 is quadratic in t on blocks of constant q, so G needs prefix sums
H0,H1,H2 of h(t), t h(t), t^2 h(t) at the ~2 sqrt(N) quotient points.
Since h*1 = 2^{n-1}, (t h)*Id = n 2^{n-1}, (t^2 h)*Id^2 = n^2 2^{n-1}
have closed-form prefix sums, a du-sieve recursion over the quotient
lattice works, seeded by a sieved table of h up to K.  All arithmetic is
mod 10^8 (only +,*; the few /2,/6 use scaled moduli 2*10^8, 6*10^8).
"""
import numpy as np
from math import isqrt

MOD = 10 ** 8
MOD2 = 2 * MOD
MOD6 = 6 * MOD
P5 = 312500  # ord(2 mod 5^8); 2^e mod 10^8 is periodic in e with period P5 for e >= 8


def _tri(y):
    # y(y+1)/2 mod MOD for int64 arrays (exact: residues mod 2*MOD keep parity)
    return (y % MOD2) * ((y + 1) % MOD2) % MOD2 // 2


def _sq(y):
    # y(y+1)(2y+1)/6 mod MOD for int64 arrays
    return ((y % MOD6) * ((y + 1) % MOD6) % MOD6) * ((2 * y + 1) % MOD6) % MOD6 // 6


def _sieve_h(K):
    """Return h[0..K] mod MOD with h = mu * (d -> 2^{d-1})."""
    comp = np.ones(K + 1, dtype=bool)
    comp[:2] = False
    for p in range(2, isqrt(K) + 1):
        if comp[p]:
            comp[p * p::p] = False
    primes = np.nonzero(comp)[0]
    mu = np.ones(K + 1, dtype=np.int8)
    mu[0] = 0
    for p in primes.tolist():
        mu[p::p] *= -1
        if p * p <= K:
            mu[p * p::p * p] = 0

    # pw[d] = 2^{d-1} mod MOD
    pw = np.empty(K + 1, dtype=np.int32)
    pw[0] = 0
    top = min(K, 8)
    pw[1:top + 1] = [1 << (d - 1) for d in range(1, top + 1)]
    if K > 8:
        cyc = np.empty(P5, dtype=np.int32)
        c = 256
        for i in range(P5):
            cyc[i] = c
            c = (c << 1) % MOD
        pw[9:] = cyc[(np.arange(9, K + 1) - 9) % P5]

    # h[e*d] += mu(e) * 2^{d-1}: per-e slices for small e, grouped by L=K//e after
    h = np.zeros(K + 1, dtype=np.int64)
    E0 = min(K, int(round((K * K / 2) ** (1.0 / 3))) + 1)
    for e in np.nonzero(mu[:E0 + 1])[0].tolist():
        l = K // e
        if mu[e] == 1:
            h[e::e] += pw[1:l + 1]
        else:
            h[e::e] -= pw[1:l + 1]
    for L in range(1, K // (E0 + 1) + 1):
        lo = max(E0, K // (L + 1))
        hi = K // L
        if hi <= lo:
            continue
        e_arr = np.arange(lo + 1, hi + 1, dtype=np.int64)
        m = mu[e_arr]
        nz = m != 0
        e_arr = e_arr[nz]
        m64 = m[nz].astype(np.int64)
        for d in range(1, L + 1):
            h[e_arr * d] += m64 * int(pw[d])
    h %= MOD
    return h


def solve(N=10 ** 11, K=8_000_000):
    K = min(max(K, isqrt(N) + 1), N)
    h = _sieve_h(K)

    t = np.arange(K + 1, dtype=np.int64)
    Hs0 = (np.cumsum(h) % MOD).astype(np.int64)
    Hs1 = np.cumsum(h * t % MOD) % MOD
    Hs2 = np.cumsum(h * (t * t % MOD) % MOD) % MOD
    del h, t

    # du-sieve: Hj at big quotient points x = N//k > K, k descending.
    # sum_{e<=x} e^j Hj(x//e) = sum_{n<=x} n^j 2^{n-1}  (closed forms below)
    kmax = N // (K + 1)
    Hb0 = np.zeros(kmax + 2, dtype=np.int64)
    Hb1 = np.zeros(kmax + 2, dtype=np.int64)
    Hb2 = np.zeros(kmax + 2, dtype=np.int64)
    for k in range(kmax, 0, -1):
        x = N // k
        if k < kmax and x == N // (k + 1):
            Hb0[k], Hb1[k], Hb2[k] = Hb0[k + 1], Hb1[k + 1], Hb2[k + 1]
            continue
        s = isqrt(x)
        # part 1: individual e in [2, s]; x//e = N//(k*e)
        e1 = np.arange(2, s + 1, dtype=np.int64)
        v1 = x // e1
        big = v1 > K
        nb = ~big
        ib = k * e1[big]
        isml = v1[nb]
        a0 = np.empty(e1.shape, np.int64)
        a1 = np.empty(e1.shape, np.int64)
        a2 = np.empty(e1.shape, np.int64)
        a0[nb] = Hs0[isml]; a0[big] = Hb0[ib]
        a1[nb] = Hs1[isml]; a1[big] = Hb1[ib]
        a2[nb] = Hs2[isml]; a2[big] = Hb2[ib]
        s0 = int((a0 % MOD).sum() % MOD)
        s1 = int((e1 * a1 % MOD).sum() % MOD)
        s2 = int(((e1 * e1 % MOD) * a2 % MOD).sum() % MOD)
        # part 2: group e in [s+1, x] by v = x//e (v <= s <= sqrt(N) <= K)
        v2 = np.arange(1, x // (s + 1) + 1, dtype=np.int64)
        ehi = x // v2
        elo = np.maximum(x // (v2 + 1) + 1, s + 1)
        ok = ehi >= elo
        v2, ehi, elo = v2[ok], ehi[ok], elo[ok]
        cnt = (ehi - elo + 1) % MOD
        se = (_tri(ehi) - _tri(elo - 1)) % MOD
        se2 = (_sq(ehi) - _sq(elo - 1)) % MOD
        s0 += int((cnt * Hs0[v2] % MOD).sum() % MOD)
        s1 += int((se * Hs1[v2] % MOD).sum() % MOD)
        s2 += int((se2 * Hs2[v2] % MOD).sum() % MOD)
        p2 = pow(2, x, MOD)
        Hb0[k] = (p2 - 1 - s0) % MOD
        Hb1[k] = ((x - 1) % MOD * p2 + 1 - s1) % MOD
        Hb2[k] = ((x * x - 2 * x + 3) % MOD * p2 - 3 - s2) % MOD

    # G = sum_t h(t) S(t)^2 over blocks of constant q = N//t; block ends are
    # exactly the quotient points V, S(t)^2 = A - B t + C t^2 on each block.
    sN = isqrt(N)
    ks = np.arange(1, sN + 1, dtype=np.int64)
    V = np.unique(np.concatenate([ks, N // ks]))
    bigV = V > K
    HV0 = np.where(bigV, Hb0[np.where(bigV, N // V, 1)], Hs0[np.where(bigV, 0, V)])
    HV1 = np.where(bigV, Hb1[np.where(bigV, N // V, 1)], Hs1[np.where(bigV, 0, V)])
    HV2 = np.where(bigV, Hb2[np.where(bigV, N // V, 1)], Hs2[np.where(bigV, 0, V)])
    d0 = np.diff(HV0, prepend=np.int64(0)) % MOD
    d1 = np.diff(HV1, prepend=np.int64(0)) % MOD
    d2 = np.diff(HV2, prepend=np.int64(0)) % MOD
    q = N // V
    qm = q % MOD
    np1 = (N + 1) % MOD
    triq = _tri(q)
    A = qm * qm % MOD * (np1 * np1 % MOD) % MOD
    B = 2 * qm % MOD * np1 % MOD * triq % MOD
    C = triq * triq % MOD
    G = int((A * d0 % MOD).sum() - (B * d1 % MOD).sum() + (C * d2 % MOD).sum()) % MOD

    M = (N + 1) ** 2
    U1 = ((N * (N + 1) // 2) % MOD) ** 2 % MOD
    fN1 = (pow(2, N + 1, MOD) - 1 - (N + 1) - N * (N + 1) // 2) % MOD
    line_sum = (2 * (N + 1) * fN1 + 2 * (G - U1)) % MOD
    return (pow(2, M, MOD) - 1 - M - line_sum) % MOD


if __name__ == "__main__":
    print(solve())
