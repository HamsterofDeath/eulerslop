#!/usr/bin/env python3
"""Project Euler 608: Divisor Sums.

For m = product p^a, summing tau(kd) over d|m gives a multiplicative
function of k.  Its Dirichlet series is zeta(s)^2 times a finite Euler
product, so the answer is a weighted sum of the ordinary divisor summatory
function over squarefree products of primes at most 200.
"""

from math import isqrt


MOD = 1_000_000_007
FACTORIAL_LIMIT = 200
N = 10**12
SMALL_LIMIT = 1_000_000


def primes_up_to(limit):
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[0:2] = b"\x00\x00"
    for p in range(2, isqrt(limit) + 1):
        if sieve[p]:
            start = p * p
            sieve[start : limit + 1 : p] = b"\x00" * (((limit - start) // p) + 1)
    return [p for p in range(2, limit + 1) if sieve[p]]


def factorial_exponent(n, prime):
    exponent = 0
    while n:
        n //= prime
        exponent += n
    return exponent


def precompute_divisor_summatory(limit):
    divisor_counts = [0] * (limit + 1)
    for divisor in range(1, limit + 1):
        for multiple in range(divisor, limit + 1, divisor):
            divisor_counts[multiple] += 1

    running = 0
    for value in range(1, limit + 1):
        running += divisor_counts[value]
        divisor_counts[value] = running
    return divisor_counts


def divisor_summatory(value):
    total = 0
    start = 1
    while start <= value:
        quotient = value // start
        end = value // quotient
        total += quotient * (end - start + 1)
        start = end + 1
    return total


def solve():
    primes = primes_up_to(FACTORIAL_LIMIT)
    divisor_sums = precompute_divisor_summatory(SMALL_LIMIT)

    base = 1
    coefficients = []
    inverse_two = (MOD + 1) // 2
    for prime in primes:
        exponent = factorial_exponent(FACTORIAL_LIMIT, prime)
        base = base * (exponent + 1) % MOD
        base = base * (exponent + 2) % MOD * inverse_two % MOD
        coefficients.append((-exponent * pow(exponent + 2, MOD - 2, MOD)) % MOD)

    large_cache = {}

    def get_divisor_sum(value):
        if value <= SMALL_LIMIT:
            return divisor_sums[value]
        cached = large_cache.get(value)
        if cached is None:
            cached = divisor_summatory(value)
            large_cache[value] = cached
        return cached

    total = 0
    prime_count = len(primes)

    def visit_subsets(start_index, product, weight):
        nonlocal total
        total += weight * get_divisor_sum(N // product)

        for index in range(start_index, prime_count):
            next_product = product * primes[index]
            if next_product > N:
                break
            visit_subsets(index + 1, next_product, weight * coefficients[index] % MOD)

    visit_subsets(0, 1, 1)
    return base * (total % MOD) % MOD


if __name__ == "__main__":
    print(solve())
