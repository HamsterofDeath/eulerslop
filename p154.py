#!/usr/bin/env python3
import numpy as np

def solve():
    N = 200000
    
    # Precompute s2 and s5
    s2 = np.zeros(N + 1, dtype=np.uint8)
    s5 = np.zeros(N + 1, dtype=np.uint8)
    for n in range(1, N + 1):
        s2[n] = s2[n >> 1] + (n & 1)
        s5[n] = s5[n // 5] + (n % 5)
        
    s2_N = s2[N]
    s5_N = s5[N]
    
    # Pre-reverse s5 to avoid negative steps and make slices contiguous
    s5_rev = s5[::-1].copy()
    
    ans = 0
    
    max_len = N // 2 + 1
    out5 = np.empty(max_len, dtype=np.uint8)
    cond5 = np.empty(max_len, dtype=np.bool_)
    
    for i in range(N // 3 + 1):
        rem = N - i
        j_min = i
        j_max = rem // 2
        if j_min > j_max:
            continue
            
        length = j_max - j_min + 1
        limit2 = s2_N + 12 - s2[i]
        limit5 = s5_N + 48 - s5[i]
        
        # Contiguous slices
        s5_j = s5[j_min : j_max + 1]
        s5_k = s5_rev[i + j_min : i + j_max + 1]
        
        np.add(s5_j, s5_k, out=out5[:length])
        np.greater_equal(out5[:length], limit5, out=cond5[:length])
        
        matching_indices = np.flatnonzero(cond5[:length])
        if len(matching_indices) == 0:
            continue
            
        s2_j = s2[j_min + matching_indices]
        s2_k = s2[(rem - j_min) - matching_indices]
        
        cond2 = (s2_j + s2_k) >= limit2
        
        valid_count = np.sum(cond2)
        ans += 6 * valid_count
        
        # Scalar corrections for boundary weights
        if j_min == i and matching_indices[0] == 0:
            if cond2[0]:
                if i == rem - i:
                    ans -= 5
                else:
                    ans -= 3
        if (rem - j_max) == j_max and matching_indices[-1] == length - 1:
            if cond2[-1]:
                ans -= 3
                
    print(ans)

if __name__ == "__main__":
    solve()
