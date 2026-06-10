#!/usr/bin/env python3
from math import gcd

def solve():
    limit = 120_000
    rad = [1] * (limit + 1)
    for i in range(2, limit + 1):
        if rad[i] == 1:
            for j in range(i, limit + 1, i):
                rad[j] *= i

    by_rad = {}
    for n in range(1, limit):
        r = rad[n]
        by_rad.setdefault(r, []).append(n)

    radicals = sorted(by_rad.keys())
    total = 0

    for i, r1 in enumerate(radicals):
        for j in range(i, len(radicals)):
            r2 = radicals[j]
            if r1 * r2 * 2 >= limit:
                break
            if gcd(r1, r2) != 1:
                continue

            for a in by_rad[r1]:
                for b in by_rad[r2]:
                    if b <= a:
                        continue
                    if gcd(a, b) != 1:
                        continue
                    c = a + b
                    if c >= limit:
                        break
                    if r1 * r2 * rad[c] < c:
                        total += c

            if r1 != r2:
                for a in by_rad[r2]:
                    for b in by_rad[r1]:
                        if b <= a:
                            continue
                        if gcd(a, b) != 1:
                            continue
                        c = a + b
                        if c >= limit:
                            break
                        if r1 * r2 * rad[c] < c:
                            total += c
    return total

if __name__ == "__main__":
    print(solve())
