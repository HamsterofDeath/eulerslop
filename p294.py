#!/usr/bin/env python3
# S(n): count k < 10^n with digit sum d(k) = 23 and k divisible by 23, for n = 11^12.
#
# Write k with n digit positions (leading zeros allowed).  Position i contributes
# d_i * 10^i mod 23, and 10 has multiplicative order 22 mod 23, so positions fall
# into 22 residue classes by i mod 22.  Class c contains N_c positions, where
# n = 22*K + 11 (11^12 ≡ 11 mod 22): classes 0..10 have K+1 positions, 11..21 have K.
#
# Since the digit sum is only 23, at most 23 positions are nonzero.  Within a class
# the positions are interchangeable for the mod-23 contribution: putting nonzero
# digits with value-sum s into class c adds s * 10^c (mod 23).  The number of ways
# to place digits of sum s into N_c distinct positions of one class is
#   g_c[s] = sum_j C(N_c, j) * W(s, j),
# where W(s, j) counts compositions of s into j parts from 1..9.  C(N_c, j) is
# computed exactly with big integers (j <= 23), then reduced mod 10^9.
#
# A DP over the 22 classes with state (digit sum so far <= 23, residue mod 23)
# then yields S(n) = dp[23][0] mod 10^9.

MOD = 10 ** 9


def solve():
    n = 11 ** 12
    K, rem = divmod(n, 22)  # rem = 11

    # W[s][j]: compositions of s into exactly j parts, each 1..9.
    W = [[0] * 24 for _ in range(24)]
    W[0][0] = 1
    for s in range(1, 24):
        for j in range(1, 24):
            W[s][j] = sum(W[s - v][j - 1] for v in range(1, 10) if v <= s)

    def binom_mod(N, j):
        num = 1
        for t in range(j):
            num *= N - t
        from math import factorial
        return (num // factorial(j)) % MOD

    # g for a class with N positions: g[s] = sum_j C(N, j) * W(s, j) mod 1e9.
    def class_g(N):
        binoms = [binom_mod(N, j) for j in range(24)]
        return [sum(binoms[j] * W[s][j] for j in range(s, -1, -1)) % MOD
                for s in range(24)]

    g_big = class_g(K + 1)   # classes 0..rem-1
    g_small = class_g(K)     # classes rem..21

    # DP over classes: state (sum s, residue r mod 23).
    dp = [[0] * 23 for _ in range(24)]
    dp[0][0] = 1
    for c in range(22):
        g = g_big if c < rem else g_small
        t = pow(10, c, 23)
        ndp = [[0] * 23 for _ in range(24)]
        for s in range(24):
            row = dp[s]
            for r in range(23):
                v = row[r]
                if v:
                    for sc in range(24 - s):
                        w = g[sc]
                        if w:
                            ndp[s + sc][(r + sc * t) % 23] = (
                                ndp[s + sc][(r + sc * t) % 23] + v * w) % MOD
        dp = ndp
    return dp[23][0] % MOD


if __name__ == "__main__":
    print(solve())
