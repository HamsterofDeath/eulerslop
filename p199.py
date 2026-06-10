import math

def solve_circles(depth):
    k0 = -1.0
    k_init = 1.0 + 2.0 / math.sqrt(3.0)
    total_sum = 3.0 * (1.0 / (k_init * k_init))
    
    def get_new_k(ka, kb, kc):
        inner = ka * kb + kb * kc + kc * ka
        inner = max(0.0, inner)
        return ka + kb + kc + 2.0 * math.sqrt(inner)
        
    def process_gap(ka, kb, kc, current_depth):
        if current_depth > depth:
            return 0.0
            
        kn = get_new_k(ka, kb, kc)
        area_sum = 1.0 / (kn * kn)
        
        area_sum += process_gap(ka, kb, kn, current_depth + 1)
        area_sum += process_gap(kb, kc, kn, current_depth + 1)
        area_sum += process_gap(kc, ka, kn, current_depth + 1)
        
        return area_sum
        
    total_sum += process_gap(k_init, k_init, k_init, 1)
    total_sum += 3.0 * process_gap(k0, k_init, k_init, 1)
    
    uncovered = 1.0 - total_sum
    return uncovered

def main():
    print(f"{solve_circles(10):.8f}")

if __name__ == "__main__":
    main()
