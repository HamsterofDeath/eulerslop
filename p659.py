#!/usr/bin/env python3
"""Project Euler 659: Largest prime."""

from array import array
from math import isqrt


LIMIT = 10_000_000
MOD = 10**18


def odd_prime_sieve(limit):
    """Return all odd primes up to limit."""
    if limit < 3:
        return []

    sieve = bytearray(b"\x01") * (limit // 2 + 1)
    sieve[0] = 0
    root = isqrt(limit)
    for i in range(1, root // 2 + 1):
        if sieve[i]:
            p = 2 * i + 1
            start = (p * p) // 2
            sieve[start::p] = b"\x00" * (((limit // 2 - start) // p) + 1)
    return [2 * i + 1 for i in range(1, limit // 2 + 1) if sieve[i]]


def sqrt_minus_one_prime(p):
    """Square root of -1 modulo a prime p == 1 (mod 4)."""
    candidate = 2
    exponent = (p - 1) // 2
    while pow(candidate, exponent, p) != p - 1:
        candidate += 1
    return pow(candidate, (p - 1) // 4, p)


def solve(limit=LIMIT, mod=MOD):
    # A prime p divides n^2+k^2 and (n+1)^2+k^2 exactly when
    # 2n+1 == 0 and 4k^2+1 == 0 modulo p.  Thus P(k) is the largest
    # prime factor of 4k^2+1.
    max_factor_to_sieve = isqrt(4 * limit * limit + 1)
    primes = odd_prime_sieve(max_factor_to_sieve)

    remaining = array("Q", (4 * k * k + 1 for k in range(limit + 1)))
    largest_small_factor = array("I", [0]) * (limit + 1)

    for p in primes:
        if p & 3 != 1:
            continue

        root_i = sqrt_minus_one_prime(p)
        inv2 = (p + 1) // 2
        root = (root_i * inv2) % p
        other_root = p - root

        for start in (root, other_root):
            if start == 0:
                start = p
            for k in range(start, limit + 1, p):
                value = remaining[k]
                if value % p == 0:
                    largest_small_factor[k] = p
                    while value % p == 0:
                        value //= p
                    remaining[k] = value

    total = 0
    for k in range(1, limit + 1):
        factor = remaining[k]
        if factor < largest_small_factor[k]:
            factor = largest_small_factor[k]
        total = (total + factor) % mod
    return total


if __name__ == "__main__":
    print(solve())
