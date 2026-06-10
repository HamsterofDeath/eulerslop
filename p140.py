#!/usr/bin/env python3

def solve():
    target = 30
    nuggets = []
    
    # Find fundamental seeds for u^2 - 5v^2 = 44 with u > 0, v > 0
    seeds = []
    for u in range(1, 100):
        for v in range(1, 50):
            if u*u - 5*v*v == 44:
                seeds.append((u, v))
    
    for u0, v0 in seeds:
        u, v = u0, v0
        while u > 0 and u < 10**15:
            if u >= 7 and (u - 7) % 5 == 0:
                n = (u - 7) // 5
                if n > 0:
                    nuggets.append(n)
            u, v = 9*u + 20*v, 4*u + 9*v
    
    nuggets = sorted(set(nuggets))
    return sum(nuggets[:target])

if __name__ == "__main__":
    print(solve())
