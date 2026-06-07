#!/usr/bin/env python3
from math import isqrt

def d(n):
    total = 1
    for i in range(2, isqrt(n) + 1):
        if n % i == 0:
            total += i
            if i != n // i:
                total += n // i
    return total

def solve():
    total = 0
    for a in range(2, 10000):
        b = d(a)
        if b != a and b < 10000 and d(b) == a:
            total += a
    return total

if __name__ == "__main__":
    print(solve())
