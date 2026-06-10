#!/usr/bin/env python3
"""p141: Sum of all progressive perfect squares < 10^12.
n = dq + r, d>r, and d,q,r are consecutive terms of a GP.
Let GP terms be g*a^2, g*a*b, g*b^2 with b>a, gcd(a,b)=1.
Case d=g*b^2, q=g*a*b, r=g*a^2: n = g*a*(g*b^3 + a) = m^2."""
from math import gcd, isqrt

def solve():
    limit = 10**12
    seen = set()
    total = 0
    for b in range(2, 10001):  # b^3 up to 1e12 → b up to 10000
        b3 = b * b * b
        for a in range(1, b):
            if gcd(a, b) != 1:
                continue
            # n = g*a*(g*b^3 + a) < limit
            # For given a,b, iterate g
            g = 1
            while True:
                n = g * a * (g * b3 + a)
                if n >= limit:
                    break
                s = isqrt(n)
                if s * s == n and n not in seen:
                    seen.add(n)
                    total += n
                g += 1
    return total

if __name__ == "__main__":
    print(solve())
