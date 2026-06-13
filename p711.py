#!/usr/bin/env python3

MOD = 1_000_000_007
INV3 = pow(3, MOD - 2, MOD)
INV7 = pow(7, MOD - 2, MOD)


def _geom_pow2(step_power, terms):
    if terms <= 0:
        return 0
    ratio = pow(2, step_power, MOD)
    return ratio * (pow(ratio, terms, MOD) - 1) * pow(ratio - 1, MOD - 2, MOD)


def _even_block_sum(max_m):
    """Sum Eric-winning values in blocks [2^(2m), 2^(2m+1))."""
    if max_m < 0:
        return 0

    if max_m == 0:
        return 1

    m = max_m
    sum_8 = _geom_pow2(3, m)
    sum_8_half = 4 * (pow(8, m, MOD) - 1) * INV7
    sum_2_prev = pow(2, m, MOD) - 1
    sum_4 = 4 * (pow(4, m, MOD) - 1) * INV3
    sum_2 = pow(2, m + 1, MOD) - 2

    return (1 + sum_8 + (sum_8_half - sum_2_prev) * INV3 + sum_4 - sum_2) % MOD


def _odd_block_sum(max_j):
    """Sum Eric-winning values 2^(2j+2)-1 from odd-indexed blocks."""
    if max_j < 0:
        return 0

    terms = max_j + 1
    powers = 4 * (pow(4, terms, MOD) - 1) * INV3
    return (powers - terms) % MOD


def solve(n=12_345_678):
    max_even_m = (n - 1) // 2
    max_odd_j = (n - 2) // 2
    total = _even_block_sum(max_even_m) + _odd_block_sum(max_odd_j)

    if n % 2 == 0:
        total += pow(2, n, MOD)

    return total % MOD


if __name__ == "__main__":
    print(solve())
