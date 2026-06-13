#!/usr/bin/env python3
"""Project Euler 800: hybrid integers."""

from math import log


def primes_up_to(limit: int) -> list[int]:
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[0:2] = b"\x00\x00"
    for p in range(2, int(limit**0.5) + 1):
        if sieve[p]:
            start = p * p
            sieve[start : limit + 1 : p] = b"\x00" * (((limit - start) // p) + 1)
    return [n for n in range(2, limit + 1) if sieve[n]]


def count_hybrid(base: int, exponent: int) -> int:
    target = exponent * log(base)
    prime_limit = int(target / log(2)) + 1
    primes = primes_up_to(prime_limit)
    logs = [log(p) for p in primes]

    count = 0
    for i, p in enumerate(primes):
        if i + 1 == len(primes):
            break
        if primes[i + 1] * logs[i] + p * logs[i + 1] > target:
            break

        lo = i + 1
        hi = len(primes) - 1
        best = i
        while lo <= hi:
            mid = (lo + hi) // 2
            if primes[mid] * logs[i] + p * logs[mid] <= target:
                best = mid
                lo = mid + 1
            else:
                hi = mid - 1
        count += best - i

    return count


def solve() -> int:
    assert count_hybrid(800, 1) == 2
    assert count_hybrid(800, 800) == 10790
    return count_hybrid(800800, 800800)


if __name__ == "__main__":
    print(solve())
