#!/usr/bin/env python3
"""Project Euler 697: Randomly Decaying Sequence."""

import math


TERMS = 10_000_000
TARGET_UPPER_TAIL = 0.25


def _regularized_gamma_q(shape, x):
    """Upper regularized incomplete gamma Q(shape, x), for x > shape."""
    eps = 1e-15
    tiny = 1e-300

    b = x + 1.0 - shape
    c = 1.0 / tiny
    d = 1.0 / b
    h = d

    for i in range(1, 100_000):
        an = -i * (i - shape)
        b += 2.0

        d = an * d + b
        if abs(d) < tiny:
            d = tiny

        c = b + an / c
        if abs(c) < tiny:
            c = tiny

        d = 1.0 / d
        delta = d * c
        h *= delta
        if abs(delta - 1.0) < eps:
            return math.exp(-x + shape * math.log(x) - math.lgamma(shape)) * h

    raise RuntimeError("gamma continued fraction did not converge")


def _gamma_quantile_for_upper_tail(shape, tail_probability):
    lo = float(shape)
    hi = float(shape)
    while _regularized_gamma_q(shape, hi) > tail_probability:
        hi += max(1.0, (hi - shape + 1.0) * 2.0)

    for _ in range(80):
        mid = (lo + hi) / 2.0
        if _regularized_gamma_q(shape, mid) > tail_probability:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2.0


def solve():
    # -log(U_1 ... U_n) is Gamma(n, 1).  We need P(Gamma(n,1)>log(c))=0.25.
    quantile = _gamma_quantile_for_upper_tail(TERMS, TARGET_UPPER_TAIL)
    return f"{quantile / math.log(10):.2f}"


if __name__ == "__main__":
    print(solve())
