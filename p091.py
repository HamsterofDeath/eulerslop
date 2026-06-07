#!/usr/bin/env python3

def solve():
    limit = 50
    triangles = set()
    for x1 in range(limit + 1):
        for y1 in range(limit + 1):
            if x1 == 0 and y1 == 0:
                continue
            for x2 in range(limit + 1):
                for y2 in range(limit + 1):
                    if x2 == 0 and y2 == 0:
                        continue
                    if x1 == x2 and y1 == y2:
                        continue
                    at_O = x1 * x2 + y1 * y2 == 0
                    at_P = x1 * (x1 - x2) + y1 * (y1 - y2) == 0
                    at_Q = x2 * (x2 - x1) + y2 * (y2 - y1) == 0
                    if at_O or at_P or at_Q:
                        if (x1 < x2) or (x1 == x2 and y1 < y2):
                            triangles.add((x1, y1, x2, y2))
                        else:
                            triangles.add((x2, y2, x1, y1))
    return len(triangles)

if __name__ == "__main__":
    print(solve())
