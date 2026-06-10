#!/usr/bin/env python3

def solve():
    limit = 1_000_000_000
    # Almost equilateral triangles (a, a, a+-1).
    # With c = a+1: integer area requires 4a^2-(a+1)^2 = d^2,
    #   i.e. (3a-1)^2 - 3d^2 = 4.
    # With c = a-1: 4a^2-(a-1)^2 = d^2, i.e. (3a+1)^2 - 3d^2 = 4.
    # So iterate X^2 - 3Y^2 = 4 (X: 2, 4, 14, 52, ... X_n = 4X_{n-1} - X_{n-2}).
    # If X = 3a-1 (X % 3 == 2): perimeter 3a+1 = X+2.
    # If X = 3a+1 (X % 3 == 1): perimeter 3a-1 = X-2.
    total = 0
    x0, x1 = 2, 4
    while True:
        x0, x1 = x1, 4 * x1 - x0
        if x1 % 3 == 2:
            a, perim = (x1 + 1) // 3, x1 + 2
        elif x1 % 3 == 1:
            a, perim = (x1 - 1) // 3, x1 - 2
        else:
            continue
        if perim > limit:
            break
        if a > 2:
            total += perim
    return total

if __name__ == "__main__":
    print(solve())
