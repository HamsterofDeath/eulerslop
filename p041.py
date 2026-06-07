#!/usr/bin/env python3
from itertools import permutations

def is_prime(n):
    if n < 2:
        return False
    if n < 4:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def solve():
    for n in range(7, 0, -1):
        for perm in permutations("7654321"[:n], n):
            num = int("".join(perm))
            if is_prime(num):
                return num
    return 0

if __name__ == "__main__":
    print(solve())
