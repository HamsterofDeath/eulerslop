#!/usr/bin/env python3
"""Project Euler 832: greedy XOR triples by base-4 digit permutation."""


MOD = 1_000_000_007
PARTNER = (0, 2, 3, 1)
XOR_DIGIT = tuple(d ^ PARTNER[d] for d in range(4))


def prefix_digit_map(total: int, digits: int, mapping: tuple[int, int, int, int]) -> int:
    """Sum mapped(x) for 0 <= x < total over fixed-width base-4 digits."""
    if total == 0 or digits == 0:
        return 0
    block = 4 ** (digits - 1)
    high, rest = divmod(total, block)
    low_all = block * (block - 1) // 2

    result = 0
    for d in range(high):
        result += block * mapping[d] * block + low_all
    if rest:
        result += rest * mapping[high] * block
        result += prefix_digit_map(rest, digits - 1, mapping)
    return result


def m_value(rounds: int) -> int:
    q = 1
    digits = 0
    while (4 * q - 1) // 3 <= rounds:
        q *= 4
        digits += 1

    completed = (q - 1) // 3
    remaining = rounds - completed
    total = q * (q - 1) // 2

    total += 6 * q * remaining
    total += remaining * (remaining - 1) // 2
    total += prefix_digit_map(remaining, digits, PARTNER)
    total += prefix_digit_map(remaining, digits, XOR_DIGIT)
    return total % MOD


def solve() -> int:
    assert m_value(10) == 642
    assert m_value(1000) == 5432148
    return m_value(10**18)


if __name__ == "__main__":
    print(solve())
