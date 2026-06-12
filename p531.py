#!/usr/bin/env python3
from math import gcd, isqrt


def g(a, n, b, m):
    d = gcd(n, m)
    if (b - a) % d:
        return 0
    n1 = n // d
    m1 = m // d
    t = ((b - a) // d * pow(n1, -1, m1)) % m1
    return (a + n * t) % (n * m1)


def _primes(limit):
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[:2] = b"\x00\x00"
    for p in range(2, isqrt(limit) + 1):
        if sieve[p]:
            start = p * p
            sieve[start:limit + 1:p] = b"\x00" * ((limit - start) // p + 1)
    return [i for i in range(limit + 1) if sieve[i]]


def _totients_interval(lo, hi):
    values = list(range(lo, hi))
    phi = values[:]
    remaining = values[:]

    for p in _primes(isqrt(hi) + 1):
        start = ((lo + p - 1) // p) * p
        for x in range(start, hi, p):
            i = x - lo
            if remaining[i] % p == 0:
                phi[i] = phi[i] // p * (p - 1)
                while remaining[i] % p == 0:
                    remaining[i] //= p

    for i, r in enumerate(remaining):
        if r > 1:
            phi[i] = phi[i] // r * (r - 1)
    return values, phi


def solve():
    assert g(2, 4, 4, 6) == 10
    assert g(3, 4, 4, 6) == 0

    nums, phi = _totients_interval(1_000_000, 1_005_000)
    total = 0
    for i, n in enumerate(nums):
        for j in range(i + 1, len(nums)):
            total += g(phi[i], n, phi[j], nums[j])
    return total


if __name__ == "__main__":
    print(solve())
