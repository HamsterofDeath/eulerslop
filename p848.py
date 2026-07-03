#!/usr/bin/env python3
"""Project Euler 848: optimal guessing game thresholds."""

from decimal import Decimal, ROUND_HALF_UP, getcontext
from fractions import Fraction


def threshold(n: int) -> int:
    if n <= 2:
        return n
    result = 3
    while result < n:
        result *= 2
    return result


def stable_scaled(n: int) -> int:
    """Return n*q(n), where p(m,n)=q(n)/m once m reaches threshold(n)."""
    if n == 1:
        return 1
    if n == 2:
        return 3

    total = 3
    previous = 2
    block = 3
    while n > block:
        total += block * (block - previous)
        previous = block
        block *= 2
    return total + block * (n - previous)


def stable_deficit(n: int) -> int:
    if n == 1:
        return 0
    if n == 2:
        return 1
    return stable_scaled(n) // 2


def probability(m: int, n: int) -> Fraction:
    if m >= threshold(n):
        return Fraction(stable_scaled(n), m * n)
    return Fraction(1, 1) - Fraction(stable_deficit(m), m * n)


def solve() -> str:
    assert probability(1, 100) == 1
    assert probability(7, 5) == Fraction(18, 35)

    total = Fraction(0, 1)
    for i in range(21):
        for j in range(21):
            total += probability(7**i, 5**j)

    getcontext().prec = 80
    value = Decimal(total.numerator) / Decimal(total.denominator)
    return str(value.quantize(Decimal("0.00000001"), rounding=ROUND_HALF_UP))


if __name__ == "__main__":
    print(solve())
