#!/usr/bin/env python3
# Project Euler 329 - Prime Frog
#
# Exact probability DP with fractions. The frog starts uniformly on 1..500,
# croaks (P w.p. 2/3 on a prime square, else 1/3; N swaps these) just before
# each jump, and jumps +-1 with prob 1/2 (forced move at squares 1 and 500).
# 15 croaks -> 14 jumps. dp[s] = probability of being on square s having
# produced the croaks heard so far.

from fractions import Fraction

def solve():
    LIMIT = 500
    sieve = [True] * (LIMIT + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(LIMIT ** 0.5) + 1):
        if sieve[i]:
            for j in range(i * i, LIMIT + 1, i):
                sieve[j] = False

    seq = "PPPPNNPPPNPPNPN"
    half = Fraction(1, 2)
    p23 = Fraction(2, 3)
    p13 = Fraction(1, 3)

    def croak(s, c):
        if sieve[s]:  # prime square
            return p23 if c == 'P' else p13
        return p13 if c == 'P' else p23

    # initial croak from the uniformly random start square
    dp = [Fraction(0)] * (LIMIT + 1)
    u = Fraction(1, LIMIT)
    for s in range(1, LIMIT + 1):
        dp[s] = u * croak(s, seq[0])

    for c in seq[1:]:
        new = [Fraction(0)] * (LIMIT + 1)
        for s in range(1, LIMIT + 1):
            if dp[s] == 0:
                continue
            if s == 1:
                new[2] += dp[s]
            elif s == LIMIT:
                new[LIMIT - 1] += dp[s]
            else:
                new[s - 1] += dp[s] * half
                new[s + 1] += dp[s] * half
        for s in range(1, LIMIT + 1):
            if new[s]:
                new[s] *= croak(s, c)
        dp = new

    ans = sum(dp, Fraction(0))
    return f"{ans.numerator}/{ans.denominator}"

if __name__ == "__main__":
    print(solve())
