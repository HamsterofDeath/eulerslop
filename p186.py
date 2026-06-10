#!/usr/bin/env python3
"""p186: Connectedness of phone users

Find the number of successful calls after which 99% of the users (1,000,000 users)
are connected to the Prime Minister (PM = 524287).
Uses Union-Find (DSU) with path compression and union by size.
"""

class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n

    def find(self, i):
        path = []
        while self.parent[i] != i:
            path.append(i)
            i = self.parent[i]
        for node in path:
            self.parent[node] = i
        return i

    def union(self, i, j):
        root_i = self.find(i)
        root_j = self.find(j)
        if root_i != root_j:
            if self.size[root_i] < self.size[root_j]:
                root_i, root_j = root_j, root_i
            self.parent[root_j] = root_i
            self.size[root_i] += self.size[root_j]
            return True
        return False

def solve():
    # Lagged Fibonacci Generator history buffer for last 55 values
    S_history = [0] * 55
    
    def get_S(k):
        if k <= 55:
            val = (100003 - 200003 * k + 300007 * k**3) % 1000000
            S_history[(k - 1) % 55] = val
            return val
        else:
            val = (S_history[(k - 25) % 55] + S_history[(k - 56) % 55]) % 1000000
            S_history[(k - 1) % 55] = val
            return val

    dsu = DSU(1000000)
    pm = 524287
    
    successful_calls = 0
    k = 1
    
    while True:
        caller = get_S(k)
        called = get_S(k + 1)
        k += 2
        
        if caller == called:
            continue
            
        successful_calls += 1
        dsu.union(caller, called)
        
        pm_root = dsu.find(pm)
        if dsu.size[pm_root] >= 990000:
            return successful_calls

if __name__ == "__main__":
    print(solve())
