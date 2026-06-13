#!/usr/bin/env python3
"""Project Euler 778: freshman's product."""


MOD = 1_000_000_009
R = 234_567
M = 765_432


def digit_counts(limit: int, position: int) -> list[int]:
    place = 10**position
    cycle = 10 * place
    full_cycles, remainder = divmod(limit + 1, cycle)
    counts = []
    for digit in range(10):
        start = digit * place
        extra = max(0, min(remainder, start + place) - start)
        counts.append(full_cycles * place + extra)
    return counts


def combine(left: list[int], right: list[int]) -> list[int]:
    out = [0] * 10
    for a, av in enumerate(left):
        if av == 0:
            continue
        for b, bv in enumerate(right):
            if bv:
                out[(a * b) % 10] = (out[(a * b) % 10] + av * bv) % MOD
    return out


def product_digit_sum(repetitions: int, counts: list[int]) -> int:
    distribution = [0] * 10
    distribution[1] = 1
    base = [count % MOD for count in counts]
    while repetitions:
        if repetitions & 1:
            distribution = combine(distribution, base)
        base = combine(base, base)
        repetitions >>= 1
    return sum(digit * count for digit, count in enumerate(distribution)) % MOD


def f_value(repetitions: int, limit: int) -> int:
    answer = 0
    place = 1
    position = 0
    while place <= limit:
        contribution = product_digit_sum(repetitions, digit_counts(limit, position))
        answer = (answer + place * contribution) % MOD
        place *= 10
        position += 1
    return answer


def solve() -> int:
    assert f_value(2, 7) == 204
    assert f_value(23, 76) == 5870548
    return f_value(R, M)


if __name__ == "__main__":
    print(solve())
