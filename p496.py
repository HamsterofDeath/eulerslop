#!/usr/bin/env python3

from math import isqrt


def mobius_sieve(limit):
    mu = [1] * (limit + 1)
    mu[0] = 0
    primes = []
    is_composite = [False] * (limit + 1)

    for i in range(2, limit + 1):
        if not is_composite[i]:
            primes.append(i)
            mu[i] = -1
        for p in primes:
            v = i * p
            if v > limit:
                break
            is_composite[v] = True
            if i % p == 0:
                mu[v] = 0
                break
            mu[v] = -mu[i]

    return mu


def weighted_squarefree_prefix(limit, mu, cache):
    if limit in cache:
        return cache[limit]

    total = 0
    d = 1
    while d * d <= limit:
        if mu[d]:
            q = limit // (d * d)
            total += mu[d] * d * d * q * (q + 1) // 2
        d += 1

    cache[limit] = total
    return total


def f(limit):
    root = isqrt(limit)
    mu = mobius_sieve(root)
    squarefree_cache = {}

    total = 0
    for r in range(1, root + 1):
        quotient = limit // r
        lo = r + 1
        hi = min(2 * r - 1, quotient)
        s = lo
        while s <= hi:
            q = quotient // s
            end = min(hi, quotient // q)
            sum_s = (s + end) * (end - s + 1) // 2
            total += r * sum_s * weighted_squarefree_prefix(q, mu, squarefree_cache)
            s = end + 1

    return total


def solve():
    assert f(15) == 45
    return str(f(10**9))


if __name__ == "__main__":
    print(solve())
