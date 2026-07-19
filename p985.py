#!/usr/bin/env python3
"""Project Euler Problem 985: Telescoping Triangles.

The required inscribed triangle is the Fagnano (orthic) triangle, which
exists precisely when the outer triangle is acute.  If x is one of the
outer angles, the corresponding orthic-triangle angle is pi - 2x, so

    x_k = pi/3 + (-2)^k * (x_0 - pi/3).

For an integer triangle that is not equilateral, the largest possible
minimum angle at a given scale is attained by consecutive isosceles
sides (m, m, m+1).  Write its equal-angle deficit from pi/3 as epsilon.
For even k, T_k exists exactly when

    epsilon < pi / (3 * 2^k).

At the first m satisfying this bound, the remaining angle is already
large enough that T_(k+1) does not exist.
"""

from math import acos, pi


TARGET_STEP = 20


def angle_deficit(equal_side: int) -> float:
    """Return pi/3 minus a base angle of (m, m, m+1)."""
    cosine = (equal_side + 1) / (2 * equal_side)
    return pi / 3 - acos(cosine)


def first_surviving_side(step: int) -> int:
    if step % 2:
        raise ValueError("the simplified bound requires an even step")

    limit = pi / (3 * 2**step)
    failing = 1
    passing = 2
    while angle_deficit(passing) >= limit:
        failing = passing
        passing *= 2

    while passing - failing > 1:
        middle = (failing + passing) // 2
        if angle_deficit(middle) < limit:
            passing = middle
        else:
            failing = middle
    return passing


def minimum_perimeter(step: int) -> int:
    equal_side = first_surviving_side(step)
    epsilon = angle_deficit(equal_side)

    # The unequal angle of T_step is pi/3 + 2^(step+1)*epsilon.
    assert pi / 3 + 2 ** (step + 1) * epsilon >= pi / 2
    return 3 * equal_side + 1


def solve() -> int:
    assert minimum_perimeter(2) == 10
    return minimum_perimeter(TARGET_STEP)


if __name__ == "__main__":
    print(solve())
