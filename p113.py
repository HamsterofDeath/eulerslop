#!/usr/bin/env python3
from math import comb

def solve():
    n = 100
    # Increasing: choose n digits from 1-9 with repetition = C(n+8, 8) - 1 (exclude all zero)
    inc = comb(n + 9, 9) - 1
    # Decreasing: choose n digits from 9-0 with repetition, including leading zeros
    # = C(n+10, 10) - (n+1) (subtract all-zero, all-digit-same as zeros)
    dec = comb(n + 10, 10) - (n + 1)
    # Flat numbers (111..1, 222..2, etc.) counted in both inc and dec
    flat = 9 * n
    return inc + dec - flat

if __name__ == "__main__":
    print(solve())
