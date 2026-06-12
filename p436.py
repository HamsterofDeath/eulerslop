import math
import numpy as np


# Renewal theory for iid U(0,1) draws: density of renewal epochs at t in [0,1]
# is e^t (plus the atom at 0).  Hence:
#  * Louise's partial sum A just before crossing 1 and her last draw x have
#    joint density f(a, x) = e^a on {0<a<1, x>1-a}  (atom a=0 has weight 0).
#  * Julie then faces gap g = 2-a-x in (0,1); her last draw y has conditional
#    density f(y|g) = 1_{y>g} + e^g - e^{max(0, g-y)} on (0,1).
# Integrating y over (x,1):
#    G(x,g) = P(y > x | g) = (1-x)e^g                      if x >= g
#           = 1 + (1-x)e^g - e^{g-x}                       if x <  g
# P(win) = int_0^1 da int_{1-a}^1 dx e^a G(x, 2-a-x).
# Doing the x-integral (kink at x = 1-a/2 where x = g) gives
#    I(a) = a/2 + (a-1)e + e^{1-a} - (e^a-1)/2,
# and int_0^1 e^a I(a) da collapses to the closed form
#    P = 1/4 + 7e/2 - 5e^2/4.


def quadrature_check():
    # Independent numerical evaluation of the 2D integral (Gauss-Legendre,
    # inner integral split at the kink x = 1 - a/2).
    nodes, weights = np.polynomial.legendre.leggauss(64)

    def G(x, g):
        return (1.0 - x) * math.exp(g) if x >= g else \
            1.0 + (1.0 - x) * math.exp(g) - math.exp(g - x)

    def inner(a):
        s = 0.0
        for lo, hi in ((1.0 - a, 1.0 - a / 2.0), (1.0 - a / 2.0, 1.0)):
            mid, half = (lo + hi) / 2.0, (hi - lo) / 2.0
            s += half * sum(w * G(mid + half * t, 2.0 - a - (mid + half * t))
                            for t, w in zip(nodes, weights))
        return s

    return 0.5 * sum(w * math.exp(0.5 + 0.5 * t) * inner(0.5 + 0.5 * t)
                     for t, w in zip(nodes, weights))


def solve():
    p = 0.25 + 3.5 * math.e - 1.25 * math.e ** 2
    assert abs(p - quadrature_check()) < 1e-12
    return f"{p:.10f}"


if __name__ == "__main__":
    print(solve())
