#!/usr/bin/env python3
"""Project Euler 647: Linear transformations of polygonal numbers."""

from math import isqrt


LIMIT = 10**12


def solve(limit: int = LIMIT) -> int:
    root = isqrt(limit)
    total = 0

    # Write r = k - 2.  For odd k, r is odd and the kth polygonal test is
    # 8rx + (r - 2)^2 being a square in one fixed residue class modulo 2r.
    # A map valid for every polygonal number must therefore scale that square
    # by a^2, with a == 1 (mod 2r).  Put a = 1 + 2rt.
    for r in range(1, (root - 1) // 2 + 1, 2):
        delta_squared = (r - 2) ** 2
        t = 1
        while True:
            a = 1 + 2 * r * t
            A = a * a
            if A > limit:
                break

            B = t * (1 + r * t) * delta_squared // 2
            if B <= limit:
                total += A + B
            t += 1

    return total


if __name__ == "__main__":
    print(solve())
