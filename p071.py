#!/usr/bin/env python3

def solve():
    best_num = 0
    best_den = 1
    # For each denominator d, find largest n/d < 3/7
    for d in range(2, 1_000_001):
        n = (3 * d - 1) // 7
        if n * best_den > best_num * d:
            best_num, best_den = n, d
    return best_num

if __name__ == "__main__":
    print(solve())
