#!/usr/bin/env python3
# Project Euler 264: Triangle Centres
#
# With circumcentre at the origin, the orthocentre is H = A + B + C.  So we
# need lattice points A, B, C with |A| = |B| = |C| (common norm n = R^2) and
# A + B + C = (5, 0).
#
# Fix a vertex A = (a, b).  Then B + C = S = (5-a, -b) and, since |B| = |C|,
# B - C is perpendicular to S.  Writing E = B - C (integer vector parallel to
# (b, 5-a)) and using |B|^2 = n:
#     |E|^2 = q := 3n + 10a - 25,         |S|^2 =: S2 = n - 10a + 25,
#     E = +- sqrt(q / S2) * (b, 5-a).
# So a solution exists iff S2 | q*b^2 and S2 | q*(5-a)^2 with both quotients
# perfect squares (E1^2 and E2^2), plus parity so B = (S+E)/2 is integral.
#
# Size bound: a^2+b^2+c^2 = 9R^2 - |OH|^2 = 9R^2 - 25 and every side <= 2R,
# hence perimeter >= (9R^2-25)/(2R) > 4.5R - 1, so perimeter <= 1e5 forces
# R <= 22223.
#
# Each triangle is discovered exactly once from each of its three vertices,
# so we sum perimeter/3 per discovery.  Mirror symmetry y -> -y lets us scan
# only b >= 0 (weight 2 for b > 0, weight 1 for b = 0).  The scan over all
# lattice points is vectorised with numpy; the cheap filter S2 | q*b^2 leaves
# only a handful of survivors for exact checking.
#
# A = (5, 0) = H itself makes S = 0 and is handled specially: B = -C on the
# circle n = 25.

import numpy as np
from math import isqrt


def solve():
    LIMIT = 10 ** 5
    RMAX = 22223
    NMAX = RMAX * RMAX

    total = 0.0

    def vertex_contribution(a, b):
        """Perimeter/3 of the triangle (if any) having vertex A=(a,b)."""
        n = a * a + b * b
        q = 3 * n + 10 * a - 25
        S2 = n - 10 * a + 25
        if q <= 0 or S2 == 0:
            return 0.0
        num1 = q * b * b
        if num1 % S2:
            return 0.0
        e1s = num1 // S2
        e1 = isqrt(e1s)
        if e1 * e1 != e1s:
            return 0.0
        c5 = 5 - a
        num2 = q * c5 * c5
        if num2 % S2:
            return 0.0
        e2s = num2 // S2
        e2 = isqrt(e2s)
        if e2 * e2 != e2s:
            return 0.0
        # E = s*(b, 5-a) with s > 0  (E -> -E only swaps B and C)
        E1 = e1  # b >= 0 here
        E2 = e2 if c5 >= 0 else -e2
        if (c5 + E1) % 2 or (b + E2) % 2:
            return 0.0
        Bx, By = (c5 + E1) // 2, (-b + E2) // 2
        Cx, Cy = (c5 - E1) // 2, (-b - E2) // 2
        if (Bx, By) == (a, b) or (Cx, Cy) == (a, b):
            return 0.0  # degenerate
        per = ((a - Bx) ** 2 + (b - By) ** 2) ** 0.5 \
            + ((Bx - Cx) ** 2 + (By - Cy) ** 2) ** 0.5 \
            + ((Cx - a) ** 2 + (Cy - b) ** 2) ** 0.5
        return per / 3.0 if per <= LIMIT else 0.0

    bsq_all = np.arange(RMAX + 1, dtype=np.int64) ** 2
    for a in range(-RMAX, RMAX + 1):
        bmax = isqrt(NMAX - a * a)
        bsq = bsq_all[: bmax + 1]
        n = bsq + a * a
        q = 3 * n + (10 * a - 25)
        S2 = n - (10 * a - 25)
        # special point A = (5,0): S = 0, B = -C on x^2+y^2 = 25
        if a == 5:
            S2[0] = 1  # avoid division by zero; handled below
        rem = (q * bsq) % S2
        good = np.nonzero((rem == 0) & (q > 0))[0]
        for b in good.tolist():
            c = vertex_contribution(a, b)
            if c:
                total += 2.0 * c if b > 0 else c
        if a == 5:
            # vertex A = H = (5,0): triangles {A, B, -B}, |B|=5, B != (+-5,0)
            for Bx, By in ((3, 4), (4, 3), (-3, 4), (-4, 3), (0, 5)):
                per = ((5 - Bx) ** 2 + By ** 2) ** 0.5 \
                    + ((5 + Bx) ** 2 + By ** 2) ** 0.5 \
                    + 2.0 * (Bx * Bx + By * By) ** 0.5
                if per <= LIMIT:
                    total += per / 3.0
    return f"{total:.4f}"


if __name__ == "__main__":
    print(solve())
