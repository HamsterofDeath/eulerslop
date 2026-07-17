#!/usr/bin/env python3
"""Project Euler 821: 123-separable sets."""

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


def exceptional_smooth(limit: int) -> set[int]:
    """Smooth points that cannot be covered in an optimal component packing."""
    values = {value for value in (6, 24, 54) if value <= limit}

    value = 384
    while value <= limit:
        values.add(value)
        value *= 8

    value = 243
    while value <= limit:
        values.add(value)
        value *= 27

    return values


def coprime_to_6_count(limit: int) -> int:
    if limit <= 0:
        return 0
    return limit - limit // 2 - limit // 3 + limit // 6


def f_value(limit: int) -> int:
    thresholds = smooth_2_3(limit)
    exceptions = exceptional_smooth(limit)
    total = 0
    component_value = 0

    for index, low in enumerate(thresholds):
        # The exact maximum for one 2^a*3^b component is the number of
        # smooth points seen so far, minus the explicit exceptional points.
        if low not in exceptions:
            component_value += 1

        high = thresholds[index + 1] - 1 if index + 1 < len(thresholds) else limit
        left = limit // (high + 1) + 1 if high < limit else 1
        right = limit // low
        if left <= right:
            bases = coprime_to_6_count(right) - coprime_to_6_count(left - 1)
            total += bases * component_value
    return total


def solve() -> int:
    assert f_value(6) == 5
    assert f_value(20) == 19
    return f_value(LIMIT)


if __name__ == "__main__":
    print(solve())
