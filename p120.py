#!/usr/bin/env python3

def solve():
    total = 0
    for a in range(3, 1001):
        # r_max = a * (largest even number < a)
        if a % 2 == 1:
            total += a * (a - 1)
        else:
            total += a * (a - 2)
    return total

if __name__ == "__main__":
    print(solve())
