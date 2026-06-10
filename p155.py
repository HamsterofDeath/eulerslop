#!/usr/bin/env python3
import numpy as np

def solve():
    S = [np.array([], dtype=np.int64) for _ in range(19)]
    S[1] = np.array([(1 << 32) | 1], dtype=np.int64)
    
    MASK = 0xffffffff
    
    for n in range(2, 19):
        all_pnum = []
        all_pden = []
        
        for a in range(1, (n // 2) + 1):
            b = n - a
            
            val_a = S[a]
            num_a = val_a >> 32
            den_a = val_a & MASK
            
            val_b = S[b]
            num_b = val_b >> 32
            den_b = val_b & MASK
            
            # Use direct broadcasting (faster than np.multiply.outer)
            term1 = num_a[:, None] * den_b
            term2 = den_a[:, None] * num_b
            
            pnum = term1 + term2
            pden = den_a[:, None] * den_b
            
            all_pnum.append(pnum.ravel())
            all_pden.append(pden.ravel())
            
        pnum_arr = np.concatenate(all_pnum)
        pden_arr = np.concatenate(all_pden)
        
        g = np.gcd(pnum_arr, pden_arr)
        pnum_arr //= g
        pden_arr //= g
        
        packed = (pnum_arr << 32) | pden_arr
        
        unique_packed = np.unique(packed)
        recip = ((unique_packed & MASK) << 32) | (unique_packed >> 32)
        
        S[n] = np.unique(np.concatenate([unique_packed, recip]))
        
    all_vals = np.concatenate([S[n] for n in range(1, 19)])
    unique_all = np.unique(all_vals)
    print(len(unique_all))

if __name__ == "__main__":
    solve()
