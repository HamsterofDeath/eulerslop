#!/usr/bin/env python3
import numpy as np

def solve():
    rows = 1000
    total_elems = rows * (rows + 1) // 2
    
    # Generate s_k
    t = 0
    s = []
    for k in range(1, total_elems + 1):
        t = (615949 * t + 797807) % (1 << 20)
        s.append(t - (1 << 19))
        
    # Build triangle as numpy arrays for prefix sums
    tri = []
    idx = 0
    for i in range(rows):
        tri.append(np.array(s[idx : idx + i + 1], dtype=np.int64))
        idx += i + 1
        
    # Compute prefix sums as numpy arrays
    pref = []
    for i in range(rows):
        p = np.zeros(i + 2, dtype=np.int64)
        p[1:] = np.cumsum(tri[i])
        pref.append(p)
        
    # dp[i] will store the current sub-triangle sum starting at row i
    dp = [np.zeros(i + 1, dtype=np.int64) for i in range(rows)]
    
    best = float('inf')
    
    # Loop over height h
    for h in range(1, rows + 1):
        for i in range(rows - h + 1):
            row = i + h - 1
            P = pref[row]
            # Slices of size i + 1
            dp[i] += P[h : h + i + 1] - P[0 : i + 1]
            
            # Update best
            current_min = np.min(dp[i])
            if current_min < best:
                best = current_min
                
    print(best)

if __name__ == "__main__":
    solve()
