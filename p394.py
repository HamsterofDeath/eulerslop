#!/usr/bin/env python3

from decimal import Decimal, getcontext, ROUND_HALF_UP

def expected(X):
    # Measure pie in fractions of the full circle and put the initial cut at
    # angle 0, with the remaining piece being the arc [0, x].  The two random
    # cuts are i.i.d. uniform on [0, x]; eating the first two pieces leaves
    # y = x - max(u, v), whose density is 2(x - y)/x^2 on [0, x].
    #
    # Let N(x) be the expected number of repetitions with fraction x left and
    # F = 1/X the stopping threshold.  Then N(x) = 0 for x < F and
    #     N(x) = 1 + (2/x^2) * Int_F^x N(y) (x - y) dy        for x >= F.
    # With G(x) = Int_F^x N(y)(x-y) dy we have G'' = N, so G satisfies the
    # Euler ODE  x^2 G'' - 2G = x^2  with G(F) = G'(F) = 0.  Homogeneous
    # solutions x^2 and 1/x, particular solution (x^2/3) ln x, hence
    #     G = (x^2/3) ln x - ((3 ln F + 1)/9) x^2 + F^3/(9x).
    # Then N(x) = 1 + 2G/x^2 and, with F = 1/X,
    #     E(X) = N(1) = 7/9 + (2/3) ln X + 2/(9 X^3).
    X = Decimal(X)
    return Decimal(7) / 9 + Decimal(2) / 3 * X.ln() + 2 / (9 * X ** 3)

def solve():
    getcontext().prec = 50
    # validate against the given values E(1) = 1, E(2), E(7.5)
    assert expected(1) == 1
    assert abs(expected(2) - Decimal("1.2676536759")) < Decimal("5e-11")
    assert abs(expected("7.5") - Decimal("2.1215732071")) < Decimal("5e-11")
    return expected(40).quantize(Decimal("1.0000000000"), rounding=ROUND_HALF_UP)

if __name__ == "__main__":
    print(solve())
