#!/usr/bin/env python3
"""Project Euler 855: optimal area in the Delphi paper game."""

from decimal import Decimal, localcontext
from fractions import Fraction
from math import factorial


def optimal_area(rows: int, columns: int) -> Fraction:
    """Return S(rows, columns) exactly.

    With t cells left, let r_i and c_j be the remaining counts in each row
    and column.  Alex can choose heights r_i/t and widths c_j/t.  This
    equalizes the inductive value of every available cell.  Weighted AM-GM
    over those cells proves that Bianca can always attain the same bound.

    The row and column factors are therefore reciprocal multinomial
    coefficients, giving the expression below.
    """
    rounds = rows * columns
    numerator = factorial(columns) ** rows * factorial(rows) ** columns
    denominator = factorial(rounds) ** 2
    return Fraction(numerator, denominator)


def solve() -> str:
    assert optimal_area(2, 2) == Fraction(1, 36)
    assert optimal_area(2, 3) == Fraction(1, 1800)

    area = optimal_area(5, 8)
    with localcontext() as context:
        context.prec = 30
        value = Decimal(area.numerator) / Decimal(area.denominator)
        return f"{value:.10e}"


if __name__ == "__main__":
    print(solve())
