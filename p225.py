#!/usr/bin/env python3
"""Project Euler 225: Tribonacci Non-divisors.

Find the 124th odd number d that never divides any term of the sequence
T1=T2=T3=1, T_n = T_{n-1} + T_{n-2} + T_{n-3}.

The sequence mod d is eventually periodic; since the step map
(a, b, c) -> (b, c, a+b+c) is invertible mod any d (you can recover
a = c' - b - a' style backwards step exactly), the orbit starting at
(1, 1, 1) is purely periodic. So iterate mod d until either a term is
0 (d divides some term) or the state returns to (1, 1, 1) (d never
divides any term).
"""


def never_divides(d):
    a, b, c = 1, 1, 1
    while True:
        a, b, c = b, c, (a + b + c) % d
        if c == 0:
            return False
        if a == 1 and b == 1 and c == 1:
            return True


def solve():
    count = 0
    d = 1
    while True:
        d += 2
        if never_divides(d):
            count += 1
            if count == 1:
                assert d == 27, f"expected first non-divisor 27, got {d}"
            if count == 124:
                return d


if __name__ == "__main__":
    print(solve())
