#!/usr/bin/env python3
import numpy as np

# Three-pile game; a move removes N>0 stones from one, two or three piles
# (same N from each chosen pile).  Find sum of (x+y+z) over losing positions
# with x <= y <= z <= 1000.
#
# Process sorted positions (x,y,z) in lexicographic order of (z,y,x); every
# position reachable from (x,y,z) by a move is, as a sorted multiset, strictly
# earlier in this order.  A position is losing iff no move reaches a losing
# position.  Each losing position L = (a,b,c) "kills" exactly the positions
# that contain, as a sub-multiset invariant:
#   - one of its pairs (a,b), (a,c), (b,c) with a larger third pile
#     (single-pile move), tracked in P[u][v];
#   - one pile value plus the difference of the other two: (a, c-b),
#     (b, c-a), (c, b-a) (two-pile move), tracked in D[pile][diff];
#   - both differences (b-a, c-b) (three-pile move), tracked in T[d1][d2].
# The seven marks a position would set are exactly the seven marks that must
# all be clear for it to be losing.  Within a fixed (y,z) row only the P[y][z]
# mark couples different x, so the smallest unmarked x (if any) is the unique
# losing x of the row; the inner x-scan is vectorised with numpy.

N = 1000


def solve():
    P = np.zeros((N + 1, N + 1), dtype=bool)   # P[u][v], u <= v: pair of piles
    D = np.zeros((N + 1, N + 1), dtype=bool)   # D[pile][difference]
    T = np.zeros((N + 1, N + 1), dtype=bool)   # T[diff1][diff2]
    total = 0
    for z in range(N + 1):
        Pz = P[:, z]
        Dz = D[z]
        for y in range(z + 1):
            if P[y, z]:
                continue
            m = y + 1
            # mask[x] = True  =>  (x,y,z) is winning
            mask = P[:m, y] | Pz[:m]
            mask |= D[:m, z - y]                  # reduce y,z together
            mask |= D[y, z - y:z + 1][::-1]       # reduce x,z together
            mask |= Dz[:m][::-1]                  # reduce x,y together
            mask |= T[:m, z - y][::-1]            # reduce all three
            x = int(np.argmin(mask))              # first False, if any
            if mask[x]:
                continue                          # row fully winning
            total += x + y + z
            P[x, y] = P[x, z] = P[y, z] = True
            D[x, z - y] = D[y, z - x] = D[z, y - x] = True
            T[y - x, z - y] = True
    return total


if __name__ == "__main__":
    print(solve())
