#!/usr/bin/env python3
from decimal import Decimal, getcontext
from fractions import Fraction


GAMMA = Decimal("0.57721566490153286060651209008240243104215933593992")


def _harmonic_decimal(n):
    if n < 1000:
        value = sum(Fraction(1, k) for k in range(1, n + 1))
        return Decimal(value.numerator) / Decimal(value.denominator)

    x = Decimal(n)
    return (
        x.ln()
        + GAMMA
        + Decimal(1) / (2 * x)
        - Decimal(1) / (12 * x * x)
        + Decimal(1) / (120 * x ** 4)
    )


def first_digits(n, digits=7):
    # The recurrences for J_A and J_B give
    #   D_n = J_B(n)-J_A(n) = D_{n-1}/2 + 2^{-n}/n,
    # hence 2^n D_n = H_n.
    getcontext().prec = 80
    ln10 = Decimal(10).ln()
    log_value = _harmonic_decimal(n).ln() / ln10 - Decimal(n) * (Decimal(2).ln() / ln10)
    exponent = log_value.to_integral_value(rounding="ROUND_FLOOR")
    frac = log_value - exponent
    mantissa = (frac * ln10).exp()
    return int(mantissa * (10 ** (digits - 1)))


def solve():
    assert str(Decimal(49) / Decimal(1280)).replace(".", "").lstrip("0")[:7] == "3828125"
    return first_digits(123456789)


if __name__ == "__main__":
    print(solve())
