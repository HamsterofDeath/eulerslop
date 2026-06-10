import math

def solve_opt(Q, limit_x=0.01):
    max_bd = Q // 2
    inv_limit = int(1 / limit_x)
    
    ans = 0
    # Case a = 0 (b = 1):
    d_min = inv_limit // 2 + 1
    d_max = max_bd
    if d_max >= d_min:
        ans += (d_max - d_min + 1)
        
    # Case a = 1:
    b_limit = int((1 + math.sqrt(1 + 4 * max_bd)) / 2)
    for b in range(inv_limit + 1, b_limit + 1):
        ans += (max_bd + b) // (b * b)
        
    # Case a > 1:
    max_a = max_bd // (100 * inv_limit)
    for a in range(2, max_a + 1):
        b_min = inv_limit * a + 1
        
        k_max_bound = (max_bd * a + b_min) // (b_min * b_min)
        k_max = min(a - 1, k_max_bound)
        
        for k_0 in range(1, k_max + 1):
            if math.gcd(k_0, a) != 1:
                continue
            r = pow(k_0, -1, a)
            
            b_max = int((1 + math.sqrt(1 + 4 * k_0 * a * max_bd)) / (2 * k_0))
            if r >= b_min:
                m_start = 0
            else:
                m_start = (b_min - r + a - 1) // a
                
            m_end = (b_max - r) // a
            
            for m_prime in range(m_start, m_end + 1):
                b = r + m_prime * a
                d_0 = (k_0 * b - 1) // a
                ans += (max_bd - b * d_0) // (b * b) + 1
                
    return ans

def main():
    print(solve_opt(10**8))

if __name__ == "__main__":
    main()
