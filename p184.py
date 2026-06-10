#!/usr/bin/env python3
"""p184: Triangles containing the origin

Count triangles with vertices in I_{105} containing the origin in their interior.
We group points by primitive directions, sort them by angle, and use a sliding window.
"""
import math

def solve():
    r = 105
    
    # Find all primitive directions inside x^2 + y^2 < r^2
    directions = []
    for x in range(-r, r + 1):
        for y in range(-r, r + 1):
            if x == 0 and y == 0:
                continue
            if x*x + y*y >= r*r:
                continue
            g = math.gcd(abs(x), abs(y))
            if g == 1:
                angle = math.atan2(y, x)
                if angle < 0:
                    angle += 2 * math.pi
                directions.append((angle, x, y))
                
    # Sort directions by angle
    directions.sort(key=lambda d: d[0])
    
    M = len(directions)
    c = []
    for angle, x, y in directions:
        # Number of points in this direction is floor(sqrt((r^2 - 1) / (x^2 + y^2)))
        limit = (r*r - 1) // (x*x + y*y)
        cnt = math.isqrt(limit)
        c.append(cnt)
        
    directions_2 = directions + [(angle + 2*math.pi, x, y) for angle, x, y in directions]
    c_2 = c + c
    
    total = 0
    right = 0
    curr_sum = 0
    curr_sum_sq = 0
    
    for i in range(M):
        target_angle = directions[i][0] + math.pi
        while right < 2*M and directions_2[right][0] < target_angle - 1e-9:
            curr_sum += c_2[right]
            curr_sum_sq += c_2[right]**2
            right += 1
            
        window_sum = curr_sum - c_2[i]
        window_sum_sq = curr_sum_sq - c_2[i]**2
        
        total += c[i] * (window_sum**2 - window_sum_sq)
        
        curr_sum -= c_2[i]
        curr_sum_sq -= c_2[i]**2
        
    return total // 6

if __name__ == "__main__":
    print(solve())
