import math

def sum_div(X):
    if X <= 0:
        return 0
    ans = 0
    limit = int(math.isqrt(X))
    for i in range(1, limit + 1):
        ans += X // i
    return 2 * ans - limit * limit

def solve_mobius_hybrid(N):
    C1 = 2 * N / math.sqrt(3)
    C2 = 6 * N / math.sqrt(3)
    
    max_g = int(math.sqrt(C2))
    
    mu = [0] * (max_g + 1)
    mu[1] = 1
    is_prime = [True] * (max_g + 1)
    is_prime[0] = is_prime[1] = False
    primes = []
    for i in range(2, max_g + 1):
        if is_prime[i]:
            primes.append(i)
            mu[i] = -1
        for p in primes:
            if i * p > max_g:
                break
            is_prime[i * p] = False
            if i % p == 0:
                mu[i * p] = 0
                break
            else:
                mu[i * p] = -mu[i]
                
    lookup_size = 20000
    lookup = [0] * lookup_size
    for X in range(1, lookup_size):
        lookup[X] = sum_div(X)
        
    ans = 0
    
    for g in range(1, max_g + 1):
        if mu[g] == 0:
            continue
        
        m_g = mu[g]
        g2 = g * g
        
        max_vp = int(C2 / g2)
        if max_vp == 0:
            continue
            
        g_mod_3 = g % 3
        
        for vp in range(1, max_vp + 1):
            limit2 = int(C2 / (g2 * vp))
            limit1 = int(C1 / (g2 * vp))
            
            if g_mod_3 == 0:
                if limit2 < lookup_size:
                    s = lookup[limit2]
                else:
                    s = sum_div(limit2)
                ans += m_g * s
            else:
                if limit1 < lookup_size:
                    s = lookup[limit1]
                else:
                    s = sum_div(limit1)
                
                rem = vp % 3
                start_dp = rem if rem > 0 else 3
                
                for dp in range(start_dp, limit2 + 1, 3):
                    s += limit2 // dp
                    if dp <= limit1:
                        s -= limit1 // dp
                
                ans += m_g * s
                
    ans -= int(C2)
    return ans // 2

def main():
    print(solve_mobius_hybrid(1053779))

if __name__ == "__main__":
    main()
