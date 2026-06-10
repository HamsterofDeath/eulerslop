#!/usr/bin/env python3
"""p175: f(n) = ways to write n as sum of powers of 2 (max 2 each).

Stern-Brocot / Stern's diatomic sequence: the ratios f(n)/f(n-1) enumerate
the positive rationals, and the run-length encoding of n's binary expansion
(read LSB to MSB) equals the continued fraction of p/q.

For p < q the CF is [0; a1, ..., am]. The runs of n from LSB to MSB are
[a1, ..., am], where the number of runs must be odd (the MSB run is ones).
If m is even, use the equivalent CF ending [..., am - 1, 1] (or merge a
trailing 1 into the previous term). The Shortened Binary Expansion (runs
read MSB to LSB) is then the reversal of that list."""
from math import gcd


def solve():
    num = 123456789
    den = 987654321
    g = gcd(num, den)
    a, b = num // g, den // g

    # Continued fraction of a/b (a < b, so cf[0] == 0).
    cf = []
    while b:
        cf.append(a // b)
        a, b = b, a % b

    terms = cf[1:]  # drop the leading 0

    # Runs of n (LSB to MSB) = terms, but the run count must be odd so the
    # most significant run consists of ones. Use the CF identity
    # [..., am] == [..., am - 1, 1] to fix the parity.
    if len(terms) % 2 == 0:
        if terms[-1] > 1:
            terms[-1] -= 1
            terms.append(1)
        else:
            terms.pop()
            terms[-1] += 1

    runs = terms[::-1]  # MSB to LSB
    return ",".join(str(r) for r in runs)


if __name__ == "__main__":
    print(solve())
