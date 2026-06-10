#!/usr/bin/env python3

def solve():
    limit = 1_000_000
    count = [0] * limit
    
    for y in range(1, limit):
        k_min = y // 4 + 1
        if k_min > y - 1:
            continue
        for k in range(k_min, y):
            n = y * (4 * k - y)
            if n >= limit:
                break
            count[n] += 1
    
    return sum(1 for c in count if c == 10)

if __name__ == "__main__":
    print(solve())
