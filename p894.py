#!/usr/bin/env python3
"""Project Euler 894: areas between a self-similar spiral of circles."""

from math import acos, cos, exp, log, log1p, pi, sin, sqrt


def log_radius_squared(step: int, scale: float, angle: float) -> float:
    power = scale**step
    denominator = (
        1 + power * power - 2 * power * cos(step * angle)
    )
    return 2 * log1p(power) - log(denominator)


def log_radius_derivatives(
    step: int,
    scale: float,
    angle: float,
) -> tuple[float, float]:
    power = scale**step
    denominator = (
        1 + power * power - 2 * power * cos(step * angle)
    )
    power_derivative = step * scale ** (step - 1)
    denominator_scale_derivative = (
        2 * power_derivative * (power - cos(step * angle))
    )
    scale_derivative = (
        2 * power_derivative / (1 + power)
        - denominator_scale_derivative / denominator
    )
    angle_derivative = (
        -2 * step * power * sin(step * angle) / denominator
    )
    return scale_derivative, angle_derivative


def spiral_parameters() -> tuple[float, float, float]:
    """Solve the tangencies at offsets 1, 7, and 8 by Newton iteration."""
    scale = 0.9
    angle = 0.83
    for _ in range(30):
        base = log_radius_squared(1, scale, angle)
        first = log_radius_squared(7, scale, angle) - base
        second = log_radius_squared(8, scale, angle) - base
        if max(abs(first), abs(second)) < 1e-15:
            break

        base_scale, base_angle = log_radius_derivatives(
            1, scale, angle
        )
        first_scale, first_angle = log_radius_derivatives(
            7, scale, angle
        )
        second_scale, second_angle = log_radius_derivatives(
            8, scale, angle
        )
        a = first_scale - base_scale
        b = first_angle - base_angle
        c = second_scale - base_scale
        d = second_angle - base_angle
        determinant = a * d - b * c
        scale += (-first * d + b * second) / determinant
        angle += (c * first - a * second) / determinant

    radius_ratio = exp(
        log_radius_squared(1, scale, angle) / 2
    )

    # The other algebraic roots make earlier circles overlap.  Checking
    # a generous finite prefix selects the required spiral.
    for step in range(2, 100):
        power = scale**step
        centre_distance = radius_ratio * sqrt(
            1 + power * power - 2 * power * cos(step * angle)
        )
        assert centre_distance + 1e-12 >= 1 + power
    return scale, angle, radius_ratio


def circular_triangle_area(radii: tuple[float, float, float]) -> float:
    """Area of the gap between three externally tangent circles."""
    first, second, third = radii
    opposite_first = second + third
    opposite_second = first + third
    opposite_third = first + second
    semiperimeter = (
        opposite_first + opposite_second + opposite_third
    ) / 2
    triangle_area = sqrt(
        semiperimeter
        * (semiperimeter - opposite_first)
        * (semiperimeter - opposite_second)
        * (semiperimeter - opposite_third)
    )

    first_angle = acos(
        (
            opposite_second**2
            + opposite_third**2
            - opposite_first**2
        )
        / (2 * opposite_second * opposite_third)
    )
    second_angle = acos(
        (
            opposite_first**2
            + opposite_third**2
            - opposite_second**2
        )
        / (2 * opposite_first * opposite_third)
    )
    third_angle = pi - first_angle - second_angle
    sectors = (
        first**2 * first_angle
        + second**2 * second_angle
        + third**2 * third_angle
    ) / 2
    return triangle_area - sectors


def solve() -> str:
    scale, _, _ = spiral_parameters()
    first_family = circular_triangle_area(
        (1, scale, scale**8)
    )
    second_family = circular_triangle_area(
        (1, scale**7, scale**8)
    )
    total = (first_family + second_family) / (1 - scale**2)
    return f"{total:.10f}"


if __name__ == "__main__":
    print(solve())
