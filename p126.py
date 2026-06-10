#!/usr/bin/env python3

def solve():
    limit = 50000
    count = [0] * (limit + 1)
    
    # Precompute quadratic terms for k
    k_quad = [4 * (k - 1) * (k - 2) for k in range(150)]
    
    for a in range(1, int((limit // 6)**0.5) + 2):
        for b in range(a, limit):
            base_ab = 2 * a * b
            if base_ab + 2 * a * b + 2 * b * b > limit:
                break
            
            sum_ab = a + b
            diff_base = 4 * sum_ab
            
            for c in range(b, limit):
                base = base_ab + 2 * sum_ab * c
                if base > limit:
                    break
                
                k_diff = diff_base + 4 * c
                count[base] += 1
                
                k = 2
                offset = base - k_diff
                while True:
                    n = offset + k * k_diff + k_quad[k]
                    if n > limit:
                        break
                    count[n] += 1
                    k += 1
                    
    for n in range(1, limit + 1):
        if count[n] == 1000:
            return n
    return 0

if __name__ == "__main__":
    print(solve())
