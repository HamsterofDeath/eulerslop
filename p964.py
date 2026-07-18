#!/usr/bin/env python3
"""Project Euler Problem 964: Musical Chairs Revisited.

The distribution for round i is the average of the uniform measures on
all conjugates of an S_i subgroup of S_n.  It therefore acts as a scalar
on every irreducible representation.  At an n-cycle only the hook
representations (n-j, 1**j) have nonzero character.  Their dimensions
are C(n-1, j), their n-cycle characters are (-1)**j, and the dimension
of their S_i-fixed subspace is C(n-i, j).
"""

from decimal import Decimal, localcontext
from fractions import Fraction
from math import comb, factorial


def probability(rounds: int) -> Fraction:
    children = rounds * (rounds - 1) // 2 + 1
    total = Fraction()

    for hook in range(children - rounds + 1):
        dimension = comb(children - 1, hook)
        term = Fraction((-1) ** hook * dimension)
        for selected in range(1, rounds + 1):
            term *= Fraction(
                comb(children - selected, hook),
                dimension,
            )
        total += term

    return total / factorial(children)


def solve() -> str:
    assert probability(3) == Fraction(1, 72)
    value = probability(7)
    with localcontext() as context:
        context.prec = 50
        return f"{Decimal(value.numerator) / value.denominator:.10e}"


if __name__ == "__main__":
    print(solve())
