#!/usr/bin/env python3
"""Project Euler 842: intersection counts over Hamiltonian cycles.

Each crossing of two diagonals corresponds to one cyclically ordered vertex
quadruple.  If m diagonals concur, the same geometric point therefore occurs
C(m, 2) times among all quadruples.  Recover those multiplicities, then count
Hamiltonian cycles containing at least two edges from each size-m matching.
"""

from math import comb, cos, factorial, isqrt, pi, sin


MOD = 1_000_000_007
INV2 = (MOD + 1) // 2
FACT = [factorial(i) % MOD for i in range(70)]


def cycles_containing_at_least_two(n: int, group_size: int) -> int:
    total = 0
    for j in range(2, group_size + 1):
        value = comb(group_size, j) * pow(2, j, MOD) % MOD
        value = value * FACT[n - j - 1] % MOD * INV2 % MOD
        total += (1 if j % 2 == 0 else -1) * (j - 1) * value
    return total % MOD


def intersection_multiplicities(n: int) -> dict[int, int]:
    """Return {number of concurrent diagonals: number of such points}."""
    points = [(cos(2 * pi * i / n), sin(2 * pi * i / n)) for i in range(n)]
    # This tolerance joins round-off variants of a true concurrence.  The
    # triangular-number check below detects a split or accidental merge.
    scale = 10**9
    pair_counts: dict[tuple[int, int], int] = {}

    # For a < b < c < d, diagonals (a,c) and (b,d) cross exactly once.
    for a in range(n - 3):
        x1, y1 = points[a]
        for b in range(a + 1, n - 2):
            x3, y3 = points[b]
            offset_x = x3 - x1
            offset_y = y3 - y1
            for c in range(b + 1, n - 1):
                x2, y2 = points[c]
                first_x = x2 - x1
                first_y = y2 - y1
                for d in range(c + 1, n):
                    x4, y4 = points[d]
                    second_x = x4 - x3
                    second_y = y4 - y3
                    denominator = first_x * second_y - first_y * second_x
                    parameter = (
                        offset_x * second_y - offset_y * second_x
                    ) / denominator
                    x = x1 + parameter * first_x
                    y = y1 + parameter * first_y
                    key = (round(x * scale), round(y * scale))
                    pair_counts[key] = pair_counts.get(key, 0) + 1

    distribution: dict[int, int] = {}
    for pairs in pair_counts.values():
        root = isqrt(1 + 8 * pairs)
        if root * root != 1 + 8 * pairs:
            raise ArithmeticError("intersection clustering lost a concurrence")
        multiplicity = (1 + root) // 2
        distribution[multiplicity] = distribution.get(multiplicity, 0) + 1
    return distribution


def t_value(n: int) -> int:
    return sum(
        point_count * cycles_containing_at_least_two(n, multiplicity)
        for multiplicity, point_count in intersection_multiplicities(n).items()
    ) % MOD


def solve() -> int:
    assert t_value(5) == 20
    assert t_value(8) == 14640
    return sum(t_value(n) for n in range(3, 61)) % MOD


if __name__ == "__main__":
    print(solve())
