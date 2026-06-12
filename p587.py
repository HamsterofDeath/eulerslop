#!/usr/bin/env python3
from math import asin, pi, sqrt


L_SECTION = 1 - pi / 4


def concave_ratio(n):
    # Unit circle centered at (1, 1), line from (0, 0) to (n, 1): y = x/n.
    # The concave area is below both the line and the lower circle arc inside
    # the lower-left unit square.
    a = 1 + 1 / (n * n)
    b = -2 - 2 / n
    disc = b * b - 4 * a
    x = (-b - sqrt(disc)) / (2 * a)

    line_area = x * x / (2 * n)
    u = x - 1
    arc_integral = -0.5 * (u * sqrt(1 - u * u) + asin(u))
    circle_area = (1 - x) - arc_integral
    return (line_area + circle_area) / L_SECTION


def solve():
    assert abs(concave_ratio(1) - 0.5) < 1e-15
    assert concave_ratio(15) < 0.1
    n = 1
    while concave_ratio(n) >= 0.001:
        n += 1
    return n


if __name__ == "__main__":
    print(solve())
