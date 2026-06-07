#!/usr/bin/env python3

def solve():
    total = 0
    a, b = 1, 2
    while a <= 4_000_000:
        if a % 2 == 0:
            total += a
        a, b = b, a + b
    return total

if __name__ == "__main__":
    print(solve())
