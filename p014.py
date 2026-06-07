#!/usr/bin/env python3

def solve():
    best_len, best_n = 0, 0
    cache = {1: 1}
    for i in range(2, 1_000_000):
        n, length = i, 0
        while n not in cache:
            n = n // 2 if n % 2 == 0 else 3 * n + 1
            length += 1
        length += cache[n]
        cache[i] = length
        if length > best_len:
            best_len, best_n = length, i
    return best_n

if __name__ == "__main__":
    print(solve())
