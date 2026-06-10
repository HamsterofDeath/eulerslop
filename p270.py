#!/usr/bin/env python3

def solve():
    # A final (uncuttable) piece must be a triangle: any piece with a boundary
    # lattice point that is not a polygon vertex, or with two non-adjacent
    # boundary points on different sides of the square, still admits a legal
    # cut.  Hence maximal cut configurations are exactly the triangulations of
    # the convex polygon formed by the 4N boundary lattice points, where a
    # diagonal is only allowed between two points NOT lying on a common side
    # of the square (same-side segments run along the border, never through
    # the interior).  Count those triangulations with the classic interval DP:
    #   G(i,j) = sum_k G(i,k) * G(k,j)   if edge (i,j) is usable, else 0.
    N = 30
    MOD = 10 ** 8
    m = 4 * N  # boundary lattice points, indexed cyclically from corner (0,0)

    # side membership by index: bottom [0,N], right [N,2N], top [2N,3N],
    # left [3N,4N-1] plus index 0 (corner (0,0) belongs to bottom and left).
    def same_side(i, j):
        if i <= N and j <= N:
            return True
        if N <= i <= 2 * N and N <= j <= 2 * N:
            return True
        if 2 * N <= i <= 3 * N and 2 * N <= j <= 3 * N:
            return True
        a = (i >= 3 * N) or (i == 0)
        b = (j >= 3 * N) or (j == 0)
        return a and b

    # allowed(i,j): boundary edge (adjacent points) or legal interior chord.
    def allowed(i, j):  # i < j
        if j == i + 1 or (i == 0 and j == m - 1):
            return True
        return not same_side(i, j)

    # G[i][j]: triangulation count of sub-polygon i..j assuming edge (i,j).
    G = [[0] * m for _ in range(m)]
    for i in range(m - 1):
        G[i][i + 1] = 1
    for span in range(2, m):
        for i in range(m - span):
            j = i + span
            if not allowed(i, j):
                continue
            Gi = G[i]
            s = 0
            for k in range(i + 1, j):
                gik = Gi[k]
                if gik:
                    s += gik * G[k][j]
            Gi[j] = s % MOD
    return G[0][m - 1]

if __name__ == "__main__":
    print(solve())
