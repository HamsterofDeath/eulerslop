#!/usr/bin/env python3
import math
import numpy as np

MOD = 10 ** 9  # last 9 digits


def solve():
    # S(n,m) = sum_{i<=m} phi(n*i).  For p not dividing n, splitting i by
    # divisibility by p (phi(pa) = (p-1)phi(a) if p∤a, p*phi(a) if p|a) gives
    #   S(pn, m) = (p-1) S(n, m) + S(pn, floor(m/p))
    # which unrolls to S(pn, m) = (p-1) * sum_{j>=0} S(n, floor(m/p^j)).
    # Peeling the 7 primes of 510510 = 2*3*5*7*11*13*17 reduces everything to
    # S(1, x) = Phi(x), the totient summatory, at nested-quotient arguments.
    X = 10 ** 11
    L = 4 * 10 ** 7  # sieve limit ~ X^(2/3)

    # ---- phi prefix sums up to L (numpy sieve) ----
    phi = np.arange(L + 1, dtype=np.int32)
    rem = np.arange(L + 1, dtype=np.int32)
    r = math.isqrt(L)
    sieve = np.ones(r + 1, dtype=bool)
    sieve[:2] = False
    for p in range(2, math.isqrt(r) + 1):
        if sieve[p]:
            sieve[p * p::p] = False
    for p in np.nonzero(sieve)[0].tolist():
        phi[p::p] -= phi[p::p] // p
        pp = p
        while pp <= L:
            rem[pp::pp] //= p
            pp *= p
    # rem[m] is now 1 or the single prime factor of m exceeding sqrt(L)
    mask = rem > 1
    phi[mask] = phi[mask] // rem[mask] * (rem[mask] - 1)
    del rem, mask
    pref = np.cumsum(phi, dtype=np.int64)
    del phi
    pref %= MOD

    # ---- Phi at the large quotient values X//k via Du-style recursion ----
    # Phi(v) = v(v+1)/2 - sum_{i=2..v} Phi(v//i), grouped over equal quotients;
    # computed in increasing v so all larger-index chain values are ready.
    cache = {}
    KX = X // (L + 1)
    for k in range(KX, 0, -1):
        v = X // k
        if v in cache:
            continue
        s = math.isqrt(v)
        K = v // (L + 1)  # i <= K  <=>  v//i > L (then K <= s since v < (L+1)^2)
        tot = 0
        for i in range(2, K + 1):          # huge quotients: from cache
            tot += cache[v // i]
        if K + 1 <= s:                      # i in [K+1, s]: quotient <= L
            iarr = np.arange(K + 1, s + 1, dtype=np.int64)
            tot += int(pref[v // iarr].sum() % MOD)
        qmax = v // (s + 1)                 # i in [s+1, v] grouped by q = v//i
        d = np.arange(1, qmax + 1, dtype=np.int64)
        cnt = v // d - np.maximum(v // (d + 1), s)
        tot += int(((cnt % MOD) * pref[d] % MOD).sum() % MOD)
        cache[v] = (v * (v + 1) // 2 - tot) % MOD

    def big_phi(m):
        return int(pref[m]) if m <= L else cache[m]

    # ---- peel the 7 primes (2 outermost so the widest level uses 17) ----
    peel = [17, 13, 11, 7, 5, 3, 2]
    memos = [None] + [{} for _ in range(7)]

    def F(k, m):  # S(product of peel[:k] reversed... any order, set is what counts)
        if k == 0:
            return big_phi(m)
        d = memos[k]
        got = d.get(m)
        if got is not None:
            return got
        p = peel[k - 1]
        t, tot = m, 0
        while t:
            tot += F(k - 1, t)
            t //= p
        res = (p - 1) * tot % MOD
        d[m] = res
        return res

    # self-check from the statement: S(510510, 10^6) = 45480596821125120
    assert F(7, 10 ** 6) == 45480596821125120 % MOD

    return F(7, X)


if __name__ == "__main__":
    print(solve())
