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

def modinv(a, m):
    # Extended Euclidean
    return pow(a, -1, m)

def solve():
    limit = 1_000_000
    # Generate consecutive primes
    primes = []
    for n in range(5, limit + 200):
        if is_prime(n):
            primes.append(n)
    
    total = 0
    for i in range(len(primes) - 1):
        p1 = primes[i]
        p2 = primes[i + 1]
        if p1 > limit:
            break
        d = len(str(p1))
        mod = 10 ** d
        k = (p1 * modinv(p2, mod)) % mod
        if k == 0:
            k = mod
        n = k * p2
        total += n
    return total

if __name__ == "__main__":
    print(solve())
