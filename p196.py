import math
import numpy as np

def S(r):
    r_start = r - 2
    r_end = r + 2
    
    start_val = r_start * (r_start - 1) // 2 + 1
    end_val = r_end * (r_end + 1) // 2
    
    L = end_val - start_val + 1
    
    limit = int(math.isqrt(end_val)) + 1
    is_prime_small = np.ones(limit, dtype=bool)
    is_prime_small[0] = is_prime_small[1] = False
    for i in range(2, int(math.isqrt(limit)) + 1):
        if is_prime_small[i]:
            is_prime_small[i*i::i] = False
    primes = np.nonzero(is_prime_small)[0]
    
    is_prime = np.ones(L, dtype=bool)
    for p in primes:
        rem = start_val % p
        if rem == 0:
            first = 0
        else:
            first = p - rem
        if start_val + first == p:
            first += p
        is_prime[first::p] = False
        
    P = {}
    for y in range(r-2, r+3):
        row_start = y * (y - 1) // 2 + 1
        offset = row_start - start_val
        P[y] = is_prime[offset : offset + y]
        
    def get_row_padded(y, target_k):
        arr = np.zeros(target_k + 2, dtype=bool)
        arr[1 : y + 1] = P[y]
        return arr
        
    def get_row_padded_from_array(arr_y, target_k):
        arr = np.zeros(target_k + 2, dtype=bool)
        arr[1 : len(arr_y) + 1] = arr_y
        return arr
        
    has_2_neighbors = {}
    for k in range(r-1, r+2):
        row_prev = get_row_padded(k-1, k)
        row_curr = get_row_padded(k, k)
        row_next = get_row_padded(k+1, k)
        
        counts = (row_prev[0:k].astype(int) + row_prev[1:k+1].astype(int) + row_prev[2:k+2].astype(int) +
                  row_curr[0:k].astype(int)                               + row_curr[2:k+2].astype(int) +
                  row_next[0:k].astype(int) + row_next[1:k+1].astype(int) + row_next[2:k+2].astype(int))
                  
        has_2_neighbors[k] = (counts >= 2)
        
    active = {}
    for y in range(r-1, r+2):
        active[y] = P[y] & has_2_neighbors[y]
        
    act_prev = get_row_padded_from_array(active[r-1], r)
    act_curr = get_row_padded_from_array(active[r], r)
    act_next = get_row_padded_from_array(active[r+1], r)
    
    neighbor_active = (act_prev[0:r] | act_prev[1:r+1] | act_prev[2:r+2] |
                       act_curr[0:r]                   | act_curr[2:r+2] |
                       act_next[0:r] | act_next[1:r+1] | act_next[2:r+2])
                       
    in_triplet = P[r] & (has_2_neighbors[r] | neighbor_active)
    
    row_r_start = r * (r - 1) // 2 + 1
    values_r = np.arange(row_r_start, row_r_start + r, dtype=np.int64)
    
    return np.sum(values_r[in_triplet])

def main():
    print(S(5678027) + S(7208785))

if __name__ == "__main__":
    main()
