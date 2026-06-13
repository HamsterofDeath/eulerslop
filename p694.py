#!/usr/bin/env python3
"""Project Euler 694: Cube-full Divisors."""

from math import isqrt


N = 10**18


def _integer_cuberoot(n):
    lo, hi = 0, 1
    while hi**3 <= n:
        hi *= 2
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if mid**3 <= n:
            lo = mid
        else:
            hi = mid
    return lo


def _primes_up_to(limit):
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[:2] = b"\x00\x00"
    for p in range(2, isqrt(limit) + 1):
        if sieve[p]:
            start = p * p
            sieve[start::p] = b"\x00" * ((limit - start) // p + 1)
    return [p for p in range(limit + 1) if sieve[p]]


def solve():
    primes = _primes_up_to(_integer_cuberoot(N))

    total = N

    def visit(start, current):
        nonlocal total
        for i in range(start, len(primes)):
            p = primes[i]
            value = current * p * p * p
            if value > N:
                break
            while value <= N:
                total += N // value
                visit(i + 1, value)
                value *= p

    visit(0, 1)
    return total


if __name__ == "__main__":
    print(solve())
