#!/usr/bin/env python3
import numpy as np

# Largest empty convex polygon ("convex hole") over 500 pseudo-random points.
#
# Classic O(n^3) approach: anchor each candidate polygon at its bottom-most
# vertex O (smallest (y, x)).  All other vertices lie above O; sorted by angle
# around O, the polygon is a fan of triangles (O, v_t, v_{t+1}).  The polygon
# is empty iff every fan triangle is empty.
#
# Emptiness in O(m^2) per anchor: for fixed first vertex j, scanning second
# vertices i in angular order, triangle (O, p_j, p_i) is empty iff p_i lies on
# or left of the ray p_j -> p_q for every already-seen q between - and because
# all relevant direction vectors live in the open half-plane left of O->p_j,
# only the running "most counter-clockwise" direction U_j must be checked.
# This scan is vectorized over j.
#
# DP: dp[j][i] = best area of an empty convex fan O,...,p_j,p_i.  When row j
# is complete, dp[j][i] = area(O,j,i) + max(0, max dp[k][j] over k with a left
# turn at j), found by sorting incoming edge directions and prefix-maxima
# (angles measured relative to O->p_j, so they live in (0, pi)).

def gen_points(n):
    s = 290797
    pts = []
    for _ in range(n):
        t = []
        for _ in range(2):
            s = s * s % 50515093
            t.append(s % 2000 - 1000)
        pts.append(tuple(t))
    return pts

def solve():
    pts = sorted(set(gen_points(500)))            # sort by (x, y); dedupe
    P = np.array(sorted(pts, key=lambda p: (p[1], p[0])), dtype=np.float64)
    n = len(P)
    best = 0.0
    for oi in range(n - 2):
        O = P[oi]
        # points strictly above O in (y, x) order = the rest of the array
        Q = P[oi + 1:]
        m = len(Q)
        if m < 2:
            break
        V = Q - O                                  # vectors O -> point
        ang = np.arctan2(V[:, 1], V[:, 0])         # in (0, pi); ties: by radius
        order = np.lexsort((V[:, 0] ** 2 + V[:, 1] ** 2, ang))
        V = V[order]
        vx, vy = V[:, 0], V[:, 1]

        # --- emptiness of all fan triangles (O, j, i), j < i angularly ---
        empty = np.zeros((m, m), dtype=bool)
        Ux = np.zeros(m)                           # running extreme direction
        Uy = np.zeros(m)
        has = np.zeros(m, dtype=bool)
        for i in range(1, m):
            dx = vx[i] - vx[:i]
            dy = vy[i] - vy[:i]
            cr = dx * Uy[:i] - dy * Ux[:i]         # cross(p_i-p_j, U_j)
            empty[:i, i] = (~has[:i]) | (cr <= 0)
            upd = ~has[:i] | (Ux[:i] * dy - Uy[:i] * dx > 0)
            Ux[:i] = np.where(upd, dx, Ux[:i])
            Uy[:i] = np.where(upd, dy, Uy[:i])
            has[:i] = True

        # doubled triangle areas: cross(v_j, v_i) for the fan triangle
        # --- DP over rows j in angular order ---
        dp = np.full((m, m), -np.inf)              # dp[j, i]
        tri = np.empty(m)
        for j in range(m - 1):
            # incoming edges k -> j: angle of (p_j - p_k) rel. d0 = O -> p_j
            d0x, d0y = vx[j], vy[j]
            if j > 0:
                ax = vx[j] - vx[:j]
                ay = vy[j] - vy[:j]
                phk = np.arctan2(d0x * ay - d0y * ax, d0x * ax + d0y * ay)
                ordk = np.argsort(phk)
                pref = np.maximum.accumulate(dp[:j, j][ordk])
                phk_sorted = phk[ordk]
            # outgoing edges j -> i
            bx = vx[j + 1:] - vx[j]
            by = vy[j + 1:] - vy[j]
            phi = np.arctan2(d0x * by - d0y * bx, d0x * bx + d0y * by)
            tri_ji = vx[j] * vy[j + 1:] - vy[j] * vx[j + 1:]  # doubled area
            base = np.zeros(m - 1 - j)
            if j > 0:
                pos = np.searchsorted(phk_sorted, phi, side="left") - 1
                ok = pos >= 0
                if ok.any():
                    base[ok] = np.maximum(0.0, pref[pos[ok]])
            row = np.where(empty[j, j + 1:], tri_ji + base, -np.inf)
            dp[j, j + 1:] = row
            mx = row.max(initial=-np.inf)
            if mx > best:
                best = mx
    return f"{best / 2:.1f}"

if __name__ == "__main__":
    print(solve())
