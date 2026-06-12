#!/usr/bin/env python3

from decimal import Decimal, getcontext
from fractions import Fraction


def r_value(a, b):
    return Fraction(b * (a - 2 * b), a - b)


def exact_g(n):
    total = Fraction(0, 1)
    for a in range(3, n + 1):
        for b in range(1, (a - 1) // 2 + 1):
            total += r_value(a, b)
    return total


def harmonic_tail(n):
    if n <= 0:
        return Decimal(0)

    x = Decimal(n)
    inv = Decimal(1) / x
    inv2 = inv * inv
    inv4 = inv2 * inv2

    return (
        x.ln()
        + inv / 2
        - inv2 / 12
        + inv4 / 120
        - inv4 * inv2 / 252
        + inv4 * inv4 / 240
        - Decimal(5) * inv4 * inv4 * inv2 / 660
    )


def harmonic_interval(lo, hi):
    if hi < lo:
        return Decimal(0)
    return harmonic_tail(hi) - harmonic_tail(lo - 1)


def g_large(n):
    h = (n + 1) // 2
    dec = Decimal

    full_sum = h * (h + 1) * (2 * h + 1) // 6 - h
    total = dec(full_sum) / 6

    lo, hi = h + 1, n - 1
    if lo > hi:
        return total

    count = hi - lo + 1
    sum_d = (lo + hi) * count // 2
    sum_d2 = hi * (hi + 1) * (2 * hi + 1) // 6
    sum_d2 -= (lo - 1) * lo * (2 * lo - 1) // 6

    c0 = dec(3 * n * (n + 1)) / 2
    c2 = dec(n * (n + 1) * (2 * n + 1)) / 6

    total += dec(count) * c0
    total -= dec(2 * n) * dec(sum_d)
    total += dec(5) * dec(sum_d2) / 6
    total -= dec(sum_d)
    total += dec(count) / 6
    total -= c2 * harmonic_interval(lo, hi)
    return total


def sci_10(value):
    return f"{value:.9e}".replace("e+", "e").replace("e0", "e")


def solve():
    assert r_value(3, 1) == Fraction(1, 2)
    assert r_value(6, 2) == 1
    assert r_value(12, 3) == 2
    assert f"{float(exact_g(10)):.8f}" == "20.59722222"
    assert f"{float(exact_g(100)):.5f}" == "19223.60980"

    getcontext().prec = 80
    return sci_10(g_large(10**11))


if __name__ == "__main__":
    print(solve())
