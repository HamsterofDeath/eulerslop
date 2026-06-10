#!/usr/bin/env python3

def solve():
    target = 12
    L_values = []
    
    # Generate from seed (4,2) - only family with even v
    u, v = 4, 2
    while len(L_values) < target:
        # Process current (u,v)
        if v % 2 == 0:
            L = v // 2
            if u >= 4 and (u - 4) % 5 == 0:
                b = (u - 4) // 5
                if b > 0:
                    L_values.append(L)
            elif (u + 4) % 5 == 0:
                b = (u + 4) // 5
                if b > 0:
                    L_values.append(L)
        # Next
        u, v = 9 * u + 20 * v, 4 * u + 9 * v
    
    return sum(L_values[:target])

if __name__ == "__main__":
    print(solve())
