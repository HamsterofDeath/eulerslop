#!/usr/bin/env python3
"""p143: Sum of distinct p+q+r ≤ 120000 for Torricelli triangles.
a^2 = q^2+r^2+qr, b^2 = r^2+p^2+rp, c^2 = p^2+q^2+pq."""
from math import isqrt, gcd

def solve():
    limit = 120000
    
    # Generate all Eisenstein pairs (u,v) with u^2+uv+v^2 a square
    # Parametrization: u=m^2-n^2, v=2mn+n^2, c=m^2+mn+n^2
    adj = {i: [] for i in range(limit)}
    eis_set = set()
    
    for m in range(2, int(limit**0.5) + 2):
        for n in range(1, m):
            if gcd(m, n) != 1:
                continue
            if (m - n) % 3 == 0:
                continue
            u = m*m - n*n
            v = 2*m*n + n*n
            if u <= 0 or v <= 0:
                continue
            if u + v >= limit:
                continue
            # Add all multiples
            k = 1
            while k * (u + v) < limit:
                a, b = k*u, k*v
                if a + b < limit:
                    adj[a].append(b)
                    adj[b].append(a)
                    eis_set.add((a, b))
                    eis_set.add((b, a))
                k += 1
    
    # For each r, find pairs (p,q) in adj[r] that are also Eisenstein
    seen_sums = set()
    for r in range(1, limit):
        neighbors = adj.get(r, [])
        ln = len(neighbors)
        for i in range(ln):
            p = neighbors[i]
            for j in range(i, ln):
                q = neighbors[j]
                if (p, q) in eis_set:
                    s = p + q + r
                    if s <= limit:
                        seen_sums.add(s)
    
    return sum(seen_sums)

if __name__ == "__main__":
    print(solve())
