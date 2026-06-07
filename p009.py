#!/usr/bin/env python3

def solve():
    for a in range(1, 500):
        for b in range(a, 500):
            c = 1000 - a - b
            if a * a + b * b == c * c:
                return a * b * c
    return 0

if __name__ == "__main__":
    print(solve())
