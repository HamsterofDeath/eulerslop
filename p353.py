#!/usr/bin/env python3
import heapq
import math
from collections import defaultdict

import numpy as np

def gen_points(r):
    # Lattice points on x^2 + y^2 + z^2 = r^2, reduced modulo the order-8
    # symmetry group acting on (x, y) (signed swaps); canonical rep x >= y >= 0.
    # For each z, scan y <= sqrt((r^2-z^2)/2) and test x^2 = N - y^2 for a
    # perfect square (exact in float64 since x^2 < 2^53).
    pts = []
    r2 = r * r
    for z in range(-r, r + 1):
        N = r2 - z * z
        y = np.arange(0, math.isqrt(N // 2) + 1, dtype=np.int64)
        x2 = N - y * y
        x = np.rint(np.sqrt(x2.astype(np.float64))).astype(np.int64)
        m = x * x == x2
        if m.any():
            xs = x[m]
            pts.append(np.stack([xs, y[m], np.full(len(xs), z, dtype=np.int64)], axis=1))
    return np.concatenate(pts, axis=0)

def M(r, C=6.0):
    # Risk of road u-v is (theta/pi)^2 with cos(theta) = u.v / r^2.  The group
    # above fixes both poles and acts by isometries, so we may search the
    # quotient graph; by the rearrangement inequality the largest dot product
    # between two orbits is attained by the canonical reps, hence quotient
    # weights are just canonical-rep angles.  Since theta1^2 + theta2^2 <
    # (theta1 + theta2)^2, long hops are dominated by chains of short ones,
    # so only edges up to angle C * (mean station spacing) are kept (result is
    # unchanged for C in 5..9); a 3D cell grid finds those pairs.  Dijkstra
    # then gives the minimal North -> South risk.
    pts = gen_points(r)
    P = pts.astype(np.float64)
    n = len(pts)
    r2f = float(r) * float(r)
    iN = int(np.flatnonzero((pts[:, 0] == 0) & (pts[:, 1] == 0) & (pts[:, 2] == r))[0])
    iS = int(np.flatnonzero((pts[:, 0] == 0) & (pts[:, 1] == 0) & (pts[:, 2] == -r))[0])
    delta = C * math.sqrt(4 * math.pi / (8 * n))  # angle cutoff
    inv_pi2 = 1.0 / (math.pi * math.pi)

    def weights(i, idxs):
        ang = np.arccos(np.clip(P[idxs] @ P[i] / r2f, -1.0, 1.0))
        return ang * ang * inv_pi2, ang

    adj = [None] * n
    if n <= 1500 or delta >= math.pi / 2:
        everything = np.arange(n)
        for i in range(n):
            adj[i] = (everything, weights(i, everything)[0])
    else:
        D = 2.0 * r * math.sin(delta / 2.0)  # chord-length cutoff
        keys = np.floor(P / D).astype(np.int64)
        grid = defaultdict(list)
        for i, k in enumerate(map(tuple, keys)):
            grid[k].append(i)
        grid = {k: np.array(v, dtype=np.int64) for k, v in grid.items()}
        for i in range(n):
            kx, ky, kz = keys[i]
            cand = np.concatenate([grid[c]
                                   for dx in (-1, 0, 1) for dy in (-1, 0, 1) for dz in (-1, 0, 1)
                                   if (c := (kx + dx, ky + dy, kz + dz)) in grid])
            d2 = ((P[cand] - P[i]) ** 2).sum(axis=1)
            sel = cand[(d2 <= D * D) & (cand != i)]
            adj[i] = (sel, weights(i, sel)[0])
        # stations can be sparse right next to a pole: also wire each pole to
        # its 32 angularly nearest stations (both directions)
        for ip in (iN, iS):
            w, ang = weights(ip, np.arange(n))
            near = np.argsort(ang)[1:33]
            ei, ew = adj[ip]
            adj[ip] = (np.concatenate([ei, near]), np.concatenate([ew, w[near]]))
            for j in near.tolist():
                ej, ewj = adj[j]
                adj[j] = (np.concatenate([ej, [ip]]), np.concatenate([ewj, [w[j]]]))

    dist = np.full(n, np.inf)
    dist[iN] = 0.0
    heap = [(0.0, iN)]
    done = np.zeros(n, dtype=bool)
    while heap:
        d, u = heapq.heappop(heap)
        if u == iS:
            return d
        if done[u]:
            continue
        done[u] = True
        idxs, w = adj[u]
        nd = d + w
        better = nd < dist[idxs]
        for v, dv in zip(idxs[better].tolist(), nd[better].tolist()):
            dist[v] = dv
            heapq.heappush(heap, (dv, v))

def solve():
    assert round(M(7), 10) == 0.1784943998
    total = sum(M(2 ** n - 1) for n in range(1, 16))
    return f"{total:.10f}"

if __name__ == "__main__":
    print(solve())
