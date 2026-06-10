#!/usr/bin/env python3
"""p183: Maximum product of parts

Find sum_{N=5..10000} D(N) where:
D(N) = N if M(N) is non-terminating, and -N if M(N) is terminating.
M(N) is the maximum of (N/k)^k.
The maximum is achieved at k = round(N / e).
"""
import math

def solve():
    e = math.e
    total_sum = 0
    
    for N in range(5, 10001):
        # Continuous maximum is at x = N/e
        # The integer maximum must be floor(N/e) or ceil(N/e)
        k1 = int(N / e)
        k2 = k1 + 1
        
        # Compare (N/k1)^k1 and (N/k2)^k2
        # We compare their logs: k1 * ln(N) - k1 * ln(k1) vs k2 * ln(N) - k2 * ln(k2)
        val1 = k1 * math.log(N) - k1 * math.log(k1)
        val2 = k2 * math.log(N) - k2 * math.log(k2)
        
        k = k1 if val1 > val2 else k2
        
        # M(N) = (N/k)^k.
        # This is a terminating decimal iff the denominator of N/k in lowest terms
        # has only 2 and 5 as prime factors.
        # Lowest terms denominator = k / gcd(N, k)
        denom = k // math.gcd(N, k)
        
        # Check if denom has only 2 and 5 as prime factors
        temp = denom
        while temp % 2 == 0:
            temp //= 2
        while temp % 5 == 0:
            temp //= 5
            
        if temp == 1:
            # Terminating
            total_sum -= N
        else:
            # Non-terminating
            total_sum += N
            
    return total_sum

if __name__ == "__main__":
    print(solve())
