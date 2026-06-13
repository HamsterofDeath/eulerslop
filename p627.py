#!/usr/bin/env python3
"""Project Euler 627: Counting products."""

from math import comb


MOD = 1_000_000_007
TARGET = 10_001
DEGREE = 10


def count_smooth_exponents(plain, sevens, two_prime):
    """Count possible 2/3/5 exponent triples for fixed large-prime slots.

    ``plain`` slots may contain any 5-smooth number up to 30.
    ``sevens`` slots already contain a 7, so their cofactors are 1, 2, 3, 4.
    ``two_prime`` slots already contain an 11 or 13, so their cofactors are
    1 or 2.
    """
    total = 0
    r = plain
    a = sevens
    t = two_prime

    for z in range(2 * r + 1):
        ymax = (6 * r + 2 * a - 3 * z) // 2
        if ymax < 0:
            continue
        ymax = min(
            ymax,
            4 * r + 2 * a + t - 2 * z,
            (6 * r + 2 * a + t - 3 * z) // 2,
            (9 * r + 4 * a + 2 * t - 4 * z) // 3,
        )
        for y in range(ymax + 1):
            xmax = min(
                4 * r + 2 * a + t - y - 2 * z,
                6 * r + 2 * a + t - 2 * y - 3 * z,
                (9 * r + 4 * a + 2 * t - 3 * y - 4 * z) // 2,
            )
            total += xmax + 1

    return total


def exact_count(slots):
    """Exact F(30, slots) for small ``slots``.

    Large primes are grouped by behavior:
    7 has cofactors 1,2,3,4; 11 and 13 have cofactors 1,2; and
    17,19,23,29 have no nontrivial cofactor.
    """
    total = 0
    for sevens in range(slots + 1):
        after_sevens = slots - sevens
        for two_prime in range(after_sevens + 1):
            split_11_13 = two_prime + 1
            after_two_prime = after_sevens - two_prime
            for solitary in range(after_two_prime + 1):
                plain = after_two_prime - solitary
                split_17_29 = comb(solitary + 3, 3)
                total += (
                    split_11_13
                    * split_17_29
                    * count_smooth_exponents(plain, sevens, two_prime)
                )
    return total


def forward_differences(values):
    diffs = []
    row = values[:]
    while row:
        diffs.append(row[0])
        row = [row[i + 1] - row[i] for i in range(len(row) - 1)]
    return diffs


def interpolate(n, diffs, mod=None):
    total = 0
    choose = 1
    for k, diff in enumerate(diffs):
        if k:
            choose = choose * (n - k + 1) // k
        total += diff * choose
        if mod is not None:
            total %= mod
    return total


def solve():
    # The exponent polytope has dimension 10, so F(30,n) is a degree-10
    # Ehrhart polynomial.  Seed it with exact small values.
    values = [exact_count(n) for n in range(DEGREE + 1)]
    diffs = forward_differences(values)

    # Cheap guard against mistakes in the decomposition above.
    assert exact_count(DEGREE + 1) == interpolate(DEGREE + 1, diffs)

    return interpolate(TARGET, diffs, MOD)


if __name__ == "__main__":
    print(solve())
