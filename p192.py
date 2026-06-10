import math
import time

def best_approximation_denom(n, D):
    limit = int(math.isqrt(n))
    if limit * limit == n:
        return 0
    
    m = 0
    d = 1
    a = limit
    
    p_prev2, q_prev2 = 0, 1
    p_prev, q_prev = 1, 0
    
    p = a * p_prev + p_prev2
    q = a * q_prev + q_prev2
    k = 0
    
    while q <= D:
        p_prev2, q_prev2 = p_prev, q_prev
        p_prev, q_prev = p, q
        
        m = a * d - m
        d = (n - m * m) // d
        a = (limit + m) // d
        
        p = a * p_prev + p_prev2
        q = a * q_prev + q_prev2
        k += 1
        
    p_k, q_k = p_prev, q_prev
    p_km1, q_km1 = p_prev2, q_prev2
    k_target = k - 1
    
    a_max = (D - q_km1) // q_k
    
    if a_max == 0:
        return q_k
    
    P = a_max * p_k + p_km1
    Q = a_max * q_k + q_km1
    
    A = 4 * n * Q * Q * q_k * q_k
    B = (P * q_k + Q * p_k) ** 2
    
    if k_target % 2 == 0:
        if A < B:
            return q_k
        else:
            return Q
    else:
        if A < B:
            return Q
        else:
            return q_k

def main():
    total = 0
    D = 10**12
    for n in range(2, 100001):
        total += best_approximation_denom(n, D)
    print(total)

if __name__ == "__main__":
    main()
