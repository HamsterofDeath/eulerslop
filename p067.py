#!/usr/bin/env python3
import urllib.request

def solve():
    url = "https://projecteuler.net/project/resources/p067_triangle.txt"
    with urllib.request.urlopen(url) as f:
        data = f.read().decode("utf-8")
    tri = [[int(n) for n in line.split()] for line in data.strip().split("\n")]
    for r in range(len(tri) - 2, -1, -1):
        for c in range(len(tri[r])):
            tri[r][c] += max(tri[r + 1][c], tri[r + 1][c + 1])
    return tri[0][0]

if __name__ == "__main__":
    print(solve())
