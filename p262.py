#!/usr/bin/env python3
# Project Euler 262: Mountain Range
#
# The exponent term |1e-6(x^2+y^2) - 0.0015(x+y) + 0.7| vanishes on the
# circle (x-750)^2 + (y-750)^2 = 425000, where h equals the polynomial part
# g(x,y); this ring is a high mountain ridge (g >= ~10972 on it) encircling
# the centre of the area.  A(200,200) and B(1400,1400) both lie outside it.
#
# At elevation f the mosquito must avoid the region {h > f}, a closed band
# around the ridge.  Crossing the ridge itself costs >= min g on the circle
# (~10972).  The cheaper way is around the ridge, squeezing between the band
# and the border of the area.  Along the bottom edge y=0 (and by x<->y
# symmetry the left edge x=0) h has a single hump whose peak (~10430.7 near
# x=900) is the bottleneck: f_min = max_x h(x, 0).  At that elevation the
# forbidden band touches y=0 at exactly one point T=(x*,0), and the trip
# A -> T -> B squeezes through it (the symmetric route through (0,x*) has
# equal length).  All other edges stay below f_min (asserted).
#
# Shortest path: a taut string from A to B around one side of a single
# obstacle K is the corresponding boundary chain of conv(K U {A,B})
# (straight tangent segments plus arcs of the contour h = f_min, shortcutting
# any concave dents).  We trace the outer contour by radial bisection from
# the ring centre (750,750), build the convex hull of contour + A + B with
# scipy, and measure the chain that passes through the bottom pinch point.

import numpy as np
from scipy.spatial import ConvexHull


def h(x, y):
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    return ((5000.0 - 0.005 * (x * x + y * y + x * y) + 12.5 * (x + y))
            * np.exp(-np.abs(1e-6 * (x * x + y * y)
                             - 0.0015 * (x + y) + 0.7)))


def solve():
    A = np.array([200.0, 200.0])
    B = np.array([1400.0, 1400.0])
    C = np.array([750.0, 750.0])          # ridge circle centre
    R0 = np.sqrt(425000.0)                 # ridge circle radius

    # ---- 1) f_min = max of h along the bottom edge y = 0 ----------------
    xs = np.linspace(0.0, 1600.0, 16001)
    i = int(np.argmax(h(xs, 0.0)))
    lo, hi = xs[i - 1], xs[i + 1]
    invphi = (np.sqrt(5.0) - 1.0) / 2.0    # golden-section maximisation
    a_, b_ = lo, hi
    c_ = b_ - invphi * (b_ - a_)
    d_ = a_ + invphi * (b_ - a_)
    fc, fd = h(c_, 0.0), h(d_, 0.0)
    for _ in range(120):
        if fc > fd:
            b_, d_, fd = d_, c_, fc
            c_ = b_ - invphi * (b_ - a_)
            fc = h(c_, 0.0)
        else:
            a_, c_, fc = c_, d_, fd
            d_ = a_ + invphi * (b_ - a_)
            fd = h(d_, 0.0)
    xstar = (a_ + b_) / 2.0
    f = float(h(xstar, 0.0))
    T = np.array([xstar, 0.0])             # pinch point on the bottom edge

    # sanity: endpoints reachable, other edges open, ridge fully above f
    assert h(*A) < f and h(*B) < f
    es = np.linspace(0.0, 1600.0, 8001)
    assert h(1600.0, es).max() < f and h(es, 1600.0).max() < f
    th_chk = np.linspace(0.0, 2 * np.pi, 4096)
    assert h(C[0] + R0 * np.cos(th_chk), C[1] + R0 * np.sin(th_chk)).min() > f

    # ---- 2) trace the outer contour h = f around the ridge --------------
    N = 200000
    th = np.linspace(0.0, 2 * np.pi, N, endpoint=False)
    ct, st = np.cos(th), np.sin(th)
    rlo = np.full(N, R0)                   # h > f on the ridge
    rhi = np.full(N, 1200.0)               # h < f well outside
    assert h(C[0] + rhi * ct, C[1] + rhi * st).max() < f
    for _ in range(55):
        mid = 0.5 * (rlo + rhi)
        inside = h(C[0] + mid * ct, C[1] + mid * st) > f
        rlo = np.where(inside, mid, rlo)
        rhi = np.where(inside, rhi, mid)
    r = 0.5 * (rlo + rhi)
    pts = np.column_stack((C[0] + r * ct, C[1] + r * st))

    # ---- 3) convex hull of contour + endpoints; take the bottom chain ---
    allpts = np.vstack((pts, T, A, B))
    hull = ConvexHull(allpts)
    verts = hull.vertices                  # counter-clockwise cycle
    n = len(allpts)
    ia = int(np.where(verts == n - 2)[0][0])   # A
    ib = int(np.where(verts == n - 1)[0][0])   # B
    cyc = list(verts)

    def chain(i, j):
        if i <= j:
            return cyc[i:j + 1]
        return cyc[i:] + cyc[:j + 1]

    c1, c2 = chain(ia, ib), chain(ib, ia)[::-1]
    ymins = [min(allpts[k][1] for k in c) for c in (c1, c2)]
    path = c1 if ymins[0] < ymins[1] else c2   # the one through T (y = 0)
    p = allpts[path]
    length = float(np.sum(np.hypot(np.diff(p[:, 0]), np.diff(p[:, 1]))))
    return f"{length:.3f}"


if __name__ == "__main__":
    print(solve())
