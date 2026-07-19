#!/usr/bin/env python3
"""Project Euler Problem 984: Knights and Horses.

The horse-disjoint closure rule forces every non-singleton connected
set into one of finitely many boundary types.  Counting their placements
gives, from board size 4 onward, a degree-eight quasi-polynomial of
period two:

    f(n) = A(n) - (-1)^n * (2n + 3) / 256,

where A is the rational polynomial encoded below.  The requested board
size is even, but the full quasi-polynomial is retained to check both
parities against the supplied examples.
"""

from fractions import Fraction


MODULUS = 1_000_000_007
TARGET = 10**18

# (power, numerator, denominator) for A(n).
POLYNOMIAL_TERMS = (
    (8, 31, 40_320),
    (7, 31, 3_360),
    (6, 67, 1_440),
    (5, 41, 320),
    (4, 313, 1_440),
    (3, -5_699, 240),
    (2, 16_049, 420),
    (1, 941_251, 4_480),
    (0, -107_261, 256),
)


def exact_count(board_size: int) -> int:
    if board_size < 4:
        return board_size * board_size

    value = sum(
        Fraction(numerator, denominator) * board_size**power
        for power, numerator, denominator in POLYNOMIAL_TERMS
    )
    parity = 1 if board_size % 2 == 0 else -1
    value -= parity * Fraction(2 * board_size + 3, 256)
    if value.denominator != 1:
        raise ArithmeticError("counting formula did not produce an integer")
    return value.numerator


def modular_count(board_size: int) -> int:
    if board_size < 4:
        return board_size * board_size % MODULUS

    reduced_size = board_size % MODULUS
    value = 0
    for power, numerator, denominator in POLYNOMIAL_TERMS:
        term = numerator * pow(reduced_size, power, MODULUS)
        term *= pow(denominator, -1, MODULUS)
        value += term

    parity = 1 if board_size % 2 == 0 else -1
    correction = parity * (2 * reduced_size + 3)
    correction *= pow(256, -1, MODULUS)
    return (value - correction) % MODULUS


def solve() -> int:
    assert exact_count(3) == 9
    assert exact_count(5) == 903
    assert exact_count(100) == 8_658_918_531_876
    assert modular_count(10_000) == 377_956_308
    return modular_count(TARGET)


if __name__ == "__main__":
    print(solve())
