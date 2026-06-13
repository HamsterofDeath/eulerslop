#!/usr/bin/env python3
"""Project Euler 685: Inverse Digit Sum II."""

from math import comb


MOD = 1_000_000_007
LIMIT = 10_000


def _bounded_count(length, deficit):
    """Count length-tuples in [0, 9] with a given sum."""
    if deficit < 0 or length < 0:
        return 0
    if length == 0:
        return int(deficit == 0)

    total = 0
    for over_limit in range(deficit // 10 + 1):
        if over_limit > length:
            break
        term = comb(length, over_limit) * comb(
            length + deficit - 10 * over_limit - 1,
            deficit - 10 * over_limit,
        )
        total += -term if over_limit & 1 else term
    return total


def _length_count(length, digit_sum):
    deficit = 9 * length - digit_sum
    if deficit < 0:
        return 0

    return sum(
        _bounded_count(length - 1, deficit - first_deficit)
        for first_deficit in range(min(8, deficit) + 1)
    )


def _append_nines(value, count):
    if count == 0:
        return value
    power = pow(10, count, MOD)
    return (value * power + power - 1) % MOD


def _zero_run_length(length, deficit, rank):
    total = _bounded_count(length, deficit)
    low, high = 0, length - 1

    while low < high:
        middle = (low + high) // 2
        if rank <= total - _bounded_count(length - middle - 1, deficit):
            high = middle
        else:
            low = middle + 1

    return low


def _unrank_suffix(length, deficit, rank, value):
    while length:
        if deficit == 0:
            return _append_nines(value, length)

        zeroes = _zero_run_length(length, deficit, rank)
        if zeroes:
            skipped = _bounded_count(length, deficit) - _bounded_count(length - zeroes, deficit)
            rank -= skipped
            value = _append_nines(value, zeroes)
            length -= zeroes

        for current_deficit in range(min(9, deficit), 0, -1):
            count = _bounded_count(length - 1, deficit - current_deficit)
            if rank > count:
                rank -= count
            else:
                value = (value * 10 + 9 - current_deficit) % MOD
                length -= 1
                deficit -= current_deficit
                break

    return value


def _nth_with_digit_sum(digit_sum, rank):
    length = (digit_sum + 8) // 9
    while True:
        count = _length_count(length, digit_sum)
        if rank <= count:
            break
        rank -= count
        length += 1

    deficit = 9 * length - digit_sum
    for first_deficit in range(min(8, deficit), -1, -1):
        count = _bounded_count(length - 1, deficit - first_deficit)
        if rank > count:
            rank -= count
        else:
            first_digit = 9 - first_deficit
            return _unrank_suffix(length - 1, deficit - first_deficit, rank, first_digit)

    raise RuntimeError("rank exceeds count")


def solve():
    total = 0
    for n in range(1, LIMIT + 1):
        total += _nth_with_digit_sum(n * n * n, n ** 4)
    return total % MOD


if __name__ == "__main__":
    print(solve())
