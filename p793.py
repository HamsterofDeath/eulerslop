#!/usr/bin/env python3
"""Project Euler 793: median of pairwise products."""


MODULUS = 50_515_093
SEED = 290_797
TARGET_N = 1_000_003


def sequence(length: int) -> list[int]:
    values = [0] * length
    value = SEED
    for i in range(length):
        values[i] = value
        value = value * value % MODULUS
    values.sort()
    return values


def products_at_most(values: list[int], limit: int) -> int:
    total = 0
    right = len(values) - 1
    for left, value in enumerate(values):
        while right > left and value * values[right] > limit:
            right -= 1
        if right <= left:
            break
        total += right - left
    return total


def median_pairwise_product(length: int) -> int:
    values = sequence(length)
    pair_count = length * (length - 1) // 2
    target_rank = (pair_count + 1) // 2

    low = values[0] * values[1]
    high = values[-2] * values[-1]
    while low < high:
        mid = (low + high) // 2
        if products_at_most(values, mid) >= target_rank:
            high = mid
        else:
            low = mid + 1
    return low


def solve() -> int:
    assert median_pairwise_product(3) == 3_878_983_057_768
    assert median_pairwise_product(103) == 492_700_616_748_525
    return median_pairwise_product(TARGET_N)


if __name__ == "__main__":
    print(solve())
