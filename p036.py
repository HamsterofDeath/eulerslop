#!/usr/bin/env python3

def solve():
    total = 0
    for n in range(1, 1_000_000):
        b = bin(n)[2:]
        s = str(n)
        if s == s[::-1] and b == b[::-1]:
            total += n
    return total

if __name__ == "__main__":
    print(solve())
