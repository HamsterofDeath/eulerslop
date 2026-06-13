#!/usr/bin/env python3
"""Project Euler 638: weighted lattice paths."""

MOD = 1_000_000_007


def binomial_mod(n, r):
    r = min(r, n - r)
    numerator = 1
    denominator = 1
    for i in range(1, r + 1):
        numerator = numerator * (n - r + i) % MOD
        denominator = denominator * i % MOD
    return numerator * pow(denominator, MOD - 2, MOD) % MOD


def q_binomial(a, b, q):
    """Gaussian binomial [a+b choose a]_q modulo MOD."""
    if q == 1:
        return binomial_mod(a + b, a)

    r = min(a, b)
    s = max(a, b)
    numerator = 1
    denominator = 1
    q_i = q % MOD
    q_s_i = pow(q, s + 1, MOD)

    for _ in range(r):
        denominator = denominator * (q_i - 1) % MOD
        numerator = numerator * (q_s_i - 1) % MOD
        q_i = q_i * q % MOD
        q_s_i = q_s_i * q % MOD

    return numerator * pow(denominator, MOD - 2, MOD) % MOD


def solve():
    total = 0
    for k in range(1, 8):
        side = 10**k + k
        total = (total + q_binomial(side, side, k)) % MOD
    return total


def main():
    print(solve())


if __name__ == "__main__":
    main()
