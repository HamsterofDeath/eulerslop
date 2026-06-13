#!/usr/bin/env python3
"""Project Euler 759: squared popcount-weighted integers."""


MOD = 1_000_000_007
TARGET = 10**16


def shifted(stats: list[int], prefix: int, extra_bits: int) -> list[int]:
    count, total, total2, bits, bits2, total_bits, total_bits2, total2_bits, total2_bits2 = stats
    p = prefix % MOD
    c = extra_bits % MOD
    return [
        count,
        (p * count + total) % MOD,
        (p * p * count + 2 * p * total + total2) % MOD,
        (c * count + bits) % MOD,
        (c * c * count + 2 * c * bits + bits2) % MOD,
        (p * c * count + p * bits + c * total + total_bits) % MOD,
        (
            p * c * c * count
            + 2 * p * c * bits
            + p * bits2
            + c * c * total
            + 2 * c * total_bits
            + total_bits2
        )
        % MOD,
        (
            p * p * c * count
            + p * p * bits
            + 2 * p * c * total
            + 2 * p * total_bits
            + c * total2
            + total2_bits
        )
        % MOD,
        (
            p * p * c * c * count
            + 2 * p * p * c * bits
            + p * p * bits2
            + 2 * p * c * c * total
            + 4 * p * c * total_bits
            + 2 * p * total_bits2
            + c * c * total2
            + 2 * c * total2_bits
            + total2_bits2
        )
        % MOD,
    ]


def precompute(bits: int) -> list[list[int]]:
    stats = [[1, 0, 0, 0, 0, 0, 0, 0, 0]]
    for bit in range(bits):
        high_block = shifted(stats[-1], pow(2, bit, MOD), 1)
        stats.append([(a + b) % MOD for a, b in zip(stats[-1], high_block)])
    return stats


STATS = precompute(TARGET.bit_length())


def s_value(limit: int) -> int:
    answer = 0
    prefix = 0
    prefix_bits = 0
    for bit in range(limit.bit_length() - 1, -1, -1):
        if (limit >> bit) & 1:
            answer = (answer + shifted(STATS[bit], prefix, prefix_bits)[8]) % MOD
            prefix = (prefix + pow(2, bit, MOD)) % MOD
            prefix_bits += 1
    return (answer + prefix * prefix % MOD * (prefix_bits * prefix_bits % MOD)) % MOD


def solve() -> int:
    assert s_value(10) == 1530
    assert s_value(100) == 4798445
    return s_value(TARGET)


if __name__ == "__main__":
    print(solve())
