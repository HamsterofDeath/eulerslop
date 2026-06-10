#!/usr/bin/env python3
"""p176: Right-angled triangles sharing a cathetus.
Smallest integer leg L such that exactly 47547 integer right triangles have one leg = L.
For odd L: count = (d(L^2)-1)/2. For even L: count = (d(L^2/4)-1)/2.
Since count = 47547, target divisor count = 95095 = 5*7*11*13*19."""
from math import prod

def solve():
    target = 2 * 47547 + 1  # 95095
    
    # Factorize target
    target_prime_factors = [5, 7, 11, 13, 19]
    
    # Case 1: odd L
    # d(L^2) = target => 2e_i+1 are the prime factors (or any odd grouping)
    # Enumerate all odd divisor factorizations of target
    def factor_into_odd(n, start=3):
        """Yield all ways to factor n into odd parts >= 3, each part list."""
        if n == 1:
            yield []
            return
        # n must be factorable into odd numbers >= 3
        d = start
        while d * d <= n:
            if n % d == 0:
                for rest in factor_into_odd(n // d, d):
                    yield [d] + rest
            d += 2
        # n itself as a single factor
        if n >= 3:
            yield [n]
    
    best = float('inf')
    
    # Odd L case
    for factors in factor_into_odd(target):
        e_list = [(f - 1) // 2 for f in factors]
        e_list.sort(reverse=True)
        L = 1
        odd_primes = [3, 5, 7, 11, 13, 17, 19, 23, 29]
        for i, e in enumerate(e_list):
            L *= odd_primes[i] ** e
        if L < best:
            best = L
    
    # Even L case
    # L = 2^k * m (m odd). d(L^2/4) = target.
    # L^2/4 = 2^(2k-2) * m^2, d = (2k-1) * d(m^2) = target.
    # (2k-1) must be an odd divisor of target, at least 3 (since k>=1 gives 2k-1>=1).
    # If 2k-1=1, then k=1 but that gives d=1*d(m^2)=target, which is the odd case.
    # Since L is even, k>=1. 2k-1=1 => k=1, but then d(m^2)=target, which is the odd m case.
    # Actually, for even L with k=1: L=2*m. L^2/4 = m^2. d(m^2)=target. This IS the odd case for m.
    # So the even case with k>=2 gives 2k-1 >= 3.
    
    def get_divisors(n):
        divs = []
        for i in range(1, int(n**0.5)+1):
            if n % i == 0:
                if i >= 3 and i % 2 == 1:
                    divs.append(i)
                j = n // i
                if j != i and j >= 3 and j % 2 == 1:
                    divs.append(j)
        return divs
    
    for odd_d in get_divisors(target):
        if odd_d < 3:
            continue
        k = (odd_d + 1) // 2
        R = target // odd_d
        
        for factors in factor_into_odd(R):
            e_list = [(f - 1) // 2 for f in factors]
            e_list.sort(reverse=True)
            L = 2 ** k
            odd_primes = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31]
            for i, e in enumerate(e_list):
                L *= odd_primes[i] ** e
            if L < best:
                best = L
    
    return best

if __name__ == "__main__":
    print(solve())
