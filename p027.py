#!/usr/bin/env python3

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
    best = (0, 0, 0)
    for a in range(-999, 1000):
        for b in range(-1000, 1001):
            n = 0
            while is_prime(n * n + a * n + b):
                n += 1
            if n > best[0]:
                best = (n, a, b)
    return best[1] * best[2]

if __name__ == "__main__":
    print(solve())
