#!/usr/bin/env python3
from math import gcd


def P(m, n):
    # For x in ((t-1)N, tN], x is in the multiplication table iff it is
    # divisible by at least one row a in [t,m].  Count each such union of
    # multiples by inclusion-exclusion over the distinct subset LCMs, updating
    # the range [t,m] incrementally as t descends.
    total = n
    coeff = {}
    for t in range(m, 1, -1):
        add = {t: 1}
        for d, c in coeff.items():
            l = d * t // gcd(d, t)
            add[l] = add.get(l, 0) - c
        for d, c in add.items():
            v = coeff.get(d, 0) + c
            if v:
                coeff[d] = v
            elif d in coeff:
                del coeff[d]
        total += sum(c * ((t * n) // d - (((t - 1) * n) // d))
                     for d, c in coeff.items())
    return total


def solve():
    assert P(3, 4) == 8
    assert P(64, 64) == 1263
    assert P(12, 345) == 1998
    assert P(32, 10 ** 15) == 13826382602124302
    return P(64, 10 ** 16)


if __name__ == "__main__":
    print(solve())
