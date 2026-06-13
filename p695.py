#!/usr/bin/env python3
"""Project Euler 695: Random Rectangles."""

from math import inf


_SIMPSON_EPS = 1e-13
_MAX_DEPTH = 40


def _integral_linear_over_ratio(slope, intercept, lo, hi):
    """Integrate (slope*r + intercept) / (2*(1+r)^3)."""

    def antiderivative(ratio):
        shifted = 1.0 + ratio
        return (
            slope * (-0.5 / shifted + 0.25 / (shifted * shifted))
            - intercept * 0.25 / (shifted * shifted)
        )

    upper = 0.0 if hi == inf else antiderivative(hi)
    return upper - antiderivative(lo)


def _conditional_max_ratio(x_ratio):
    """Expected max area factor for aligned x/y orderings, with b scaled to 1."""
    if x_ratio == 0.0:
        return 0.25

    threshold = 1.0 / x_ratio
    return _integral_linear_over_ratio(
        0.0, 1.0, 0.0, threshold
    ) + _integral_linear_over_ratio(x_ratio, 0.0, threshold, inf)


def _conditional_median_ratio(x_ratio):
    """Expected median area factor for the four crossed x/y orderings."""
    if x_ratio == 0.0:
        cuts = [0.0, 1.0, inf]
    else:
        cuts = [0.0, x_ratio, 1.0 / (x_ratio + 1.0)]
        if x_ratio < 1.0:
            cuts.append((1.0 - x_ratio) / x_ratio)
        cuts = sorted(set(cut for cut in cuts if cut >= 0.0))
        cuts.append(inf)

    total = 0.0
    lines = ((x_ratio + 1.0, 0.0), (x_ratio, x_ratio), (0.0, 1.0))
    for lo, hi in zip(cuts, cuts[1:]):
        if lo == hi:
            continue
        midpoint = lo + 1.0 if hi == inf else (lo + hi) * 0.5
        median_line = sorted(
            lines, key=lambda line: line[0] * midpoint + line[1]
        )[1]
        total += _integral_linear_over_ratio(*median_line, lo, hi)
    return total


def _adaptive_simpson(function, lo, hi, eps, whole, f_lo, f_mid, f_hi, depth):
    mid = (lo + hi) * 0.5
    left_mid = (lo + mid) * 0.5
    right_mid = (mid + hi) * 0.5

    f_left_mid = function(left_mid)
    f_right_mid = function(right_mid)
    left = (mid - lo) * (f_lo + 4.0 * f_left_mid + f_mid) / 6.0
    right = (hi - mid) * (f_mid + 4.0 * f_right_mid + f_hi) / 6.0
    refined = left + right

    if depth == 0 or abs(refined - whole) <= 15.0 * eps:
        return refined + (refined - whole) / 15.0

    return _adaptive_simpson(
        function, lo, mid, eps * 0.5, left, f_lo, f_left_mid, f_mid, depth - 1
    ) + _adaptive_simpson(
        function, mid, hi, eps * 0.5, right, f_mid, f_right_mid, f_hi, depth - 1
    )


def _integrate(function, lo, hi):
    mid = (lo + hi) * 0.5
    f_lo = function(lo)
    f_mid = function(mid)
    f_hi = function(hi)
    whole = (hi - lo) * (f_lo + 4.0 * f_mid + f_hi) / 6.0
    return _adaptive_simpson(
        function, lo, hi, _SIMPSON_EPS, whole, f_lo, f_mid, f_hi, _MAX_DEPTH
    )


def _outer_expectation(conditional):
    # With a=x*b, integrating over the Dirichlet spacings leaves the same
    # ratio kernel as in the inner y-spacing integral.
    def transformed(unit_interval):
        if unit_interval == 1.0:
            return 0.0
        x_ratio = unit_interval / (1.0 - unit_interval)
        jacobian = 1.0 / ((1.0 - unit_interval) * (1.0 - unit_interval))
        return conditional(x_ratio) * jacobian / (2.0 * (1.0 + x_ratio) ** 3)

    split_points = (
        0.0,
        0.25,
        0.3819660112501051,
        0.5,
        0.6180339887498949,
        0.75,
        1.0,
    )
    return sum(
        _integrate(transformed, split_points[i], split_points[i + 1])
        for i in range(len(split_points) - 1)
    )


def solve():
    aligned = _outer_expectation(_conditional_max_ratio)
    crossed = _outer_expectation(_conditional_median_ratio)
    expectation = (aligned + 2.0 * crossed) / 3.0
    return f"{expectation:.10f}"


if __name__ == "__main__":
    print(solve())
