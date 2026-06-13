#!/usr/bin/env python3
"""Project Euler 686: Powers of Two."""

import math


LEADING_DIGITS = 123
TARGET_OCCURRENCE = 678_910


def _power_index_with_prefix(prefix, occurrence):
    digits = len(str(prefix))
    lower = math.log10(prefix) - digits + 1
    upper = math.log10(prefix + 1) - digits + 1
    step = math.log10(2)

    fractional = 0.0
    found = 0
    exponent = 0
    while found < occurrence:
        exponent += 1
        fractional += step
        if fractional >= 1.0:
            fractional -= 1.0
        if lower <= fractional < upper:
            found += 1

    return exponent


def solve():
    return _power_index_with_prefix(LEADING_DIGITS, TARGET_OCCURRENCE)


if __name__ == "__main__":
    print(solve())
