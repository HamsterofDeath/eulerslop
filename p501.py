#!/usr/bin/env python3
from functools import lru_cache
from math import isqrt


N = 10 ** 12
SIEVE_LIMIT = 2_000_000


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


def _iroot3(n):
    return _iroot(n, 3)


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
    c = prime_count(_iroot3(x))
    total = _phi(x, a) + (b + a - 2) * (b - a + 1) // 2

    for i in range(a, b):
        w = x // PRIMES[i]
        total -= prime_count(w)
        if i < c:
            lim = prime_count(isqrt(w))
            for j in range(i, lim):
                total -= prime_count(w // PRIMES[j]) - j
    return total


def f(limit):
    # Exactly eight divisors means one of p^7, p^3*q, or p*q*r.
    total = prime_count(_iroot(limit, 7))

    for p in PRIMES:
        p3 = p ** 3
        if p3 > limit:
            break
        qmax = limit // p3
        total += prime_count(qmax) - (1 if p <= qmax else 0)

    for i, p in enumerate(PRIMES):
        if p ** 3 > limit:
            break
        qmax = isqrt(limit // p)
        for j in range(i + 1, len(PRIMES)):
            q = PRIMES[j]
            if q > qmax:
                break
            total += prime_count(limit // (p * q)) - j - 1

    return total


def solve():
    assert f(100) == 10
    assert f(1000) == 180
    assert f(10 ** 6) == 224427
    return f(N)


if __name__ == "__main__":
    print(solve())
