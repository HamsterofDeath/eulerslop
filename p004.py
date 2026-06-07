#!/usr/bin/env python3

def solve():
    best = 0
    for a in range(999, 99, -1):
        for b in range(a, 99, -1):
            p = a * b
            if p <= best:
                break
            s = str(p)
            if s == s[::-1]:
                best = p
    return best

if __name__ == "__main__":
    print(solve())
