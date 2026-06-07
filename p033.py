#!/usr/bin/env python3
from math import gcd

def solve():
    num = 1
    den = 1
    for a in range(10, 100):
        for b in range(a + 1, 100):
            if a % 10 == 0 and b % 10 == 0:
                continue
            sa, sb = str(a), str(b)
            for i in range(2):
                for j in range(2):
                    if sa[i] == sb[j]:
                        na = int(sa[1 - i])
                        nb = int(sb[1 - j])
                        if nb != 0 and a * nb == b * na:
                            num *= a
                            den *= b
    return den // gcd(num, den)

if __name__ == "__main__":
    print(solve())
