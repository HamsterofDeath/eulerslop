#!/usr/bin/env python3
import math
import numpy as np

def solve():
    N = 10**8
    
    total = 0
    # 1. Integer divisors (b=0)
    i = 1
    while i <= N:
        q = N // i
        j = N // q
        total += q * (i + j) * (j - i + 1) // 2
        i = j + 1
        
    # 2. Precompute S(M) up to K = 500,000
    K = 500000
    sigma = np.arange(K + 1, dtype=np.int64)
    sigma[2:] += 1
    for d in range(2, K // 2 + 1):
        sigma[2*d::d] += d
    S_lookup = np.cumsum(sigma)
    
    def get_S_large(M):
        s = 0
        i = 1
        while i <= M:
            q = M // i
            j = M // q
            s += q * (i + j) * (j - i + 1) // 2
            i = j + 1
        return s

    limit = int(math.isqrt(N))
    
    # (1, 1) case
    total += 2 * get_S_large(N // 2)
    
    # 3. Gaussian divisors (b>0)
    for a1 in range(2, limit + 1):
        max_b1 = int(math.isqrt(N - a1*a1))
        lim_b = min(a1 - 1, max_b1)
        if lim_b < 1:
            continue
            
        b_arr = np.arange(1, lim_b + 1, dtype=np.int64)
        coprime = np.gcd(a1, b_arr) == 1
        b_coprime = b_arr[coprime]
        
        g = a1*a1 + b_coprime*b_coprime
        M = N // g
        
        mask_small = M <= K
        M_small = M[mask_small]
        
        total += 2 * np.sum((a1 + b_coprime[mask_small]) * S_lookup[M_small])
        
        if not np.all(mask_small):
            M_large = M[~mask_small]
            b_large = b_coprime[~mask_small]
            for b_val, M_val in zip(b_large, M_large):
                total += 2 * (a1 + b_val) * get_S_large(M_val)
                
    print(total)

if __name__ == "__main__":
    solve()
