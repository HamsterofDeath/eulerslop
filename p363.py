#!/usr/bin/env python3
import math
import numpy as np

def solve():
    # With P0=(1,0), P1=(1,v), P2=(v,1), P3=(0,1) the Bernstein expansion is
    #   x(t) = 1 + 3(v-1) t^2 + (2-3v) t^3,   y(t) = x(1-t).
    # The area bounded by O P0, the curve, and P3 O follows from Green's
    # theorem: A(v) = 1/2 * Int_0^1 (x y' - y x') dt; the two segments through
    # the origin contribute nothing.  The integrand is a degree-5 polynomial
    # in t, so a few Gauss-Legendre nodes integrate it exactly; we bisect on v
    # until A(v) = pi/4.  Then L(v) = Int_0^1 sqrt(x'^2 + y'^2) dt is computed
    # with composite Gauss-Legendre (smooth integrand, converges far below
    # the requested precision) and compared with pi/2.
    def xy_derivs(v, t):
        x = 1.0 + 3.0 * (v - 1.0) * t * t + (2.0 - 3.0 * v) * t ** 3
        y = 3.0 * v * t + (3.0 - 6.0 * v) * t * t + (3.0 * v - 2.0) * t ** 3
        dx = 6.0 * (v - 1.0) * t + (6.0 - 9.0 * v) * t * t
        dy = 3.0 * v + (6.0 - 12.0 * v) * t + (9.0 * v - 6.0) * t * t
        return x, y, dx, dy

    # Gauss-Legendre nodes mapped to [0, 1]
    nodes8, weights8 = np.polynomial.legendre.leggauss(8)
    t8, w8 = 0.5 * (nodes8 + 1.0), 0.5 * weights8

    def area(v):
        x, y, dx, dy = xy_derivs(v, t8)
        return 0.5 * float(np.dot(w8, x * dy - y * dx))

    # A(v) is increasing near the root; bisect to machine precision.
    target = math.pi / 4.0
    lo, hi = 0.0, 1.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if mid == lo or mid == hi:
            break
        if area(mid) < target:
            lo = mid
        else:
            hi = mid
    v = 0.5 * (lo + hi)

    # arc length: 64 panels x 16 Gauss nodes
    nodes16, weights16 = np.polynomial.legendre.leggauss(16)
    panels = 64
    h = 1.0 / panels
    starts = np.arange(panels) * h
    t = (starts[:, None] + 0.5 * h * (nodes16 + 1.0)[None, :]).ravel()
    w = np.tile(0.5 * h * weights16, panels)
    _, _, dx, dy = xy_derivs(v, t)
    length = float(np.dot(w, np.sqrt(dx * dx + dy * dy)))

    deviation = 100.0 * (length - math.pi / 2.0) / (math.pi / 2.0)
    return f"{deviation:.10f}"

if __name__ == "__main__":
    print(solve())
