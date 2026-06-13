#!/usr/bin/env python3
from math import isqrt


N = 10**36
MOBIUS_PRECOMPUTE = 5_000_000


def _mobius_and_prefix(limit):
    mu = [0] * (limit + 1)
    mu[1] = 1
    primes = []
    composite = bytearray(limit + 1)

    for n in range(2, limit + 1):
        if not composite[n]:
            primes.append(n)
            mu[n] = -1
        for p in primes:
            q = n * p
            if q > limit:
                break
            composite[q] = 1
            if n % p == 0:
                mu[q] = 0
                break
            mu[q] = -mu[n]

    prefix = [0] * (limit + 1)
    total = 0
    for n in range(1, limit + 1):
        total += mu[n]
        prefix[n] = total
    return mu, prefix


MU, MERTENS_PREFIX = _mobius_and_prefix(MOBIUS_PRECOMPUTE)
MERTENS_CACHE = {}


def mertens(n):
    if n <= MOBIUS_PRECOMPUTE:
        return MERTENS_PREFIX[n]
    cached = MERTENS_CACHE.get(n)
    if cached is not None:
        return cached

    total = 1
    left = 2
    while left <= n:
        quotient = n // left
        right = n // quotient
        total -= (right - left + 1) * mertens(quotient)
        left = right + 1

    MERTENS_CACHE[n] = total
    return total


def even_squarefree_count(limit):
    squarefree = 0
    root = isqrt(limit)
    mu = MU
    for d in range(1, root + 1):
        squarefree += mu[d] * (limit // (d * d))
    return (squarefree + mertens(limit)) // 2


def f(limit):
    # A die finishes on 1 exactly when tau(n) == 1 (mod 6).
    # This forces every prime exponent to be 0 or 4 mod 6, with an even
    # number of 4 mod 6 exponents: n = a^6 b^4, b squarefree, mu(b)=1.
    total = 0
    cache = {}
    a = 1
    while True:
        a6 = a**6
        if a6 > limit:
            break
        b_limit = isqrt(isqrt(limit // a6))
        count = cache.get(b_limit)
        if count is None:
            count = even_squarefree_count(b_limit)
            cache[b_limit] = count
        total += count
        a += 1
    return total


def solve():
    assert f(100) == 2
    assert f(10**8) == 69
    return f(N)


if __name__ == "__main__":
    print(solve())
