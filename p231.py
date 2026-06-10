#!/usr/bin/env python3
import numpy as np

def legendre(n, p):
    """Exponent of prime p in n! via Legendre's formula."""
    e = 0
    pk = p
    while pk <= n:
        e += n // pk
        pk *= p
    return e

def factor_sum(n, k):
    """Sum of p * exponent over prime factorisation of C(n, k)."""
    sieve = np.ones(n + 1, dtype=bool)
    sieve[:2] = False
    for p in range(2, int(n ** 0.5) + 1):
        if sieve[p]:
            sieve[p * p::p] = False
    primes = np.flatnonzero(sieve)

    total = 0
    for p in primes.tolist():
        e = legendre(n, p) - legendre(k, p) - legendre(n - k, p)
        if e:
            total += p * e
    return total

def solve():
    assert factor_sum(10, 3) == 14
    return factor_sum(20000000, 15000000)

if __name__ == "__main__":
    print(solve())
