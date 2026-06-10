import math
import numpy as np

def solve():
    L = 2**25
    
    # 1. Find primes up to sqrt(L)
    sqrt_L = int(math.isqrt(L))
    is_prime = [True] * (sqrt_L + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(math.isqrt(sqrt_L)) + 1):
        if is_prime[i]:
            for j in range(i*i, sqrt_L + 1, i):
                is_prime[j] = False
    primes = [i for i, p in enumerate(is_prime) if p]
    
    # 2. Initialize mu and val arrays
    mu = np.ones(L, dtype=np.int8)
    val = np.arange(L, dtype=np.int32)
    
    # 3. Sieve with primes <= sqrt(L)
    for p in primes:
        val[p::p] //= p
        mu[p::p] *= -1
        mu[p*p::p*p] = 0
    
    # 4. Handle primes > sqrt(L)
    mask = (mu != 0) & (val > 1)
    mu[mask] *= -1
    
    # 5. Calculate final sum
    N = 2**50 - 1
    d = np.arange(1, L, dtype=np.int64)
    ans = np.sum(mu[1:].astype(np.int64) * (N // (d * d)))
    print(ans)

if __name__ == "__main__":
    solve()
