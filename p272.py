#!/usr/bin/env python3
# Problem 272: Modular Cubes, part 2
#
# The number of cube roots of unity mod n is multiplicative over prime powers:
# a component p^e contributes 3 roots iff p = 1 (mod 3) (any e >= 1) or
# p = 3 with e >= 2; otherwise it contributes 1 root. Hence C(n) = 3^t - 1
# where t is the number of "contributing" components, and C(n) = 242 means
# t = 5 exactly.
#
# So n = (product of exactly 5 contributing prime-power components) * f, where
# the free factor f only uses primes p = 2 (mod 3) (any power) and at most one
# factor of 3 (3^1 is non-contributing, 3^2 would be a 6th component).
#
# Enumerate the 5 components recursively in increasing prime order (3^e with
# e >= 2 allowed as the first component). For the 5th (largest) prime with
# exponent 1 the loop is vectorised with numpy: contribution is
# core4 * sum(q * T(N // (core4 * q))) where T(L) is the precomputed sum of all
# valid free factors <= L (two tables: free factors that may / may not contain
# a single 3, depending on whether the core already used 3^e).

import numpy as np

def solve():
    N = 10 ** 11
    K = 5  # exactly 5 contributing components

    # Largest possible 5th prime: the other 4 components are at least
    # 9*7*13*19 (core containing 3^2) or 7*13*19*31 (core without 3).
    LIM1 = N // min(9 * 7 * 13 * 19, 7 * 13 * 19 * 31)
    sieve = np.ones(LIM1 + 1, dtype=bool)
    sieve[:2] = False
    for i in range(2, int(LIM1 ** 0.5) + 1):
        if sieve[i]:
            sieve[i * i::i] = False
    primes = np.nonzero(sieve)[0].astype(np.int64)
    p1 = primes[primes % 3 == 1]           # primes = 1 (mod 3)
    p1_list = [int(x) for x in p1]
    NP = len(p1_list)

    # Free-factor tables up to max needed L = N / (9*7*13*19*31).
    MAXL = N // (9 * 7 * 13 * 19 * 31)
    good = np.ones(MAXL + 1, dtype=bool)
    good[0] = False
    for q in p1_list:
        if q > MAXL:
            break
        good[q::q] = False
    vals = np.arange(MAXL + 1, dtype=np.int64)
    ga = good.copy()
    ga[9::9] = False                       # at most one factor of 3
    gb = good.copy()
    gb[3::3] = False                       # no factor of 3 at all
    cums_a = np.cumsum(np.where(ga, vals, 0))   # core has no 3-component
    cums_b = np.cumsum(np.where(gb, vals, 0))   # core contains 3^e (e>=2)

    total = 0

    def last_level(start, prod, cums):
        # 5th component: prime q > p1[start-1], exponent 1 (vectorised) ...
        s = 0
        hi = N // prod
        idx_hi = int(np.searchsorted(p1, hi, side='right'))
        if idx_hi > start:
            qs = p1[start:idx_hi]
            L = N // (prod * qs)
            s += int(np.dot(qs, cums[L]))
        # ... or exponent >= 2 (few cases, plain loop)
        i = start
        while i < NP:
            q = p1_list[i]
            qe = q * q
            if prod * qe > N:
                break
            while prod * qe <= N:
                s += qe * int(cums[N // (prod * qe)])
                qe *= q
            i += 1
        return prod * s

    def rec(start, depth, prod, has3):
        nonlocal total
        rem = K - depth
        if rem == 1:
            total += last_level(start, prod, cums_b if has3 else cums_a)
            return
        i = start
        while i + rem - 1 < NP:
            q = p1_list[i]
            # cheapest way to finish: q^1 times the next rem-1 primes
            tail = 1
            for j in range(i + 1, i + rem):
                tail *= p1_list[j]
            if prod * q * tail > N:
                break
            qe = q
            while prod * qe * tail <= N:
                rec(i + 1, depth + 1, prod * qe, has3)
                qe *= q
            i += 1

    # optional first component 3^e (e >= 2)
    tail4 = 7 * 13 * 19 * 31
    pe = 9
    while pe * tail4 <= N:
        rec(0, 1, pe, True)
        pe *= 3
    # all components are primes = 1 (mod 3)
    rec(0, 0, 1, False)

    return total

if __name__ == "__main__":
    print(solve())
