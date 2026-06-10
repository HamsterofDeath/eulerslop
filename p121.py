#!/usr/bin/env python3
from fractions import Fraction

def solve():
    turns = 15
    dp = [Fraction(0)] * (turns + 1)
    dp[0] = Fraction(1)
    for t in range(1, turns + 1):
        new = [Fraction(0)] * (turns + 1)
        for b in range(t + 1):
            if b > 0:
                new[b] += dp[b-1] * Fraction(1, t + 1)
            if b < t:
                new[b] += dp[b] * Fraction(t, t + 1)
        dp = new
    prob = sum(dp[b] for b in range(turns // 2 + 1, turns + 1))
    return prob.denominator // prob.numerator

if __name__ == "__main__":
    print(solve())
