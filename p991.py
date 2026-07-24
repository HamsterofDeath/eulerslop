#!/usr/bin/env python3
"""Project Euler Problem 991: Fruit Salad.

Put a = apple and y = banana + pineapple.  The equation becomes

    a/y + y/(a + pineapple) = 4.

Write gcd(a, y) out and set a/y = (4q-d)/q in lowest terms.  Since
gcd(d, q) = 1, integrality forces every solution to be a multiple of

    apple     = d(4q-d),
    pineapple = d^2-4qd+q^2,
    banana    = 5qd-q^2-d^2.

The primitive total is d(5q-d).  The two positivity tests select two
short intervals for d/q, and all multiples up to the limit contribute
an arithmetic-series sum.
"""

from math import gcd, isqrt


LIMIT = 10_000_000


def solve(limit: int = LIMIT) -> int:
    answer = 0

    # Positivity implies d(5q-d) > q^2, so q <= sqrt(limit).
    for q in range(1, isqrt(limit) + 1):
        # The admissible intervals lie inside (q/5, 3q/10) and
        # (37q/10, 4q), respectively.  Integer tests below impose
        # the exact irrational quadratic boundaries.
        ranges = (
            range(q // 5 + 1, 3 * q // 10 + 1),
            range(37 * q // 10, 4 * q),
        )
        for candidates in ranges:
            for d in candidates:
                pineapple = d * d - 4 * q * d + q * q
                banana = 5 * q * d - q * q - d * d
                if pineapple <= 0 or banana <= 0 or gcd(d, q) != 1:
                    continue

                primitive_total = d * (5 * q - d)
                multiples = limit // primitive_total
                answer += (
                    primitive_total
                    * multiples
                    * (multiples + 1)
                    // 2
                )

    return answer


if __name__ == "__main__":
    print(solve())
