#!/usr/bin/env python3
from math import gcd, isqrt


def S(limit):
    total = 0
    y = 1
    while True:
        if y * y * (y + 1) * (y + 1) > limit:
            break
        for x in range(1, y + 1):
            rb = y * y * (x + y) * (x + y)
            if rb > limit:
                break
            if gcd(x, y) != 1:
                continue

            # With A = k*x*(x+y), B = k*y*(x+y), C = k*x*y, the curvatures
            # satisfy 1/C = 1/A + 1/B.  Squaring gives the three integer radii.
            base_sum = (x + y) * (x + y) * (x * x + y * y) + x * x * y * y
            repeats = limit // rb
            total += base_sum * repeats * (repeats + 1) // 2
        y += 1
    return total


def solve():
    assert S(5) == 9
    assert S(100) == 3072
    return S(10 ** 9)


if __name__ == "__main__":
    print(solve())
