#!/usr/bin/env python3

def solve():
    count = 0
    num, den = 3, 2
    for _ in range(1000):
        if len(str(num)) > len(str(den)):
            count += 1
        num, den = num + 2 * den, num + den
    return count

if __name__ == "__main__":
    print(solve())
