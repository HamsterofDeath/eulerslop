#!/usr/bin/env python3
"""Project Euler 216: Primality of 2n^2-1.

Count n <= 50,000,000 such that t(n) = 2n^2 - 1 is prime.

Method: a prime p divides 2n^2 - 1 iff n^2 == (p+1)/2 (mod p), which has
solutions iff 2 is a quadratic residue mod p, i.e. p == +-1 (mod 8).
For every such prime p up to sqrt(2N^2 - 1) we compute a square root r of
(p+1)/2 mod p (a single modular exponentiation when p == 7 (mod 8),
Tonelli-Shanks when p == 1 (mod 8)) and strike out all n == +-r (mod p)
in a numpy boolean array.  Any t(n) surviving the sieve has no prime
factor up to sqrt(t(n)) and is therefore prime.  The handful of small n
whose t(n) is itself a sieving prime (and thus got struck by itself) are
repaired by direct trial division at the end.
"""

from math import isqrt

import numpy as np

N = 50_000_000


def prime_sieve(limit):
    """All primes <= limit as a numpy int64 array."""
    flags = np.ones(limit + 1, dtype=bool)
    flags[:2] = False
    for p in range(2, isqrt(limit) + 1):
        if flags[p]:
            flags[p * p:: p] = False
    return np.nonzero(flags)[0]


def sqrt_mod_ts(a, p):
    """Tonelli-Shanks square root of a mod p (p odd prime, a a residue)."""
    q = p - 1
    s = 0
    while q & 1 == 0:
        q >>= 1
        s += 1
    # Find a quadratic non-residue z (2 is a residue here, start at 3).
    z = 3
    e = (p - 1) >> 1
    while pow(z, e, p) != p - 1:
        z += 2
    m = s
    c = pow(z, q, p)
    t = pow(a, q, p)
    r = pow(a, (q + 1) >> 1, p)
    while t != 1:
        t2 = t
        i = 0
        while t2 != 1:
            t2 = t2 * t2 % p
            i += 1
        b = pow(c, 1 << (m - i - 1), p)
        m = i
        c = b * b % p
        t = t * c % p
        r = r * b % p
    return r


def solve():
    bound = isqrt(2 * N * N - 1)  # largest possible prime factor of a composite t(n)
    primes = prime_sieve(bound)

    is_t_prime = np.ones(N + 1, dtype=bool)
    is_t_prime[:2] = False  # n starts at 2

    residue = primes & 7
    p7 = primes[residue == 7].tolist()  # sqrt via single pow
    p1 = primes[residue == 1].tolist()  # sqrt via Tonelli-Shanks

    def strike(r, p):
        is_t_prime[(r if r >= 2 else r + p):: p] = False
        r2 = p - r
        is_t_prime[(r2 if r2 >= 2 else r2 + p):: p] = False

    for p in p7:
        # (p+1)/2 is the inverse of 2 mod p; p == 3 (mod 4) so sqrt is a pow.
        strike(pow((p + 1) >> 1, (p + 1) >> 2, p), p)

    for p in p1:
        strike(sqrt_mod_ts((p + 1) >> 1, p), p)

    # Repair small n where t(n) itself is a sieving prime (struck by itself).
    small_primes = primes[primes <= isqrt(bound)].tolist()
    for n in range(2, isqrt((bound + 1) // 2) + 1):
        t = 2 * n * n - 1
        prime = True
        for p in small_primes:
            if p * p > t:
                break
            if t % p == 0:
                prime = False
                break
        is_t_prime[n] = prime

    return int(np.count_nonzero(is_t_prime))


if __name__ == "__main__":
    print(solve())
