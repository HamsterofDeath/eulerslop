#!/usr/bin/env python3
# Project Euler 285: Pythagorean Odds.
#
# With u = k*a + 1, v = k*b + 1, the pair (u, v) is uniform on the square
# [1, k+1]^2 (Jacobian 1/k^2).  The score is k exactly when
#     (k - 1/2)^2 <= u^2 + v^2 < (k + 1/2)^2,
# so P(k) = area of the annulus slice inside the square divided by k^2, and
# the expected total is  sum_k k * P(k) = sum_k (A(k+1/2) - A(k-1/2)) / k.
#
# A(R) = area{ u >= 1, v >= 1, u^2 + v^2 <= R^2 }.  The circle's upper bound
# never exceeds the square's far sides (sqrt(R^2 - 1) < k + 1 for R = k+1/2),
# so integrating sqrt(R^2-u^2) - 1 for u from 1 to sqrt(R^2-1) gives the
# closed form
#     A(R) = (R^2/2) * (acos(1/R) - asin(1/R)) - sqrt(R^2 - 1) + 1
# valid for R >= sqrt(2); A(R) = 0 otherwise (circle misses the corner (1,1)).
# acos(1/R) - asin(1/R) = pi/2 - 2*asin(1/R) is used for numerical stability.

from math import asin, sqrt, pi


def area(R):
    if R * R <= 2.0:
        return 0.0
    return (R * R / 2.0) * (pi / 2.0 - 2.0 * asin(1.0 / R)) - sqrt(R * R - 1.0) + 1.0


def solve():
    total = 0.0
    for k in range(1, 10 ** 5 + 1):
        total += (area(k + 0.5) - area(k - 0.5)) / k
    return f"{total:.5f}"


if __name__ == "__main__":
    print(solve())
