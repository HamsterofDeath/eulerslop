#!/usr/bin/env python3
from math import isqrt
import numpy as np

def solve():
    # A geometric triangle has sides k*p^2 <= k*p*q <= k*q^2 with gcd(p,q)=1
    # (q/p is the reduced ratio, k any positive integer).  The triangle
    # inequality k*p^2 + k*p*q > k*q^2 means q/p < golden ratio, and the
    # perimeter is k*s with s = p^2 + p*q + q^2.  So the count is
    #   A = sum over coprime wedge pairs (p,q) of floor(P/s).
    # Let F(x) = #{(p,q): p <= q, q^2 < p^2+pq, s <= x} WITHOUT coprimality.
    # Scaling (p,q) -> (dp,dq) multiplies s by d^2, and summing the Moebius
    # inversion over both the scale d and the multiplier k collapses
    # (sum_{d^2 | n} mu(d) = [n squarefree]) to
    #   A = sum over squarefree n of F(P // n).
    # Evaluate by Dirichlet hyperbola split at X*Y ~ P:
    #   A = sum_{n<=X squarefree} F(P//n) + sum_{s<=Y} cnt[s]*Q(P//s)
    #       - Q(X)*F(Y)
    # with Q = squarefree-counting function and cnt[s] = #pairs of size s.
    # The middle term is evaluated by expanding Q(z) = sum mu(d)*(z//d^2)
    # and swapping the sums; large d are grouped by the value of P//d^2.
    P = 25 * 10 ** 12
    X = isqrt(P) // 10
    Y = P // X
    Dmax = isqrt(P // 3)        # largest d with P//d^2 >= smallest s = 3
    D0 = 20000                  # d-loop / quotient-grouping switchover
    N = max(X, Dmax)

    # Moebius function and Mertens prefix sums up to N
    mu = np.ones(N + 1, dtype=np.int64)
    comp = np.zeros(N + 1, dtype=bool)
    for i in range(2, isqrt(N) + 1):
        if not comp[i]:
            comp[i * i::i] = True
    for p in np.nonzero(~comp)[0][2:]:
        mu[p::p] *= -1
        if p * p <= N:
            mu[p * p::p * p] = 0
    mert = np.cumsum(mu)

    def isqrt_v(t):
        # exact vectorized integer sqrt (t < 2^53 so one fixup suffices)
        r = np.sqrt(t.astype(np.float64)).astype(np.int64)
        r -= r * r > t
        r += (r + 1) * (r + 1) <= t
        return r

    # qtri[p] = floor(phi*p): largest q with q^2 < p^2 + p*q, plus prefix
    # sums of the per-p wedge counts (q from p to qtri[p])
    pmax_g = isqrt(P // 3)
    parr = np.arange(pmax_g + 1, dtype=np.int64)
    qtri = (parr + isqrt_v(5 * parr * parr)) // 2
    qtri += (qtri + 1) * (qtri + 1) < parr * parr + parr * (qtri + 1)
    qtri[1:] -= ~(qtri[1:] * qtri[1:] < parr[1:] * parr[1:] + parr[1:] * qtri[1:])
    PS = np.zeros(pmax_g + 1, dtype=np.int64)
    PS[1:] = np.cumsum(qtri[1:] - parr[1:] + 1)

    # multiplicities cnt[s] for all pairs with s <= Y (compressed)
    pm = isqrt(Y // 3)
    p = np.arange(1, pm + 1, dtype=np.int64)
    qhi = np.minimum((isqrt_v(4 * Y - 3 * p * p) - p) // 2, qtri[1:pm + 1])
    lens = qhi - p + 1
    pf = np.repeat(p, lens)
    qf = pf + np.arange(int(lens.sum()), dtype=np.int64) \
        - np.repeat(np.cumsum(lens) - lens, lens)
    s_uni, c_arr = np.unique(pf * pf + pf * qf + qf * qf, return_counts=True)
    FY = int(c_arr.sum())

    # T1 = sum_{n<=X squarefree} F(P//n).  For p <= pa = isqrt(4x/21) the
    # size bound never binds ((3+sqrt5)*pa^2 < x), so that part is a prefix
    # sum lookup; only the short range pa < p <= isqrt(x/3) needs work.
    T1 = 0
    n_all = np.nonzero(mu[1:X + 1])[0] + 1
    x_all = P // n_all
    pa_all = isqrt_v(4 * x_all // 21)
    lens_all = isqrt_v(x_all // 3) - pa_all
    T1 += int(PS[pa_all].sum())
    cum = np.cumsum(lens_all)
    budget = 2 * 10 ** 7
    bounds = np.searchsorted(cum, np.arange(budget, int(cum[-1]) + budget, budget))
    i0 = 0
    for i1 in bounds:
        i1 = min(int(i1) + 1, len(n_all))
        if i1 <= i0:
            continue
        pa, lens = pa_all[i0:i1], lens_all[i0:i1]
        tot = int(lens.sum())
        pf = np.repeat(pa, lens) + 1 + np.arange(tot, dtype=np.int64) \
            - np.repeat(np.cumsum(lens) - lens, lens)
        xf = np.repeat(x_all[i0:i1], lens)
        q1 = (isqrt_v(4 * xf - 3 * pf * pf) - pf) // 2
        T1 += int((np.minimum(q1, qtri[pf]) - pf + 1).sum())
        i0 = i1

    # T2 = sum_{s<=Y} cnt[s] * Q(P//s)
    #    = sum_d mu(d) * sum_{s <= min(Y, P//d^2)} cnt[s] * ((P//d^2)//s)
    T2 = 0
    for d in range(1, min(D0, Dmax) + 1):
        m = int(mu[d])
        if m:
            M = P // (d * d)
            j = np.searchsorted(s_uni, M, 'right')
            T2 += m * int(np.dot(c_arr[:j], M // s_uni[:j]))
    if D0 < Dmax:
        # group d > D0 by M = P//d^2; W[M] = sum_s cnt[s]*(M//s) via a
        # harmonic sieve (W = prefix sums of sum_{s|j} cnt[s])
        Mcap = P // ((D0 + 1) * (D0 + 1))
        G = np.zeros(Mcap + 1, dtype=np.int64)
        small = s_uni <= Mcap
        for sv, cv in zip(s_uni[small].tolist(), c_arr[small].tolist()):
            G[sv::sv] += cv
        W = np.cumsum(G)
        d = D0 + 1
        while d <= Dmax:
            M = P // (d * d)
            dh = min(isqrt(P // M), Dmax)
            T2 += int(mert[dh] - mert[d - 1]) * int(W[M])
            d = dh + 1

    # Q(X) for the hyperbola overlap correction
    dq = np.arange(1, isqrt(X) + 1, dtype=np.int64)
    QX = int(np.dot(mu[1:isqrt(X) + 1], X // (dq * dq)))

    return T1 + T2 - QX * FY

if __name__ == "__main__":
    print(solve())
