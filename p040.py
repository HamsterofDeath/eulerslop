#!/usr/bin/env python3
from functools import reduce
from operator import mul

def solve():
    s = ""
    n = 1
    while len(s) < 1_000_000:
        s += str(n)
        n += 1
    digits = [int(s[10**i - 1]) for i in range(7)]
    return reduce(mul, digits)

if __name__ == "__main__":
    print(solve())
