#!/usr/bin/env python3
"""Project Euler 897: optimal polygonal interpolation of x^4."""

from math import copysign, sin, pi


def maximum_polygon_area(vertex_count: int) -> float:
    interval_count = vertex_count - 1
    nodes = [-1.0]
    for index in range(1, interval_count):
        # The tiny asymmetric perturbation avoids the inferior stationary
        # solution having a vertex exactly at zero.
        nodes.append(
            -1
            + 2 * index / interval_count
            + 1e-6 * sin(pi * index / interval_count)
        )
    nodes.append(1.0)

    for _ in range(20_000):
        maximum_change = 0.0
        for index in range(1, interval_count):
            left = nodes[index - 1]
            right = nodes[index + 1]
            mean_cube = (
                (right**4 - left**4) / (4 * (right - left))
            )
            updated = copysign(abs(mean_cube) ** (1 / 3), mean_cube)
            maximum_change = max(
                maximum_change,
                abs(updated - nodes[index]),
            )
            nodes[index] = updated
        if maximum_change < 1e-14:
            break

    lower_trapezoids = sum(
        (nodes[index + 1] - nodes[index])
        * (nodes[index] ** 4 + nodes[index + 1] ** 4)
        / 2
        for index in range(interval_count)
    )
    return 2 - lower_trapezoids


def solve() -> str:
    assert f"{maximum_polygon_area(3):.9f}" == "1.000000000"
    assert f"{maximum_polygon_area(5):.9f}" == "1.477309771"
    return f"{maximum_polygon_area(101):.9f}"


if __name__ == "__main__":
    print(solve())
