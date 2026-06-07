#!/usr/bin/env python3
from math import isqrt

def is_prime(n):
    if n < 2:
        return False
    if n < 4:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def solve():
    n = 9
    while True:
        if not is_prime(n):
            found = False
            for s in range(1, isqrt(n // 2) + 1):
                if is_prime(n - 2 * s * s):
                    found = True
                    break
            if not found:
                return n
        n += 2

if __name__ == "__main__":
    print(solve())
