#!/usr/bin/env python3
import urllib.request
import heapq

def solve():
    url = "https://projecteuler.net/project/resources/p083_matrix.txt"
    with urllib.request.urlopen(url) as f:
        data = f.read().decode("utf-8")
    grid = [[int(n) for n in line.split(",")] for line in data.strip().split("\n")]
    size = len(grid)

    dist = [[float('inf')] * size for _ in range(size)]
    dist[0][0] = grid[0][0]
    pq = [(grid[0][0], 0, 0)]
    dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    while pq:
        d, r, c = heapq.heappop(pq)
        if d > dist[r][c]:
            continue
        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            if 0 <= nr < size and 0 <= nc < size:
                nd = d + grid[nr][nc]
                if nd < dist[nr][nc]:
                    dist[nr][nc] = nd
                    heapq.heappush(pq, (nd, nr, nc))
    return dist[size - 1][size - 1]

if __name__ == "__main__":
    print(solve())
