#!/usr/bin/env python3
from math import isqrt

def divisor_count(n):
    count = 0
    for i in range(1, isqrt(n) + 1):
        if n % i == 0:
            count += 2 if i * i != n else 1
    return count

def solve():
    n = 1
    tri = 1
    while divisor_count(tri) <= 500:
        n += 1
        tri += n
    return tri

if __name__ == "__main__":
    print(solve())
