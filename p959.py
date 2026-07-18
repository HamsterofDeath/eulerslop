#!/usr/bin/env python3
"""Project Euler Problem 959: Asymmetric Random Walk.

By reversing a walk prefix, the probability that its endpoint is new
equals the probability of no return to zero.  Thus the limiting range
growth is the escape probability.

For coprime jumps -a and +b, a return has ak right jumps and bk left
jumps for some k.  If u_k is its probability, renewal theory gives

    f(a,b) = 1 / sum(k>=0, u_k),
    u_k = binom((a+b)k, ak) / 2**((a+b)k).

Successive terms are evaluated by an exact rational product and summed
with Decimal precision.
"""

from decimal import Decimal, getcontext
from math import gcd, prod


getcontext().prec = 70


def escape_probability(left: int, right: int) -> Decimal:
    common = gcd(left, right)
    left //= common
    right //= common
    if left == right:
        return Decimal(0)

    period = left + right
    term = Decimal(1)
    total = term
    index = 0

    while term > Decimal("1e-60"):
        numerator = prod(
            range(period * index + 1, period * (index + 1) + 1)
        )
        denominator = (
            prod(
                range(left * index + 1, left * (index + 1) + 1)
            )
            * prod(
                range(right * index + 1, right * (index + 1) + 1)
            )
            * 2**period
        )
        term *= Decimal(numerator) / Decimal(denominator)
        total += term
        index += 1

    return Decimal(1) / total


def solve() -> str:
    assert escape_probability(1, 1) == 0
    sample = escape_probability(1, 2)
    assert abs(sample - Decimal("0.427050983")) < Decimal("1e-9")
    return f"{escape_probability(89, 97):.9f}"


if __name__ == "__main__":
    print(solve())
