#!/usr/bin/env python3
"""Project Euler 246: Tangents to an Ellipse.

The locus of points equidistant from circle c (centre M(-2000,1500),
radius 15000) and point G(8000,1500) is an ellipse with foci M and G and
major axis 2a = 15000 (sum of focal distances equals the radius).
So a = 7500, c = d(M,G)/2 = 5000, b^2 = a^2 - c^2 = 31250000,
centre (3000, 1500).

Count lattice points P strictly outside the ellipse for which the angle
between the two tangents from P exceeds 45 degrees.

Exact integer test: shift coordinates so the ellipse is x^2/A + y^2/B = 1
with A = a^2, B = b^2 (lattice points stay lattice points).  The pair of
tangent lines from P(x0, y0) is S*S1 = T^2.  Its quadratic part (scaled by
A^2 B^2 to stay integral) has coefficients
    a' = B*S1' - B^2*x0^2
    b' = A*S1' - A^2*y0^2
    h' = -x0*y0*A*B
where S1' = B*x0^2 + A*y0^2 - A*B (positive iff P is strictly outside).
The angle between the lines satisfies tan(theta) = 2*sqrt(h'^2-a'b')/(a'+b'),
with a'+b' <= 0 exactly when theta >= 90 degrees (a'+b' = 0 on the director
circle x0^2+y0^2 = A+B).  Hence

    theta > 45  <=>  a'+b' <= 0  or  4*(h'^2 - a'*b') > (a'+b')^2

which is an exact comparison of integers.
"""

from math import isqrt

A = 7500 * 7500          # a^2
B = 31250000             # b^2 = a^2 - c^2


def angle_gt_45(x0, y0):
    """True iff the tangents from strictly-outside point (x0,y0) make an
    angle greater than 45 degrees."""
    x2 = x0 * x0
    y2 = y0 * y0
    s1 = B * x2 + A * y2 - A * B
    # caller guarantees s1 > 0 (strictly outside)
    ap = B * s1 - B * B * x2
    bp = A * s1 - A * A * y2
    s = ap + bp
    if s <= 0:
        return True  # angle >= 90 degrees
    h2 = x2 * y2 * A * A * B * B
    return 4 * (h2 - ap * bp) > s * s


def inside_or_on(x0, y0):
    return B * x0 * x0 + A * y0 * y0 <= A * B


def row_count(y0, hi):
    """Number of integer x0 (both signs) with (x0,y0) strictly outside the
    ellipse and tangent angle > 45 degrees."""
    y2 = y0 * y0
    # largest |x0| inside or on the ellipse (k = -1 if row misses ellipse)
    rhs = A * (B - y2)
    if rhs >= 0:
        k = isqrt(rhs // B)
        while (k + 1) * (k + 1) * B <= rhs:
            k += 1
        while k >= 0 and k * k * B > rhs:
            k -= 1
    else:
        k = -1

    def good(x0):
        # inside the closed isoptic region (incl. ellipse interior)
        if inside_or_on(x0, y0):
            return True
        return angle_gt_45(x0, y0)

    if not good(k + 1 if k >= 0 else 0):
        # no qualifying point on this row (region is convex and symmetric)
        if k >= 0:
            # there might still be none beyond the ellipse edge
            return 0
        return 0

    # binary search largest x0 with good(x0) True; good is True on [0, X]
    lo, hh = (k + 1 if k >= 0 else 0), hi
    while lo < hh:
        mid = (lo + hh + 1) // 2
        if good(mid):
            lo = mid
        else:
            hh = mid - 1
    X = lo
    inside_cnt = 2 * k + 1 if k >= 0 else 0
    return 2 * X + 1 - inside_cnt


def solve():
    hi = 60000  # safely beyond the 45-degree isoptic
    assert not angle_gt_45(hi, 0) and not angle_gt_45(0, hi)

    total = row_count(0, hi)
    y0 = 1
    b_int = isqrt(B)
    while True:
        c = row_count(y0, hi)
        if c == 0 and y0 > b_int:
            break
        total += 2 * c
        y0 += 1
    return total


if __name__ == "__main__":
    print(solve())
