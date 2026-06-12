#!/usr/bin/env python3
from decimal import Decimal, ROUND_HALF_UP, getcontext
from fractions import Fraction


def E(n):
    # The largest k whose relative order is not yet fixed contributes an
    # expected (2^(k-1)-1)/k front moves.
    return sum(Fraction(2 ** (k - 1) - 1, k) for k in range(2, n + 1))


def _format_two(value):
    getcontext().prec = 50
    dec = Decimal(value.numerator) / Decimal(value.denominator)
    return str(dec.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def solve():
    assert E(4) == Fraction(13, 4)
    assert E(10) == Fraction(4629, 40)
    return _format_two(E(30))


if __name__ == "__main__":
    print(solve())
