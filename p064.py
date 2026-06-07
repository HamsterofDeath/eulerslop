#!/usr/bin/env python3

def period_sqrt(n):
    sqrt_n = int(n ** 0.5)
    if sqrt_n * sqrt_n == n:
        return 0
    a0 = sqrt_n
    m, d, a = 0, 1, a0
    period = 0
    while a != 2 * a0:
        m = d * a - m
        d = (n - m * m) // d
        a = (a0 + m) // d
        period += 1
    return period

def solve():
    return sum(1 for n in range(1, 10001) if period_sqrt(n) % 2 == 1)

if __name__ == "__main__":
    print(solve())
