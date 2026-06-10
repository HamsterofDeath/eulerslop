#!/usr/bin/env python3
import numpy as np

# Three similar triangles (a = c).
#
# Put P = (p, q) on AC, p + q = a, and let X = b - a > 0, Y = d - a > 0.
# A and C contribute 135-degree angles to ABP and CDP; for P between A and C
# the only option for triangle BDP is angle BPD = 135 degrees, which with
# tan(u) = X/(X+2q), tan(v) = Y/(Y+2p) and u + v = 45 degrees reduces to
#       X*Y = 2*p*q.
# The remaining requirement (angle DBP equal to u or v) factors algebraically:
#   angle DBP = u :  (X^2 - 2pq)(X^2 + 2qX + 2q^2) = 0  =>  X = Y (b = d)
#   angle DBP = v :  (p - q)(qY + pX + 2pq) = 0          =>  p = q
# (verified against exact brute force: 92 triplets for b+d<100, no other cases)
#
# Family 1 (b = d): need integer 0 < p < a with p(a-p) = 2x^2, x = (b-a)/2.
#   The pair {p, a-p} with product 2x^2 is parametrized by {2g*al^2, g*be^2}
#   with gcd(al, be) = 1, be odd, x = g*al*be.  Triplet <-> (g, al, be), and
#   b + d < L  <=>  g*(2*al^2 + 2*al*be + be^2) <= (L-1)//2.
# Family 2 (p = q = a/2): X*Y = 2p^2, ordered (X, Y) = (2g*al^2, g*be^2) in
#   either order, p = g*al*be, b + d = g*(2*al^2 + 4*al*be + be^2) <= L-1.
# The families are disjoint (X = Y resp. would force 2 to be a square).


def family_sum(M, mid_coef):
    # Sum over coprime (al, be), be odd, of M // (2*al^2 + mid_coef*al*be + be^2).
    total = 0
    al = 1
    while 2 * al * al + mid_coef * al + 1 <= M:
        # largest be with Q <= M
        rem = M - 2 * al * al
        c = mid_coef * al // 2
        bmax = int((c * c + rem) ** 0.5) - c
        while 2 * al * al + mid_coef * al * (bmax + 1) + (bmax + 1) ** 2 <= M:
            bmax += 1
        B = np.arange(1, bmax + 1, 2, dtype=np.int64)  # odd be only
        B = B[np.gcd(B, al) == 1]
        if B.size:
            Q = 2 * al * al + mid_coef * al * B + B * B
            total += int((M // Q).sum())
        al += 1
    return total


def solve():
    L = 10**8
    f1 = family_sum((L - 1) // 2, 2)      # b = d
    f2 = 2 * family_sum(L - 1, 4)         # p = q, ordered (b, d)
    return f1 + f2


if __name__ == "__main__":
    print(solve())
