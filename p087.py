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
    limit = 50_000_000
    is_prime = sieve(int(limit ** 0.5) + 1)
    primes = [i for i, p in enumerate(is_prime) if p]
    seen = set()
    for p1 in primes:
        s1 = p1 * p1
        if s1 >= limit:
            break
        for p2 in primes:
            s2 = s1 + p2 * p2 * p2
            if s2 >= limit:
                break
            for p3 in primes:
                s3 = s2 + p3 * p3 * p3 * p3
                if s3 >= limit:
                    break
                seen.add(s3)
    return len(seen)

if __name__ == "__main__":
    print(solve())
