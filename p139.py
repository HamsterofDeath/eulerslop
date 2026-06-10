#!/usr/bin/env python3
from math import gcd

def solve():
    limit = 100_000_000
    count = 0
    
    for m in range(2, 10000):
        if 2 * m * (m + 1) >= limit:
            break
        for n in range(1, m):
            if (m - n) % 2 == 0:
                continue
            if gcd(m, n) != 1:
                continue
            a = m * m - n * n
            b = 2 * m * n
            c = m * m + n * n
            base_perim = 2 * m * (m + n)
            if base_perim >= limit:
                break
            hole = abs(b - a)
            if c % hole == 0:
                count += (limit - 1) // base_perim
    return count

if __name__ == "__main__":
    print(solve())
