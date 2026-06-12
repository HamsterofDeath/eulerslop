#!/usr/bin/env python3
from functools import lru_cache
from itertools import product
from math import gcd


LIMIT = 10**16
PRIMES_FOR_MIN_VALUE = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]


@lru_cache(maxsize=None)
def gozinta_count(exponents):
    if not exponents:
        return 1

    total = 0
    for divisor_exponents in product(*(range(e + 1) for e in exponents)):
        if divisor_exponents == exponents:
            continue
        reduced = tuple(sorted((e for e in divisor_exponents if e), reverse=True))
        total += gozinta_count(reduced)
    return total


def _is_prime(n):
    if n < 2:
        return False
    small_primes = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)
    for p in small_primes:
        if n % p == 0:
            return n == p

    d = n - 1
    shifts = 0
    while d % 2 == 0:
        shifts += 1
        d //= 2

    for a in small_primes:
        if a >= n:
            continue
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(shifts - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def _pollard_rho(n):
    if n % 2 == 0:
        return 2
    if n % 3 == 0:
        return 3

    c = 1
    while True:
        x = y = 2
        divisor = 1
        while divisor == 1:
            x = (x * x + c) % n
            y = (y * y + c) % n
            y = (y * y + c) % n
            divisor = gcd(abs(x - y), n)
        if divisor != n:
            return divisor
        c += 1


def _factor(n, out):
    if n == 1:
        return
    if _is_prime(n):
        out.append(n)
        return
    divisor = _pollard_rho(n)
    _factor(divisor, out)
    _factor(n // divisor, out)


@lru_cache(maxsize=None)
def exponent_partition(n):
    factors = []
    _factor(n, factors)
    counts = {}
    for p in factors:
        counts[p] = counts.get(p, 0) + 1
    return tuple(sorted(counts.values(), reverse=True))


def exponent_partitions_under(limit):
    partitions = []

    def search(max_exponent, prime_index, value, current):
        if current:
            partitions.append(tuple(current))
        if prime_index >= len(PRIMES_FOR_MIN_VALUE):
            return

        prime = PRIMES_FOR_MIN_VALUE[prime_index]
        next_value = value * prime
        exponent = 1
        while exponent <= max_exponent and next_value <= limit:
            current.append(exponent)
            search(exponent, prime_index + 1, next_value, current)
            current.pop()
            exponent += 1
            next_value *= prime

    search(64, 0, 1, [])
    return partitions


def solve():
    assert gozinta_count((2, 1)) == 8
    assert gozinta_count((4, 1)) == 48
    assert gozinta_count((3, 1, 1)) == 132

    hits = {1}
    for exponents in exponent_partitions_under(LIMIT):
        count = gozinta_count(exponents)
        if count <= LIMIT and exponent_partition(count) == exponents:
            hits.add(count)

    return sum(hits)


if __name__ == "__main__":
    print(solve())
