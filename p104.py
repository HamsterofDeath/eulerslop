#!/usr/bin/env python3
from math import log10

def is_pandigital(s):
    return len(s) == 9 and set(s) == set("123456789")

def solve():
    a, b = 1, 1
    k = 3
    mod = 10 ** 9
    while True:
        a, b = b, (a + b) % mod
        if k >= 541:
            tail = str(b).zfill(9)
            if is_pandigital(tail):
                # Check first 9 digits using log
                # F_k ≈ phi^k / sqrt(5)
                phi = (1 + 5 ** 0.5) / 2
                logF = k * log10(phi) - log10(5) / 2
                frac = logF - int(logF)
                head = str(int(10 ** (frac + 8)))
                if is_pandigital(head):
                    return k
        k += 1

if __name__ == "__main__":
    print(solve())
