"""Project Euler 445: Retractions A.

f(x)=ax+b mod n is a retraction iff a(a-1)=0 and ab=0 mod n. By CRT, per
prime power p^e||n: a=0 or 1 mod p^e; a=1 forces b=0 mod p^e, a=0 leaves b
free (p^e choices). Excluding a=0 mod n gives R(n) = prod(1+p^e) - n.

So sum_{k=1}^{N-1} R(C(N,k)) = sum_k P(k) - (2^N - 2) where
P(k) = prod_p (1 + p^{e_p(C(N,k))}) and e_p = (s_p(k)+s_p(N-k)-s_p(N))/(p-1)
(Legendre). P(k)/P(k-1) only differs at k = 0 or N+1 mod p, so per prime we
mark those event positions with the ratio (vectorized exponent computation
from base-p digit sums), multiply all ratio arrays together (parallel over
primes), then a single prefix product yields all P(k). Symmetry
C(N,k)=C(N,N-k) restricts work to k <= N/2.
"""
import multiprocessing as mp

import numpy as np

MOD = 1_000_000_007
_G = None  # (N, K) in workers


def _init(N, K):
    global _G
    _G = (N, K)


def _dsum(a, p):
    # vectorized base-p digit sum
    a = a.copy()
    s = a % p
    a //= p
    while a.any():
        s += a % p
        a //= p
    return s


def _process(chunk):
    N, K = _G
    r = np.ones(K + 1, np.int64)
    for p in chunk:
        p = int(p)
        sN, t = 0, N
        while t:
            sN += t % p
            t //= p
        # event positions: exponent of p can only change there
        ks = np.arange(p, K + 1, p, dtype=np.int64)  # p | k
        r0 = (N + 1) % p
        if r0:  # p | N+1-k, disjoint from multiples of p
            ks = np.concatenate((ks, np.arange(r0, K + 1, p, dtype=np.int64)))
        # exponents of p in C(N,k) and C(N,k-1) via Legendre digit sums
        e1 = (_dsum(ks, p) + _dsum(N - ks, p) - sN) // (p - 1)
        e0 = (_dsum(ks - 1, p) + _dsum(N + 1 - ks, p) - sN) // (p - 1)
        emax = int(max(e1.max(), e0.max()))
        F = np.ones(emax + 1, np.int64)  # F[e] = 1 + p^e (=1 for e=0)
        pe = 1
        for e in range(1, emax + 1):
            pe *= p  # p^e <= N < MOD (Kummer), exact
            F[e] = 1 + pe
        Finv = np.array([pow(int(x), MOD - 2, MOD) for x in F], np.int64)
        r[ks] = r[ks] * (F[e1] * Finv[e0] % MOD) % MOD
    return r


def solve(N=10**7):
    K = N // 2
    # prime sieve up to N
    sieve = np.ones(N + 1, bool)
    sieve[:2] = False
    for i in range(2, int(N**0.5) + 1):
        if sieve[i]:
            sieve[i * i:: i] = False
    primes = np.nonzero(sieve)[0].astype(np.int64)
    small = primes[primes <= K]
    big = primes[primes > K]  # single event each: e goes 0->1 at k = N+1-p

    W = min(24, mp.cpu_count(), len(small)) or 1
    r = np.ones(K + 1, np.int64)
    with mp.Pool(W, initializer=_init, initargs=(N, K)) as pool:
        for arr in pool.imap_unordered(_process, [small[i::W] for i in range(W)]):
            r = r * arr % MOD
    r[N + 1 - big] = r[N + 1 - big] * (1 + big) % MOD

    # prefix product: P(k) for k=1..K; sum 2*P(1..K-1) + P(K)
    rl = r.tolist()
    acc, S = 1, 0
    for k in range(1, K):
        acc = acc * rl[k] % MOD
        S += acc
    accK = acc * rl[K] % MOD
    return (2 * S + accK - (pow(2, N, MOD) - 2)) % MOD


if __name__ == "__main__":
    print(solve())
