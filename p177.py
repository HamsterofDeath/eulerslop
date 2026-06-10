#!/usr/bin/env python3
"""p177: Integer Angled Quadrilaterals

Count all convex quadrilaterals (up to similarity) where all 8 angles
(splits of vertex angles by diagonals) are integer degrees.
This uses a fast meet-in-the-middle search by grouping angles on opposite sides
of the diagonals, sorting/matching with bisect.
"""
import math
from bisect import bisect_left, bisect_right

def solve():
    # Precompute sines in degrees
    sin_val = [math.sin(math.radians(i)) for i in range(180)]
    
    seen = set()
    tol = 1e-9
    
    def canonical(a1, a2, d2, d1, c2, c1, b2, b1):
        t1 = (a1, a2, d2, d1, c2, c1, b2, b1)
        t2 = (b2, b1, a1, a2, d2, d1, c2, c1)
        t3 = (c2, c1, b2, b1, a1, a2, d2, d1)
        t4 = (d2, d1, c2, c1, b2, b1, a1, a2)
        t5 = (a2, a1, b1, b2, c1, c2, d1, d2)
        t6 = (b1, b2, c1, c2, d1, d2, a2, a1)
        t7 = (c1, c2, d1, d2, a2, a1, b1, b2)
        t8 = (d1, d2, a2, a1, b1, b2, c1, c2)
        return min(t1, t2, t3, t4, t5, t6, t7, t8)

    # T ranges from 1 to 90, so S1 = 180 - T ranges from 90 to 179.
    # When T=1 (S1=179), the loops for b/d are empty, so we can start S1 at 90 and end at 178.
    for S1 in range(90, 179):
        S2 = 180 - S1
        
        # Compute pairs of (value, x, y)
        pairs = []
        for x in range(1, S1):
            f_x = sin_val[x] / sin_val[S1 - x]
            for y in range(1, S2):
                f_y = sin_val[y] / sin_val[S2 - y]
                val = f_x * f_y
                pairs.append((val, x, y))
                
        # Sort values for binary search
        pairs.sort(key=lambda p: p[0])
        vals = [p[0] for p in pairs]
        
        n = len(pairs)
        for i in range(n):
            val_i, x1, y1 = pairs[i]
            # We want val_j * val_i in [1 - tol, 1 + tol]
            target_min = (1.0 - tol) / val_i
            target_max = (1.0 + tol) / val_i
            
            idx_start = bisect_left(vals, target_min)
            idx_end = bisect_right(vals, target_max)
            
            for j in range(idx_start, idx_end):
                _, x2, y2 = pairs[j]
                h = (x1, S1 - x1, y1, S2 - y1, x2, S1 - x2, y2, S2 - y2)
                seen.add(canonical(*h))
                
    return len(seen)

if __name__ == "__main__":
    print(solve())
