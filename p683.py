#!/usr/bin/env python3
"""Project Euler 683: The Chase II."""

import math


LIMIT = 500


def _round_payment_expectation(players):
    total = 0.0
    weighted = 0.0

    for j in range(1, players):
        angle = 2.0 * math.pi * j / players
        eigenvalue = ((1.0 + 2.0 * math.cos(angle)) / 3.0) ** 2
        gap = 1.0 - eigenvalue
        total += 1.0 / gap
        weighted += eigenvalue / (gap * gap)

    return 2.0 * (total * total + weighted) + total


def _format_scientific(value):
    mantissa, exponent = f"{value:.8e}".split("e")
    return f"{mantissa}e{int(exponent)}"


def solve():
    expected_total = sum(_round_payment_expectation(players) for players in range(2, LIMIT + 1))
    return _format_scientific(expected_total)


if __name__ == "__main__":
    print(solve())
