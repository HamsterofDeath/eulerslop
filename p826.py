#!/usr/bin/env python3
"""Project Euler 826: painted nearest-neighbour gaps."""

from math import isqrt


def primes_below(limit: int) -> list[int]:
    sieve = bytearray(b"\x01") * limit
    sieve[:2] = b"\x00\x00"
    for p in range(2, isqrt(limit - 1) + 1):
        if sieve[p]:
            start = p * p
            sieve[start:limit:p] = b"\x00" * (((limit - 1 - start) // p) + 1)
    return [p for p in range(3, limit, 2) if sieve[p]]


def f_value(n: int) -> float:
    return (7 * n + 15) / (18 * (n + 1))


def solve() -> str:
    assert f_value(3) == 0.5
    primes = primes_below(1_000_000)
    average = sum(f_value(p) for p in primes) / len(primes)
    return f"{average:.10f}"


if __name__ == "__main__":
    print(solve())
