#!/usr/bin/env python3
# Project Euler 261: Pivotal Square Sums
#
# Sum of (m+1) consecutive squares ending at k equals sum of m consecutive
# squares starting at n+1:
#     (m+1) k (k-m) = m n (n+m+1).
# Substituting v = 2k - m, u = 2n + m + 1 turns this into the Pell-like
# equation
#     (m+1) v^2 - m u^2 = -m (m+1).
# Its automorphism (from the Pell unit (2m+1) + 2*sqrt(m(m+1))) is
#     (v, u) -> ((2m+1) v + 2m u, 2(m+1) v + (2m+1) u).
# By Nagell's bound every solution class contains a fundamental solution with
# 0 < u <= m+1.  The equation forces (m+1) | u^2, so writing m+1 = a^2 b with
# b squarefree, u = a*b*j for some 1 <= j <= a, and then
#     v^2 = m (b j^2 - 1)
# must be a perfect square.  (j = a gives the main seed (v, u) = (m, m+1).)
# Iterating the automorphism from each fundamental (+-v, u) enumerates every
# solution; we keep those with integer k = (v+m)/2 <= 1e10 and n >= k,
# collecting distinct k.

from math import isqrt


def solve():
    LIMIT = 10 ** 10
    # smallest k of the main class is 2m(m+1), so m is bounded by:
    M = 1
    while 2 * M * (M + 1) <= LIMIT:
        M += 1

    # smallest-prime-factor sieve to split m+1 = a^2 * b (b squarefree)
    spf = list(range(M + 2))
    for p in range(2, isqrt(M + 1) + 1):
        if spf[p] == p:
            for q in range(p * p, M + 2, p):
                if spf[q] == q:
                    spf[q] = p

    pivots = set()
    for m in range(1, M + 1):
        # factor m+1 -> a^2 * b
        t = m + 1
        a = 1
        b = 1
        while t > 1:
            p = spf[t]
            e = 0
            while t % p == 0:
                t //= p
                e += 1
            a *= p ** (e // 2)
            if e % 2:
                b *= p
        # fundamental seeds: u = a*b*j, v = sqrt(m*(b*j^2 - 1)), j = 1..a
        seeds = []
        ab = a * b
        for j in range(1, a + 1):
            u = ab * j
            v2 = m * (b * j * j - 1)
            v = isqrt(v2)
            if v * v != v2:
                continue
            # parity needed for integer k = (v+m)/2 and n = (u-m-1)/2
            if (v - m) % 2 or (u - m - 1) % 2:
                continue
            seeds.append((v, u))
            if v:
                seeds.append((-v, u))
        c1, c2, c3 = 2 * m + 1, 2 * m, 2 * (m + 1)
        vlim = 2 * LIMIT - m  # k <= LIMIT  <=>  v <= 2*LIMIT - m
        for v, u in seeds:
            # the seed itself may already be a valid solution
            while v <= vlim:
                if v > 0:
                    k = (v + m) // 2
                    n = (u - m - 1) // 2
                    if n >= k:
                        pivots.add(k)
                v, u = c1 * v + c2 * u, c3 * v + c1 * u
    return sum(pivots)


if __name__ == "__main__":
    print(solve())
