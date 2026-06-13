#!/usr/bin/env python3
"""Project Euler 717: Summation of a Modular Formula."""

from math import isqrt


LIMIT = 10_000_000


def _odd_primes_below(limit):
    if limit <= 3:
        return

    sieve = bytearray(b"\x01") * limit
    sieve[0:2] = b"\x00\x00"
    if limit > 4:
        sieve[4::2] = b"\x00" * (((limit - 1) - 4) // 2 + 1)

    for n in range(3, isqrt(limit - 1) + 1, 2):
        if sieve[n]:
            start = n * n
            step = 2 * n
            sieve[start::step] = b"\x00" * (((limit - 1) - start) // step + 1)

    for p in range(3, limit, 2):
        if sieve[p]:
            yield p


def _g(p):
    residue = pow(2, pow(2, p, p - 1), p)
    multiplier = (residue * ((p + 1) // 2)) % p
    two_to_p_mod_p2 = pow(2, p, p * p)
    return ((multiplier * two_to_p_mod_p2 - residue) // p) % p


def solve():
    return sum(_g(p) for p in _odd_primes_below(LIMIT))


if __name__ == "__main__":
    print(solve())
