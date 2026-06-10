#!/usr/bin/env python3
"""Project Euler 210: Obtuse Angled Triangles.

Count points B = (x, y) with |x| + |y| <= r such that triangle OBC is
obtuse, where O = (0, 0) and C = (r/4, r/4).

- Obtuse at O  <=>  OB.OC < 0  <=>  x + y < 0.
  Points in the diamond with x + y < 0: r^2 + r/2; minus the r/2
  degenerate points on the line y = x gives r^2.
- Obtuse at C  <=>  CB.CO < 0  <=>  x + y > r/2.
  Points in the diamond with x + y > r/2: r^2/2 + r/4; minus the r/4
  degenerate diagonal points gives r^2/2.
- Obtuse at B  <=>  B strictly inside the circle with diameter OC
  (center (r/8, r/8), squared radius r^2/32, tangent to both lines
  x + y = 0 and x + y = r/2, so the three regions are disjoint),
  minus the r/4 - 1 degenerate diagonal points inside that circle.

For r = 10^9 both r/8 and r^2/32 are integers, so the circle count is
done exactly: row dy contains the integers dx with dx^2 < R2 - dy^2,
i.e. 2*isqrt(R2 - dy^2 - 1) + 1 of them.
"""
from math import isqrt


def points_strictly_inside_circle(R2):
    """Lattice points (dx, dy) with dx^2 + dy^2 < R2 (integer center)."""
    M = R2 - 1  # dx^2 + dy^2 <= M
    D = isqrt(M)
    s = 0
    for dy in range(1, D + 1):
        s += isqrt(M - dy * dy)
    # row dy = 0 contributes 2D + 1; rows +-dy contribute 2*(2*t + 1)
    return 2 * D + 1 + 4 * s + 2 * D


def solve():
    r = 10**9
    assert r % 8 == 0
    R2 = r * r // 32  # squared radius of the circle with diameter OC
    obtuse_at_o = r * r
    obtuse_at_c = r * r // 2
    obtuse_at_b = points_strictly_inside_circle(R2) - (r // 4 - 1)
    return obtuse_at_o + obtuse_at_c + obtuse_at_b


if __name__ == "__main__":
    print(solve())
