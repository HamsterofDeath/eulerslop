#!/usr/bin/env python3
"""Project Euler 760: summing bitwise OR over additive pairs."""


MOD = 1_000_000_007
TARGET = 10**18


def residue_pairs_with_zero_bit(bit_value: int, residue_limit: int) -> int:
    q = bit_value
    if residue_limit >= 2 * q - 2:
        return q * q
    if residue_limit < q:
        return (residue_limit + 1) * (residue_limit + 2) // 2
    missing = 2 * q - 2 - residue_limit
    return q * q - missing * (missing + 1) // 2


def g_sum(limit: int) -> int:
    total_pairs = (limit + 1) * (limit + 2) // 2
    answer = 0

    for bit in range(limit.bit_length() + 1):
        q = 1 << bit
        period = 2 * q
        full_blocks = limit // period
        remainder = limit % period
        both_zero = q * q * (full_blocks * (full_blocks + 1) // 2)
        both_zero += (full_blocks + 1) * residue_pairs_with_zero_bit(q, remainder)
        answer += 2 * q * (total_pairs - both_zero)

    return answer % MOD


def solve() -> int:
    assert g_sum(10) == 754
    assert g_sum(100) == 583766
    return g_sum(TARGET)


if __name__ == "__main__":
    print(solve())
