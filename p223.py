#!/usr/bin/env python3
import numpy as np

# Solutions of a^2 + b^2 - c^2 = 1 form a forest under the three Barning/Hall
# matrices (the same ones that generate the Pythagorean triple tree):
#   A: (a,b,c) -> ( a - 2b + 2c,  2a - b + 2c,  2a - 2b + 3c)
#   B: (a,b,c) -> ( a + 2b + 2c,  2a + b + 2c,  2a + 2b + 3c)
#   C: (a,b,c) -> (-a + 2b + 2c, -2a + b + 2c, -2a + 2b + 3c)
# Every ordered solution (a,b,c) with a,b >= 1 appears exactly once in the
# forest rooted at (1,1,1), (1,2,2) and (2,1,2).
#
# The swap map M(a,b,c) = (b,a,c) satisfies M A = C M and M B = B M, so
# tree(2,1,2) is the mirror of tree(1,2,2), and inside tree(1,1,1) the
# B-chain (1,1,1) -> (5,5,7) -> (29,29,41) -> ... (the a=b Pell solutions)
# is fixed by M while the A- and C-subtrees hanging off that chain are
# mirrors of each other.  Hence, with
#   E   = number of a=b solutions (Pell chain) with perimeter <= L,
#   S   = total nodes in the subtrees rooted at A(p) for Pell nodes p,
#   T   = total nodes in tree(1,2,2),
# the number of unordered solutions a <= b is  E + S + T.
#
# The only slow chains (perimeter step +4) are the a=1 solutions (1,b,b),
# which exist for every b (1 + b^2 = b^2 + 1).  They form two A-chains
# (odd b from (1,1,1), even b from (1,2,2)), so they are counted in closed
# form and only their B/C children are fed back into the BFS.


def count(limit):
    # a = b solutions: 2a^2 = c^2 + 1 (Pell chain, advanced by matrix B)
    pell = []
    x, c = 1, 1
    while 2 * x + c <= limit:
        pell.append((x, c))
        x, c = 3 * x + 2 * c, 4 * x + 3 * c
    total = len(pell)

    # a = 1 solutions (1,b,b), b >= 2 (b = 1 is the Pell node (1,1,1))
    bmax = (limit - 1) // 2
    total += max(bmax - 1, 0)

    # BFS seeds: the (1,b,b) nodes that can still produce children
    # (B child perimeter 12b+5, C child perimeter 12b-5), plus the
    # A-children of the Pell nodes (x,x,c), x > 1: A = (2c-x, x+2c, 3c).
    bseed = min(bmax, (limit + 5) // 12)
    if bseed >= 2:
        b0 = np.arange(2, bseed + 1, dtype=np.int64)
        a0 = np.ones_like(b0)
        c0 = b0.copy()
    else:
        a0 = b0 = c0 = np.empty(0, dtype=np.int64)

    sa, sb, sc = [], [], []
    for x, cc in pell[1:]:
        if 7 * cc <= limit:
            sa.append(2 * cc - x)
            sb.append(x + 2 * cc)
            sc.append(3 * cc)
    pa = np.asarray(sa, dtype=np.int64)
    pb = np.asarray(sb, dtype=np.int64)
    pc = np.asarray(sc, dtype=np.int64)
    total += pa.size

    a = np.concatenate([a0, pa])
    b = np.concatenate([b0, pb])
    c = np.concatenate([c0, pc])

    while a.size:
        parts = []
        # A children only for a != 1 (the a = 1 chain is counted above)
        m = a != 1
        am, bm, cm = a[m], b[m], c[m]
        na = am - 2 * bm + 2 * cm
        nb = 2 * am - bm + 2 * cm
        nc = 2 * am - 2 * bm + 3 * cm
        keep = na + nb + nc <= limit
        parts.append((na[keep], nb[keep], nc[keep]))

        for s in (1, -1):  # B and C
            na = s * a + 2 * b + 2 * c
            nb = 2 * s * a + b + 2 * c
            nc = 2 * s * a + 2 * b + 3 * c
            keep = na + nb + nc <= limit
            parts.append((na[keep], nb[keep], nc[keep]))

        a = np.concatenate([p[0] for p in parts])
        b = np.concatenate([p[1] for p in parts])
        c = np.concatenate([p[2] for p in parts])
        total += a.size

    return total


def solve():
    return count(25_000_000)


if __name__ == "__main__":
    print(solve())
