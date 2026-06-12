#!/usr/bin/env python3
import numpy as np

MOD = 1_000_000_033
N = 100


def solve():
    # Bolker-Crapo: a braced m x n grid is rigid iff the bipartite "brace
    # graph" (left vertices = rows, right vertices = columns, an edge (i,j)
    # for each braced cell) is connected.  So R(m,n) counts edge subsets of
    # K_{m,n} forming a connected spanning subgraph.  Standard recurrence:
    # subtract, over the component containing row 1 spanning i rows and j
    # columns (not all of them),
    #   R(m,n) = 2^(mn) - sum_{(i,j)!=(m,n)} binom(m-1,i-1) binom(n,j)
    #                       R(i,j) 2^((m-i)(n-j)),
    # where R(1,0)=1 (isolated row vertex) and R(i,0)=0 for i>1.
    # The inner double sum is vectorised with numpy (int64; each product of
    # two residues < MOD^2 < 2^63).

    # Binomials and powers of 2 mod MOD.
    binom = np.zeros((N + 1, N + 1), dtype=np.int64)
    binom[:, 0] = 1
    for a in range(1, N + 1):
        binom[a, 1:a + 1] = (binom[a - 1, 0:a] + binom[a - 1, 1:a + 1]) % MOD
    pow2 = np.ones(N * N + 1, dtype=np.int64)
    for e in range(1, N * N + 1):
        pow2[e] = pow2[e - 1] * 2 % MOD

    C = np.zeros((N + 1, N + 1), dtype=np.int64)
    C[1, 0] = 1
    for m in range(1, N + 1):
        bi = binom[m - 1, 0:m]            # binom(m-1, i-1), i = 1..m
        rows = np.arange(m - 1, -1, -1)   # m - i,            i = 1..m
        for n in range(1, N + 1):
            bj = binom[n, 0:n + 1]        # binom(n, j),      j = 0..n
            cols = np.arange(n, -1, -1)   # n - j
            term = bi[:, None] * bj[None, :] % MOD
            term = term * C[1:m + 1, 0:n + 1] % MOD
            term = term * pow2[np.outer(rows, cols)] % MOD
            # The (i,j)=(m,n) entry contributes 0 since C[m,n] is still 0.
            s = int(term.sum()) % MOD     # <= 101*101 residues: fits int64
            C[m, n] = (pow2[m * n] - s) % MOD

    return int(C[1:, 1:].sum()) % MOD


if __name__ == "__main__":
    print(solve())
