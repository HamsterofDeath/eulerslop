#!/usr/bin/env python3

def solve():
    primes = []
    n = 2
    while len(primes) < 10_001:
        is_prime = all(n % p != 0 for p in primes if p * p <= n)
        if is_prime:
            primes.append(n)
        n += 1
    return primes[-1]

if __name__ == "__main__":
    print(solve())
