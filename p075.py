#!/usr/bin/env python3
from math import gcd, isqrt

def solve():
    limit = 1_500_000
    # Generate primitive Pythagorean triples
    cnt = [0] * (limit + 1)
    for m in range(2, isqrt(limit // 2) + 1):
        for n in range(1, m):
            if (m + n) % 2 == 0 or gcd(m, n) != 1:
                continue
            a = m * m - n * n
            b = 2 * m * n
            c = m * m + n * n
            p = a + b + c
            for k in range(p, limit + 1, p):
                cnt[k] += 1
    return sum(1 for c in cnt if c == 1)

if __name__ == "__main__":
    print(solve())
