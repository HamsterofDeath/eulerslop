#!/usr/bin/env python3

def sieve(n):
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(n ** 0.5) + 1):
        if is_prime[i]:
            for j in range(i * i, n + 1, i):
                is_prime[j] = False
    return is_prime

def solve():
    target = 5000
    is_prime = sieve(100)  # generous upper bound
    primes = [i for i, p in enumerate(is_prime) if p]
    ways = [0] * 100
    ways[0] = 1
    for p in primes:
        for amount in range(p, 100):
            ways[amount] += ways[amount - p]
    for i, w in enumerate(ways):
        if w > target:
            return i

if __name__ == "__main__":
    print(solve())
