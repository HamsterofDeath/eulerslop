#!/usr/bin/env python3
"""Project Euler 847: three-plate search capacities."""

from functools import cache


MOD = 1_000_000_007
INV2 = (MOD + 1) // 2
INV6 = pow(6, -1, MOD)
TARGET = (10**19 - 1) // 9


def sum_linear(k: int) -> int:
    return k % MOD * ((k + 1) % MOD) % MOD * INV2 % MOD


def sum_squares(k: int) -> int:
    return k % MOD * ((k + 1) % MOD) % MOD * ((2 * k + 1) % MOD) % MOD * INV6 % MOD


def sum_shifted_choose2(offset: int, count: int, coefficient: int) -> int:
    """Sum C(offset + coefficient*e + 2, 2) for 1 <= e <= count."""
    if count <= 0:
        return 0

    h = offset % MOD
    k = count % MOD
    c = coefficient % MOD
    total = k * (h * h + 3 * h + 2) % MOD
    total += c * (2 * h + 3) % MOD * sum_linear(count)
    total += c * c % MOD * sum_squares(count)
    return total * INV2 % MOD


def low_bad(high: int, limit: int) -> int:
    """Bad triples where all plates are below the current high capacity."""
    max_sum = min(limit, 2 * high)
    excess_count = max_sum - high
    if excess_count <= 0:
        return 0

    fixed = (high + 2) % MOD * ((high + 1) % MOD) % MOD * INV2 % MOD
    total = sum_shifted_choose2(high, excess_count, 1)
    total -= 3 * (excess_count % MOD) % MOD * fixed
    total += 3 * sum_shifted_choose2(high, excess_count, -1)
    total -= sum_shifted_choose2(high, min(excess_count, high // 2), -2)
    return total % MOD


@cache
def bad_count(questions: int, limit: int) -> int:
    """Triples with sum <= limit needing one more than ceil(log2(sum)) questions."""
    if questions <= 2 or limit <= 0:
        return 0

    high = 1 << (questions - 1)
    limit = min(limit, 2 * high)
    return (3 * bad_count(questions - 1, limit - high) + low_bad(high, limit)) % MOD


def choose3(n: int) -> int:
    return n % MOD * ((n - 1) % MOD) % MOD * ((n - 2) % MOD) % MOD * INV6 % MOD


def triples_up_to(limit: int) -> int:
    if limit <= 0:
        return 0
    return (choose3(limit + 3) - 1) % MOD


def h_sum(limit: int) -> int:
    total = 0
    questions = 1
    while (1 << (questions - 1)) < limit:
        lower = 1 << (questions - 1)
        upper = min(limit, 1 << questions)
        total += questions * (triples_up_to(upper) - triples_up_to(lower))
        total += bad_count(questions, upper)
        total %= MOD
        questions += 1
    return total


def solve() -> int:
    assert h_sum(6) == 203
    assert h_sum(20) == 7718
    assert h_sum(111) == 1_634_144
    return h_sum(TARGET)


if __name__ == "__main__":
    print(solve())
