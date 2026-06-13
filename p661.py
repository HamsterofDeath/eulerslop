#!/usr/bin/env python3
"""Project Euler 661: expected chess-match lead counts."""

from math import sqrt


def expected_a_leads(pa: float, pb: float, stop: float) -> float:
    """Expected number of post-game positions where A leads.

    Let F_i be the discounted expected count from score difference i.  Away
    from the boundary the birth-death recurrence has two characteristic roots;
    boundedness at +/- infinity leaves only two boundary equations for F_0.
    """

    q = 1.0 - stop
    draw = 1.0 - pa - pb
    middle = 1.0 - q * draw
    disc = sqrt(middle * middle - 4.0 * q * q * pa * pb)

    low = 2.0 * q * pb / (middle + disc)
    high = (middle + disc) / (2.0 * q * pa)

    always_positive = 1.0 / stop
    rhs = 1.0 - pb + q * pa * always_positive * (1.0 - low)
    return (1.0 / q + low * rhs / (q * pb)) / (high - low)


def solve(limit: int = 50) -> str:
    total = 0.0
    for k in range(3, limit + 1):
        pa = 1.0 / sqrt(k + 3.0)
        pb = pa + 1.0 / (k * k)
        stop = 1.0 / (k * k * k)
        total += expected_a_leads(pa, pb, stop)
    return f"{total:.4f}"


if __name__ == "__main__":
    print(solve())
