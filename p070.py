#!/usr/bin/env python3

def solve():
    limit = 10_000_000
    phi = list(range(limit))
    for i in range(2, limit):
        if phi[i] == i:
            for j in range(i, limit, i):
                phi[j] -= phi[j] // i

    best_ratio = float('inf')
    best_n = 0
    for n in range(2, limit):
        p = phi[n]
        if sorted(str(n)) == sorted(str(p)):
            ratio = n / p
            if ratio < best_ratio:
                best_ratio, best_n = ratio, n
    return best_n

if __name__ == "__main__":
    print(solve())
