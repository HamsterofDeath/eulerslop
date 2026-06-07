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
    primes = 3
    total = 5
    n = 3
    while primes / total >= 0.1:
        n += 2
        side = n * n
        for _ in range(3):
            side -= n - 1
            if is_prime(side):
                primes += 1
        total += 4
    return n

if __name__ == "__main__":
    print(solve())
