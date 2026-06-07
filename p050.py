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
    limit = 1_000_000
    is_prime = sieve(limit)
    primes = [i for i, p in enumerate(is_prime) if p]

    best_len = 0
    best_prime = 0
    for start in range(len(primes)):
        total = 0
        for end in range(start, len(primes)):
            total += primes[end]
            if total >= limit:
                break
            length = end - start + 1
            if length > best_len and is_prime[total]:
                best_len = length
                best_prime = total
    return best_prime

if __name__ == "__main__":
    print(solve())
