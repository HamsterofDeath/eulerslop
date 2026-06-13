#!/usr/bin/env python3
"""Project Euler 675: 2^omega over divisors of factorials."""

from array import array
from math import isqrt


LIMIT = 10_000_000
MOD = 1_000_000_087


def _odd_smallest_prime_factors(limit: int) -> array:
    """Return smallest odd prime factors for odd numbers, indexed by n // 2."""
    factors = array("I", [0]) * (limit // 2 + 1)
    root = isqrt(limit)

    for p in range(3, root + 1, 2):
        if factors[p >> 1] == 0:
            for index in range((p * p) >> 1, len(factors), p):
                if factors[index] == 0:
                    factors[index] = p

    return factors


def _modular_inverses(limit: int) -> array:
    """Return inverses modulo MOD for all integers up to 2 * limit + 1."""
    inverses = array("I", [0]) * (2 * limit + 2)
    inverses[1] = 1

    mod = MOD
    for n in range(2, len(inverses)):
        inverses[n] = (mod - (mod // n) * inverses[mod % n] % mod) % mod

    return inverses


def F(limit: int) -> int:
    factors = _odd_smallest_prime_factors(limit)
    inverses = _modular_inverses(limit)
    exponents = array("I", [0]) * (limit + 1)

    current = 1
    total = 0
    mod = MOD

    for n in range(2, limit + 1):
        remaining = n

        if remaining & 1 == 0:
            exponent = (remaining & -remaining).bit_length() - 1
            old_factor = (exponents[2] << 1) + 1
            exponents[2] += exponent
            current = current * (old_factor + (exponent << 1)) % mod
            current = current * inverses[old_factor] % mod
            remaining >>= exponent

        while remaining > 1:
            prime = factors[remaining >> 1]
            if prime == 0:
                old_factor = (exponents[remaining] << 1) + 1
                exponents[remaining] += 1
                current = current * (old_factor + 2) % mod
                current = current * inverses[old_factor] % mod
                break

            exponent = 0
            while remaining % prime == 0:
                remaining //= prime
                exponent += 1

            old_factor = (exponents[prime] << 1) + 1
            exponents[prime] += exponent
            current = current * (old_factor + (exponent << 1)) % mod
            current = current * inverses[old_factor] % mod

        total += current
        if total >= mod:
            total -= mod

    return total


def solve() -> int:
    return F(LIMIT)


if __name__ == "__main__":
    print(solve())
