#!/usr/bin/env python3
import numpy as np
from math import gcd, sqrt

# Project Euler 314: maximize enclosed-area / wall-length for a closed polygon
# with vertices on a 501x501 lattice (500m x 500m square).
#
# The optimum is convex and symmetric under the square's 8 symmetries, so work
# in coordinates centered on the square and consider only the octant
# 0 <= x <= y <= 250: a boundary piece runs from a post (0, y0) on the vertical
# axis to the diagonal y = x, with edge slopes in [-1, 0].  The full wall is the
# 8-fold reflection of that path, so  ratio = (octant area term)/(octant length).
# For an edge p=(x-a, y+b) -> q=(x, y) the (clockwise) shoelace contribution is
# (q_x*p_y - p_x*q_y)/2 = (x*b + a*y)/2, and any lattice edge splits into
# collinear primitive steps with both area and length additive, so the DP only
# needs primitive step vectors (a, -b), 0 <= b <= a <= K, gcd(a, b) = 1.
# (The optimal corner arcs have radius ~ ratio ~ 132.5, whose best lattice
# approximations use primitive edges far shorter than K.)
#
# An edge of slope -1 may cross the diagonal at a half-integer point
# ((x+y)/2 odd): handled by an optional terminal half-edge from (x, x+1) to
# (x+1/2, x+1/2) adding area (2x+1)/4 and length 1/sqrt(2).  (The statement's
# example - corners cut by 75m triangles - is exactly such a shape; it
# evaluates to 238750/(1400+300*sqrt(2)) ~ 130.87 in this formulation.)
#
# The ratio A/L is maximized by Dinkelbach iteration: for fixed lam the DP
# maximizes A - lam*L (all terms additive per edge), then lam <- A/L of the
# optimizer; converges superlinearly and stops when the optimum value hits 0.

N = 250
NEG = -1e18


class OctantDP:
    def __init__(self, K):
        dirs = [(1, 0)] + [(a, b) for a in range(1, K + 1)
                           for b in range(1, a + 1) if gcd(a, b) == 1]
        dirs.sort()  # ascending a, so a prefix covers all steps with a <= x
        self.a = np.array([d[0] for d in dirs])
        self.b = np.array([d[1] for d in dirs])
        self.r = np.hypot(self.a, self.b)
        ys = np.arange(N + 1)
        self.ys = ys
        col = self.b[:, None] + ys[None, :]      # source y for each (dir, y)
        self.ok = col <= N
        self.colc = np.minimum(col, N)
        self.gain_ay = 0.5 * self.a[:, None] * ys[None, :]

    def run(self, lam):
        """Maximize sum(area) - lam*sum(length); return (best value, its L)."""
        g = np.full((N + 1, N + 1), NEG)   # g[x, y]: best value of path ending (x, y)
        gL = np.zeros((N + 1, N + 1))      # length of that best path
        g[0, :] = 0.0                      # paths start anywhere on the axis x = 0
        ys = self.ys
        for x in range(1, N + 1):
            nd = np.searchsorted(self.a, x, side='right')  # steps with a <= x
            rows = (x - self.a[:nd])[:, None]
            cols = self.colc[:nd]
            C = g[rows, cols] + self.gain_ay[:nd] \
                + (0.5 * x) * self.b[:nd, None] - lam * self.r[:nd, None]
            C[~self.ok[:nd]] = NEG
            CL = gL[rows, cols] + self.r[:nd, None]
            idx = C.argmax(axis=0)
            g[x] = C[idx, ys]
            gL[x] = CL[idx, ys]
            g[x, :x] = NEG                 # outside the octant
        # Terminal 1: end at a post (d, d) on the diagonal (d >= 1).
        d = np.arange(1, N + 1)
        v1 = g[d, d]
        l1 = gL[d, d]
        # Terminal 2: from (x, x+1) take a half-edge of slope -1 to the diagonal.
        xh = np.arange(N)
        v2 = g[xh, xh + 1] + (2 * xh + 1) / 4.0 - lam / sqrt(2)
        l2 = gL[xh, xh + 1] + 1 / sqrt(2)
        v = np.concatenate([v1, v2])
        l = np.concatenate([l1, l2])
        i = int(np.argmax(v))
        return v[i], l[i]


def solve():
    lam = 125.0  # ratio of the plain 500x500 square, a safe lower bound
    for K in (48, 72):  # converge with K=48, then confirm with larger steps
        dp = OctantDP(K)
        while True:
            v, length = dp.run(lam)
            # optimizer has A = v + lam*L, so the improved ratio is lam + v/L
            new = lam + v / length
            if abs(new - lam) < 1e-12:
                lam = new
                break
            lam = new
    return f"{lam:.8f}"


if __name__ == "__main__":
    print(solve())
