#!/usr/bin/env python3
import numpy as np

MOD = 1234567891011
START = 10 ** 14
COUNT = 100000

def small_primes(limit):
    """All primes <= limit via numpy sieve."""
    sieve = np.ones(limit + 1, dtype=bool)
    sieve[:2] = False
    for p in range(2, int(limit ** 0.5) + 1):
        if sieve[p]:
            sieve[p * p::p] = False
    return np.nonzero(sieve)[0]

def primes_after(start, count):
    """First `count` primes > start, via a segmented sieve.

    sqrt(start + window) barely exceeds 10^7, so sieving with primes up to
    10^7 + 10 is a fully deterministic primality test for the segment.
    """
    window = 8 * 10 ** 6  # avg gap near 10^14 is ~32, so this is ample
    base = small_primes(10 ** 7 + 10)
    seg = np.ones(window, dtype=bool)  # seg[i] represents start + 1 + i
    lo = start + 1
    for p in base:
        p = int(p)
        first = (-lo) % p
        seg[first::p] = False
    primes = (lo + np.nonzero(seg)[0])[:count]
    assert len(primes) == count
    return [int(p) for p in primes]

def fib_pair(n, m):
    """(F(n), F(n+1)) mod m by fast doubling."""
    if n == 0:
        return 0, 1
    a, b = fib_pair(n >> 1, m)
    c = a * ((2 * b - a) % m) % m
    d = (a * a + b * b) % m
    if n & 1:
        return d, (c + d) % m
    return c, d

def solve():
    ps = primes_after(START, COUNT)
    # Precompute F(g), F(g+1) mod MOD for every possible gap g, then advance
    # along consecutive primes with F(n+g) = F(g)F(n+1) + F(g-1)F(n),
    # F(n+g+1) = F(g+1)F(n+1) + F(g)F(n)  (addition formula).
    maxgap = max(b - a for a, b in zip(ps, ps[1:]))
    fib = [0, 1]
    for _ in range(maxgap + 1):
        fib.append((fib[-1] + fib[-2]) % MOD)

    fa, fb = fib_pair(ps[0], MOD)  # F(p1), F(p1+1)
    total = fa
    for i in range(1, COUNT):
        g = ps[i] - ps[i - 1]
        fa, fb = ((fib[g] * fb + fib[g - 1] * fa) % MOD,
                  (fib[g + 1] * fb + fib[g] * fa) % MOD)
        total += fa
    return total % MOD

if __name__ == "__main__":
    print(solve())
