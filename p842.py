#!/usr/bin/env python3
"""Project Euler 842: intersection counts over Hamiltonian cycles."""

from math import comb, cos, factorial, pi, sin


MOD = 1_000_000_007
INV2 = (MOD + 1) // 2
FACT = [factorial(i) % MOD for i in range(70)]


def crossing(a: int, b: int, c: int, d: int) -> bool:
    if len({a, b, c, d}) < 4:
        return False
    if a > b:
        a, b = b, a
    return (a < c < b) != (a < d < b)


def intersection(p1, p2, p3, p4) -> tuple[float, float]:
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3
    x4, y4 = p4
    den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    a = x1 * y2 - y1 * x2
    b = x3 * y4 - y3 * x4
    return (
        round((a * (x3 - x4) - (x1 - x2) * b) / den, 10),
        round((a * (y3 - y4) - (y1 - y2) * b) / den, 10),
    )


def cycles_containing_at_least_two(n: int, group_size: int) -> int:
    total = 0
    for j in range(2, group_size + 1):
        value = comb(group_size, j) * pow(2, j, MOD) % MOD
        value = value * FACT[n - j - 1] % MOD * INV2 % MOD
        total += (1 if j % 2 == 0 else -1) * (j - 1) * value
    return total % MOD


def t_value(n: int) -> int:
    points = [(cos(2 * pi * i / n), sin(2 * pi * i / n)) for i in range(n)]
    chords = [
        (i, j)
        for i in range(n)
        for j in range(i + 1, n)
        if j != i + 1 and not (i == 0 and j == n - 1)
    ]

    groups: dict[tuple[float, float], set[tuple[int, int]]] = {}
    for index, first in enumerate(chords):
        for second in chords[index + 1 :]:
            if crossing(first[0], first[1], second[0], second[1]):
                key = intersection(
                    points[first[0]], points[first[1]], points[second[0]], points[second[1]]
                )
                groups.setdefault(key, set()).update((first, second))

    return sum(cycles_containing_at_least_two(n, len(group)) for group in groups.values()) % MOD


def solve() -> int:
    assert t_value(5) == 20
    assert t_value(8) == 14640
    return sum(t_value(n) for n in range(3, 61)) % MOD


if __name__ == "__main__":
    print(solve())
