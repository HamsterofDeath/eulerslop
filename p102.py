#!/usr/bin/env python3
import urllib.request

def contains_origin(ax, ay, bx, by, cx, cy):
    # Barycentric / sign of cross products
    # Point (0,0) is inside if signs of cross products all match
    d1 = ax * by - ay * bx
    d2 = bx * cy - by * cx
    d3 = cx * ay - cy * ax
    return (d1 > 0 and d2 > 0 and d3 > 0) or (d1 < 0 and d2 < 0 and d3 < 0)

def solve():
    url = "https://projecteuler.net/project/resources/p102_triangles.txt"
    with urllib.request.urlopen(url) as f:
        data = f.read().decode("utf-8").strip().split("\n")
    count = 0
    for line in data:
        x1, y1, x2, y2, x3, y3 = map(int, line.split(","))
        if contains_origin(x1, y1, x2, y2, x3, y3):
            count += 1
    return count

if __name__ == "__main__":
    print(solve())
