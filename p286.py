#!/usr/bin/env python3
"""Project Euler 286: Scoring probabilities.

Barbara scores from distance x with probability p_x = 1 - x/q.  The number
of points over shots x = 1..50 has probability generating function
    prod_{x=1}^{50} ((1 - p_x) + p_x * z),
so P(score = 20) is the coefficient of z^20, computable by a small DP.
P(20) is a smooth, strictly decreasing function of q in the region of
interest (q >= 50, where the mean score already exceeds 20), so we solve
P(20)(q) = 0.02 by Brent root-finding.
"""

from scipy.optimize import brentq


def prob20(q):
    # DP over shots: dp[k] = probability of exactly k points so far.
    # We only need counts up to 20.
    dp = [0.0] * 21
    dp[0] = 1.0
    for x in range(1, 51):
        p = 1.0 - x / q
        new = [0.0] * 21
        for k in range(21):
            v = dp[k]
            if v:
                new[k] += v * (1.0 - p)          # miss
                if k < 20:
                    new[k + 1] += v * p          # score
        dp = new
    return dp[20]


def solve():
    # For q in [50, 60] the mean score goes from 24.5 to 28.75 and P(20)
    # decreases monotonically through 0.02 (P(20) ~ 0.042 at q=50,
    # ~0.002 at q=60), so this bracket contains exactly one root.
    q = brentq(lambda t: prob20(t) - 0.02, 50.0, 60.0, xtol=1e-13, rtol=8.9e-16)
    return f"{q:.10f}"


if __name__ == "__main__":
    print(solve())
