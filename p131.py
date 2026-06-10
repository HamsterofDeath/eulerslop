#!/usr/bin/env python3

def is_prime(n):
    if n < 2: return False
    if n < 4: return True
    if n % 2 == 0 or n % 3 == 0: return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0: return False
        i += 6
    return True

def solve():
    limit = 1_000_000
    count = 0
    c = 2
    while True:
        p = 3*c*c - 3*c + 1
        if p >= limit:
            break
        if is_prime(p):
            count += 1
        c += 1
    return count

if __name__ == "__main__":
    print(solve())
