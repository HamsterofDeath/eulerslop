#!/usr/bin/env python3
from itertools import combinations

def is_prime(n):
    if n < 2: return False
    if n < 4: return True
    if n % 2 == 0 or n % 3 == 0: return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0: return False
        i += 6
    return True

def S(n, d):
    # Find max M, then N and S
    for M in range(n, 0, -1):
        # Generate numbers with M copies of digit d and n-M other positions (0-9)
        # Positions 0..n-1, choose M positions for d
        primes = []
        for pos in combinations(range(n), M):
            template = [-1] * n
            for p in pos:
                template[p] = d
            # Fill other positions (non-leading)
            def gen(idx):
                if idx == n:
                    num = 0
                    for x in template:
                        num = num * 10 + x
                    if template[0] != 0 and is_prime(num):
                        primes.append(num)
                    return
                if template[idx] != -1:
                    gen(idx + 1)
                else:
                    start = 1 if idx == 0 else 0
                    for x in range(start, 10):
                        template[idx] = x
                        gen(idx + 1)
                        template[idx] = -1
            gen(0)
        if primes:
            return M, len(primes), sum(primes)
    return 0, 0, 0

def solve():
    total = 0
    for d in range(10):
        M, N, s = S(10, d)
        total += s
    return total

if __name__ == "__main__":
    print(solve())
