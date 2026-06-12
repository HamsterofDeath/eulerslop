#!/usr/bin/env python3
from math import isqrt


def T(limit):
    triangles = set()

    for diff in range(1, 101):
        # With b = a + diff, the cosine rule gives
        #   c^2 = a^2 + ab + b^2.
        # Setting x = 2c and y = a + b turns this into
        #   x^2 - 3y^2 = diff^2.
        #
        # Multiplication by (2 + sqrt(3))^2 = 7 + 4sqrt(3) preserves
        # the parity conditions x = 2c and y = 2a + diff.  Reversing
        # that recurrence is positive unless y <= 4*diff, so those are
        # enough reduced seeds for each fixed difference.
        for y0 in range(1, 4 * diff + 1):
            x2 = 3 * y0 * y0 + diff * diff
            x0 = isqrt(x2)
            if x0 * x0 != x2:
                continue
            if x0 % 2 or (y0 - diff) % 2:
                continue

            x, y = x0, y0
            while x <= 2 * limit:
                a = (y - diff) // 2
                if a > 0:
                    triangles.add((diff, y))
                x, y = 7 * x + 12 * y, 4 * x + 7 * y

    return len(triangles)


def solve():
    assert T(1000) == 235
    assert T(10**8) == 1245
    return T(10**100)


if __name__ == "__main__":
    print(solve())
