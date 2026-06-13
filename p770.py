#!/usr/bin/env python3
"""Project Euler 770: guaranteed betting growth."""

from decimal import Decimal, getcontext
from fractions import Fraction
from math import comb


TARGET = Fraction(19999, 10000)
PI = Decimal("3.1415926535897932384626433832795028841971693993751")


def guaranteed_value(n: int) -> Fraction:
    ratio = Fraction(comb(2 * n, n), 4**n)
    return Fraction(2, 1 + ratio)


def log_central_ratio(n: int) -> Decimal:
    x = Decimal(n)
    return (
        -((PI * x).ln() / 2)
        - Decimal(1) / (8 * x)
        + Decimal(1) / (192 * x**3)
        - Decimal(1) / (640 * x**5)
    )


def solve() -> int:
    getcontext().prec = 60
    assert min(n for n in range(1, 20) if guaranteed_value(n) >= Fraction(17, 10)) == 10

    threshold_log = -Decimal(19999).ln()
    low, high = 0, 1
    while log_central_ratio(high) > threshold_log:
        high *= 2
    while low + 1 < high:
        mid = (low + high) // 2
        if log_central_ratio(mid) <= threshold_log:
            high = mid
        else:
            low = mid
    return high


if __name__ == "__main__":
    print(solve())
