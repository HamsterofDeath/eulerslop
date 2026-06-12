#!/usr/bin/env python3
from decimal import Decimal, getcontext
from fractions import Fraction


def _small_E(n):
    a = [Fraction(0) for _ in range(max(n, 3))]
    pref = [Fraction(0) for _ in range(max(n, 3))]
    for k in range(1, n):
        a[k] = Fraction(1) + Fraction(2, k) * (pref[k - 2] if k >= 2 else 0)
        pref[k] = pref[k - 1] + a[k]
    occupied = Fraction(1) + a[n - 3]
    return (Fraction(n) - occupied) / n


def solve():
    assert _small_E(4) == Fraction(1, 2)
    assert _small_E(6) == Fraction(5, 9)

    # The line-segment recurrence has generating function
    # A(x)=(1-exp(-2x))/(2(1-x)^2).  For the initial cycle, the empty fraction
    # at N=10^18 differs from its limit (1+e^-2)/2 by far less than 1e-14.
    getcontext().prec = 50
    ans = (Decimal(1) + (Decimal(-2)).exp()) / 2
    return f"{ans:.14f}"


if __name__ == "__main__":
    print(solve())
