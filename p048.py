#!/usr/bin/env python3

def solve():
    mod = 10 ** 10
    total = 0
    for n in range(1, 1001):
        total = (total + pow(n, n, mod)) % mod
    return total

if __name__ == "__main__":
    print(solve())
