#!/usr/bin/env python3
from itertools import permutations

def solve():
    total = 0
    for perm in permutations("0123456789"):
        if perm[0] == '0':
            continue
        s = "".join(perm)
        if int(s[1:4]) % 2 != 0:
            continue
        if int(s[2:5]) % 3 != 0:
            continue
        if int(s[3:6]) % 5 != 0:
            continue
        if int(s[4:7]) % 7 != 0:
            continue
        if int(s[5:8]) % 11 != 0:
            continue
        if int(s[6:9]) % 13 != 0:
            continue
        if int(s[7:10]) % 17 != 0:
            continue
        total += int(s)
    return total

if __name__ == "__main__":
    print(solve())
