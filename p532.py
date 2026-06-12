#!/usr/bin/env python3
from math import asin, cos, pi, sin, sqrt


SMALL_CIRCLE_RADIUS = 0.999
THETA0 = asin(SMALL_CIRCLE_RADIUS)


def path_length(n, steps=20000):
    # Symmetry keeps the bots on a shrinking regular n-gon.  If theta is the
    # colatitude and delta is the longitude gap, the geodesic pursuit direction
    # gives ds/dtheta = sqrt(2-k*sin(theta)^2)/(cos(theta)*sqrt(k)),
    # where k = 1-cos(delta).
    k = 1 - cos(2 * pi / n)
    h = THETA0 / steps

    def integrand(theta):
        s = sin(theta)
        return sqrt(2 - k * s * s) / (cos(theta) * sqrt(k))

    total = integrand(0) + integrand(THETA0)
    for i in range(1, steps):
        total += (4 if i & 1 else 2) * integrand(i * h)
    return total * h / 3


def solve():
    assert f"{3 * path_length(3):.2f}" == "8.52"
    n = 3
    while path_length(n) <= 1000:
        n += 1
    return f"{n * path_length(n):.2f}"


if __name__ == "__main__":
    print(solve())
