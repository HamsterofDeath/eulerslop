#!/usr/bin/env python3
"""Project Euler 633: square prime factors."""

from math import pi


def primes_upto(limit):
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[:2] = b"\x00\x00"
    root = int(limit**0.5)
    for n in range(2, root + 1):
        if sieve[n]:
            start = n * n
            sieve[start : limit + 1 : n] = b"\x00" * (((limit - start) // n) + 1)
    return (n for n in range(limit + 1) if sieve[n])


def c_square_prime_factors(k):
    # For each prime p, p^2 divides a random integer with limiting
    # probability 1/p^2.  Factor out product_p(1 - 1/p^2) = 1/zeta(2).
    coeff = [0.0] * (k + 1)
    coeff[0] = 1.0
    for p in primes_upto(5_000_000):
        term = 1.0 / (p * p - 1.0)
        for j in range(k, 0, -1):
            coeff[j] += coeff[j - 1] * term
    return (6.0 / (pi * pi)) * coeff[k]


def solve():
    return f"{c_square_prime_factors(7):.4e}"


def main():
    print(solve())


if __name__ == "__main__":
    main()
