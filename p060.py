#!/usr/bin/env python3

def sieve(n):
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(n ** 0.5) + 1):
        if is_prime[i]:
            for j in range(i * i, n + 1, i):
                is_prime[j] = False
    return is_prime

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

def concat_prime(a, b):
    return is_prime(int(str(a) + str(b))) and is_prime(int(str(b) + str(a)))

def solve():
    # Need to find 5 primes where all pairs concatenate to primes
    # Search incrementally
    from itertools import combinations

    is_prime_arr = sieve(10000)
    primes = [i for i, p in enumerate(is_prime_arr) if p and i > 2]
    # Limit search space
    primes = [p for p in primes if p < 10000]

    # Build graph: for each prime, find compatible primes
    for i, p in enumerate(primes):
        compat = [q for q in primes[i+1:] if concat_prime(p, q)]
        if len(compat) < 4:
            continue
        for c1 in compat:
            compat2 = [r for r in compat if r > c1 and concat_prime(c1, r)]
            if len(compat2) < 3:
                continue
            for c2 in compat2:
                compat3 = [r for r in compat2 if r > c2 and concat_prime(c2, r)]
                if len(compat3) < 2:
                    continue
                for c3 in compat3:
                    compat4 = [r for r in compat3 if r > c3 and concat_prime(c3, r)]
                    for c4 in compat4:
                        return p + c1 + c2 + c3 + c4
    return 0

if __name__ == "__main__":
    print(solve())
