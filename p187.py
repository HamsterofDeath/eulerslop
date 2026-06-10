#!/usr/bin/env python3
"""p187: Semiprimes

Find the number of semiprimes (composite with exactly 2 prime factors) below 10^8.
Uses a memory-efficient bytearray-based sieve.
"""
import math
from bisect import bisect_right

def solve():
    limit = 100000000
    sieve_limit = limit // 2
    
    is_prime = bytearray([1]) * (sieve_limit + 1)
    is_prime[0] = is_prime[1] = 0
    
    for i in range(2, int(sieve_limit**0.5) + 1):
        if is_prime[i]:
            is_prime[i*i::i] = bytearray([0]) * len(range(i*i, sieve_limit + 1, i))
            
    primes = [i for i in range(2, sieve_limit + 1) if is_prime[i]]
    
    total = 0
    p_limit = int(math.isqrt(limit - 1))
    
    for p in primes:
        if p > p_limit:
            break
        max_q = (limit - 1) // p
        idx = bisect_right(primes, max_q)
        idx_p = bisect_right(primes, p - 1)
        total += (idx - idx_p)
        
    return total

if __name__ == "__main__":
    print(solve())
