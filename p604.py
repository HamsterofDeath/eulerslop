#!/usr/bin/env python3
from math import gcd, pi


def _totients(limit: int) -> list[int]:
    phi = list(range(limit + 1))
    for p in range(2, limit + 1):
        if phi[p] == p:
            for multiple in range(p, limit + 1, p):
                phi[multiple] -= phi[multiple] // p
    return phi


def _initial_limit(n: int) -> int:
    # sum_{k<=m} k*phi(k)/2 is asymptotic to m^3/pi^2.
    return max(64, int((pi * pi * n) ** (1 / 3) * 1.25) + 100)


def _has_one_more_vector(height: int, slack: int, budget: int) -> bool:
    """Can one primitive vector of height at least `height` fit in the square?"""
    for total in range(height, height + slack + 1):
        lo = max(1, total - budget)
        hi = min(budget, total - 1)
        if lo > hi:
            continue
        center = total // 2
        for delta in range(max(center - lo, hi - center) + 1):
            a = center - delta
            if lo <= a <= hi and gcd(a, total) == 1:
                return True
            a = center + 1 + delta
            if lo <= a <= hi and gcd(a, total) == 1:
                return True
    return False


def _partial_count(height: int, phi_height: int, remaining: int) -> int:
    count = min(phi_height, 2 * remaining // height)
    if count <= 0:
        return 0

    # Complementary primitive vectors (a,b), (b,a) have the same height and
    # exactly balanced coordinate cost.
    if count % 2 == 0:
        return count

    if height % 2 == 1:
        # The middle vector ((h-1)/2, (h+1)/2) is primitive when h is odd.
        return count

    slack = 2 * remaining - count * height
    paired_cost = (count - 1) * height // 2
    single_budget = remaining - paired_cost
    if _has_one_more_vector(height, slack, single_budget):
        return count

    return count - 1


def F(n: int) -> int:
    limit = _initial_limit(n)

    while True:
        phi = _totients(limit)
        used = 0
        count = 0

        for height in range(2, limit + 1):
            layer_cost = height * phi[height] // 2
            if used + layer_cost > n:
                return 1 + count + _partial_count(height, phi[height], n - used)
            used += layer_cost
            count += phi[height]

        limit *= 2


def solve() -> int:
    assert F(1) == 2
    assert F(3) == 3
    assert F(9) == 6
    assert F(11) == 7
    assert F(100) == 30
    assert F(50_000) == 1898
    return F(10**18)


if __name__ == "__main__":
    print(solve())
