#!/usr/bin/env python3
from functools import lru_cache
from math import isqrt


SIEVE_LIMIT = 1_000_000


def _sieve(limit):
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[:2] = b"\x00\x00"
    for p in range(2, isqrt(limit) + 1):
        if sieve[p]:
            start = p * p
            sieve[start:limit + 1:p] = b"\x00" * ((limit - start) // p + 1)
    primes = [i for i in range(limit + 1) if sieve[i]]
    pi = [0] * (limit + 1)
    count = 0
    for i in range(limit + 1):
        if sieve[i]:
            count += 1
        pi[i] = count
    return primes, pi


PRIMES, PI_SMALL = _sieve(SIEVE_LIMIT)


def _iroot(n, k):
    lo, hi = 0, int(n ** (1 / k)) + 3
    while hi ** k <= n:
        hi *= 2
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if mid ** k <= n:
            lo = mid
        else:
            hi = mid - 1
    return lo


@lru_cache(maxsize=None)
def _phi(x, s):
    if s == 0:
        return x
    return _phi(x, s - 1) - _phi(x // PRIMES[s - 1], s - 1)


@lru_cache(maxsize=None)
def prime_count(x):
    if x < SIEVE_LIMIT:
        return PI_SMALL[x]

    a = prime_count(isqrt(isqrt(x)))
    b = prime_count(isqrt(x))
    c = prime_count(_iroot(x, 3))
    total = _phi(x, a) + (b + a - 2) * (b - a + 1) // 2
    for i in range(a, b):
        w = x // PRIMES[i]
        total -= prime_count(w)
        if i < c:
            lim = prime_count(isqrt(w))
            for j in range(i, lim):
                total -= prime_count(w // PRIMES[j]) - j
    return total


def _sum_floor_half(n):
    m = n // 2
    return m * m if n % 2 == 0 else m * m + m


def _three_or_more_count(n):
    if n < 6:
        return sum(max(0, i // 2 - 2) for i in range(1, n + 1))
    return _sum_floor_half(n) - 2 * n + 4


def S(n):
    if n < 4:
        small_primes = {p for p in PRIMES if p <= n}
        ones = sum(1 for i in range(1, n + 1) if i in small_primes)
        twos = sum(
            1
            for i in range(1, n + 1)
            if any((i - p) in small_primes for p in small_primes)
        )
        return ones + twos + _three_or_more_count(n)

    # k = 1 contributes primes.  k = 2 contributes even numbers >= 4 and
    # odd numbers p+2 with p an odd prime.  For k >= 3 every i >= 2k is
    # representable as a sum of k primes in this range.
    one_prime = prime_count(n)
    two_primes = (n // 2 - 1) + max(0, prime_count(n - 2) - 1)
    return one_prime + two_primes + _three_or_more_count(n)


def solve():
    assert S(10) == 20
    assert S(100) == 2402
    assert S(1000) == 248838

    fib = [0, 1]
    for _ in range(44):
        fib.append(fib[-1] + fib[-2])
    return sum(S(fib[k]) for k in range(3, 45))


if __name__ == "__main__":
    print(solve())
