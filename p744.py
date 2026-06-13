#!/usr/bin/env python3
"""Project Euler 744: expected duration before the red card."""

from decimal import Decimal, ROUND_HALF_UP, getcontext
from fractions import Fraction


TARGET_N = 10**11
TARGET_P = Fraction(4999, 10_000)


def exact_probability(n: int, p: Fraction) -> Fraction:
    q = 1 - p
    expected_time = Fraction(0)

    expert_term = p**n
    viewer_term = q**n
    for other_score in range(n):
        if other_score > 0:
            expert_term *= Fraction(n + other_score - 1, other_score) * q
            viewer_term *= Fraction(n + other_score - 1, other_score) * p
        expected_time += (n + other_score) * (expert_term + viewer_term)

    return 1 - expected_time / (2 * n + 1)


def target_probability(n: int, p: Fraction) -> Decimal:
    getcontext().prec = 50
    q = Decimal(p.denominator - p.numerator) / Decimal(p.denominator)
    return Decimal(1) - Decimal(n) / (q * Decimal(2 * n + 1))


def rounded(value: Decimal) -> str:
    return str(value.quantize(Decimal("0.0000000001"), rounding=ROUND_HALF_UP))


def solve() -> str:
    assert rounded(Decimal(exact_probability(6, Fraction(1, 2)).numerator) / Decimal(exact_probability(6, Fraction(1, 2)).denominator)) == "0.2851562500"
    p = exact_probability(10, Fraction(3, 7))
    assert rounded(Decimal(p.numerator) / Decimal(p.denominator)) == "0.2330040743"
    assert rounded(target_probability(10_000, Fraction(3, 10))) == "0.2857499982"
    return rounded(target_probability(TARGET_N, TARGET_P))


if __name__ == "__main__":
    print(solve())
