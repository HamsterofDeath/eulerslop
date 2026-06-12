#!/usr/bin/env python3
import numpy as np
from math import isqrt

P = 10**9


def _tmod(x):
    # T(x) = x*(x+1)/2 mod P; works on int64 arrays/scalars with x <= ~1e11
    # (reduce mod 2P first so the product stays below 2^63).
    a = x % (2 * P)
    b = (x + 1) % (2 * P)
    return (a * b % (2 * P)) // 2


def euler_s(N):
    # sigma(mn) = sum_{d | gcd(m,n)} mu(d)*d*sigma(m/d)*sigma(n/d), hence
    #   S(N) = sum_{d<=N} mu(d)*d * D(N//d)^2,  D(x) = sum_{k<=x} sigma(k).
    # Sieve D(x) and M1(x) = sum_{d<=x} mu(d)*d for x <= V ~ N^(2/3); above V
    # evaluate D by the O(sqrt x) hyperbola sum and M1 by the memoized
    # quotient-blocked recursion M1(x) = 1 - sum_{e=2..x} e*M1(x//e)
    # (from (mu*id) * id = unit). All arithmetic mod P = 1e9.
    V = min(N, max(isqrt(N) + 1, int(round(N ** (2.0 / 3.0)))))
    Dmax = N // (V + 1)  # exactly the d' with N//d' > V

    # --- Moebius sieve up to V -> Msmall[x] = M1(x) mod P ---
    mu = np.ones(V + 1, dtype=np.int8)
    pprod = np.ones(V + 1, dtype=np.int64)
    sv = isqrt(V)
    isp = np.ones(sv + 1, dtype=bool)
    isp[: min(2, sv + 1)] = False
    for i in range(2, isqrt(sv) + 1):
        if isp[i]:
            isp[i * i :: i] = False
    for pr in np.nonzero(isp)[0]:
        pr = int(pr)
        mu[pr::pr] *= -1
        mu[pr * pr :: pr * pr] = 0
        pprod[pr::pr] *= pr
    ar = np.arange(V + 1, dtype=np.int64)
    leftover = pprod != ar  # one extra prime factor > sqrt(V) remains
    del pprod
    mu[leftover] *= -1
    del leftover
    f = mu.astype(np.int64)
    del mu
    f *= ar  # f[d] = mu(d)*d, |sum| < V^2 fits int64
    del ar
    np.cumsum(f, out=f)
    f %= P
    Msmall = f

    # --- sigma sieve up to V -> Dsmall[x] = D(x) mod P ---
    sig = np.zeros(V + 1, dtype=np.int64)
    K = min(V, 80000)
    for k in range(1, K + 1):  # divisor k added to all its multiples
        sig[k::k] += k
    if V > K:
        # group k > K by j = V//k (number of multiples), vectorize over k
        for j in range(1, V // (K + 1) + 1):
            klo = max(K + 1, V // (j + 1) + 1)
            khi = V // j
            if klo > khi:
                continue
            kv = np.arange(klo, khi + 1, dtype=np.int64)
            for m in range(1, j + 1):
                sig[m * klo : m * khi + 1 : m] += kv
    np.cumsum(sig, out=sig)  # max ~0.82*V^2 fits int64
    sig %= P
    Dsmall = sig

    # --- big tables at x = N//d' > V, indexed by d' (increasing x order) ---
    M1big = np.zeros(Dmax + 1, dtype=np.int64)
    Dbig = np.zeros(Dmax + 1, dtype=np.int64)
    for dp in range(Dmax, 0, -1):
        v = N // dp
        s = isqrt(v)
        a = np.arange(1, s + 1, dtype=np.int64)
        q = v // a
        # D(v) = sum_{a<=s} T(v//a) + sum_{b<=s} b*(v//b) - s*T(s)
        t1 = int(np.sum(_tmod(q)))
        t2 = int(np.sum(a * (q % P) % P))
        Dbig[dp] = (t1 + t2 - (s % P) * int(_tmod(np.int64(s)))) % P
        # M1(v) = 1 - sum_{e=2..s} e*M1(v//e) - sum over quotient blocks e>s
        ks, qs = a[1:], q[1:]  # e = 2..s and v//e; note v//e = N//(dp*e)
        vals = np.where(
            qs <= V,
            Msmall[np.minimum(qs, V)],
            M1big[np.minimum(dp * ks, Dmax)],  # dp*e <= Dmax whenever q > V
        )
        part1 = int(np.sum(ks * vals % P))
        q2 = np.arange(1, v // (s + 1) + 1, dtype=np.int64)  # quotients <= s
        hi = v // q2
        lo = np.maximum(v // (q2 + 1) + 1, s + 1)
        tsum = (_tmod(hi) - _tmod(lo - 1)) % P  # sum of e over the block
        part2 = int(np.sum(Msmall[q2] * tsum % P))
        M1big[dp] = (1 - part1 - part2) % P

    # --- final sum over distinct quotients v = N//d ---
    sq = isqrt(N)
    vs = np.concatenate(
        [
            np.arange(1, sq + 1, dtype=np.int64),
            N // np.arange(1, N // (sq + 1) + 1, dtype=np.int64),
        ]
    )

    def m1_at(t):  # t entries are of the form N//k (or 0)
        ts = np.maximum(t, 1)
        if Dmax > 0:
            bigv = M1big[np.minimum(N // ts, Dmax)]
        else:
            bigv = np.zeros_like(t)
        return np.where(t <= V, Msmall[np.minimum(t, V)], bigv)

    diff = (m1_at(N // vs) - m1_at(N // (vs + 1))) % P  # sum of mu(d)d in block
    if Dmax > 0:
        dvbig = Dbig[np.minimum(N // vs, Dmax)]
    else:
        dvbig = np.zeros_like(vs)
    dv = np.where(vs <= V, Dsmall[np.minimum(vs, V)], dvbig)
    return int(np.sum(diff * (dv * dv % P) % P) % P)


def solve():
    return euler_s(10**11)


if __name__ == "__main__":
    print(solve())
