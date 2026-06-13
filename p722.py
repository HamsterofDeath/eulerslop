#!/usr/bin/env python3
"""Project Euler 722: slowly convergent divisor-power Lambert series."""

from decimal import Decimal, ROUND_HALF_UP, getcontext
from math import factorial


K = 15
POWER = 25
TERMS_FOR_ZETA = 300
DIGITS_AFTER_DECIMAL = 12


def zeta_by_summation(s: int) -> Decimal:
    """Compute zeta(s) by direct summation; for s=16 the tail is tiny."""
    total = Decimal(0)
    for n in range(1, TERMS_FOR_ZETA + 1):
        total += Decimal(1) / (Decimal(n) ** s)
    return total


def scientific(value: Decimal, digits_after: int) -> str:
    exponent = value.adjusted()
    mantissa = value.scaleb(-exponent)
    quantum = Decimal(1).scaleb(-digits_after)
    rounded = mantissa.quantize(quantum, rounding=ROUND_HALF_UP)
    if rounded == Decimal(10).quantize(quantum):
        exponent += 1
        rounded = Decimal(1).quantize(quantum)
    return f"{rounded}e{exponent}"


def solve() -> str:
    getcontext().prec = 120

    q = Decimal(1) - Decimal(1) / (1 << POWER)
    t = -q.ln()

    # E_k(e^-t) has Mellin transform Gamma(s) zeta(s) zeta(s-k) t^-s.
    # For odd k=15 all positive-power residues vanish by zeta's trivial zeros.
    leading = Decimal(factorial(K)) * zeta_by_summation(K + 1) / (t ** (K + 1))

    # Residue at s=0: zeta(0) zeta(-15) = -3617 / 16320.
    constant_residue = -Decimal(3617) / Decimal(16320)
    return scientific(leading + constant_residue, DIGITS_AFTER_DECIMAL)


if __name__ == "__main__":
    print(solve())
