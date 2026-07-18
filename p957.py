#!/usr/bin/env python3
"""Project Euler Problem 957: Point Genesis.

Put the red points at the projective coordinate vertices.  A blue point
then has labels (a,b,c) with c=b/a.  Choosing the two initial blue
points algebraically independently turns labels into exponent vectors
in Z^2.  If A, B, C are the three label projections, one day replaces
the blue set by

    A x B, {(a,a+c)}, and {(b-c,b)}.

The projections remain all lattice points of three linearly equivalent
hexagons.  Their scale doubles each day.  Inclusion-exclusion gives

    g(n+1) = 3*s(n)^2 - 2*h(n),

where s is the number of points in one hexagon and h counts compatible
triples b-a=c.  Direct summation over the hexagon inequalities yields
the quartic lattice polynomials used below.
"""

from math import comb


def even_projection(scale: int) -> tuple[int, int]:
    """Projection size and compatible triples for the even family."""
    size = 3 * scale * scale + 5 * scale + 2
    compatible = (
        2
        + 56 * comb(scale, 1)
        + 222 * comb(scale, 2)
        + 294 * comb(scale, 3)
        + 126 * comb(scale, 4)
    )
    return size, compatible


def odd_projection(scale: int) -> tuple[int, int]:
    """Projection size and compatible triples for the odd family."""
    offset = scale - 1
    size = 3 * scale * scale + scale
    compatible = (
        10
        + 106 * comb(offset, 1)
        + 306 * comb(offset, 2)
        + 336 * comb(offset, 3)
        + 126 * comb(offset, 4)
    )
    return size, compatible


def maximum_blue_points(days: int) -> int:
    projection_day = days - 1
    if projection_day % 2 == 0:
        scale = (2**projection_day - 1) // 3
        size, compatible = even_projection(scale)
    else:
        scale = (2**projection_day + 1) // 3
        size, compatible = odd_projection(scale)

    return 3 * size * size - 2 * compatible


def solve() -> int:
    assert maximum_blue_points(1) == 8
    assert maximum_blue_points(2) == 28
    return maximum_blue_points(16)


if __name__ == "__main__":
    print(solve())
