#!/usr/bin/env python3

def solve():
    total = 1
    n = 1
    for layer in range(3, 1002, 2):
        for _ in range(4):
            n += layer - 1
            total += n
    return total

if __name__ == "__main__":
    print(solve())
