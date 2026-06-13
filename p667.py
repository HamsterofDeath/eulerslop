#!/usr/bin/env python3
"""Project Euler 667: Moving Pentagon."""

import math


def points_from_cos(c):
    """The optimal family is the symmetric concave unit-edge pentagon."""
    s = math.sqrt(1.0 - c * c)
    d = 1.0 + 2.0 * c
    h = math.sqrt(max(0.0, 1.0 - d * d / 4.0))
    return [
        (0.0, 0.0),
        (1.0, 0.0),
        (1.0 + c, s),
        (0.5, s - h),
        (-c, s),
    ]


def area_from_cos(c):
    s = math.sqrt(1.0 - c * c)
    d = 1.0 + 2.0 * c
    h = math.sqrt(max(0.0, 1.0 - d * d / 4.0))
    return 0.5 * (s + d * (s - h))


def corner_width(poly, theta):
    """Width needed at the corner for this orientation.

    After shifting the lower-left bounding-box corner to the origin, the
    forbidden corridor region is where both coordinates exceed W.  Along an
    edge, max(min(x,y)) can only occur at a vertex or at x == y.
    """
    co = math.cos(theta)
    si = math.sin(theta)
    rotated = [(x * co - y * si, x * si + y * co) for x, y in poly]
    min_x = min(x for x, _ in rotated)
    min_y = min(y for _, y in rotated)
    shifted = [(x - min_x, y - min_y) for x, y in rotated]

    best = max(min(x, y) for x, y in shifted)
    for i in range(5):
        x1, y1 = shifted[i]
        x2, y2 = shifted[(i + 1) % 5]
        d1 = x1 - y1
        d2 = x2 - y2
        if d1 * d2 < 0.0:
            t = d1 / (d1 - d2)
            x = x1 + t * (x2 - x1)
            if x > best:
                best = x
    return best


def maximize_on_interval(f, lo, hi):
    inv_phi = (math.sqrt(5.0) - 1.0) / 2.0
    x1 = hi - inv_phi * (hi - lo)
    x2 = lo + inv_phi * (hi - lo)
    f1 = f(x1)
    f2 = f(x2)
    for _ in range(70):
        if f1 < f2:
            lo = x1
            x1 = x2
            f1 = f2
            x2 = lo + inv_phi * (hi - lo)
            f2 = f(x2)
        else:
            hi = x2
            x2 = x1
            f2 = f1
            x1 = hi - inv_phi * (hi - lo)
            f1 = f(x1)
    theta = (lo + hi) / 2.0
    return f(theta)


def max_corner_on_turn(c):
    """Maximum corner width over the quarter-turn that limits the optimum."""
    poly = points_from_cos(c)
    lo = -math.pi / 2.0
    hi = 0.0
    samples = 900
    values = [
        corner_width(poly, lo + (hi - lo) * i / samples)
        for i in range(samples + 1)
    ]
    best = max(values[0], values[-1])

    for i in range(1, samples):
        if values[i] >= values[i - 1] and values[i] >= values[i + 1]:
            a = lo + (hi - lo) * (i - 1) / samples
            b = lo + (hi - lo) * (i + 1) / samples
            best = max(best, maximize_on_interval(lambda t: corner_width(poly, t), a, b))
    return best


def solve():
    # Below the optimum the endpoint width sin(a) controls the turn; above it
    # an interior orientation of the same connected corner arc becomes wider.
    lo = 0.490
    hi = 0.491
    for _ in range(60):
        mid = (lo + hi) / 2.0
        straight_width = math.sqrt(1.0 - mid * mid)
        if max_corner_on_turn(mid) <= straight_width:
            lo = mid
        else:
            hi = mid

    c = lo
    width = math.sqrt(1.0 - c * c)
    return area_from_cos(c) / (width * width)


if __name__ == "__main__":
    print(f"{solve():.10f}")
