#!/usr/bin/env python3

from functools import lru_cache

MOD = 10**9


@lru_cache(maxsize=None)
def losing_prefix_sum(first_limit, second_limit, third_limit):
    first_limit = min(first_limit, second_limit, third_limit)
    second_limit = min(second_limit, third_limit)
    if first_limit <= 0 or second_limit <= 1 or third_limit <= 2:
        return 0, 0

    half = 1 << ((third_limit - 1).bit_length() - 1)

    def lower_half(a, b, c):
        return losing_prefix_sum(min(a, half), min(b, half), min(c, half))

    count, total = losing_prefix_sum(min(first_limit, half), min(second_limit, half), half)

    for limits in (
        (first_limit, second_limit - half, third_limit - half),
        (second_limit - half, first_limit, third_limit - half),
        (second_limit - half, third_limit - half, first_limit),
    ):
        sub_count, sub_total = lower_half(*limits)
        count += sub_count
        total += sub_total + 2 * half * sub_count

    # The extra cross-half cold positions are (a, half - 1, half + a).
    if second_limit > half - 1:
        max_a = min(first_limit - 1, third_limit - half - 1, half - 2)
        if max_a >= 0:
            special_count = max_a + 1
            special_total = max_a * (max_a + 1) + (2 * half - 1) * special_count
            count += special_count
            total += special_total

    return count, total


def zero_heap_sum(limit):
    max_j = (limit - 3) // 2
    if max_j < 0:
        return 0
    count = max_j + 1
    return 2 * max_j * (max_j + 1) + 3 * count


def f(limit):
    _, total = losing_prefix_sum(limit, limit, limit)
    return total - zero_heap_sum(limit)


def solve():
    assert f(8) == 42
    assert f(128) == 496062
    return str(f(10**18) % MOD)


if __name__ == "__main__":
    print(solve())
