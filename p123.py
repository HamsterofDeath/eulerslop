#!/usr/bin/env python3

def sieve(limit):
    is_p = [True] * (limit + 1)
    is_p[0] = is_p[1] = False
    for i in range(2, int(limit**0.5) + 1):
        if is_p[i]:
            for j in range(i*i, limit + 1, i):
                is_p[j] = False
    return [i for i in range(2, limit + 1) if is_p[i]]

def solve():
    target = 10 ** 10
    primes = sieve(1_000_000)
    for n in range(7037, len(primes) + 1, 2):
        p = primes[n - 1]
        r = (2 * n * p) % (p * p)
        if r > target:
            return n

if __name__ == "__main__":
    print(solve())
