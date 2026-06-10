#!/usr/bin/env python3

def solve():
    limit = 10**7
    
    # Sieve to find primes up to 5000
    sieve_limit = 5000
    is_prime = [True] * (sieve_limit + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(sieve_limit**0.5) + 1):
        if is_prime[i]:
            for j in range(i*i, sieve_limit + 1, i):
                is_prime[j] = False
    primes = [i for i, p in enumerate(is_prime) if p]
    
    best_ratio = 2.0
    best_n = 0
    
    for i in range(len(primes)):
        p = primes[i]
        for j in range(i, len(primes)):
            q = primes[j]
            n = p * q
            if n >= limit:
                break
            
            # Check ratio first (extremely fast)
            ratio = n / ((p - 1) * (q - 1))
            if ratio >= best_ratio:
                continue
                
            phi = (p - 1) * (q - 1)
            if sorted(str(n)) == sorted(str(phi)):
                best_ratio = ratio
                best_n = n
                    
    return best_n

if __name__ == "__main__":
    print(solve())
