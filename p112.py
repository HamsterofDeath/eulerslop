#!/usr/bin/env python3

def is_bouncy(n):
    s = str(n)
    inc = True
    dec = True
    for i in range(len(s) - 1):
        if s[i] < s[i + 1]:
            dec = False
        if s[i] > s[i + 1]:
            inc = False
    return not inc and not dec

def solve():
    bouncy = 0
    n = 0
    while True:
        n += 1
        if is_bouncy(n):
            bouncy += 1
        if bouncy * 100 == 99 * n:
            return n

if __name__ == "__main__":
    print(solve())
