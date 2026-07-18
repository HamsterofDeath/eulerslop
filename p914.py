"""Project Euler Problem 914: Pythagorean Triangles.

A primitive Pythagorean triple has Euclid parameters m > n with coprime,
opposite-parity values.  Writing x = m - n, its inradius is n*x, x is odd,
and its hypotenuse is (n+x)^2 + n^2.

For fixed n, the largest admissible coprime odd x is optimal.  The continuous
upper envelope of n*x has one maximum, so an outward search from that maximum
can stop exactly when the envelope no longer exceeds the best integer result.
"""

from decimal import Decimal, localcontext
from math import gcd, isqrt


TARGET_RADIUS = 10**18


def continuous_optimum(hypotenuse_limit: int) -> int:
    """Return the integer immediately below the optimal continuous n."""
    with localcontext() as context:
        context.prec = 60
        sqrt_two = Decimal(2).sqrt()
        optimum_squared = (
            Decimal(hypotenuse_limit) * (Decimal(2) - sqrt_two) / 4
        )
        return int(optimum_squared.sqrt())


def continuous_product_at_most(
    n: int,
    hypotenuse_limit: int,
    product: int,
) -> bool:
    """Test n*(sqrt(limit-n^2)-n) <= product using integer arithmetic."""
    n_squared = n * n
    return n_squared * (hypotenuse_limit - n_squared) <= (
        product + n_squared
    ) ** 2


def best_product_for_n(n: int, hypotenuse_limit: int) -> tuple[int, int]:
    """Return the best inradius and its odd, coprime x for a fixed n."""
    x = isqrt(hypotenuse_limit - n * n) - n
    if x % 2 == 0:
        x -= 1
    while x > 0 and gcd(n, x) != 1:
        x -= 2
    return n * x, x


def maximum_inradius(radius: int) -> int:
    # The triangle must not touch the circle, hence its integral hypotenuse is
    # at most 2*radius - 1.
    hypotenuse_limit = 2 * radius - 1
    center = continuous_optimum(hypotenuse_limit)
    best, _ = best_product_for_n(center, hypotenuse_limit)

    left_finished = False
    right_finished = False
    distance = 1

    while not (left_finished and right_finished):
        if not left_finished:
            n = center - distance
            if n <= 0 or continuous_product_at_most(
                n, hypotenuse_limit, best
            ):
                left_finished = True
            else:
                candidate, _ = best_product_for_n(n, hypotenuse_limit)
                best = max(best, candidate)

        if not right_finished:
            n = center + distance
            if continuous_product_at_most(n, hypotenuse_limit, best):
                right_finished = True
            else:
                candidate, _ = best_product_for_n(n, hypotenuse_limit)
                best = max(best, candidate)

        distance += 1

    return best


def solve() -> int:
    assert maximum_inradius(100) == 36
    return maximum_inradius(TARGET_RADIUS)


if __name__ == "__main__":
    print(solve())
