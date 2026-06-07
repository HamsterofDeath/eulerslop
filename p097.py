#!/usr/bin/env python3

def solve():
    mod = 10 ** 10
    # 28433 * 2^7830457 + 1 (mod 10^10)
    result = (28433 * pow(2, 7830457, mod) + 1) % mod
    return result

if __name__ == "__main__":
    print(solve())
