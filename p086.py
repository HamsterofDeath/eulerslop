#!/usr/bin/env python3
from math import isqrt

def count_sol(M):
    total = 0
    for s in range(2, 2 * M + 1):
        for c in range(1, M + 1):
            if isqrt(c * c + s * s) ** 2 == c * c + s * s:
                lo = max(1, s - c)
                hi = min(c, s // 2)
                if lo <= hi:
                    total += hi - lo + 1
    return total

def solve():
    target = 1_000_000
    M = 1817
    count = count_sol(M)
    while count <= target:
        M += 1
        count = count_sol(M)
    return M

if __name__ == "__main__":
    print(solve())
