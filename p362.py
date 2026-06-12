#!/usr/bin/env python3
import sys
import math
import numpy as np

def solve():
    # S(n) = sum_{k=2..n} Fsf(k) counts all multisets of squarefree integers
    # >= 2 whose product lies in [2, n], i.e. all non-empty non-decreasing
    # squarefree sequences with product <= n.  Count them recursively:
    #   f(L, m) = #sequences with factors >= m and product <= L
    #           = (Q(L) - Q(m-1))                       (single factor)
    #           + sum_{j squarefree, m <= j <= sqrt(L)} f(L//j, j)
    # where Q(x) = #squarefree numbers <= x.  A child f(L//j, j) has an empty
    # inner loop exactly when j^3 > L (then L//j < j^2), so it collapses to
    # Q(L//j) - Q(j-1); that whole tail over j in (cbrt(L), sqrt(L)] is done
    # vectorized with a Q lookup table (L//j <= L^(2/3) <= 4.7e6 there).
    # Genuine recursion is only needed for j <= cbrt(L).
    N = 10 ** 10
    SQRT_N = math.isqrt(N)       # 10^5: factors in any sequence head
    TAB = 10 ** 7                # direct Q table size

    # squarefree sieve up to TAB and prefix counts Q
    sq = np.ones(TAB + 1, dtype=bool)
    sq[0] = False
    for p in range(2, math.isqrt(TAB) + 1):
        sq[p * p::p * p] = False
    Qtab = np.cumsum(sq, dtype=np.int64)

    # squarefree numbers >= 2 up to sqrt(N), for loops and tail sums
    SF = np.flatnonzero(sq[:SQRT_N + 1]).astype(np.int64)[1:]  # drop 1
    SF_list = [int(v) for v in SF]
    sf_small = sq[:SQRT_N + 1]

    # Moebius values up to sqrt(N) for Q(x) when x > TAB
    mu = np.ones(SQRT_N + 1, dtype=np.int64)
    prim = np.ones(SQRT_N + 1, dtype=bool)
    prim[:2] = False
    for p in range(2, SQRT_N + 1):
        if prim[p]:
            prim[p * p::p] = False
            mu[p::p] *= -1
            mu[p * p::p * p] = 0
    dnz = np.flatnonzero(mu).astype(np.int64)
    dnz2 = dnz * dnz
    munz = mu[dnz]

    def Q(x):
        if x <= TAB:
            return int(Qtab[x])
        k = np.searchsorted(dnz, math.isqrt(x), side="right")
        return int(np.dot(munz[:k], x // dnz2[:k]))

    sys.setrecursionlimit(10000)
    memo = {}

    def f(L, m):
        # non-empty non-decreasing squarefree sequences, factors >= m,
        # product <= L (always called with L >= m >= 2)
        key = (L, m)
        v = memo.get(key)
        if v is not None:
            return v
        res = Q(L) - int(Qtab[m - 1])
        hi = math.isqrt(L)
        if hi >= m:
            t = round(L ** (1.0 / 3.0))
            while t * t * t > L:
                t -= 1
            while (t + 1) ** 3 <= L:
                t += 1
            # tail: children with j^3 > L are pure squarefree counts
            lo = max(t + 1, m)
            if lo <= hi:
                i0 = np.searchsorted(SF, lo)
                i1 = np.searchsorted(SF, hi, side="right")
                js = SF[i0:i1]
                res += int(np.sum(Qtab[L // js], dtype=np.int64)
                           - np.sum(Qtab[js - 1], dtype=np.int64))
            # head: real recursion for j <= cbrt(L)
            for j in range(m, min(t, hi) + 1):
                if sf_small[j]:
                    res += f(L // j, j)
        memo[key] = res
        return res

    return f(N, 2)

if __name__ == "__main__":
    print(solve())
