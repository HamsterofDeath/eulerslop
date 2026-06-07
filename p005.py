#!/usr/bin/env python3
from math import gcd

def solve():
    result = 1
    for i in range(2, 21):
        result = result * i // gcd(result, i)
    return result

if __name__ == "__main__":
    print(solve())
