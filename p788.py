#!/usr/bin/env python3
"""Project Euler 788: dominating numbers."""


MOD = 1_000_000_007


def build_combinations(limit: int) -> list[list[int]]:
    choose = [[0] * (limit + 1) for _ in range(limit + 1)]
    choose[0][0] = 1
    for n in range(1, limit + 1):
        choose[n][0] = choose[n][n] = 1
        for k in range(1, n):
            choose[n][k] = (choose[n - 1][k - 1] + choose[n - 1][k]) % MOD
    return choose


def dominant_count(limit: int) -> int:
    choose = build_combinations(limit)
    pow9 = [1] * (limit + 1)
    for i in range(1, limit + 1):
        pow9[i] = pow9[i - 1] * 9 % MOD

    total = 0
    for length in range(1, limit + 1):
        for copies in range(length // 2 + 1, length + 1):
            nonzero_digit = choose[length - 1][copies - 1] * pow9[length - copies]
            if copies <= length - 1:
                nonzero_digit += 8 * choose[length - 1][copies] * pow9[length - 1 - copies]
            zero_digit = 0
            if copies <= length - 1:
                zero_digit = choose[length - 1][copies] * pow9[length - copies]
            total = (total + 9 * nonzero_digit + zero_digit) % MOD
    return total


def solve() -> int:
    assert dominant_count(4) == 603
    assert dominant_count(10) == 21_893_256
    return dominant_count(2022)


if __name__ == "__main__":
    print(solve())
