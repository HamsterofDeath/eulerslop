#!/usr/bin/env python3
"""Project Euler 649: Low-Down Triple Deuce."""

MOD = 10**9
N = 10_000_019
COINS = 100

GRUNDY_PERIOD = (0, 0, 1, 1, 2, 2, 3, 3, 4)
XOR_STATES = 8


def coordinate_grundy_counts(n):
    """Counts of one-dimensional Grundy values for coordinates 0..n-1."""
    q, r = divmod(n, len(GRUNDY_PERIOD))
    counts = [0] * XOR_STATES
    for value in GRUNDY_PERIOD:
        counts[value] += q
    for value in GRUNDY_PERIOD[:r]:
        counts[value] += 1
    return counts


def square_grundy_counts(n, mod):
    """Counts of square Grundy values g(x) xor g(y), modulo mod."""
    coordinate_counts = coordinate_grundy_counts(n)
    square_counts = [0] * XOR_STATES
    for gx, cx in enumerate(coordinate_counts):
        if not cx:
            continue
        for gy, cy in enumerate(coordinate_counts):
            if cy:
                square_counts[gx ^ gy] = (
                    square_counts[gx ^ gy] + cx * cy
                ) % mod
    return square_counts


def losing_arrangements(n, coins, mod):
    """Number of distinguishable-coin arrangements with total xor zero."""
    square_counts = square_grundy_counts(n, mod)
    dp = [0] * XOR_STATES
    dp[0] = 1
    for _ in range(coins):
        next_dp = [0] * XOR_STATES
        for old_xor, ways in enumerate(dp):
            if not ways:
                continue
            for square_xor, count in enumerate(square_counts):
                if count:
                    next_dp[old_xor ^ square_xor] = (
                        next_dp[old_xor ^ square_xor] + ways * count
                    ) % mod
        dp = next_dp
    return dp[0]


def solve(n=N, coins=COINS, mod=MOD):
    total = pow((n * n) % mod, coins, mod)
    return (total - losing_arrangements(n, coins, mod)) % mod


if __name__ == "__main__":
    print(solve())
