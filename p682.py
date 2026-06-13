#!/usr/bin/env python3
"""Project Euler 682: 5-smooth pairs."""

MOD = 1_000_000_007
TARGET = 10_000_000
# LCM of the nonzero 2x2 minors for the exponent-count/prime-sum system.
PERIOD = 840
DEGREE = 4


def _triangle(n: int) -> int:
    return (n + 1) * (n + 2) // 2 if n >= 0 else 0


def _coefficient(a: int, b: int, c: int, k: int) -> int:
    """Coefficient of t^k in (1+...+t^a)(1+...+t^b)(1+...+t^c)."""

    return (
        _triangle(k)
        - _triangle(k - a - 1)
        - _triangle(k - b - 1)
        - _triangle(k - c - 1)
        + _triangle(k - a - b - 2)
        + _triangle(k - a - c - 2)
        + _triangle(k - b - c - 2)
        - _triangle(k - a - b - c - 3)
    )


def _exact_value(n: int) -> int:
    total = 0
    for c_sum in range(n // 5 + 1):
        max_b_sum = (n - 5 * c_sum) // 3
        first_b_sum = (n - 3 * c_sum) & 3

        for b_sum in range(first_b_sum, max_b_sum + 1, 4):
            omega = (n - b_sum - 3 * c_sum) // 4
            a_sum = (n - 3 * b_sum - 5 * c_sum) // 2
            total += _coefficient(a_sum, b_sum, c_sum, omega)

    return total


def _interpolate_mod(values: list[int], x: int) -> int:
    result = 0
    for i, value in enumerate(values):
        numerator = 1
        denominator = 1
        for j in range(len(values)):
            if i == j:
                continue
            numerator = numerator * (x - j) % MOD
            denominator = denominator * (i - j) % MOD
        result = (result + value * numerator * pow(denominator, -1, MOD)) % MOD
    return result


def solve():
    residue = TARGET % PERIOD
    x = (TARGET - residue) // PERIOD
    values = [
        _exact_value(residue + PERIOD * i) % MOD
        for i in range(DEGREE + 1)
    ]
    return _interpolate_mod(values, x)


if __name__ == "__main__":
    print(solve())
