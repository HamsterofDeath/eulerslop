#!/usr/bin/env python3
from math import isqrt
import sys


N = 201_820_182_018
MOD = 10**9


def _prime_sums_on_floor_values(limit):
    values = []
    i = 1
    while i <= limit:
        value = limit // i
        values.append(value)
        i = limit // value + 1

    sums = {value: value * (value + 1) // 2 - 1 for value in values}
    root = isqrt(limit)

    for p in range(2, root + 1):
        if sums[p] == sums[p - 1]:
            continue
        before_p = sums[p - 1]
        p2 = p * p
        for value in values:
            if value < p2:
                break
            sums[value] -= p * (sums[value // p] - before_p)

    for key in list(sums):
        sums[key] %= MOD
    return sums


def _primes_upto(limit):
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[:2] = b"\x00\x00"
    for p in range(2, isqrt(limit) + 1):
        if sieve[p]:
            start = p * p
            sieve[start : limit + 1 : p] = b"\x00" * ((limit - start) // p + 1)
    return [n for n in range(limit + 1) if sieve[n]]


def largest_prime_factor_sum(limit):
    prime_sums = _prime_sums_on_floor_values(limit)
    primes = _primes_upto(isqrt(limit))
    sum_before_prime = [prime_sums[p - 1] for p in primes]

    # Write n uniquely as m*p, where p is one copy of the largest prime factor.
    # For each valid m, all prime p in [P(m), floor(limit/m)] contribute.
    total = prime_sums[limit]
    sys.setrecursionlimit(10_000)

    def visit(start_index, m):
        nonlocal total
        q_limit = isqrt(limit // m)
        for index in range(start_index, len(primes)):
            q = primes[index]
            if q > q_limit:
                break
            next_m = m * q
            total += prime_sums[limit // next_m] - sum_before_prime[index]
            visit(index, next_m)

    visit(0, 1)
    return total % MOD


def solve():
    assert largest_prime_factor_sum(10) == 32
    assert largest_prime_factor_sum(100) == 1915
    assert largest_prime_factor_sum(10_000) == 10_118_280
    return largest_prime_factor_sum(N)


if __name__ == "__main__":
    print(solve())
