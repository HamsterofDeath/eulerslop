#!/usr/bin/env python3
"""Project Euler 206: Concealed Square.

Find the unique positive integer whose square has the form
1_2_3_4_5_6_7_8_9_0, where each "_" is a single digit.

The square ends in 0, so it must end in 00, hence the digit before the
final 0 is 0 and n is a multiple of 10.  Write n = 10*k; then k**2 must
match 1_2_3_4_5_6_7_8_9 (17 digits, fixed digits at even positions).
Since k**2 ends in 9, k must end in 3 or 7, leaving only two candidates
per block of ten to test.
"""

import math


def solve():
    target = "123456789"
    lo = math.isqrt(10203040506070809)
    hi = math.isqrt(19293949596979899)

    start = lo - lo % 10  # align to a multiple of 10
    for base in range(start, hi + 1, 10):
        for k in (base + 3, base + 7):
            if k < lo or k > hi:
                continue
            if str(k * k)[::2] == target:
                return 10 * k
    return None


if __name__ == "__main__":
    print(solve())
