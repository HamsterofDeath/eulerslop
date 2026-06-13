#!/usr/bin/env python3
"""Project Euler 630: Crossed lines."""

from collections import defaultdict
from math import gcd


def generated_points(count):
    state = 290797
    points = []
    for _ in range(count):
        state = (state * state) % 50515093
        x = state % 2000 - 1000
        state = (state * state) % 50515093
        y = state % 2000 - 1000
        points.append((x, y))
    return points


def normalized_line(point_a, point_b):
    x1, y1 = point_a
    x2, y2 = point_b
    dx = x2 - x1
    dy = y2 - y1
    if dx == 0 and dy == 0:
        return None

    a = dy
    b = -dx
    divisor = gcd(abs(a), abs(b))
    a //= divisor
    b //= divisor
    if a < 0 or (a == 0 and b < 0):
        a = -a
        b = -b

    c = -(a * x1 + b * y1)
    return a, b, c


def solve(n=2500):
    points = generated_points(n)
    lines = set()
    slope_counts = defaultdict(int)

    for i, point in enumerate(points):
        for j in range(i):
            line = normalized_line(point, points[j])
            if line is None or line in lines:
                continue
            lines.add(line)
            slope_counts[line[:2]] += 1

    line_count = len(lines)
    parallel_or_same_slope = sum(count * count for count in slope_counts.values())
    return line_count * line_count - parallel_or_same_slope


if __name__ == "__main__":
    print(solve())
