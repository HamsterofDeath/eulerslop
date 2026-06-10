#!/usr/bin/env python3
import urllib.request

def solve():
    url = "https://projecteuler.net/project/resources/p107_network.txt"
    with urllib.request.urlopen(url) as f:
        data = f.read().decode("utf-8").strip().split("\n")
    
    n = len(data)
    edges = []
    total_weight = 0
    for i in range(n):
        row = data[i].strip().split(",")
        for j in range(i + 1, n):
            w = row[j].strip()
            if w != "-":
                w = int(w)
                edges.append((w, i, j))
                total_weight += w
    
    # Kruskal's MST
    parent = list(range(n))
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    
    def union(x, y):
        x, y = find(x), find(y)
        if x != y:
            parent[y] = x
            return True
        return False
    
    edges.sort()
    mst_weight = 0
    for w, u, v in edges:
        if union(u, v):
            mst_weight += w
    
    return total_weight - mst_weight

if __name__ == "__main__":
    print(solve())
