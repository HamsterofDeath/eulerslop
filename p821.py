#!/usr/bin/env python3
"""Project Euler 821: 123-separable sets."""

from math import gcd


LIMIT = 10**16


def smooth_2_3(limit: int) -> list[int]:
    values = set()
    power2 = 1
    while power2 <= limit:
        value = power2
        while value <= limit:
            values.add(value)
            value *= 3
        power2 *= 2
    return sorted(values)


def component_value(limit: int) -> int:
    # A component consists of m*2^a*3^b for fixed gcd(m, 6) = 1.
    # Choosing one (a mod 2, b mod 2) class is 123-separable and covers all
    # component points except the opposite parity class; the best class is optimal.
    totals = [[0, 0], [0, 0]]
    power2 = 1
    a = 0
    while power2 <= limit:
        value = power2
        b = 0
        while value <= limit:
            weight = 1 + (2 * value <= limit) + (3 * value <= limit)
            totals[a & 1][b & 1] += weight
            value *= 3
            b += 1
        power2 *= 2
        a += 1
    return max(max(row) for row in totals)


def coprime_to_6_count(limit: int) -> int:
    if limit <= 0:
        return 0
    return limit - limit // 2 - limit // 3 + limit // 6


def f_value(limit: int) -> int:
    thresholds = smooth_2_3(limit)
    total = 0
    for index, low in enumerate(thresholds):
        high = thresholds[index + 1] - 1 if index + 1 < len(thresholds) else limit
        left = limit // (high + 1) + 1 if high < limit else 1
        right = limit // low
        if left <= right:
            bases = coprime_to_6_count(right) - coprime_to_6_count(left - 1)
            total += bases * component_value(low)
    return total


def solve() -> int:
    assert f_value(6) == 5
    assert f_value(20) == 19
    return f_value(LIMIT)


if __name__ == "__main__":
    print(solve())
