#!/usr/bin/env python3
# Lenticular pairs L(100000).
#
# Geometry reduction:
# * The two circles meet at lattice points A, B; the open chord lies inside the
#   lens, so B - A = (p, q) must be primitive.  A lattice centre equidistant from
#   A and B needs p^2 + q^2 even, hence p, q both odd.
# * Lattice centres lie on the perpendicular bisector, spaced L = |AB| apart, and
#   the point reflection through the midpoint of AB (a lattice symmetry) forces
#   them to sit exactly at signed distances t = j*L/2 from the chord for ALL odd
#   j, giving radius r^2 = L^2 (j^2 + 1) / 4 (an integer).
# * If both centres are on the same side of the chord, the lens contains the
#   nearer centre (a lattice point), so the centres must be on opposite sides;
#   the lens is then the union of the two minor segments, and by the midpoint
#   symmetry "segment of circle j is lattice-free" is side-independent.
# * Coordinates along/across the chord: u = px + qy, w = qx - py; lattice points
#   are (u, w) with u ≡ c0*w (mod L^2) where c0 = -q * p^{-1} mod L^2.  A point on
#   row w = k >= 1 lies strictly inside circle j iff u (L^2 - u) > k^2 + j k L^2.
#   So circle j has an empty segment iff for all k >= 1 (only k < L^2/4 matter):
#       u_k (L^2 - u_k) <= k^2 + j k L^2,  u_k = k c0 mod L^2.
#   Valid j form an interval [j0, jmax] of odd numbers (jmax from r <= N).
# * Row k = 1 alone forces j >= (c (L^2 - c) - 1)/L^2 with c = min(c0, L^2 - c0),
#   and any nonzero lattice point on row 1 has length sqrt(c0^2+1)/L >= 1, so
#   c >= sqrt(L^2 - 1).  Combining with j0 <= jmax ~ 2N/L gives L^2 <~ 2N: only
#   short chords can contribute, so all of them can be enumerated directly.
#
# A lenticular pair for chord class (p,q) is any unordered pair (j1, j2) from its
# odd interval (sides are independent).  Distinct (r1, r2) are counted with
# inclusion-exclusion over chord classes: classes sharing L^2 merge (keep minimal
# j0); for values r^2 shared between different L^2 classes, |union of symmetric
# squares| = sum over class subsets T, (-1)^{|T|+1} * C2(|intersection of value
# sets|), where only subsets of small "owner sets" of duplicated values matter.

import numpy as np
from math import gcd, isqrt
from collections import Counter, defaultdict


def solve(N=100000):
    N2 = N * N
    # enumeration bound for L^2 (see header): L^2 <= 2N + slack
    LIM = 2 * N + 4 * isqrt(2 * N) + 16

    best_j0 = {}  # L^2 -> minimal j0 over chords of that length
    p = 1
    while p * p + 1 <= LIM:
        for q in range(1, p + 1, 2):
            L2 = p * p + q * q
            if L2 > LIM:
                break
            if gcd(p, q) != 1:
                continue
            # jmax: largest odd j with L2*(j^2+1) <= 4 N^2
            t = 4 * N2 // L2 - 1
            if t < 1:
                continue
            jmax = isqrt(t)
            if jmax % 2 == 0:
                jmax -= 1
            if jmax < 1:
                continue
            c0 = (-q * pow(p, -1, L2)) % L2
            c = min(c0, L2 - c0)
            # necessary condition from row k=1
            if c * (L2 - c) - 1 > jmax * L2:
                continue
            # exact minimal j via full scan of rows k = 1 .. L2//4
            kk = np.arange(1, L2 // 4 + 1, dtype=np.int64)
            if kk.size:
                u = (kk * c0) % L2
                f = u * (L2 - u) - kk * kk
                jreq = int(np.max(-((-f) // (kk * L2))))
            else:
                jreq = 1
            j0 = max(1, jreq)
            if j0 % 2 == 0:
                j0 += 1
            if j0 > jmax:
                continue
            if L2 not in best_j0 or j0 < best_j0[L2]:
                best_j0[L2] = j0
        p += 2

    # value sets per class
    classes = sorted(best_j0.items())
    n_sizes = []
    all_vals = []
    all_ids = []
    for idx, (L2, j0) in enumerate(classes):
        t = 4 * N2 // L2 - 1
        jmax = isqrt(t)
        if jmax % 2 == 0:
            jmax -= 1
        j = np.arange(j0, jmax + 1, 2, dtype=np.int64)
        v = L2 * (j * j + 1) // 4
        n_sizes.append(v.size)
        all_vals.append(v)
        all_ids.append(np.full(v.size, idx, dtype=np.int32))

    def C2(n):
        return n * (n + 1) // 2

    ans = sum(C2(n) for n in n_sizes)

    # find values shared by several classes
    vals = np.concatenate(all_vals)
    ids = np.concatenate(all_ids)
    order = np.argsort(vals, kind="stable")
    vals = vals[order]
    ids = ids[order]
    # group boundaries
    diff = np.nonzero(np.diff(vals))[0] + 1
    starts = np.concatenate(([0], diff))
    ends = np.concatenate((diff, [vals.size]))
    owner_counter = Counter()
    for s, e in zip(starts, ends):
        if e - s >= 2:
            owner_counter[tuple(sorted(ids[s:e].tolist()))] += 1

    # inclusion-exclusion over subsets (size >= 2) of owner sets
    sub_counts = defaultdict(int)
    from itertools import combinations
    for owners, cnt in owner_counter.items():
        m = len(owners)
        for size in range(2, m + 1):
            for T in combinations(owners, size):
                sub_counts[T] += cnt
    for T, cnt in sub_counts.items():
        sign = -1 if len(T) % 2 == 0 else 1
        ans += sign * C2(cnt)
    return ans


if __name__ == "__main__":
    print(solve())
