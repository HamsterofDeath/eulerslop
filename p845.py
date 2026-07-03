#!/usr/bin/env python3
"""Project Euler 845: nth integer with prime digit sum."""


def prime_sieve(limit: int) -> set[int]:
    sieve = [True] * (limit + 1)
    sieve[:2] = [False, False]
    for p in range(2, int(limit**0.5) + 1):
        if sieve[p]:
            for q in range(p * p, limit + 1, p):
                sieve[q] = False
    return {i for i, ok in enumerate(sieve) if ok}


PRIMES = prime_sieve(200)


def count_good(limit: int) -> int:
    if limit <= 0:
        return 0
    digits = [int(ch) for ch in str(limit)]
    remaining = len(digits)
    ways = [[0] * (9 * remaining + 1) for _ in range(remaining + 1)]
    ways[0][0] = 1
    for length in range(remaining):
        for s, value in enumerate(ways[length]):
            if value:
                for d in range(10):
                    ways[length + 1][s + d] += value

    total = 0
    prefix_sum = 0
    for pos, digit in enumerate(digits):
        rest = len(digits) - pos - 1
        for d in range(digit):
            for suffix_sum, value in enumerate(ways[rest]):
                if prefix_sum + d + suffix_sum in PRIMES:
                    total += value
        prefix_sum += digit

    if prefix_sum in PRIMES:
        total += 1
    return total


def d_value(index: int) -> int:
    lo, hi = 1, 1
    while count_good(hi) < index:
        hi *= 2
    while lo < hi:
        mid = (lo + hi) // 2
        if count_good(mid) >= index:
            hi = mid
        else:
            lo = mid + 1
    return lo


def solve() -> int:
    assert d_value(61) == 157
    assert d_value(10**8) == 403539364
    return d_value(10**16)


if __name__ == "__main__":
    print(solve())
