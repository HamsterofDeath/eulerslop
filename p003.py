#!/usr/bin/env python3

def solve():
    n = 600_851_475_143
    factor = 2
    while factor * factor <= n:
        if n % factor == 0:
            n //= factor
        else:
            factor += 1 if factor == 2 else 2
    return n

if __name__ == "__main__":
    print(solve())
