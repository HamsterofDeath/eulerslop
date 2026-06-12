#!/usr/bin/env python3
# Project Euler 438: monic integer polynomial p = x^n + a1*x^(n-1) + ... + an
# must have n real roots whose sorted floors are exactly 1..n, i.e. exactly
# one root in each half-open interval [i, i+1).
#
# DFS over the coefficients a_1, ..., a_n with three pruning layers:
#  * exact interval arithmetic at integer probe points k: p(k) = prod(k - x_i)
#    must lie in the interval product of [k-i-1, k-i], which constrains the
#    not-yet-chosen coefficients linearly (constraint propagation);
#  * derivative chain: P_d(x) = p^(n-d)(x)/(n-d)! = sum a_m C(n-m,n-d) x^(d-m)
#    must be real-rooted with all roots in (1, n+1).  a_d is the constant term
#    of P_d, so the admissible a_d form an interval cut out by sign conditions
#    at the critical points of P_d (the roots of P_(d-1), carried numerically;
#    a +-1 margin keeps this prune safe) and exact sign conditions at 1, n+1;
#  * the last coefficient a_n shifts every p(k) by a constant, so the strict
#    sign conditions (-1)^(n+1-k) p(k) > 0 at k = 1..n+1 cut out an interval
#    of a_n whose every interior integer is valid (strict sign alternation at
#    n+2 consecutive integers forces n real roots, one per open (k, k+1)).
#    The interval is counted in closed form; only its two endpoints (integer
#    roots, p(k) = 0) need the exact divide-and-check verification.

import numpy as np


def _eval(c, x):
    v = 0
    for a in c:
        v = v * x + a
    return v


def _verify(c, n):
    # Exact check that monic integer poly c (degree n) has exactly one root in
    # each [k, k+1) for k = 1..n.
    q = list(c)
    used = set()
    for k in range(1, n + 1):
        if _eval(q, k) == 0:
            nq = [q[0]]  # synthetic division by (x - k)
            for a in q[1:-1]:
                nq.append(a + nq[-1] * k)
            q = nq
            if _eval(q, k) == 0:
                return False  # multiple root at k -> floors can't be distinct
            used.add(k)
    # q (degree = #unused intervals) must change sign across every unused unit
    # interval; that forces exactly one simple real root in each and none
    # anywhere else, so the floor multiset is exactly {1..n}.
    for k in range(1, n + 1):
        if k not in used and _eval(q, k) * _eval(q, k + 1) >= 0:
            return False
    return True


def _esym(vals):
    # elementary symmetric polynomials e_0..e_len of vals
    vals = list(vals)
    e = [1] + [0] * len(vals)
    c = 0
    for v in vals:
        c += 1
        for m in range(c, 0, -1):
            e[m] += v * e[m - 1]
    return e


def search(n):
    # Returns (count of valid tuples, sum of S(t)).
    if n == 1:
        return (1, 1)  # x + a_1 with root -a_1 in [1, 2): only a_1 = -1
    K = list(range(-2, n + 3))  # integer probe points
    npts = len(K)
    pw = [[k ** d for d in range(n + 1)] for k in K]
    # outer bounds for p(k): interval product of (k - [i, i+1]), i = 1..n
    PL, PU = [], []
    for k in K:
        lo = hi = 1
        for i in range(1, n + 1):
            a, b = k - i - 1, k - i
            vals = (lo * a, lo * b, hi * a, hi * b)
            lo, hi = min(vals), max(vals)
        PL.append(lo)
        PU.append(hi)
    # Vieta box: e_m is increasing in each (positive) root, roots_i in [i,i+1)
    el, eh = _esym(range(1, n + 1)), _esym(range(2, n + 2))
    box = {}
    for m in range(1, n + 1):
        lo, hi = el[m], eh[m] - 1
        box[m] = (-hi, -lo) if m & 1 else (lo, hi)
    # binomials for the derivative chain
    C = [[0] * (n + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        C[i][0] = 1
        for j in range(1, i + 1):
            C[i][j] = C[i - 1][j - 1] + (C[i - 1][j] if j <= i - 1 else 0)

    res = [0, 0]  # count, sum of S(t)
    # probe-point indices of k = 1..n+1 in K, split by required sign of p(k)
    kpos = [K.index(k) for k in range(1, n + 2) if (n + 1 - k) % 2 == 0]
    kneg = [K.index(k) for k in range(1, n + 2) if (n + 1 - k) % 2 == 1]

    def tri(x):  # 1 + 2 + ... + x
        return x * (x + 1) // 2 if x > 0 else 0

    def abs_sum(a, b):  # sum of |c| over integers c in [a, b]
        if a > b:
            return 0
        if a >= 0:
            return tri(b) - tri(a - 1)
        if b <= 0:
            return tri(-a) - tri(-b - 1)
        return tri(b) + tri(-a)

    def tri_vec(x):  # vectorized 1 + 2 + ... + x
        return np.where(x > 0, x * (x + 1) // 2, 0)

    def abs_sum_vec(a, b):  # vectorized sum of |c| over integers c in [a, b]
        return np.where(a >= 0, tri_vec(b) - tri_vec(a - 1),
                        np.where(b <= 0, tri_vec(-a) - tri_vec(-b - 1),
                                 tri_vec(b) + tri_vec(-a)))

    def close(F, coeffs, cand):
        # last two coefficients at once, vectorized over candidates a = a_(n-1)
        # (cand): a_n shifts every p(k) by a constant, so the sign conditions
        # (-1)^(n+1-k) p(k) >= 0 at k = 1..n+1 cut out an interval
        # [lo(a), hi(a)] of a_n.  Every interior integer is valid: strict
        # alternation at n+2 consecutive integers forces n real roots, one per
        # open (k, k+1).  Only the endpoints (some p(k) = 0, i.e. an integer
        # root) need the exact divide-and-check verification.
        A = np.asarray(cand, dtype=np.int64)
        los = np.maximum.reduce([-(F[ki] + A * K[ki]) for ki in kpos])
        his = np.minimum.reduce([-(F[ki] + A * K[ki]) for ki in kneg])
        cnt = his - los - 1
        pos = cnt > 0
        if pos.any():
            base = sum(abs(a) for a in coeffs[1:]) + np.abs(A[pos])
            res[0] += int(cnt[pos].sum())
            res[1] += int((base * cnt[pos]).sum()) \
                + int(abs_sum_vec(los[pos] + 1, his[pos] - 1).sum())
        for i in np.flatnonzero(his >= los):
            a = int(A[i])
            for c in {int(los[i]), int(his[i])}:
                if _verify(coeffs + [a, c], n):
                    res[0] += 1
                    res[1] += sum(abs(x) for x in coeffs[1:]) + abs(a) + abs(c)

    def lastlevels(A2, crit2, F, rng, coeffs):
        # batched handling of the last three coefficients.  A2: candidates for
        # a_(n-2) (P_(n-2) real-rooted); crit2[w]: sorted roots of P_(n-2),
        # i.e. critical points of P_(n-1)/2.  For each candidate, the window
        # of a_(n-1) keeping P_(n-1) real-rooted in (1, n+1) comes from sign
        # conditions at the critical points (numeric, +-1 margin) and exact
        # ones at 1 and n+1; the flattened (a_(n-2), a_(n-1)) grid then goes
        # through the closed-form a_n count of close().
        d1 = n - 1
        # P_(n-1)(x) = B(x) + 2*a_(n-2)*x + a_(n-1)
        Bc = [coeffs[m] * (n - m) for m in range(n - 2)] + [0, 0]
        qv = np.polyval(np.array(Bc, dtype=float), crit2) \
            + 2.0 * A2[:, None].astype(float) * crit2
        nc = n - 2  # number of critical points; column i is a local minimum
        mins = [i for i in range(nc) if (nc - 1 - i) % 2 == 0]
        maxs = [i for i in range(nc) if (nc - 1 - i) % 2 == 1]
        hi1 = np.floor(-qv[:, mins]).astype(np.int64).min(axis=1) + 1
        blo, bhi = rng[d1]
        lo1 = np.full(len(A2), blo, dtype=np.int64)
        hi1 = np.minimum(hi1, bhi)
        if maxs:
            lo1 = np.maximum(
                lo1, np.ceil(-qv[:, maxs]).astype(np.int64).max(axis=1) - 1)
        B1, Bn1 = _eval(Bc, 1), _eval(Bc, n + 1)
        if d1 % 2 == 0:  # sign of P_(n-1)(1) is (-1)^(n-1)
            lo1 = np.maximum(lo1, -(B1 + 2 * A2))
        else:
            hi1 = np.minimum(hi1, -(B1 + 2 * A2))
        lo1 = np.maximum(lo1, -(Bn1 + 2 * (n + 1) * A2))  # P_(n-1)(n+1) > 0
        L = np.maximum(hi1 - lo1 + 1, 0)
        keep = L > 0
        if not keep.any():
            return
        A2, lo1, L = A2[keep], lo1[keep], L[keep]
        tot = int(L.sum())
        widx = np.repeat(np.arange(len(L)), L)
        starts = np.cumsum(L) - L
        a1f = lo1[widx] + np.arange(tot, dtype=np.int64) - starts[widx]
        a2f = A2[widx]
        los = np.maximum.reduce(
            [-(F[ki] + a2f * K[ki] ** 2 + a1f * K[ki]) for ki in kpos])
        his = np.minimum.reduce(
            [-(F[ki] + a2f * K[ki] ** 2 + a1f * K[ki]) for ki in kneg])
        cnt = his - los - 1
        pos = cnt > 0
        if pos.any():
            base = sum(abs(a) for a in coeffs[1:]) \
                + np.abs(a2f[pos]) + np.abs(a1f[pos])
            res[0] += int(cnt[pos].sum())
            res[1] += int((base * cnt[pos]).sum()) \
                + int(abs_sum_vec(los[pos] + 1, his[pos] - 1).sum())
        pre = sum(abs(a) for a in coeffs[1:])
        for i in np.flatnonzero(his >= los):
            t2, t1 = int(a2f[i]), int(a1f[i])
            for c in {int(los[i]), int(his[i])}:
                if _verify(coeffs + [t2, t1, c], n):
                    res[0] += 1
                    res[1] += pre + abs(t2) + abs(t1) + abs(c)

    def dfs(j, F, rng, coeffs, crit):
        # j coefficients fixed; F[ki] = fixed part of p(K[ki]);
        # rng[m] = (lo, hi) candidate range for a_m, m = j+1..n;
        # crit = sorted real roots of P_j (critical points of P_(j+1) / (n-j))
        rem = sorted(rng)
        # constraint propagation: a few monotone narrowing sweeps (any cutoff
        # is sound; ranges only shrink)
        for _ in range(4):
            changed = False
            for ki in range(npts):
                L = PL[ki] - F[ki]
                U = PU[ki] - F[ki]
                tl, th = {}, {}
                Tl = Th = 0
                for m in rem:
                    cc = pw[ki][n - m]
                    lo, hi = rng[m]
                    a, b = (lo * cc, hi * cc) if cc >= 0 else (hi * cc, lo * cc)
                    tl[m], th[m] = a, b
                    Tl += a
                    Th += b
                if Tl > U or Th < L:
                    return  # infeasible
                for m in rem:
                    cc = pw[ki][n - m]
                    if cc == 0:
                        continue
                    A = L - (Th - th[m])  # cc * a_m must lie in [A, B]
                    B = U - (Tl - tl[m])
                    if cc > 0:
                        nlo, nhi = -((-A) // cc), B // cc
                    else:
                        nlo, nhi = -((-B) // cc), A // cc
                    lo, hi = rng[m]
                    if nlo > lo or nhi < hi:
                        lo, hi = max(lo, nlo), min(hi, nhi)
                        if lo > hi:
                            return
                        rng[m] = (lo, hi)
                        a, b = (lo * cc, hi * cc) if cc >= 0 \
                            else (hi * cc, lo * cc)
                        Tl += a - tl[m]
                        Th += b - th[m]
                        tl[m], th[m] = a, b
                        changed = True
            if not changed:
                break
        d = j + 1  # next coefficient a_d = constant term of P_d
        lo, hi = rng[d]
        # P_d(x) = qc(x) + a_d, qc fixed; P_d must be real-rooted in (1, n+1).
        qc = [coeffs[m] * C[n - m][n - d] for m in range(d)] + [0.0]
        # exact endpoint sign conditions: sign P_d(1) = (-1)^d, P_d(n+1) > 0
        q1 = _eval([coeffs[m] * C[n - m][n - d] for m in range(d)] + [0], 1)
        qn1 = _eval([coeffs[m] * C[n - m][n - d] for m in range(d)] + [0],
                    n + 1)
        if d % 2 == 0:
            lo = max(lo, -q1)
        else:
            hi = min(hi, -q1)
        lo = max(lo, -qn1)
        # critical-point window: local minima of P_d need value <= 0, local
        # maxima >= 0 (rightmost critical point is a minimum); +-1 margin
        # absorbs the floating-point error of crit
        if len(crit):
            qv = np.polyval(np.array(qc, dtype=float), crit)
            for i in range(len(crit)):
                if (len(crit) - 1 - i) % 2 == 0:  # local minimum
                    hi = min(hi, int(np.floor(-qv[i])) + 1)
                else:  # local maximum
                    lo = max(lo, int(np.ceil(-qv[i])) - 1)
        if lo > hi:
            return
        if d == n - 1:
            close(F, coeffs, range(lo, hi + 1))
            return
        sub = {m: rng[m] for m in rem if m != d}
        kpw = [pw[ki][n - d] for ki in range(npts)]
        cand = np.arange(lo, hi + 1, dtype=np.int64)
        # vectorized one-sweep feasibility: with the remaining coefficients in
        # their current boxes, every probe point must stay reachable
        keep = np.ones(len(cand), dtype=bool)
        for ki in range(npts):
            slo = shi = 0
            for m in rem:
                if m == d:
                    continue
                cc = pw[ki][n - m]
                mlo, mhi = rng[m]
                slo += mlo * cc if cc >= 0 else mhi * cc
                shi += mhi * cc if cc >= 0 else mlo * cc
            t = F[ki] + cand * kpw[ki]
            keep &= (t + slo <= PU[ki]) & (t + shi >= PL[ki])
        cand = cand[keep]
        if not len(cand):
            return
        # children's critical points: roots of P_d for each candidate a_d,
        # via batched companion-matrix eigenvalues
        lead = float(C[n][n - d])
        comp = np.zeros((len(cand), d, d))
        if d > 1:
            comp[:, 1:, :-1] = np.eye(d - 1)
            comp[:, 0, :] = -np.array(qc[1:], dtype=float) / lead
        comp[:, 0, -1] = -cand.astype(float) / lead
        rts = np.linalg.eigvals(comp)
        good = np.abs(rts.imag).max(axis=1) <= 1e-2  # else not real-rooted
        rr = np.sort(rts.real, axis=1)
        if d == n - 2:
            if good.any():
                lastlevels(cand[good], rr[good], F, sub, coeffs)
            return
        for idx in range(len(cand)):
            if not good[idx]:
                continue
            a = int(cand[idx])
            F2 = [F[ki] + a * kpw[ki] for ki in range(npts)]
            dfs(d, F2, dict(sub), coeffs + [a], rr[idx])

    dfs(0, [pw[ki][n] for ki in range(npts)], dict(box), [1],
        np.empty(0))
    return tuple(res)


def solve():
    return search(7)[1]


if __name__ == "__main__":
    print(solve())
