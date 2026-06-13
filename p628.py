#!/usr/bin/env python3
"""Project Euler 628: Open chess positions."""


MOD = 1_008_691_207
N = 100_000_000


def factorial_prefix_sum(n, mod):
    """Return sum(k!, k=0..n-1) modulo ``mod``."""
    fact = 1
    total = 1
    for k in range(1, n):
        fact = (fact * k) % mod
        total += fact
        if total >= mod:
            total -= mod
    return total


def solve(n=N, mod=MOD):
    # Closed positions are the union of two symmetric forced-border events.
    # Inclusion-exclusion simplifies the open count to this expression.
    return ((n - 3) * factorial_prefix_sum(n, mod) + 2) % mod


if __name__ == "__main__":
    print(solve())
