#!/usr/bin/env python3

def cycle_length(d):
    if d % 2 == 0 or d % 5 == 0:
        return 0  # terminating decimal
    remainder = 1
    seen = {}
    pos = 0
    while remainder != 0 and remainder not in seen:
        seen[remainder] = pos
        remainder = (remainder * 10) % d
        pos += 1
    if remainder == 0:
        return 0
    return pos - seen[remainder]

def solve():
    best_length = 0
    best_d = 0
    for d in range(2, 1000):
        length = cycle_length(d)
        if length > best_length:
            best_length, best_d = length, d
    return best_d

if __name__ == "__main__":
    print(solve())
