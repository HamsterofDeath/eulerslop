#!/usr/bin/env python3
"""Project Euler 822: repeated squaring by logarithmic merge order."""

from math import floor, log2, log


MOD = 1_234_567_891


def selected_counts(n: int, rounds: int) -> dict[int, int]:
    entries = []
    floor_sum = 0
    for a in range(2, n + 1):
        value = log2(log(a))
        whole = floor(value)
        entries.append((value - whole, a, whole))
        floor_sum += whole

    count = n - 1
    base = (rounds + floor_sum) // count
    extra = rounds - (count * base - floor_sum)
    entries.sort()

    result = {}
    for index, (_, a, whole) in enumerate(entries):
        result[a] = base - whole + (1 if index < extra else 0)
    return result


def s_value(n: int, rounds: int) -> int:
    total = 0
    for a, k in selected_counts(n, rounds).items():
        total += pow(a, pow(2, k, MOD - 1), MOD)
    return total % MOD


def solve() -> int:
    assert s_value(5, 3) == 34
    assert s_value(10, 100) == 845339386
    return s_value(10_000, 10**16)


if __name__ == "__main__":
    print(solve())
