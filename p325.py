#!/usr/bin/env python3
from math import isqrt
import sys

# This is Euclid's game: from (x, y), x < y, subtract a positive multiple of
# x from y.  Its losing (P-)positions are exactly the pairs with
#   x < y < phi*x,   phi = (1+sqrt(5))/2
# (verifiable by brute force; from such a pair the only moves jump across the
# golden-ratio cone into a winning position and vice versa).
#
# So  S(N) = sum_x sum_{y=x+1}^{u(x)} (x+y)  with u(x) = min(N, floor(phi*x)).
# Writing floor(phi*x) = x + g(x), g(x) = floor(beta*x), beta = 1/phi =
# (sqrt(5)-1)/2, the inner sum for u(x) = floor(phi*x) equals
#   2*x*g(x) + (g(x)^2 + g(x))/2,
# so we need W = sum g, Wx = sum x*g, W2 = sum g^2 up to x0, the largest x
# with floor(phi*x) <= N.  These weighted Beatty sums satisfy exact integer
# recursions obtained by counting lattice points 1 <= y <= beta*x both ways
# (y <= beta*x  <=>  x >= floor(phi*y)+1, and floor(phi*y) = y + g(y)):
# each step shrinks n by the factor beta, giving O(log n) depth.

def fbeta(x):
    # floor(beta*x) = floor((sqrt(5)-1)x/2), exact via integer sqrt
    return (isqrt(5 * x * x) - x) // 2

def beatty_sums(n):
    # returns (W, Wx, W2) = (sum g, sum x*g, sum g^2) for x = 1..n
    if n <= 0:
        return 0, 0, 0
    m = fbeta(n)
    W_m, Wx_m, W2_m = beatty_sums(m)
    sy = m * (m + 1) // 2
    sy2 = m * (m + 1) * (2 * m + 1) // 6
    sf = sy + W_m                                   # sum of f_y = y + g_y
    sf2 = sy2 + 2 * Wx_m + W2_m                     # sum of f_y^2
    W = n * m - sf
    Wx = m * n * (n + 1) // 2 - (sf2 + sf) // 2
    W2 = n * m * m - 2 * (sy2 + Wx_m) + sf
    return W, Wx, W2

def S(N):
    # x0 = largest x with floor(phi*x) <= N  <=>  x <= floor((N+1)*beta)
    x0 = fbeta(N + 1)
    W, Wx, W2 = beatty_sums(x0)
    total = 2 * Wx + (W2 + W) // 2
    # tail x0 < x <= N-1: every y in (x, N] is losing; closed-form sums
    a, b = x0 + 1, N - 1
    if a <= b:
        sq = lambda k: k * (k + 1) * (2 * k + 1) // 6
        S1 = (a + b) * (b - a + 1) // 2             # sum x
        S2 = sq(b) - sq(a - 1)                      # sum x^2
        total += N * S1 - S2 + (b - a + 1) * N * (N + 1) // 2 - (S2 + S1) // 2
    return total

def solve():
    sys.setrecursionlimit(10000)
    assert S(10) == 211 and S(10 ** 4) == 230312207313   # given check values
    return S(10 ** 16) % 7 ** 10

if __name__ == "__main__":
    print(solve())
