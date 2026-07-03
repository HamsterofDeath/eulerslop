#!/usr/bin/env python3
"""Project Euler 811: sparse bits and gap products."""

from functools import cache
from math import comb


MOD = 1_000_062_031
TARGET_T = 10**14 + 31
TARGET_R = 62


def bit_exponents_of_power(t: int, r: int) -> list[int]:
    exponents = []
    for j in range(r + 1):
        coefficient = comb(r, j)
        bit = 0
        while coefficient:
            if coefficient & 1:
                exponents.append(j * t + bit)
            coefficient >>= 1
            bit += 1
    return sorted(exponents)


def value_from_exponents(exponents: list[int], modulus: int = MOD) -> int:
    count = len(exponents)
    lambdas = [0] * (count + 1)
    lambdas[1] = 8 % modulus
    for i in range(2, count + 1):
        lambdas[i] = (5 * lambdas[i - 1] + 3) % modulus

    result = pow(lambdas[count], exponents[0], modulus)
    for i in range(1, count):
        gap = exponents[i] - exponents[i - 1] - 1
        result = result * pow(lambdas[count - i], gap, modulus) % modulus
    return result


@cache
def direct_a(n: int) -> int:
    if n == 0:
        return 1
    if n & 1:
        return direct_a(n // 2) % MOD
    half = n // 2
    return (3 * direct_a(half) + 5 * direct_a(n - (half & -half))) % MOD


def set_bit_exponents(n: int) -> list[int]:
    return [bit for bit in range(n.bit_length()) if (n >> bit) & 1]


def solve() -> int:
    assert value_from_exponents(bit_exponents_of_power(3, 2)) == 636_056
    for n in range(1, 500):
        assert direct_a(n) == value_from_exponents(set_bit_exponents(n))
    return value_from_exponents(bit_exponents_of_power(TARGET_T, TARGET_R))


if __name__ == "__main__":
    print(solve())
