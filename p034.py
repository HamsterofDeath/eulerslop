#!/usr/bin/env python3
from math import factorial

def solve():
    total = 0
    for n in range(10, 50000):
        if n == sum(factorial(int(d)) for d in str(n)):
            total += n
    return total

if __name__ == "__main__":
    print(solve())
