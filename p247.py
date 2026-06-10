#!/usr/bin/env python3
"""Project Euler 247: Squares Under a Hyperbola.

Squares are inscribed greedily under y = 1/x (x >= 1, 0 <= y <= 1/x).
Each square placed in a region with lower-left corner (x, y) has side s
solving (x + s)(y + s) = 1, and spawns two new regions: one to its right
(index left+1) and one above (index below+1). The square inherits the
region's index (left, below). We pop regions in decreasing order of the
side of the square they contain; the k-th pop is square S_k. There are
C(6,3) = 20 squares with index (3,3); the answer is the rank n of the
last one encountered in size order.
"""
import heapq
from math import sqrt


def largest_side(x, y):
    # side s of largest square with lower-left corner (x, y) under 1/x:
    # (x + s)(y + s) = 1  =>  s = (-(x+y) + sqrt((x-y)^2 + 4)) / 2
    return (sqrt((x - y) * (x - y) + 4.0) - (x + y)) / 2.0


def solve():
    target = (3, 3)
    total_targets = 20  # C(6,3) regions have index (3,3)
    found = 0
    answer = 0

    # heap entries: (-side, x, y, left, below)
    x0, y0 = 1.0, 0.0
    heap = [(-largest_side(x0, y0), x0, y0, 0, 0)]
    n = 0
    while heap and found < total_targets:
        neg_s, x, y, left, below = heapq.heappop(heap)
        s = -neg_s
        n += 1
        if (left, below) == target:
            found += 1
            answer = n
        # Children regions: right (x+s, y) and top (x, y+s). Every region
        # must stay in play because n ranks ALL squares by size.
        heapq.heappush(heap, (-largest_side(x + s, y), x + s, y, left + 1, below))
        heapq.heappush(heap, (-largest_side(x, y + s), x, y + s, left, below + 1))
    return answer


if __name__ == "__main__":
    print(solve())
