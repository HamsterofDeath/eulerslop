#!/usr/bin/env python3

def solve():
    count = 0
    for n in range(1, 100):
        lo = 10 ** (n - 1)
        hi = 10 ** n - 1
        x = 1
        found = False
        while True:
            p = x ** n
            if p < lo:
                x += 1
                continue
            if p > hi:
                break
            found = True
            count += 1
            x += 1
    return count

if __name__ == "__main__":
    print(solve())
