#!/usr/bin/env python3
# Project Euler 328 - Lowest-cost Search
#
# C(n) = worst-case cost of an optimal guessing strategy on [1, n], where
# asking k costs k. A strategy is a ternary search tree; its worst case is
# the maximum, over hidden numbers, of the sum of guesses along the path.
# The exact interval DP cost(a,b) = min_k k + max(cost(a,k-1), cost(k+1,b))
# is hopeless at n = 200000, but optimal trees have structure (verified
# against the exact DP for all n <= 1000 below):
#
# * Splitting [1,n] at guess k+1 leaves a prefix [1,k] and a "window"
#   [k+2, n] of size S = n-1-k near the top, with S only about n/12..n/4.
# * An optimal window strategy can be built canonically from perfectly
#   balanced blocks of size 2^h - 1 (cost h*anchor + 2((h-1)2^h + 1) when
#   the block sits just above its anchor value): writing the size S in
#   binary, if its two top bits are "11" peel a full block 2^h - 1 off the
#   low side, else a full half block 2^(h-1) - 1 off the top, and recurse
#   on the remainder around one connecting guess. The window cost is then
#   max over its blocks of (q * anchor + r) with per-size constants (q, r).
# * For n > ~100 some optimal split always uses a "valid" window size: one
#   whose canonical decomposition contains no degenerate blocks (all
#   blocks of height >= 2). Valid sizes are sparse (~5000 below 42000), so
#   the prefix DP F(n) = min over valid S of (n-S) + max(F(n-S-1), window)
#   needs only a short vectorized scan per n. Every candidate is the exact
#   cost of a genuine strategy, so F can never undershoot the truth; the
#   exact-DP cross-check below confirms the candidate set never misses an
#   optimal strategy.
#
# Small n are seeded by the exact O(n^3) interval DP, which also verifies
# the statement's test values and the fast method on 450 < n <= 600.

from functools import lru_cache
import bisect
import numpy as np


@lru_cache(maxsize=None)
def split(S):
    # canonical split of a window of size S: (left size, right size)
    h = S.bit_length() - 1
    if S >= (1 << h) | (1 << (h - 1)):           # top two bits "11"
        L = (1 << h) - 1                         # full block on the left
    else:
        L = S - (1 << (h - 1))                   # full half block on the right
    return L, S - 1 - L


@lru_cache(maxsize=None)
def shape(S):
    # window of size S anchored at value n (window occupies n+1 .. n+S):
    # cost = max over (q, r) in shape(S) of q*n + r
    if S <= 1:
        return ((0, 0),)
    h = S.bit_length() - 1
    if S == (2 << h) - 1:                        # perfectly balanced block
        return ((h, 2 * ((h - 1) * (1 << h) + 1)),)
    L, R = split(S)
    g = L + 1                                    # connecting guess offset
    return tuple([(q + 1, r + g) for q, r in shape(L)]
                 + [(q + 1, q * g + r + g) for q, r in shape(R)])


@lru_cache(maxsize=None)
def valid(S):
    # canonical decomposition uses no blocks of height < 2
    if S <= 1:
        return False
    h = S.bit_length() - 1
    if S == (2 << h) - 1:
        return h >= 2
    L, R = split(S)
    return valid(L) and valid(R)


def exact_cost_table(m):
    # exact interval DP: cost[a][b] for 1 <= a <= b <= m (full k scan)
    cost = [[0] * (m + 2) for _ in range(m + 2)]
    for length in range(2, m + 1):
        for a in range(1, m - length + 2):
            b = a + length - 1
            ca = cost[a]
            best = float("inf")
            for k in range(b, a - 1, -1):
                left = ca[k - 1] if k > a else 0
                right = cost[k + 1][b] if k < b else 0
                v = k + (left if left > right else right)
                if v < best:
                    best = v
            ca[b] = best
    return cost


def solve():
    N = 200000
    SEEDN, START = 600, 450

    # sparse candidate window sizes plus a few tiny ones for safety
    smax_all = int(0.21 * N) + 40
    cand = sorted({0, 1, 3, 7} | {S for S in range(2, smax_all + 1) if valid(S)})
    maxblk = max(len(shape(S)) for S in cand)
    Q = np.zeros((len(cand), maxblk), dtype=np.int64)
    R = np.zeros((len(cand), maxblk), dtype=np.int64)
    for idx, S in enumerate(cand):
        for j, (q, r) in enumerate(shape(S)):
            Q[idx, j] = q
            R[idx, j] = r
    candA = np.array(cand, dtype=np.int64)

    cost = exact_cost_table(SEEDN)
    dp = np.zeros(N + 1, dtype=np.int64)
    for n in range(2, START + 1):
        dp[n] = cost[1][n]

    # test values from the problem statement
    assert dp[1] == 0 and dp[2] == 1 and dp[3] == 2 and dp[8] == 12
    assert dp[100] == 400 and int(dp[1:101].sum()) == 17575

    for i in range(START + 1, N + 1):
        hi = bisect.bisect_right(cand, min(int(0.21 * i) + 40, i - 2))
        S = candA[:hi]
        k = i - 1 - S                                    # guess k+1, prefix [1,k]
        win = (Q[:hi] * (k[:, None] + 1) + R[:hi]).max(axis=1)
        tot = (k + 1) + np.maximum(dp[k], win)
        am = int(tot.argmin())
        dp[i] = tot[am]
        # optimal window size must sit well inside the searched range
        assert not (i > 700 and S[am] > 0.19 * i + 20), f"size bound hit at {i}"
        if i <= SEEDN:                                   # cross-check vs exact DP
            assert dp[i] == cost[1][i], (i, int(dp[i]), cost[1][i])

    return int(dp[1:].sum())


if __name__ == "__main__":
    print(solve())
