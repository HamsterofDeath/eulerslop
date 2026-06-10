#!/usr/bin/env python3
import numpy as np
from math import isqrt

# Cardano triplets: cbrt(a+b*sqrt(c)) + cbrt(a-b*sqrt(c)) = 1.
# Cubing s=1 gives  a^2 - b^2 c = ((1-2a)/3)^3, i.e.  27 b^2 c = (a+1)^2 (8a-1),
# which forces a = 3m-1, reducing to:    b^2 c = m^2 (8m - 3).
# Write 8m-3 = q^2 r with r squarefree.  Then b^2 | m^2 q^2 r forces b | m*q,
# so with D = m*q/b every divisor D of m*q gives one triplet:
#     a = 3m-1,  b = m*q/D,  c = D^2 r,   need  a + b + c <= N.
#
# Counting (m, D) pairs:
#  * m is bounded: min over real b of b + K/b^2 (K = m^2(8m-3)) is
#    1.5*(2K)^(1/3), so 3m-1 + 1.5*(2K)^(1/3) <= N caps m around N/6.78.
#  * q(m), r(m) come from a vectorized "squarefree part" sieve over 8m-3.
#  * For each D = 1..T we count valid m vectorized (D | m*q plus the bound);
#    for D > T only m with r <= (N+1-3m)/(T+1)^2 can work - a tiny set - and
#    those are handled by explicit divisor enumeration via an SPF table.

def solve(N=110_000_000):

    # ---- bound for m: 3m-1 + 1.5*(2*m^2*(8m-3))^(1/3) <= N (continuous lower
    # bound for b+c on the curve b^2 c = m^2(8m-3)); small safety margin.
    lo, hi = 1, N
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if 3 * mid - 1 + 1.5 * (2 * mid * mid * (8 * mid - 3)) ** (1 / 3) <= N + 2:
            lo = mid
        else:
            hi = mid - 1
    M = lo

    # ---- smallest prime factor table up to M (used for the leftover m's)
    spf = np.zeros(M + 1, dtype=np.int32)
    for i in range(2, isqrt(M) + 1):
        if spf[i] == 0:
            sl = spf[i * i::i]
            sl[sl == 0] = i
    # primes (needed up to sqrt(8M-3) for the square sieve)
    wmax = 8 * M - 3
    pmax = isqrt(wmax)
    sieve = np.ones(pmax + 1, dtype=bool)
    sieve[:2] = False
    for i in range(2, isqrt(pmax) + 1):
        if sieve[i]:
            sieve[i * i::i] = False
    primes = np.flatnonzero(sieve)

    # ---- squarefree decomposition 8m-3 = q^2 * r, vectorized sieve.
    # 8m-3 is odd, so only odd primes matter.  q *= p once for every p^2 | 8m-3.
    q = np.ones(M + 1, dtype=np.int64)
    for p in primes[1:]:
        p = int(p)
        pe = p * p
        while pe <= wmax:
            m0 = (3 * pow(8, -1, pe)) % pe
            if m0 == 0:
                m0 = pe
            if m0 <= M:
                q[m0::pe] *= p
            pe *= p * p
    marr = np.arange(M + 1, dtype=np.int64)
    r = (8 * marr - 3) // (q * q)
    mq = marr * q
    lim = N + 1 - 3 * marr          # need b + c <= lim,  b = mq/D, c = D^2 r
    r[0] = lim[0] = 1               # m=0 is not used; keep values harmless
    mq[0] = 1

    count = 0
    T = 1024

    # sort m by r so that the "r small enough" prefix is contiguous
    order = np.argsort(r[1:], kind="stable").astype(np.int64) + 1
    r_sorted = r[order]

    # ---- vectorized passes over D = 1..T
    for D in range(1, T + 1):
        DD = D * D
        if DD > N:
            break
        # only m with D^2 * r <= lim can qualify; r <= N is a cheap superset
        pos = int(np.searchsorted(r_sorted, N // DD, side="right"))
        if pos == 0:
            continue
        if pos >= M - 1:
            idx = marr[1:]
        else:
            idx = order[:pos]
        sub = mq[idx]
        sel = sub % D == 0
        if not sel.any():
            continue
        idx2 = idx[sel]
        ok = mq[idx2] // D + DD * r[idx2] <= lim[idx2]
        count += int(np.count_nonzero(ok))

    # ---- leftover: D > T possible only when (T+1)^2 * r <= lim
    cand = np.flatnonzero(r * (T + 1) * (T + 1) <= lim)
    cand = cand[cand >= 1]
    spf_l = spf  # local
    for m in cand.tolist():
        rm = int(r[m])
        limm = int(lim[m])
        # factorize m * q(m)
        fac = {}
        for v in (m, int(q[m])):
            while v > 1:
                p = int(spf_l[v])
                if p == 0:
                    p = v
                while v % p == 0:
                    fac[p] = fac.get(p, 0) + 1
                    v //= p
        L = isqrt(limm // rm)
        divs = [1]
        for p, e in fac.items():
            cur = divs
            divs = []
            pk = 1
            for _ in range(e + 1):
                for d in cur:
                    nd = d * pk
                    if nd <= L:
                        divs.append(nd)
                pk *= p
        mqm = int(mq[m])
        for D in divs:
            if D > T and mqm // D + D * D * rm <= limm:
                count += 1
    return count

if __name__ == "__main__":
    print(solve())
