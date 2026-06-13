#!/usr/bin/env python3
"""Project Euler 656: Palindromic sequences."""

from math import isqrt

LIMIT = 1000
PREFIXES = 100
MOD = 10**15


def continued_fraction_period_sqrt(n):
    """Periodic part of the continued fraction for sqrt(n)."""
    a0 = isqrt(n)
    m = 0
    d = 1
    a = a0
    period = []

    while True:
        m = d * a - m
        d = (n - m * m) // d
        a = (a0 + m) // d
        period.append(a)
        if a == 2 * a0:
            return period


def h_value(beta, count=PREFIXES, mod=MOD):
    """Sum of the first `count` palindromic prefix lengths for sqrt(beta)."""
    period = continued_fraction_period_sqrt(beta)

    total = 0
    found = 0

    # The word starts with a run of zeros of every length 1..a_1.
    for n in range(1, period[0] + 1):
        total = (total + n) % mod
        found += 1
        if found == count:
            return total

    denominators = []
    q_prev_prev = 1
    q_prev = 0
    index = 0

    while found < count:
        partial = 0 if index == 0 else period[(index - 1) % len(period)]
        q = (partial * q_prev + q_prev_prev) % mod
        denominators.append(q)

        if index >= 3 and index % 2 == 1:
            for k in range(1, partial + 1):
                length = denominators[index - 2] + k * denominators[index - 1]
                total = (total + length) % mod
                found += 1
                if found == count:
                    return total

        q_prev_prev, q_prev = q_prev, q
        index += 1

    return total


def solve(limit=LIMIT):
    total = 0
    for beta in range(2, limit + 1):
        root = isqrt(beta)
        if root * root != beta:
            total = (total + h_value(beta)) % MOD
    return total


if __name__ == "__main__":
    print(solve())
