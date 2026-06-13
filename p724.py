#!/usr/bin/env python3
"""Project Euler 724: coupon-collector package distances."""

from decimal import Decimal, ROUND_HALF_UP, getcontext
from fractions import Fraction


N = 10**8
CONSTANT_SUM_LIMIT = 10_000


def exact_expectation(n: int) -> Fraction:
    h1 = sum(Fraction(1, k) for k in range(1, n + 1))
    h2 = sum(Fraction(1, k * k) for k in range(1, n + 1))
    return Fraction(n, 2) * (h1 * h1 + h2)


def constants() -> tuple[Decimal, Decimal]:
    m = Decimal(CONSTANT_SUM_LIMIT)
    h1 = sum(Decimal(1) / Decimal(k) for k in range(1, CONSTANT_SUM_LIMIT + 1))
    h2 = sum(Decimal(1) / (Decimal(k) * Decimal(k)) for k in range(1, CONSTANT_SUM_LIMIT + 1))

    gamma = (
        h1
        - m.ln()
        - Decimal(1) / (2 * m)
        + Decimal(1) / (12 * m**2)
        - Decimal(1) / (120 * m**4)
        + Decimal(1) / (252 * m**6)
        - Decimal(1) / (240 * m**8)
    )
    zeta2 = (
        h2
        + Decimal(1) / m
        - Decimal(1) / (2 * m**2)
        + Decimal(1) / (6 * m**3)
        - Decimal(1) / (30 * m**5)
        + Decimal(1) / (42 * m**7)
        - Decimal(1) / (30 * m**9)
    )
    return gamma, zeta2


def harmonic_asymptotics(n: int, gamma: Decimal, zeta2: Decimal) -> tuple[Decimal, Decimal]:
    x = Decimal(n)
    h1 = (
        x.ln()
        + gamma
        + Decimal(1) / (2 * x)
        - Decimal(1) / (12 * x**2)
        + Decimal(1) / (120 * x**4)
        - Decimal(1) / (252 * x**6)
        + Decimal(1) / (240 * x**8)
    )
    h2 = (
        zeta2
        - Decimal(1) / x
        + Decimal(1) / (2 * x**2)
        - Decimal(1) / (6 * x**3)
        + Decimal(1) / (30 * x**5)
        - Decimal(1) / (42 * x**7)
        + Decimal(1) / (30 * x**9)
    )
    return h1, h2


def expected_distance(n: int) -> Decimal:
    gamma, zeta2 = constants()
    h1, h2 = harmonic_asymptotics(n, gamma, zeta2)
    return Decimal(n) * (h1 * h1 + h2) / 2


def solve() -> int:
    getcontext().prec = 80
    assert exact_expectation(2) == Fraction(7, 2)
    assert exact_expectation(5) == Fraction(12019, 720)
    return int(expected_distance(N).to_integral_value(rounding=ROUND_HALF_UP))


if __name__ == "__main__":
    print(solve())
