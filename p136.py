import numpy as np

def solve():
    limit = 50000000
    
    # Sieve up to limit
    is_prime = np.ones(limit, dtype=bool)
    is_prime[0] = is_prime[1] = False
    
    for i in range(2, int(limit**0.5) + 1):
        if is_prime[i]:
            is_prime[i*i::i] = False
            
    primes = np.nonzero(is_prime)[0]
    count1 = np.sum(primes % 4 == 3)
    count2 = np.sum(primes < 12500000)
    count3 = np.sum(primes < 3125000)
    
    ans = count1 + count2 + count3
    print(ans)

if __name__ == "__main__":
    solve()
