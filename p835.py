#!/usr/bin/env python3
"""Project Euler 835: supernatural Pythagorean triangles."""

from decimal import Decimal, ROUND_FLOOR, getcontext


MOD = 1_234_567_891
EXPONENT = 10_000_000_000


def brute_sum(limit: int) -> int:
    total = 0
    n = 1
    while True:
        perimeter = 2 * (n + 1) * (2 * n + 1)
        if perimeter > limit:
            break
        total += perimeter
        n += 1

    x, y = 1, 1
    while True:
        perimeter = 2 * (x + y) * (x + 2 * y)
        if perimeter > limit:
            break
        total += perimeter
        x, y = x + 2 * y, x + y

    if limit >= 12:
        total -= 12  # 3-4-5 occurs in both families.
    return total


def polynomial_family_sum() -> int:
    # 2(n+1)(2n+1) <= 10^E gives K = 5*10^(E/2-1)-1 because E is even.
    k = (5 * pow(10, EXPONENT // 2 - 1, MOD) - 1) % MOD
    return (
        4 * k * (k + 1) % MOD * (2 * k + 1) * pow(6, -1, MOD)
        + 6 * k * (k + 1) % MOD * pow(2, -1, MOD)
        + 2 * k
    ) % MOD


def mat_mul(a: list[list[int]], b: list[list[int]]) -> list[list[int]]:
    return [
        [sum(a[i][k] * b[k][j] for k in range(3)) % MOD for j in range(3)]
        for i in range(3)
    ]


def mat_pow(matrix: list[list[int]], exponent: int) -> list[list[int]]:
    result = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    while exponent:
        if exponent & 1:
            result = mat_mul(result, matrix)
        matrix = mat_mul(matrix, matrix)
        exponent >>= 1
    return result


def pell_family_count() -> int:
    getcontext().prec = 120
    sqrt2 = Decimal(2).sqrt()
    lam = Decimal(3) + 2 * sqrt2
    coeff = (Decimal(70) - Decimal(12) / lam) / (lam - 1 / lam)
    estimate = ((Decimal(EXPONENT) - coeff.log10()) / lam.log10()).to_integral_value(
        rounding=ROUND_FLOOR
    )
    return int(estimate) + 1


def pell_family_sum(count: int) -> int:
    if count <= 0:
        return 0
    if count == 1:
        return 12
    # P_k = 6P_{k-1} - P_{k-2}; state is [P_k, P_{k-1}, sum_to_k].
    transition = [[6, -1 % MOD, 0], [1, 0, 0], [6, -1 % MOD, 1]]
    power = mat_pow(transition, count - 2)
    initial = [70, 12, 82]
    return sum(power[2][i] * initial[i] for i in range(3)) % MOD


def solve() -> int:
    assert brute_sum(100) == 258
    assert brute_sum(10_000) == 172004
    return (polynomial_family_sum() + pell_family_sum(pell_family_count()) - 12) % MOD


if __name__ == "__main__":
    print(solve())
