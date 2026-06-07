#!/usr/bin/env python3

def solve():
    # Number of rectangles in a grid of size w x h is w(w+1)h(h+1)/4
    target = 2_000_000
    best_diff = float('inf')
    best_area = 0
    for w in range(1, 2000):
        for h in range(1, w + 1):
            rects = w * (w + 1) * h * (h + 1) // 4
            diff = abs(rects - target)
            if diff < best_diff:
                best_diff = diff
                best_area = w * h
            if rects > target:
                break
    return best_area

if __name__ == "__main__":
    print(solve())
