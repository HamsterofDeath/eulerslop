#!/usr/bin/env python3
"""Project Euler 761: critical runner speed in a regular hexagonal pool.

For a regular n-gon, symmetry reduces the pursuit game to an angular branch
K and a final escape angle alpha.  At the critical speed V, the last straight
swim meets the boundary at cos(alpha) = 1 / V.

For n = 6 the branch calculation gives K = 2 and the inverse-cosine argument
-1/8.  Thus cos(alpha) = (sqrt(21) - 3) / 8 and, equivalently,
V = 2 + 2*sqrt(21)/3.
"""

from math import acos, cos, pi, sin, tan


def critical_speed(sides: int) -> float:
    """Return the critical runner/swimmer speed ratio for a regular polygon."""
    if sides < 3:
        raise ValueError("a polygon must have at least three sides")

    theta = pi / sides
    tangent = tan(theta)

    # The optimal escape geometry changes branch whenever its angle crosses
    # another half-sector.  K is the final branch before the sign change.
    for k in range(sides + 1):
        boundary = sin(k * theta) - (k + sides) * tangent * cos(k * theta)
        if boundary >= 0.0:
            branch = k - 1
            break
    else:
        raise ArithmeticError("failed to locate the angular branch")

    argument = (
        2.0 * sin(branch * theta) / ((branch + sides) * tangent)
        - cos(branch * theta)
    )
    argument = max(-1.0, min(1.0, argument))
    alpha = (branch * theta + acos(argument)) / 2.0
    return 1.0 / cos(alpha)


def solve() -> str:
    # The square value supplied in the statement checks the general formula.
    assert f"{critical_speed(4):.8f}" == "5.78859314"
    return f"{critical_speed(6):.8f}"


if __name__ == "__main__":
    print(solve())
