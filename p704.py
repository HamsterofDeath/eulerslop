#!/usr/bin/env python3
"""Project Euler 704: Factors of two in binomial coefficients."""


def _sum_floor_log2(limit):
    total = 0
    bit = 1
    exponent = 0

    while (bit << 1) <= limit:
        total += exponent * bit
        bit <<= 1
        exponent += 1

    return total + exponent * (limit - bit + 1)


def _sum_v2_factorial(limit):
    total = 0
    power = 2

    while power <= limit:
        total += limit // power
        power <<= 1

    return total


def _summatory(limit):
    if limit <= 0:
        return 0

    # F(n) is the maximum number of binary carries in m + (n-m).  A carry can
    # start at the least significant zero of n and run up to the top bit.
    return (
        _sum_floor_log2(limit)
        - _sum_v2_factorial(limit + 1)
        + (limit + 1).bit_length()
        - 1
    )


def solve():
    return _summatory(10**16)


if __name__ == "__main__":
    print(solve())
