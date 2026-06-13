#!/usr/bin/env python3
"""Project Euler 634: numbers of the form a^2 b^3."""

from math import isqrt


def icbrt(n):
    lo, hi = 0, 1
    while hi * hi * hi <= n:
        hi *= 2
    while lo + 1 < hi:
        mid = (lo + hi) // 2
        if mid * mid * mid <= n:
            lo = mid
        else:
            hi = mid
    return lo


def mobius_and_primes(limit):
    mu = [0] * (limit + 1)
    mu[1] = 1
    primes = []
    composite = bytearray(limit + 1)
    for n in range(2, limit + 1):
        if not composite[n]:
            primes.append(n)
            mu[n] = -1
        for p in primes:
            v = n * p
            if v > limit:
                break
            composite[v] = 1
            if n % p == 0:
                mu[v] = 0
                break
            mu[v] = -mu[n]
    return mu, primes


def cubefree_count(n, mu):
    return sum(mu[d] * (n // (d * d * d)) for d in range(1, icbrt(n) + 1))


def F(n):
    max_b = icbrt(n)
    mu, primes = mobius_and_primes(max_b)

    total = 0
    for b in range(2, max_b + 1):
        if mu[b]:
            total += isqrt(n // (b * b * b)) - 1

    # Perfect squares have normalized squarefree cubic part 1.  Such x=m^2
    # works iff m has a proper cube divisor; the only non-cubefree misses are
    # prime cubes.
    m_limit = isqrt(n)
    cube_limit = icbrt(m_limit)
    prime_cubes = sum(1 for p in primes if p <= cube_limit)
    total += m_limit - cubefree_count(m_limit, mu) - prime_cubes
    return total


def solve():
    return F(9 * 10**18)


def main():
    print(solve())


if __name__ == "__main__":
    main()
