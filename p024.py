#!/usr/bin/env python3
from itertools import permutations

def solve():
    return int("".join(list(permutations("0123456789"))[999999]))

if __name__ == "__main__":
    print(solve())
