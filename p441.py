#!/usr/bin/env python3
import numpy as np
from math import fsum, log


def solve():
    # A coprime pair p < q contributes 1/(pq) to R(M) exactly for
    # q <= M <= min(p+q, N), i.e. with weight min(p+q, N) - q + 1.  Hence
    #   S(N) = sum_{p+q<=N} (1/q + 1/(pq)) + sum_{q<=N<p+q} (N-q+1)/(pq)
    # over coprime p < q.  Mobius inversion over g = gcd(p,q) turns each part
    # into sums over d of mu(d)/d^k times unrestricted double sums up to
    # K = floor(N/d), which collapse via harmonic sums.  With
    # H(n) = sum 1/i, Q(n) = sum 1/i^2 one gets the exact identities
    #   sum_{p<q<=K} 1/(pq)              = (H(K)^2 - Q(K)) / 2
    #   sum_{p<q<=K, p+q>K} 1/(pq)       = Q(floor(K/2)) / 2
    #   sum_{p+q<=K} 1/q - sum_{p<q<=K, p+q>K} 1/p = -H(floor(K/2))
    # (the last after the K*(H-difference) terms cancel), so with h = K//2:
    #   S(N) = sum_d mu(d) * [ -H(h)/d + (H(K)^2 - Q(K) + N*Q(h)) / (2 d^2) ].
    # Group d by the ~2*sqrt(N) distinct values of K = N//d.
    N = 10 ** 7
    GAMMA = 0.5772156649015328606065120900824024310421593359399
    ZETA2 = 1.6449340668482264364724151666460251892189499012068

    # exact small values; asymptotic expansions beyond (error < 1e-16 there)
    SMALL = 2000
    H_small = np.concatenate([[0.0], np.cumsum(1.0 / np.arange(1, SMALL + 1))])
    Q_small = np.concatenate([[0.0], np.cumsum(1.0 / np.arange(1, SMALL + 1) ** 2)])

    def H(x):
        if x <= SMALL:
            return float(H_small[x])
        t = float(x)
        return (log(t) + GAMMA + 1 / (2 * t) - 1 / (12 * t * t)
                + 1 / (120 * t ** 4) - 1 / (252 * t ** 6))

    def Q(x):  # sum_{i<=x} 1/i^2 = zeta(2) - trigamma(x+1)
        if x <= SMALL:
            return float(Q_small[x])
        z = float(x) + 1.0
        return ZETA2 - (1 / z + 1 / (2 * z * z) + 1 / (6 * z ** 3)
                        - 1 / (30 * z ** 5) + 1 / (42 * z ** 7))

    # Mobius function by sieve
    mu = np.ones(N + 1, dtype=np.int8)
    sieve = np.ones(N + 1, dtype=bool)
    sieve[:2] = False
    for p in range(2, int(N ** 0.5) + 1):
        if sieve[p]:
            sieve[p * p::p] = False
    primes = np.nonzero(sieve)[0]
    for p in primes:
        mu[p::p] *= -1
    for p in primes[primes.astype(np.int64) ** 2 <= N]:
        mu[p * p::p * p] = 0
    mu[0] = 0

    dv = np.arange(N + 1, dtype=np.float64)
    dv[0] = 1.0
    mud1 = mu / dv          # mu(d)/d
    mud2 = mud1 / dv        # mu(d)/d^2

    parts = []
    d1 = 1
    while d1 <= N:
        K = N // d1
        d2 = N // K
        h = K // 2
        s1 = float(mud1[d1:d2 + 1].sum())
        s2 = float(mud2[d1:d2 + 1].sum())
        HK = H(K)
        parts.append(-H(h) * s1 + (HK * HK - Q(K) + N * Q(h)) * 0.5 * s2)
        d1 = d2 + 1
    return f"{fsum(parts):.4f}"


if __name__ == "__main__":
    print(solve())
