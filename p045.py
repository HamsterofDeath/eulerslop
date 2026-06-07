#!/usr/bin/env python3

def solve():
    n = 286
    while True:
        t = n * (n + 1) // 2
        # Check if pentagonal: solve n(3n-1)/2 = t => 3n^2 - n - 2t = 0
        # n = (1 + sqrt(1 + 24t)) / 6
        p = (1 + (1 + 24 * t) ** 0.5) / 6
        if p == int(p):
            # Check if hexagonal: solve n(2n-1) = t => 2n^2 - n - t = 0
            h = (1 + (1 + 8 * t) ** 0.5) / 4
            if h == int(h):
                return t
        n += 1

if __name__ == "__main__":
    print(solve())
