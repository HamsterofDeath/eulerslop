#!/usr/bin/env python3
"""p157: Count solutions to 1/a+1/b=p/10^n for n=1..9."""
from math import gcd

def divisor_count(m):
    if m <= 0:
        return 0
    cnt = 1
    d = 2
    while d * d <= m:
        e = 0
        while m % d == 0:
            m //= d
            e += 1
        if e > 0:
            cnt *= e + 1
        d += 1 if d == 2 else 2
    if m > 1:
        cnt *= 2
    return cnt

def count_sols(n):
    cnt = 0
    # Case 1: x=1, y=2^i * 5^j, i=0..n, j=0..n
    for i in range(n + 1):
        for j in range(n + 1):
            x = 1
            y = (2 ** i) * (5 ** j)
            k = (10 ** n) // (x * y)
            m = k * (x + y)
            cnt += divisor_count(m)
    
    # Case 2+3: x=2^i, y=5^j OR x=5^j, y=2^i, i=1..n, j=1..n
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            if (2 ** i) <= (5 ** j):
                x = 2 ** i
                y = 5 ** j
            else:
                x = 5 ** j
                y = 2 ** i
            k = (10 ** n) // (x * y)
            m = k * (x + y)
            cnt += divisor_count(m)
    
    return cnt

def solve():
    total = 0
    for n in range(1, 10):
        total += count_sols(n)
    return total

if __name__ == "__main__":
    print(solve())
