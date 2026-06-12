#!/usr/bin/env python3
from fractions import Fraction
from decimal import Decimal, getcontext


def solve():
    # Compound (Wald-type) distribution chain.  If X = sum of N iid dice
    # rolls (N random, independent of the rolls), then
    #   E[X]   = E[N] * mu,
    #   Var(X) = E[N] * var + Var(N) * mu^2   (law of total variance),
    # where mu, var are mean/variance of a single die.  A fair s-sided die
    # has mu = (s+1)/2 and var = (s^2 - 1)/12.  Chain through 4 -> 6 -> 8
    # -> 12 -> 20 sided dice exactly with rationals.
    mean = Fraction(5, 2)            # E[T] for the d4
    var = Fraction(4 * 4 - 1, 12)    # Var(T)
    for s in (6, 8, 12, 20):
        mu = Fraction(s + 1, 2)
        v = Fraction(s * s - 1, 12)
        mean, var = mean * mu, mean * v + var * mu * mu

    getcontext().prec = 50
    result = Decimal(var.numerator) / Decimal(var.denominator)
    return str(result.quantize(Decimal("0.0001")))


if __name__ == "__main__":
    print(solve())
