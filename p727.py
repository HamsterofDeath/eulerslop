#!/usr/bin/env python3
"""Project Euler 727: triangle of circular arcs."""

from math import gcd, sqrt


LIMIT = 100


def circumcenter(p: tuple[float, float], q: tuple[float, float], r: tuple[float, float]) -> tuple[float, float]:
    ax, ay = p
    bx, by = q
    cx, cy = r
    determinant = 2 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by))
    ux = (
        (ax * ax + ay * ay) * (by - cy)
        + (bx * bx + by * by) * (cy - ay)
        + (cx * cx + cy * cy) * (ay - by)
    ) / determinant
    uy = (
        (ax * ax + ay * ay) * (cx - bx)
        + (bx * bx + by * by) * (ax - cx)
        + (cx * cx + cy * cy) * (bx - ax)
    ) / determinant
    return ux, uy


def center_distance(a: int, b: int, c: int) -> float:
    center_b = (a + b, 0.0)
    center_c_x = ((a + c) ** 2 - (b + c) ** 2 + (a + b) ** 2) / (2 * (a + b))
    center_c_y = sqrt((a + c) ** 2 - center_c_x * center_c_x)

    tangency_ab = (float(a), 0.0)
    tangency_ac = (a * center_c_x / (a + c), a * center_c_y / (a + c))
    tangency_bc = (
        center_b[0] + b * (center_c_x - center_b[0]) / (b + c),
        b * center_c_y / (b + c),
    )
    circum = circumcenter(tangency_ab, tangency_ac, tangency_bc)

    ka, kb, kc = 1 / a, 1 / b, 1 / c
    inner_radius = 1 / (ka + kb + kc + 2 * sqrt(ka * kb + kb * kc + kc * ka))
    ex = ((a + inner_radius) ** 2 - (b + inner_radius) ** 2 + (a + b) ** 2) / (2 * (a + b))
    ey = sqrt((a + inner_radius) ** 2 - ex * ex)

    return sqrt((circum[0] - ex) ** 2 + (circum[1] - ey) ** 2)


def solve() -> str:
    total = 0.0
    count = 0
    for a in range(1, LIMIT + 1):
        for b in range(a + 1, LIMIT + 1):
            for c in range(b + 1, LIMIT + 1):
                if gcd(gcd(a, b), c) == 1:
                    total += center_distance(a, b, c)
                    count += 1
    return f"{total / count:.8f}"


if __name__ == "__main__":
    print(solve())
