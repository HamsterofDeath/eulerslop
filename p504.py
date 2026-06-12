#!/usr/bin/env python3
from collections import Counter
from math import gcd, isqrt


def count_quadrilaterals(m):
    squares = {i * i for i in range(1, isqrt(2 * m * m) + 3)}
    total = 0

    for a in range(1, m + 1):
        for c in range(1, m + 1):
            ac = a + c
            # Pick's theorem gives
            # I = (sum(edge rectangle areas - edge gcds)) / 2 + 1.
            values = Counter(
                b * ac - gcd(a, b) - gcd(b, c)
                for b in range(1, m + 1)
            )
            for x, count_x in values.items():
                for sq in squares:
                    total += count_x * values.get(2 * (sq - 1) - x, 0)

    return total


def solve():
    assert count_quadrilaterals(4) == 42
    return count_quadrilaterals(100)


if __name__ == "__main__":
    print(solve())
