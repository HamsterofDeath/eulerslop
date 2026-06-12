#!/usr/bin/env python3

MOD = 1_234_567_890


def valuation_counts(limit):
    counts = []
    power = 1
    while power <= limit:
        counts.append(limit // power - limit // (2 * power))
        power *= 2
    return counts


def S(limit):
    counts = valuation_counts(limit)

    losing = 0
    for i, a_count in enumerate(counts):
        for j, b_count in enumerate(counts):
            k = i ^ j
            if k < len(counts):
                losing += a_count * b_count * counts[k]

    return (limit**3 - losing) % MOD


def solve():
    # For one pile, the Sprague-Grundy value is v2(n): moves can reach every
    # smaller 2-adic valuation, can jump above it, and can never reach itself.
    assert S(10) == 692
    assert S(100) == 735_494
    return S(123_456_787_654_321)


if __name__ == "__main__":
    print(solve())
