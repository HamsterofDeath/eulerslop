#!/usr/bin/env python3
"""Project Euler 700: Eulercoin."""


STEP = 1_504_170_715_041_707
MODULUS = 4_503_599_627_370_517
INVERSE_STEP = pow(STEP, -1, MODULUS)
SMALL_SCAN_LIMIT = 20_000_000


def solve():
    total = 0
    value = 0
    best = MODULUS

    while best > SMALL_SCAN_LIMIT:
        value = (value + STEP) % MODULUS
        if value < best:
            best = value
            total += value

    best_index = MODULUS
    for coin in range(1, best):
        index = (INVERSE_STEP * coin) % MODULUS
        if index < best_index:
            best_index = index
            total += coin

    return total


if __name__ == "__main__":
    print(solve())
