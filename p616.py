#!/usr/bin/env python3
from math import isqrt

LIMIT = 10**12


def prime_flags(limit):
    is_prime = bytearray(b"\x01") * (limit + 1)
    is_prime[:2] = b"\x00\x00"
    for p in range(2, isqrt(limit) + 1):
        if is_prime[p]:
            start = p * p
            is_prime[start : limit + 1 : p] = b"\x00" * (
                (limit - start) // p + 1
            )
    return is_prime


def solve(limit=LIMIT):
    # The creative numbers are exactly the perfect powers a^b with composite
    # base a, except 16.  The exception only decomposes into powers of two,
    # while every larger composite-base perfect power can generate 36 and then
    # expose any requested exponent.
    root = isqrt(limit)
    is_prime = prime_flags(root)

    creative = set()
    for base in range(4, root + 1):
        if is_prime[base]:
            continue
        value = base * base
        while value <= limit:
            creative.add(value)
            value *= base

    creative.discard(16)
    return sum(creative)


if __name__ == "__main__":
    print(solve())
