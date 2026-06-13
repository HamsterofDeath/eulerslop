#!/usr/bin/env python3
"""Project Euler 684: Inverse Digit Sum."""


MOD = 1_000_000_007
FIBONACCI_LIMIT = 90


def _sum_minimal_digit_sum_numbers(k):
    full_blocks, remainder = divmod(k, 9)
    power = pow(10, full_blocks, MOD)

    complete = 6 * (power - 1) - 9 * full_blocks
    partial = remainder * (remainder + 3) // 2 * power - remainder
    return (complete + partial) % MOD


def solve():
    previous, current = 0, 1
    total = 0

    for index in range(2, FIBONACCI_LIMIT + 1):
        previous, current = current, previous + current
        total += _sum_minimal_digit_sum_numbers(current)

    return total % MOD


if __name__ == "__main__":
    print(solve())
