#!/usr/bin/env python3
"""Project Euler 676: matching digit sums in power-of-two bases."""

from functools import cache


LIMIT = 10**16
MOD = 10**16


def M(limit: int, high_bits: int, low_bits: int) -> int:
    bit_count = limit.bit_length()
    weights = [
        (1 << (position % high_bits)) - (1 << (position % low_bits))
        for position in range(bit_count)
    ]
    powers = [(1 << position) % MOD for position in range(bit_count)]

    @cache
    def search(position: int, tight: bool, difference: int) -> tuple[int, int]:
        if position < 0:
            return (1, 0) if difference == 0 else (0, 0)

        max_bit = (limit >> position) & 1 if tight else 1
        count = 0
        value_sum = 0

        for bit in range(max_bit + 1):
            sub_count, sub_sum = search(
                position - 1,
                tight and bit == max_bit,
                difference + bit * weights[position],
            )
            count += sub_count
            value_sum = (value_sum + sub_sum + bit * powers[position] * sub_count) % MOD

        return count, value_sum

    return search(bit_count - 1, True, 0)[1]


def solve() -> int:
    answer = 0
    for high_bits in range(3, 7):
        for low_bits in range(1, high_bits - 1):
            answer = (answer + M(LIMIT, high_bits, low_bits)) % MOD
    return answer


if __name__ == "__main__":
    print(solve())
