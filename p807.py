#!/usr/bin/env python3
"""Project Euler 807: linked random polygons by an integral operator."""

from decimal import Decimal, ROUND_HALF_UP, getcontext
from fractions import Fraction


TARGET_N = 80


def add_term(poly: list[dict[int, Fraction]], degree: int, exponent: int, value: Fraction) -> None:
    if value == 0:
        return
    coeffs = poly[degree]
    coeffs[exponent] = coeffs.get(exponent, Fraction(0)) + value
    if coeffs[exponent] == 0:
        del coeffs[exponent]


def apply_operator(poly: list[dict[int, Fraction]]) -> list[dict[int, Fraction]]:
    """Apply the Laurent-polynomial kernel K_q to a polynomial in u.

    For a red edge u -> v and a random blue endpoint, the linking contribution is
    +1 with probability max(u-v, 0), -1 with probability max(v-u, 0), and 0
    otherwise. The corresponding integral kernel is piecewise linear, so it maps
    polynomials to polynomials.
    """
    result: list[dict[int, Fraction]] = [{} for _ in range(len(poly) + 2)]
    for degree, coeffs in enumerate(poly):
        if not coeffs:
            continue
        for exponent, coefficient in coeffs.items():
            add_term(result, 0, exponent, coefficient / (degree + 1))

            denominator = (degree + 1) * (degree + 2)
            left = coefficient / denominator
            add_term(result, degree + 2, exponent + 1, left)
            add_term(result, degree + 2, exponent, -left)

            right_terms = (
                (0, coefficient / (degree + 2)),
                (1, -coefficient / (degree + 1)),
                (degree + 2, left),
            )
            for target_degree, value in right_terms:
                add_term(result, target_degree, exponent - 1, value)
                add_term(result, target_degree, exponent, -value)
    return result


def probability(n: int) -> Fraction:
    poly: list[dict[int, Fraction]] = [{0: Fraction(1)}]
    for _ in range(n - 1):
        poly = apply_operator(poly)

    return sum(coeffs.get(0, Fraction(0)) / (degree + 1) for degree, coeffs in enumerate(poly))


def solve() -> str:
    assert probability(3) == Fraction(11, 20)
    assert probability(5) == Fraction(15619, 36288)

    getcontext().prec = 80
    result = probability(TARGET_N)
    value = Decimal(result.numerator) / Decimal(result.denominator)
    return str(value.quantize(Decimal("0.0000000001"), rounding=ROUND_HALF_UP))


if __name__ == "__main__":
    print(solve())
