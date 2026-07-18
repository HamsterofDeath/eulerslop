#!/usr/bin/env python3
"""Project Euler 904: medians of integer right triangles."""

import math


def extended_gcd(a: int, b: int) -> tuple[int, int, int]:
    if b == 0:
        return a, 1, 0
    divisor, x, y = extended_gcd(b, a % b)
    return divisor, y, x - a // b * y


def ceil_divide(numerator: int, denominator: int) -> int:
    return -((-numerator) // denominator)


def furthest_lattice_point(
    numerator: int,
    denominator: int,
    delta_numerator: int,
    delta_denominator: int,
    limit: int,
) -> tuple[int, int]:
    """Take the furthest point on an affine ray inside the circle."""
    shift = max(
        0,
        (
            ceil_divide(-numerator, delta_numerator)
            if delta_numerator
            else 0
        ),
        ceil_divide(1 - denominator, delta_denominator),
    )
    numerator += shift * delta_numerator
    denominator += shift * delta_denominator

    quadratic = (
        delta_numerator * delta_numerator
        + delta_denominator * delta_denominator
    )
    linear = 2 * (
        numerator * delta_numerator
        + denominator * delta_denominator
    )
    constant = numerator * numerator + denominator * denominator - limit
    discriminant = linear * linear - 4 * quadratic * constant
    steps = (
        -linear + math.isqrt(discriminant)
    ) // (2 * quadratic)

    def norm(candidate_steps: int) -> int:
        p = numerator + candidate_steps * delta_numerator
        q = denominator + candidate_steps * delta_denominator
        return p * p + q * q

    while norm(steps + 1) <= limit:
        steps += 1
    while steps >= 0 and norm(steps) > limit:
        steps -= 1

    return (
        numerator + steps * delta_numerator,
        denominator + steps * delta_denominator,
    )


def outside_neighbor(
    numerator: int,
    denominator: int,
    limit: int,
    above: bool,
) -> tuple[int, int]:
    """Return the height-limited Farey neighbor away from the target."""
    if above:
        _, x, y = extended_gcd(denominator, numerator)
        initial_numerator, initial_denominator = x, -y
    else:
        _, x, y = extended_gcd(numerator, denominator)
        initial_numerator, initial_denominator = -y, x

    return furthest_lattice_point(
        initial_numerator,
        initial_denominator,
        numerator,
        denominator,
        limit,
    )


def maximum_step(
    a: int,
    b: int,
    c: int,
    d: int,
    limit: int,
) -> int:
    """Largest t with (a+tc)^2+(b+td)^2 <= limit."""
    quadratic = c * c + d * d
    linear = 2 * (a * c + b * d)
    constant = a * a + b * b - limit
    discriminant = linear * linear - 4 * quadratic * constant
    steps = (
        -linear + math.isqrt(discriminant)
    ) // (2 * quadratic)

    def norm(candidate_steps: int) -> int:
        p = a + candidate_steps * c
        q = b + candidate_steps * d
        return p * p + q * q

    while norm(steps + 1) <= limit:
        steps += 1
    while norm(steps) > limit:
        steps -= 1
    return steps


def slope_neighbors(
    target: float,
    hypotenuse_limit: int,
) -> tuple[tuple[int, int] | None, tuple[int, int] | None]:
    """Find adjacent primitive Pythagorean parameters around target.

    Accelerated Stern--Brocot descent works for the circular height
    p^2+q^2 because every fraction between Farey neighbors has
    componentwise no smaller numerator and denominator than their
    mediant.  If a final fraction has two odd coordinates, its outward
    Farey neighbor is the nearest parameter of opposite parity.
    """
    lower_numerator, lower_denominator = 0, 1
    upper_numerator, upper_denominator = 1, 1

    while (
        (lower_numerator + upper_numerator) ** 2
        + (lower_denominator + upper_denominator) ** 2
        <= hypotenuse_limit
    ):
        mediant_numerator = lower_numerator + upper_numerator
        mediant_denominator = lower_denominator + upper_denominator

        if mediant_numerator / mediant_denominator < target:
            height_steps = maximum_step(
                lower_numerator,
                lower_denominator,
                upper_numerator,
                upper_denominator,
                hypotenuse_limit,
            )
            target_steps = max(
                1,
                int(
                    (
                        target * lower_denominator
                        - lower_numerator
                    )
                    / (
                        upper_numerator
                        - target * upper_denominator
                    )
                ),
            )
            steps = min(height_steps, target_steps)

            while (
                steps > 1
                and (
                    lower_numerator + steps * upper_numerator
                )
                / (
                    lower_denominator + steps * upper_denominator
                )
                >= target
            ):
                steps -= 1
            while (
                steps < height_steps
                and (
                    lower_numerator + (steps + 1) * upper_numerator
                )
                / (
                    lower_denominator
                    + (steps + 1) * upper_denominator
                )
                < target
            ):
                steps += 1

            lower_numerator += steps * upper_numerator
            lower_denominator += steps * upper_denominator
        else:
            height_steps = maximum_step(
                upper_numerator,
                upper_denominator,
                lower_numerator,
                lower_denominator,
                hypotenuse_limit,
            )
            target_steps = max(
                1,
                int(
                    (
                        upper_numerator
                        - target * upper_denominator
                    )
                    / (
                        target * lower_denominator
                        - lower_numerator
                    )
                ),
            )
            steps = min(height_steps, target_steps)

            while (
                steps > 1
                and (
                    upper_numerator + steps * lower_numerator
                )
                / (
                    upper_denominator + steps * lower_denominator
                )
                <= target
            ):
                steps -= 1
            while (
                steps < height_steps
                and (
                    upper_numerator
                    + (steps + 1) * lower_numerator
                )
                / (
                    upper_denominator
                    + (steps + 1) * lower_denominator
                )
                > target
            ):
                steps += 1

            upper_numerator += steps * lower_numerator
            upper_denominator += steps * lower_denominator

    if lower_numerator == 0:
        lower = None
    elif (lower_numerator - lower_denominator) & 1:
        lower = (lower_numerator, lower_denominator)
    else:
        lower = outside_neighbor(
            lower_numerator,
            lower_denominator,
            hypotenuse_limit,
            above=False,
        )
        if lower[0] == 0:
            lower = None

    if (upper_numerator - upper_denominator) & 1:
        upper = (upper_numerator, upper_denominator)
    else:
        upper = outside_neighbor(
            upper_numerator,
            upper_denominator,
            hypotenuse_limit,
            above=True,
        )
    if upper[0] >= upper[1]:
        upper = None

    return lower, upper


def median_angle(numerator: int, denominator: int) -> float:
    p_squared = numerator * numerator
    q_squared = denominator * denominator
    hypotenuse = p_squared + q_squared
    tangent = (
        3
        * numerator
        * denominator
        * (q_squared - p_squared)
        / (hypotenuse * hypotenuse)
    )
    return math.atan(tangent)


def best_perimeter(angle_degrees: float, limit: int) -> int:
    """Return f(angle_degrees, limit)."""
    target_angle = math.radians(angle_degrees)
    small_slope = math.tan(
        math.asin(4 * math.tan(target_angle) / 3) / 4
    )
    large_slope = (1 - small_slope) / (1 + small_slope)

    best = None
    for slope in (small_slope, large_slope):
        for parameter in slope_neighbors(slope, limit):
            if parameter is None:
                continue
            numerator, denominator = parameter
            hypotenuse = (
                numerator * numerator + denominator * denominator
            )
            scale = limit // hypotenuse
            perimeter = (
                2
                * scale
                * denominator
                * (denominator + numerator)
            )
            area = (
                scale
                * scale
                * numerator
                * denominator
                * (
                    denominator * denominator
                    - numerator * numerator
                )
            )
            candidate = (
                abs(
                    median_angle(numerator, denominator)
                    - target_angle
                ),
                -area,
                perimeter,
            )
            if best is None or candidate < best:
                best = candidate

    return best[2]


def perimeter_sum(count: int, limit: int) -> int:
    return sum(
        best_perimeter(number ** (1 / 3), limit)
        for number in range(1, count + 1)
    )


def solve() -> int:
    assert best_perimeter(30, 10**2) == 198
    assert best_perimeter(10, 10**6) == 1_600_158
    assert perimeter_sum(10, 10**6) == 16_684_370
    return perimeter_sum(45_000, 10**10)


if __name__ == "__main__":
    print(solve())
