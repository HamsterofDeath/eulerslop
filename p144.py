#!/usr/bin/env python3
"""p144: Count laser beam reflections in ellipse 4x^2+y^2=100 before exiting."""
from math import sqrt

def solve():
    # Ellipse: 4x^2 + y^2 = 100
    # Tangent slope at (x,y): m = -4x/y
    # Normal: n = (4x, y)  (since tangent is (-y, 4x) or something...)
    # Normal vector: (4x, y) (gradient of F = 4x^2+y^2)
    
    x, y = 0.0, 10.1  # start point
    x1, y1 = 1.4, -9.6  # first hit
    
    # Direction from start to first hit
    dx = x1 - x
    dy = y1 - y
    
    count = 0
    px, py = x1, y1
    
    while True:
        # Reflect
        # Normal at (px,py): grad = (8px, 2py) or (4px, py)? 
        # For ellipse 4x^2+y^2=100, gradient is (8x, 2y), but tangent slope = -4x/y.
        # Normal direction: (4x, y) is perpendicular to tangent.
        nx, ny = 4 * px, py
        nlen = sqrt(nx*nx + ny*ny)
        nx /= nlen
        ny /= nlen
        
        # Reflect: v' = v - 2(v·n)n
        dot = dx * nx + dy * ny
        rx = dx - 2 * dot * nx
        ry = dy - 2 * dot * ny
        
        # Find intersection of ray from (px,py) in direction (rx,ry) with ellipse
        # Param: (px + t*rx, py + t*ry) satisfies 4x^2+y^2=100
        # 4(px+t*rx)^2 + (py+t*ry)^2 = 100
        # 4px^2 + 8px*rx*t + 4rx^2*t^2 + py^2 + 2py*ry*t + ry^2*t^2 = 100
        # (4rx^2+ry^2)*t^2 + (8px*rx+2py*ry)*t + (4px^2+py^2-100) = 0
        # Since (px,py) is on ellipse: 4px^2+py^2 = 100, so constant term = 0
        # t * [(4rx^2+ry^2)*t + (8px*rx+2py*ry)] = 0
        # t=0 (current point) or t = -(8px*rx+2py*ry)/(4rx^2+ry^2)
        
        # But we want the OTHER intersection (next reflection point)
        a = 4*rx*rx + ry*ry
        b = 8*px*rx + 2*py*ry
        t = -b / a
        
        px += t * rx
        py += t * ry
        
        count += 1
        
        # Exit check: -0.01 <= x <= 0.01 and y > 0
        if -0.01 <= px <= 0.01 and py > 0:
            break
        
        dx, dy = rx, ry
    
    return count

if __name__ == "__main__":
    print(solve())
