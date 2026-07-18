#!/usr/bin/env python3
"""Project Euler 906: probability of a three-voter Condorcet winner."""

import math

from scipy.integrate import quad


def agreement_probability(option_count: int) -> float:
    """Return P(option_count).

    Give every voter and option an independent uniform score.  Conditional
    on the three scores x,y,z of one fixed option, another option defeats
    it in a majority with probability

        xy + xz + yz - 2xyz.

    The other options are conditionally independent.  Multiplying the
    resulting integral by n and integrating out x gives

      P(n) = integral_0^1 integral_0^1
             ((1-yz)^n - ((1-y)(1-z))^n)
             / (y+z-2yz) dy dz.

    The numerator and denominator vanish together at the origin.  The
    divided difference below uses expm1 for stability, while y=u^2 and
    z=v^2 make adaptive quadrature resolve the narrow large-n peak.
    """
    n = option_count

    def divided_difference(y: float, z: float) -> float:
        difference = y + z - 2 * y * z
        upper = 1 - y * z
        lower = upper - difference

        if difference == 0:
            return n * upper ** (n - 1)
        if lower <= 0:
            return upper**n / difference

        upper_log = n * math.log1p(-y * z)
        ratio_log = n * math.log(lower / upper)
        return (
            math.exp(upper_log)
            * (-math.expm1(ratio_log))
            / difference
        )

    def outer_integrand(u: float) -> float:
        if u == 0:
            return 0.0
        y = u * u

        def inner_integrand(v: float) -> float:
            if v == 0:
                return 0.0
            z = v * v
            jacobian = 4 * u * v
            return jacobian * divided_difference(y, z)

        return quad(
            inner_integrand,
            0.0,
            1.0,
            epsabs=2e-13,
            epsrel=2e-12,
            limit=300,
        )[0]

    return quad(
        outer_integrand,
        0.0,
        1.0,
        epsabs=2e-13,
        epsrel=2e-12,
        limit=300,
    )[0]


def solve() -> str:
    assert abs(agreement_probability(3) - 17 / 18) < 1e-12
    assert abs(
        agreement_probability(10) - 0.6760292265
    ) < 1e-10
    return f"{agreement_probability(20_000):.10f}"


if __name__ == "__main__":
    print(solve())
