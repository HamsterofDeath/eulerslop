#!/usr/bin/env python3
"""Project Euler 831: leading base-7 digits from a coefficient formula."""

from fractions import Fraction
from math import comb


def multiply(a: list[Fraction], b: list[Fraction]) -> list[Fraction]:
    result = [Fraction(0) for _ in range(6)]
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            if i + j < 6:
                result[i + j] += x * y
    return result


def reduced_coefficient(m: int) -> int:
    # The double finite difference gives
    # g(m) = [z^5] (1+z)^5 (7+21z+35z^2+35z^3+21z^4+7z^5+z^6)^m.
    # Thus g(m) = 7^m * P(m), and only P(m) determines the leading base-7
    # digits.
    base = [Fraction(x, 7) for x in (7, 21, 35, 35, 21, 7)]
    result = [Fraction(1), Fraction(0), Fraction(0), Fraction(0), Fraction(0), Fraction(0)]
    exponent = m
    while exponent:
        if exponent & 1:
            result = multiply(result, base)
        base = multiply(base, base)
        exponent >>= 1

    prefix = [Fraction(comb(5, i)) for i in range(6)]
    value = multiply(prefix, result)[5]
    assert value.denominator == 1
    return value.numerator


def to_base7(n: int) -> str:
    digits = []
    while n:
        digits.append(str(n % 7))
        n //= 7
    return "".join(reversed(digits)) or "0"


def solve() -> str:
    assert reduced_coefficient(10) * 7**10 == 127278262644918
    return to_base7(reduced_coefficient(142857))[:10]


if __name__ == "__main__":
    print(solve())
