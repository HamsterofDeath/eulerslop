#!/usr/bin/env python3
from math import isqrt


def _mobius_and_divisors(limit):
    mu = [1] * (limit + 1)
    mu[0] = 0
    primes = []
    composite = [False] * (limit + 1)
    for i in range(2, limit + 1):
        if not composite[i]:
            primes.append(i)
            mu[i] = -1
        for p in primes:
            v = i * p
            if v > limit:
                break
            composite[v] = True
            if i % p == 0:
                mu[v] = 0
                break
            mu[v] = -mu[i]

    divisors = [[] for _ in range(limit + 1)]
    for d in range(1, limit + 1):
        if mu[d]:
            for m in range(d, limit + 1, d):
                divisors[m].append((d, mu[d]))
    return divisors


def _floor_sum(n, lo, hi):
    if lo > hi or n < lo:
        return 0
    hi = min(hi, n)
    total = 0
    i = lo
    while i <= hi:
        q = n // i
        j = min(hi, n // q)
        total += q * (j - i + 1)
        i = j + 1
    return total


def F(limit):
    bmax = isqrt(limit)
    while bmax * (bmax + 1) > limit:
        bmax -= 1
    mobius_divisors = _mobius_and_divisors(bmax)

    total = 0
    for b in range(2, bmax + 1):
        m = limit // b
        for d, mu in mobius_divisors[b]:
            total += mu * _floor_sum(m // d, b // d + 1, (2 * b - 1) // d)
    return total


def solve():
    assert F(15) == 4
    assert F(1000) == 1069
    return F(10 ** 12)


if __name__ == "__main__":
    print(solve())
