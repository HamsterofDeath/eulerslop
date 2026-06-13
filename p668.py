#!/usr/bin/env python3
"""Project Euler 668: Square root smooth numbers."""

from math import isqrt


N = 10_000_000_000


def prime_count_table(n):
    """Return pi(v) for every distinct v = floor(n / k), plus small v."""
    values = []
    i = 1
    while i <= n:
        v = n // i
        values.append(v)
        i = n // v + 1

    counts = {v: v - 1 for v in values}
    for p in range(2, isqrt(n) + 1):
        if counts[p] == counts[p - 1]:
            continue
        before_p = counts[p - 1]
        p2 = p * p
        for v in values:
            if v < p2:
                break
            counts[v] -= counts[v // p] - before_p
    return counts


def sum_primes_up_to(limit):
    sieve = bytearray(b"\x01") * (limit + 1)
    if limit >= 0:
        sieve[0:1] = b"\x00"
    if limit >= 1:
        sieve[1:2] = b"\x00"
    for p in range(2, isqrt(limit) + 1):
        if sieve[p]:
            start = p * p
            sieve[start : limit + 1 : p] = b"\x00" * (((limit - start) // p) + 1)
    return sum(i for i in range(limit + 1) if sieve[i])


def solve(n=N):
    root = isqrt(n)
    pi = prime_count_table(n)

    # A non-smooth m has a unique largest prime factor p >= sqrt(m), so
    # m = p * k with k <= p.  Count those pairs and subtract from all m.
    not_smooth = sum_primes_up_to(root)
    for k in range(1, root):
        not_smooth += k * (pi[n // k] - pi[n // (k + 1)])
    return n - not_smooth


if __name__ == "__main__":
    print(solve())
