#!/usr/bin/env python3
from decimal import Decimal, getcontext

def solve():
    getcontext().prec = 105
    total = 0
    for n in range(2, 100):
        r = int(n ** 0.5)
        if r * r == n:
            continue
        s = str(Decimal(n).sqrt()).replace(".", "")[:100]
        total += sum(int(d) for d in s)
    return total

if __name__ == "__main__":
    print(solve())
