#!/usr/bin/env python3
def solve():
    limit = 1000000
    
    # mdrs[i] initialized with the digital root of i
    # dr(i) = (i - 1) % 9 + 1
    mdrs = [0] * limit
    for i in range(2, limit):
        mdrs[i] = (i - 1) % 9 + 1
        
    for i in range(2, int(limit**0.5) + 1):
        val = mdrs[i]
        # j >= i to avoid double-counting pairs (i, j)
        for j in range(i, (limit - 1) // i + 1):
            prod = i * j
            alt = val + mdrs[j]
            if alt > mdrs[prod]:
                mdrs[prod] = alt
                
    print(sum(mdrs[2:]))

if __name__ == "__main__":
    solve()
