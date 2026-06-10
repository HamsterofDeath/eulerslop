#!/usr/bin/env python3
import numpy as np

# Protein folding in the 2D HP model, chain length N = 15.
#
# A folding is a self-avoiding walk (SAW) of N lattice points. An "H-H contact"
# is a pair of residues that are unit-distance neighbours on the lattice AND
# are both H. This includes consecutive residues (they are always adjacent),
# matching the statement's length-8 average 850/2^8 = 3.3203125.
#
# Because the lattice is bipartite, two residues i < j can be neighbours only
# when (j - i) is odd; so the only possible contact pairs are those 42 (for
# N=15) index pairs. Every SAW realises some subset of these pairs as actual
# contacts; we call that subset its "contact configuration".
#
# Plan:
#   1. Enumerate all SAWs (reduced by the 8-fold lattice symmetry, which leaves
#      contact configurations unchanged) and collect the set of distinct
#      contact configurations.
#   2. For each protein string (a 15-bit H/P mask, 2^15 of them) the score of a
#      configuration is the number of its pairs whose both endpoints are H; the
#      optimal folding picks the configuration maximising that score.
#   3. Average the optimum over all 2^15 proteins.
# Step 2/3 are vectorised: for each possible pair build an indicator vector over
# all masks, then each configuration's score vector is a subset-sum, and we keep
# the elementwise maximum.

N = 15
DIRS = [(1, 0), (-1, 0), (0, 1), (0, -1)]


def enumerate_configs():
    # Possible contact pairs (i, j), j - i odd.
    pairs = [(i, j) for i in range(N) for j in range(i + 1, N) if (j - i) % 2 == 1]
    configs = set()
    xs = [0] * N
    ys = [0] * N
    occ = {(0, 0): 0}

    def dfs(k, used_vertical):
        if k == N:
            c = 0
            for idx, (i, j) in enumerate(pairs):
                if abs(xs[i] - xs[j]) + abs(ys[i] - ys[j]) == 1:
                    c |= 1 << idx
            configs.add(c)
            return
        px, py = xs[k - 1], ys[k - 1]
        for di, (dx, dy) in enumerate(DIRS):
            # Symmetry reduction: fix first step East, and force the first
            # vertical move to be North (removes rotations + reflection).
            nuv = used_vertical
            if k == 1 and di != 0:
                continue
            if not used_vertical and di in (2, 3):
                if di == 3:
                    continue
                nuv = True
            nx, ny = px + dx, py + dy
            if (nx, ny) in occ:
                continue
            occ[(nx, ny)] = k
            xs[k] = nx
            ys[k] = ny
            dfs(k + 1, nuv)
            del occ[(nx, ny)]

    dfs(1, False)
    return pairs, configs


def solve():
    pairs, configs = enumerate_configs()
    M = 1 << N
    masks = np.arange(M, dtype=np.uint32)

    # B[k] = indicator over all proteins that both endpoints of pair k are H.
    B = np.empty((len(pairs), M), dtype=np.int16)
    for k, (i, j) in enumerate(pairs):
        B[k] = (((masks >> i) & 1) & ((masks >> j) & 1)).astype(np.int16)

    best = np.zeros(M, dtype=np.int16)
    for c in configs:
        idxs = [k for k in range(len(pairs)) if (c >> k) & 1]
        if not idxs:
            continue
        np.maximum(best, B[idxs].sum(axis=0), out=best)

    total = int(best.sum())
    # Exact rational average; printed with all needed decimals (a dyadic value).
    return repr(total / M)


if __name__ == "__main__":
    print(solve())
