#!/usr/bin/env python3
"""Project Euler 607: Marsh Crossing.

Use coordinates perpendicular and parallel to the marsh strips.  The
shortest path is piecewise linear, and the lateral displacement in each
medium satisfies the same Lagrange multiplier condition.
"""

from math import hypot, nextafter, sqrt


def solve():
    total_parallel = 100.0 / sqrt(2.0)
    outside_width = (100.0 / sqrt(2.0) - 50.0) / 2.0
    widths = [outside_width, 10.0, 10.0, 10.0, 10.0, 10.0, outside_width]
    speeds = [10.0, 9.0, 8.0, 7.0, 6.0, 5.0, 10.0]

    def displacement(multiplier):
        total = 0.0
        for width, speed in zip(widths, speeds):
            scaled = multiplier * speed
            total += width * scaled / sqrt(1.0 - scaled * scaled)
        return total

    lo = 0.0
    hi = nextafter(1.0 / max(speeds), 0.0)
    for _ in range(100):
        mid = (lo + hi) / 2.0
        if displacement(mid) < total_parallel:
            lo = mid
        else:
            hi = mid

    multiplier = (lo + hi) / 2.0
    days = 0.0
    for width, speed in zip(widths, speeds):
        scaled = multiplier * speed
        lateral = width * scaled / sqrt(1.0 - scaled * scaled)
        days += hypot(width, lateral) / speed
    return f"{days:.10f}"


if __name__ == "__main__":
    print(solve())
