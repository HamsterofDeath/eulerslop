#!/usr/bin/env python3

def solve():
    limit = 1_000_000
    phi = list(range(limit + 1))
    for i in range(2, limit + 1):
        if phi[i] == i:  # prime
            for j in range(i, limit + 1, i):
                phi[j] -= phi[j] // i
    best_ratio = 0
    best_n = 0
    for n in range(2, limit + 1):
        ratio = n / phi[n]
        if ratio > best_ratio:
            best_ratio, best_n = ratio, n
    return best_n

if __name__ == "__main__":
    print(solve())
