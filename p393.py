#!/usr/bin/env python3

def count(n):
    # A valid migration is a permutation of the n*n cells where each cell maps
    # to an orthogonal neighbour (everyone moves, in-degree = out-degree = 1)
    # and no grid edge is used by two ants.  Two ants on the same edge can only
    # happen head-on (a 2-cycle), so each edge is in one of 3 states: unused,
    # or an arrow in one of its two directions.  We count these directed
    # configurations with a broken-profile DP, sweeping cell by cell in
    # column-major order.
    #
    # Profile when about to process cell (r, c):
    #   h[i], i >= r : state of the horizontal edge (i, c-1)-(i, c)
    #   h[i], i <  r : state of the horizontal edge (i, c)-(i, c+1)
    #   v            : state of the vertical edge (r-1, c)-(r, c)
    # Horizontal edge codes: 0 unused, 1 rightward, 2 leftward.
    # Vertical edge codes:   0 unused, 1 downward,  2 upward.
    # Processing (r, c) consumes its left edge h[r] and top edge v, chooses its
    # right edge R and bottom edge B, and enforces exactly one incoming and one
    # outgoing arrow among the four incident edges.  Border edges are pinned
    # to 0 (state starts all-zero, and R/B are forced to 0 on the last
    # column/row), which also makes "no edge" behave as "unused".
    from collections import defaultdict

    p3n = 3 ** n
    dp = {0: 1}
    for c in range(n):
        last_col = (c == n - 1)
        for r in range(n):
            p3r = 3 ** r
            Rs = (0,) if last_col else (0, 1, 2)
            Bs = (0,) if r == n - 1 else (0, 1, 2)
            ndp = defaultdict(int)
            for state, cnt in dp.items():
                L = (state // p3r) % 3   # left edge: 1 = in, 2 = out
                T = state // p3n         # top edge:  1 = in, 2 = out
                base = state - L * p3r - T * p3n
                ins = (L == 1) + (T == 1)
                outs = (L == 2) + (T == 2)
                if ins > 1 or outs > 1:
                    continue
                for R in Rs:             # right edge: 1 = out, 2 = in
                    i1 = ins + (R == 2)
                    o1 = outs + (R == 1)
                    if i1 > 1 or o1 > 1:
                        continue
                    for B in Bs:         # bottom edge: 1 = out, 2 = in
                        if i1 + (B == 2) == 1 and o1 + (B == 1) == 1:
                            ndp[base + R * p3r + B * p3n] += cnt
            dp = ndp
    # all frontier edges must end unused
    return dp.get(0, 0)

def solve():
    assert count(4) == 88  # given check value f(4) = 88
    return count(10)

if __name__ == "__main__":
    print(solve())
