#!/usr/bin/env python3

from math import acos, floor, pi


TAU = 2.0 * pi


def arrangements_for_sizes(sun, small, large):
    """Count valid offsets for C=s+p+q, S=s, planet sizes p<q."""
    distance = small + large - TAU
    if distance <= large - small:
        return 0

    outer_side = sun + large
    inner_side = sun + small
    d2 = distance * distance

    cos_outer = (d2 + outer_side * outer_side - inner_side * inner_side) / (
        2.0 * distance * outer_side
    )
    cos_inner = (d2 + inner_side * inner_side - outer_side * outer_side) / (
        2.0 * distance * inner_side
    )

    # Floating roundoff can push a value a hair outside the valid range.
    cos_outer = min(1.0, max(-1.0, cos_outer))
    cos_inner = min(1.0, max(-1.0, cos_inner))

    alpha = acos(cos_outer)
    beta = acos(cos_inner)

    # At the degenerate lower offset the phase value is exactly -(s+p).
    # Every integer phase reached after that and no later than the one at
    # the one-centimetre clearance limit gives one valid arrangement.
    phase_limit = (outer_side * alpha - inner_side * beta) / pi
    return max(0, floor(phase_limit + 1.0e-12) + sun + small)


def solve(limit=500):
    total = 0
    for sun in range(5, limit - 9):
        max_small = (limit - sun - 1) // 2
        for small in range(5, max_small + 1):
            max_large = limit - sun - small
            for large in range(small + 1, max_large + 1):
                total += arrangements_for_sizes(sun, small, large)
    return total


if __name__ == "__main__":
    print(solve())
