#!/usr/bin/env python3
"""Project Euler 645: Every Day is a Holiday."""

import math


def _covered_edge_subset_polynomial(days: int, x: float) -> float:
    """Return sum_F (-1)^|F| x^|V(F)| for edge subsets F of C_days."""
    if x <= 0.0:
        return 1.0
    if x >= 1.0:
        return 0.0

    # Transfer matrix over whether the previous/current cycle edge is chosen:
    # T[a,b] = (-1)^b x^(a or b).  The cycle polynomial is trace(T^days).
    root = math.sqrt((1.0 - x) * (1.0 + 3.0 * x))
    lambda_plus = (1.0 - x + root) * 0.5
    lambda_minus = (1.0 - x - root) * 0.5

    positive = math.exp(days * math.log(lambda_plus)) if lambda_plus else 0.0
    if lambda_minus == 0.0:
        return positive

    negative = math.exp(days * math.log(-lambda_minus))
    if days & 1:
        negative = -negative
    return positive + negative


def _integrand(days: int, x: float) -> float:
    if x == 0.0:
        return 0.0
    return (1.0 - _covered_edge_subset_polynomial(days, x)) / x


def _adaptive_simpson(function, start: float, end: float, tolerance: float) -> float:
    def simpson(a: float, b: float, fa: float, fm: float, fb: float) -> float:
        return (b - a) * (fa + 4.0 * fm + fb) / 6.0

    def recurse(a, b, fa, fm, fb, whole, eps, depth):
        mid = (a + b) * 0.5
        left_mid = (a + mid) * 0.5
        right_mid = (mid + b) * 0.5
        f_left_mid = function(left_mid)
        f_right_mid = function(right_mid)
        left = simpson(a, mid, fa, f_left_mid, fm)
        right = simpson(mid, b, fm, f_right_mid, fb)
        refined = left + right

        if depth <= 0 or abs(refined - whole) <= 15.0 * eps:
            return refined + (refined - whole) / 15.0
        return (
            recurse(a, mid, fa, f_left_mid, fm, left, eps * 0.5, depth - 1)
            + recurse(mid, b, fm, f_right_mid, fb, right, eps * 0.5, depth - 1)
        )

    midpoint = (start + end) * 0.5
    f_start = function(start)
    f_midpoint = function(midpoint)
    f_end = function(end)
    initial = simpson(start, end, f_start, f_midpoint, f_end)
    return recurse(
        start, end, f_start, f_midpoint, f_end, initial, tolerance, 40
    )


def expected_emperors(days: int) -> float:
    if days <= 0:
        raise ValueError("days must be positive")
    if days <= 2:
        return 1.0

    # After a set of birthdays has appeared, all days are holidays iff no two
    # adjacent days are still unhit.  Inclusion-exclusion over the adjacent
    # unhit pairs gives E = D * integral_0^1 (1 - P_D(x)) / x dx.
    integral = _adaptive_simpson(
        lambda x: _integrand(days, x), 0.0, 1.0, 1e-10
    )
    return days * integral


def solve() -> str:
    return f"{expected_emperors(10_000):.4f}"


def main() -> None:
    print(solve())


if __name__ == "__main__":
    main()
