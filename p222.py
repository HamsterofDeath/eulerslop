#!/usr/bin/env python3
"""Project Euler 222: Sphere Packing.

Pack 21 balls of radii 30..50 mm in a tube of internal radius 50 mm,
minimising the tube length.  Two consecutive balls of radii r1, r2 sit
against opposite walls; their centres advance axially by
sqrt((r1+r2)^2 - (100-r1-r2)^2).  Total length for an ordering
r_1..r_n is r_1 + r_n + sum of consecutive advances.

The optimal ordering is a "valley": radii decrease to the minimum and
then increase (largest balls at the ends).  This permits an O(n^2) DP
that inserts balls in increasing size at either end of the partial
sequence.  The script verifies this DP against a full O(2^n * n^2)
bitmask DP on a smaller instance before trusting it for n = 21.
"""

from math import sqrt


def advance(r1, r2, tube=100):
    s = r1 + r2
    return sqrt(s * s - (tube - s) * (tube - s))


def valley_dp(radii):
    """Min length assuming an optimal valley ordering; O(n^2)."""
    r = sorted(radii)
    n = len(r)
    INF = float("inf")
    # dp[e]: balls r[0..k] placed, ends are r[k] and r[e] (e < k),
    # value = sum of advances so far.
    dp = [INF] * n
    dp[0] = advance(r[0], r[1]) if n > 1 else 0.0
    for k in range(1, n - 1):
        new = [INF] * n
        # attach r[k+1] next to current end r[k]: other end e unchanged
        for e in range(k):
            if dp[e] < INF:
                new[e] = dp[e] + advance(r[k], r[k + 1])
        # attach r[k+1] next to the other end r[e]: ends become r[k], r[k+1]
        best = min(dp[e] + advance(r[e], r[k + 1]) for e in range(k) if dp[e] < INF)
        new[k] = min(new[k], best)
        dp = new
    if n == 1:
        return 2 * r[0]
    return min(dp[e] + r[n - 1] + r[e] for e in range(n - 1) if dp[e] < INF)


def bitmask_dp(radii):
    """Exact min length over all orderings; O(2^n * n^2)."""
    r = list(radii)
    n = len(r)
    INF = float("inf")
    cost = [[advance(a, b) for b in r] for a in r]
    size = 1 << n
    # dp[mask][last] = min(r_first + advances) over orderings of mask ending at last
    dp = [None] * size
    for i in range(n):
        row = [INF] * n
        row[i] = float(r[i])
        dp[1 << i] = row
    for mask in range(1, size):
        row = dp[mask]
        if row is None:
            continue
        free = (size - 1) & ~mask
        for last in range(n):
            v = row[last]
            if v == INF:
                continue
            c = cost[last]
            m = free
            while m:
                bit = m & -m
                j = bit.bit_length() - 1
                nm = mask | bit
                nrow = dp[nm]
                if nrow is None:
                    nrow = [INF] * n
                    dp[nm] = nrow
                w = v + c[j]
                if w < nrow[j]:
                    nrow[j] = w
                m ^= bit
    full = dp[size - 1]
    return min(full[i] + r[i] for i in range(n))


def solve():
    # Verify the valley DP against the exhaustive bitmask DP on a
    # smaller instance of the same problem (largest 12 balls).
    small = list(range(39, 51))
    a, b = valley_dp(small), bitmask_dp(small)
    assert abs(a - b) < 1e-9, (a, b)

    length_mm = valley_dp(range(30, 51))
    return round(length_mm * 1000)


if __name__ == "__main__":
    print(solve())
