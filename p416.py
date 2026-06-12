#!/usr/bin/env python3
import numpy as np
from math import comb

MOD = 10**9


def build_matrix(m):
    # Unfold the m round trips: each trip = outward path + (reversed) homeward
    # path, both increasing paths 1 -> n with steps in {1,2,3}.  A path is
    # determined by its visited set, so F(m,n) counts 2m-tuples of such paths
    # whose union misses at most one square.
    #
    # Sweep columns left to right.  After processing column i each of the
    # P = 2m paths has its last visited square at i, i-1 or i-2 (offset 0/1/2;
    # offset 2 must visit column i+1 since the max jump is 3).  Paths are
    # exchangeable, so the state is (c0, c1, c2) = counts per offset, plus a
    # flag marking whether the single allowed unvisited column was used.
    P = 2 * m
    index = {}
    for c0 in range(P + 1):
        for c1 in range(P + 1 - c0):
            for flag in (0, 1):
                index[(c0, c1, P - c0 - c1, flag)] = len(index)
    S = len(index)
    M = np.zeros((S, S), dtype=np.int64)
    for (c0, c1, c2, flag), i in index.items():
        # k0 of the offset-0 paths and k1 of the offset-1 paths visit the
        # next column; all offset-2 paths must.
        for k0 in range(c0 + 1):
            for k1 in range(c1 + 1):
                w = comb(c0, k0) * comb(c1, k1)
                ns = (k0 + k1 + c2, c0 - k0, c1 - k1)
                if k0 + k1 + c2 > 0:
                    M[i, index[ns + (flag,)]] += w
                elif flag == 0:  # column unvisited (forces c2 == 0): burn flag
                    M[i, index[ns + (1,)]] += w
    return M % MOD, index


def matmul_mod(A, B):
    # Exact int64 matmul mod 1e9 via 15-bit limb splitting + float64 BLAS:
    # all partial products stay below 2^53.
    a1 = (A >> 15).astype(np.float64)
    a0 = (A & 32767).astype(np.float64)
    b1 = (B >> 15).astype(np.float64)
    b0 = (B & 32767).astype(np.float64)
    hh = (a1 @ b1).astype(np.int64) % MOD
    hl = (a1 @ b0 + a0 @ b1).astype(np.int64) % MOD
    ll = (a0 @ b0).astype(np.int64) % MOD
    return (hh * ((1 << 30) % MOD) + (hl << 15) + ll) % MOD


def F(m, n):
    M, index = build_matrix(m)
    R = np.identity(len(index), dtype=np.int64)
    e = n - 2  # columns 2..n-1; column 1 is the start, column n absorbs all
    while e:
        if e & 1:
            R = matmul_mod(R, M)
        M = matmul_mod(M, M)
        e >>= 1
    # Start: all 2m paths sit on column 1.  End: every state jumps into
    # column n in exactly one way, both flag values allowed -> sum the row.
    return int(R[index[(2 * m, 0, 0, 0)]].sum() % MOD)


def solve():
    return F(10, 10**12)


if __name__ == "__main__":
    print(solve())
