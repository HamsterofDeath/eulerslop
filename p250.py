#!/usr/bin/env python3
import numpy as np

def solve():
    MOD = 10 ** 16
    N = 250250
    P = 250

    # Count how many of 1^1, 2^2, ..., N^N fall into each residue class mod 250.
    counts = [0] * P
    for i in range(1, N + 1):
        counts[pow(i, i, P)] += 1

    # Subset-sum DP over residues mod 250.
    # ways[m] = number of subsets (so far) whose sum is congruent to m (mod 250),
    # counted modulo 10^16 (only the rightmost 16 digits are needed).
    ways = np.zeros(P, dtype=np.int64)
    ways[0] = 1

    # Adding an item with residue r: ways_new[m] = ways[m] + ways[(m - r) mod 250],
    # which is a cyclic shift (np.roll) plus an addition.
    # Values stay below 10^16, so a single sum < 2*10^16 fits safely in int64.
    for r in range(1, P):
        for _ in range(counts[r]):
            ways = (ways + np.roll(ways, r)) % MOD

    total = int(ways[0])
    # Items with residue 0 are free choices: each doubles every subset count.
    total = total * pow(2, counts[0], MOD) % MOD
    # Exclude the empty subset.
    return (total - 1) % MOD

if __name__ == "__main__":
    print(solve())
