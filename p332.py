#!/usr/bin/env python3
import numpy as np
from math import isqrt

def min_area(r):
    # All lattice points on the sphere x^2+y^2+z^2 = r^2.
    pts = []
    r2 = r * r
    for x in range(-r, r + 1):
        x2 = x * x
        for y in range(-r, r + 1):
            z2 = r2 - x2 - y * y
            if z2 < 0:
                continue
            z = isqrt(z2)
            if z * z == z2:
                pts.append((x, y, z))
                if z:
                    pts.append((x, y, -z))
    P = np.array(pts, dtype=np.int64)
    n = len(P)
    U = P / r
    D = U @ U.T  # pairwise dot products of unit vectors

    # The 48-element symmetry group (coordinate permutations and sign flips)
    # preserves the point set and areas, so a minimal triangle can be mapped
    # so that one vertex lies in the fundamental domain 0 <= x <= y <= z.
    F = [idx for idx, (x, y, z) in enumerate(pts) if 0 <= x <= y <= z]

    best = np.inf
    for i in F:
        # det[j,k] = P_i . (P_j x P_k): integer, zero iff i,j,k coplanar with
        # the centre (degenerate spherical triangle) - exact test.
        C = np.cross(P[i], P)            # (n,3) integer cross products
        det = C @ P.T                    # (n,n) integers
        # Van Oosterom-Strackee: tan(E/2) = |a.(bxc)| / (1 + a.b + b.c + c.a)
        # for unit vectors; atan2 handles excess E up to 2*pi correctly.
        den = 1.0 + D[i][:, None] + D[i][None, :] + D
        num = np.abs(det) / float(r ** 3)
        E = 2.0 * np.arctan2(num, den)
        E[det == 0] = np.inf             # exclude degenerate triples
        m = E.min()
        if m < best:
            best = m
    return best * r2

def solve():
    assert abs(min_area(14) - 3.294040) < 5e-7  # given example A(14)
    total = sum(min_area(r) for r in range(1, 51))
    return f"{total:.6f}"

if __name__ == "__main__":
    print(solve())
