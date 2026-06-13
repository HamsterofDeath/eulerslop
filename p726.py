#!/usr/bin/env python3
"""Project Euler 726: falling bottles."""


MOD = 1_000_000_033
LIMIT = 10_000


def values(limit: int) -> list[int]:
    result = []
    previous_cells = 0
    factorial_segment = 1
    collapse_product = 1
    power_of_two = 1
    current_f = 1

    for n in range(1, limit + 1):
        cells = n * (n + 1) // 2
        factorial_segment = 1
        for x in range(previous_cells + 1, cells + 1):
            factorial_segment = factorial_segment * x % MOD

        # Hook lengths for the staircase poset are odd numbers 2k-1.
        # Collapse choices from height k contribute 2^k-1 downward paths.
        power_of_two = power_of_two * 2 % MOD
        collapse_product = (
            collapse_product
            * (power_of_two - 1)
            * pow(2 * n - 1, MOD - 2, MOD)
        ) % MOD

        current_f = current_f * factorial_segment % MOD * collapse_product % MOD
        result.append(current_f)
        previous_cells = cells

    return result


def solve() -> int:
    first_values = values(3)
    assert first_values == [1, 6, 1008]
    return sum(values(LIMIT)) % MOD


if __name__ == "__main__":
    print(solve())
