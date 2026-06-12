#!/usr/bin/env python3
from bisect import bisect_right
from math import isqrt

def solve():
    # phi(n^2) = n*phi(n).  For n = prod p^e:
    #   n*phi(n) = prod p^(2e-1) * (p-1),
    # so we need, for every prime p, the total exponent of p in that product
    # to be divisible by 3.  The (p-1) factors only involve primes smaller
    # than p, so build n by choosing prime powers in strictly DECREASING
    # prime order: when prime p is chosen, all contributions to p's exponent
    # from larger primes' (q-1) are already known (residual res mod 3), and
    # the requirement res + 2e - 1 ≡ 0 (mod 3) fixes e ≡ 2 - 2*res (mod 3).
    #
    # The largest prime in n has res = 0, hence e ≡ 2 (mod 3), e >= 2, so all
    # primes dividing n are < sqrt(10^10) = 10^5.  A prime with a nonzero
    # residual MUST be included (with e >= 1); primes with residual 0 may be
    # skipped.  DFS with the residual map as state.
    MAXN = 10 ** 10 - 1
    PLIM = 10 ** 5

    # smallest-prime-factor sieve for factoring p-1
    spf = list(range(PLIM + 1))
    for i in range(2, isqrt(PLIM) + 1):
        if spf[i] == i:
            for j in range(i * i, PLIM + 1, i):
                if spf[j] == j:
                    spf[j] = i
    primes = [i for i in range(2, PLIM + 1) if spf[i] == i]

    def factor(x):
        f = {}
        while x > 1:
            p = spf[x]
            c = 0
            while x % p == 0:
                x //= p
                c += 1
            f[p] = c
        return f

    fact_pm1 = {p: factor(p - 1) for p in primes}
    pindex = {p: i for i, p in enumerate(primes)}

    total = 0

    def dfs(hi, n, r):
        # hi: only primes[0..hi] may still be chosen; r: prime -> residual
        # exponent (mod 3, nonzero) of n*phi(n) accumulated so far.
        nonlocal total
        if not r:
            if n > 1:
                total += n
            lo = -1                      # any remaining prime is optional
        else:
            q = max(r)
            lo = pindex[q]               # cannot skip past the forced prime q
            if lo > hi:
                return                   # forced prime already passed: dead
        j_new = min(hi, bisect_right(primes, isqrt(MAXN // n)) - 1)
        for j in range(max(lo, 0), hi + 1):
            p = primes[j]
            res = r.get(p, 0)
            if res == 0:
                if j > j_new:
                    continue             # needs e>=2 but p^2*n too big
                e = 2
            elif res == 2:
                e = 1
            else:                        # res == 1
                e = 3
            pe = p ** e
            while n * pe <= MAXN:
                r2 = dict(r)
                r2.pop(p, None)
                for fp, fe in fact_pm1[p].items():
                    v = (r2.get(fp, 0) + fe) % 3
                    if v:
                        r2[fp] = v
                    else:
                        r2.pop(fp, None)
                dfs(j - 1, n * pe, r2)
                pe *= p ** 3
    dfs(len(primes) - 1, 1, {})
    return total

if __name__ == "__main__":
    print(solve())
