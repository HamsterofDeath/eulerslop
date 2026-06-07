#!/usr/bin/env python3
from math import log10

def solve():
    a, b, index = 1, 1, 2
    while True:
        a, b = b, a + b
        index += 1
        if b >= 10 ** 999:
            return index

if __name__ == "__main__":
    print(solve())
