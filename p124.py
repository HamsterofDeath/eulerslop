#!/usr/bin/env python3

def solve():
    limit = 100_000
    rad = [1] * (limit + 1)
    for i in range(2, limit + 1):
        if rad[i] == 1:  # prime
            for j in range(i, limit + 1, i):
                rad[j] *= i
    
    # Sort by (rad[n], n)
    items = [(rad[n], n) for n in range(1, limit + 1)]
    items.sort()
    return items[9999][1]  # E(10000), 0-indexed

if __name__ == "__main__":
    print(solve())
