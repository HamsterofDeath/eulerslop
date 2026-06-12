#!/usr/bin/env python3
from math import isqrt

def solve():
    # By Marden's theorem the maximal-area ellipse inscribed in a triangle is
    # the Steiner inellipse, whose foci are the roots of p'(t) where
    # p(t) = (t-z1)(t-z2)(t-z3) and z1,z2,z3 are the vertices as complex
    # numbers.  Foci +-sqrt(13) force the roots of 3t^2 - 2e1 t + e2 to be
    # +-sqrt(13), i.e. e1 = z1+z2+z3 = 0 and e2 = -39, equivalently
    # z1^2+z2^2+z3^2 = e1^2 - 2e2 = 78.
    #
    # Fix a pivot vertex z = z1 (Gaussian integer).  Then z2,z3 are the roots
    # of t^2 + z t + (z^2-39), so z2,z3 = (-z +- w)/2 with
    #   w^2 = 156 - 3 z^2   and   w == z (mod 2)  in Z[i].
    #
    # Each triangle corresponds to 6 such pairs (3 pivots x sign of w).
    # The pairs are the elements x = w + z*sqrt(-3) of Z[i][sqrt(-3)] with
    # x * sigma(x) = 156 (sigma: sqrt(-3) -> -sqrt(-3)); the parity condition
    # makes the set stable under the norm-1 unit eps = 2 + sqrt(3)
    # = 2 + i*sqrt(-3):
    #   (z, w) -> (2z + i w, 2w - 3 i z),
    # a Pell-type ladder whose inverse shrinks any large solution by a factor
    # ~ 2 - sqrt(3).  Hence every orbit contains a small element: brute force
    # over |Re z|,|Im z| <= 100 finds all orbit seeds (empirically all orbit
    # minima have coordinates <= 12), and walking each orbit with eps^{+-1}
    # until it leaves the box enumerates every admissible pair.

    def gaussian_sqrts(P, Q):
        # all w = c + d*i with w^2 = P + Q*i
        N = P * P + Q * Q
        M = isqrt(N)
        if M * M != N or (M + P) % 2:
            return []
        c2, d2 = (M + P) // 2, (M - P) // 2
        c, d = isqrt(c2), isqrt(d2)
        if c * c != c2 or d * d != d2:
            return []
        return [(sc, sd)
                for sc in ({c, -c}) for sd in ({d, -d})
                if 2 * sc * sd == Q]

    # seed solutions of w^2 + 3 z^2 = 156, w == z (mod 2), with small z
    seeds = set()
    L = 100
    for a in range(-L, L + 1):
        for b in range(-L, L + 1):
            for c, d in gaussian_sqrts(156 - 3 * (a * a - b * b), -6 * a * b):
                if (c - a) % 2 == 0 and (d - b) % 2 == 0:
                    seeds.add(((a, b), (c, d)))

    def eps(p):       # multiply w + z*sqrt(-3) by 2 + i*sqrt(-3)
        (a, b), (c, d) = p
        return ((2 * a - d, 2 * b + c), (2 * c + 3 * b, 2 * d - 3 * a))

    def eps_inv(p):   # multiply by 2 - i*sqrt(-3)
        (a, b), (c, d) = p
        return ((2 * a + d, 2 * b - c), (2 * c - 3 * b, 2 * d + 3 * a))

    def area_sum(n):
        bound = 4 * n + 100        # any pair fitting in [-n,n]^2 has coords <= 2n
        pairs = set()
        for s in seeds:
            for step in (eps, eps_inv):
                cur = s
                pairs.add(cur)
                while True:
                    cur = step(cur)
                    (a, b), (c, d) = cur
                    if max(abs(a), abs(b), abs(c), abs(d)) > bound:
                        break
                    pairs.add(cur)
        tris = {}
        for (a, b), (c, d) in pairs:
            vs = ((a, b), ((-a + c) // 2, (-b + d) // 2),
                  ((-a - c) // 2, (-b - d) // 2))
            if max(max(abs(x), abs(y)) for x, y in vs) > n:
                continue
            (x1, y1), (x2, y2), (x3, y3) = vs
            ar2 = abs(x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2))
            if ar2:                # exclude degenerate (collinear) triples
                tris[tuple(sorted(vs))] = ar2
        total2 = sum(tris.values())
        assert total2 % 2 == 0
        return total2 // 2

    # check against the values given in the statement
    assert area_sum(8) == 72
    assert area_sum(10) == 252
    assert area_sum(100) == 34632
    assert area_sum(1000) == 3529008

    return area_sum(10 ** 9)

if __name__ == "__main__":
    print(solve())
