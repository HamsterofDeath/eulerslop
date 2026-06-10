#!/usr/bin/env python3
from math import log2, ceil

def min_multiplications(target):
    best = 20
    
    def dfs(chain):
        nonlocal best
        depth = len(chain) - 1
        last = chain[-1]
        
        lb = depth + ceil(log2(target / last))
        if lb >= best:
            return
            
        if last == target:
            best = depth
            return
            
        # Star chain restriction: nxt must be last + chain[j]
        # Iterate in reverse to try larger additions first
        for j in range(len(chain) - 1, -1, -1):
            nxt = last + chain[j]
            if nxt > target:
                continue
            dfs(chain + [nxt])
            
    dfs([1])
    return best

def solve():
    total = 0
    for k in range(1, 201):
        total += min_multiplications(k)
    return total

if __name__ == "__main__":
    print(solve())
