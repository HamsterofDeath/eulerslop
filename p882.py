#!/usr/bin/env python3
"""Project Euler 882: dyadic values of a partisan deletion game."""

from fractions import Fraction


LIMIT = 100_000


def simplest_dyadic(
    left: Fraction | None,
    right: Fraction | None,
    maximum_denominator_power: int,
) -> Fraction:
    """Return the simplest dyadic strictly between two game values."""
    if left is None and right is None:
        return Fraction(0)
    if right is None:
        assert left is not None
        return Fraction(left.numerator // left.denominator + 1)
    if left is None:
        return Fraction((right.numerator - 1) // right.denominator)

    for exponent in range(maximum_denominator_power + 1):
        denominator = 1 << exponent
        first_numerator = (
            left.numerator * denominator // left.denominator + 1
        )
        last_numerator = (
            (
                right.numerator * denominator
                + right.denominator
                - 1
            )
            // right.denominator
            - 1
        )
        if first_numerator <= last_numerator:
            return Fraction(first_numerator, denominator)
    raise AssertionError("dyadic search bound was insufficient")


def game_values(limit: int) -> list[Fraction]:
    """Compute the surreal-number value of every binary string up to limit."""
    values = [Fraction(0)] * (limit + 1)
    denominator_bound = limit.bit_length() + 1

    for number in range(1, limit + 1):
        binary = f"{number:b}"
        left_options: list[Fraction] = []
        right_options: list[Fraction] = []

        for index, digit in enumerate(binary):
            remainder = binary[:index] + binary[index + 1 :]
            follower = int(remainder, 2) if remainder else 0
            if digit == "1":
                left_options.append(values[follower])
            else:
                right_options.append(values[follower])

        left = max(left_options) if left_options else None
        right = min(right_options) if right_options else None
        values[number] = simplest_dyadic(
            left,
            right,
            denominator_bound,
        )

    return values


def minimum_skips(limit: int) -> int:
    """Return S(limit).

    Each single-number game is a (positive) dyadic number: its Left
    options delete a one and its Right options delete a zero.  Disjoint
    games add, and one paid pass offsets one unit of positive game value.
    Therefore Zero needs the ceiling of the total value of all copies.
    """
    values = game_values(limit)
    total = sum(
        (multiplicity * values[multiplicity]
         for multiplicity in range(1, limit + 1)),
        Fraction(0),
    )
    return (total.numerator + total.denominator - 1) // total.denominator


def solve() -> int:
    assert minimum_skips(2) == 2
    assert minimum_skips(5) == 17
    assert minimum_skips(10) == 64
    return minimum_skips(LIMIT)


if __name__ == "__main__":
    print(solve())
