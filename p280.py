#!/usr/bin/env python3
import numpy as np

def solve():
    # Markov chain on states (ant position, bottom-row seed bitmask B,
    # top-row filled bitmask T, carrying flag c), with |B| + |T| + c = 5.
    # Pick-up / drop happens on ARRIVAL at a square, so within a "phase"
    # (B, T, c) the trigger squares are not valid positions. Every phase
    # transition strictly increases the potential 2*|T| + c, so phases form
    # a DAG and can be solved one 25x25 linear system at a time, in
    # decreasing potential order, with numpy.
    #
    # E[state] = 1 + average of E[successor states]; the walk ends when the
    # 5th seed is dropped.
    W = 5
    cells = W * W
    bottom = list(range(0, W))            # row 0 (seeds start here)
    top = list(range(cells - W, cells))   # row 4 (seeds dropped here)

    neigh = [[] for _ in range(cells)]
    for r in range(W):
        for col in range(W):
            i = r * W + col
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nr, nc = r + dr, col + dc
                if 0 <= nr < W and 0 <= nc < W:
                    neigh[i].append(nr * W + nc)

    def popcount(x):
        return bin(x).count("1")

    # Enumerate all phases (B, T, c) with |B| + |T| + c = 5.
    phases = []
    for B in range(32):
        for T in range(32):
            for c in (0, 1):
                if popcount(B) + popcount(T) + c == 5:
                    phases.append((B, T, c))
    phases.sort(key=lambda p: 2 * popcount(p[1]) + p[2], reverse=True)

    E = {}  # (B, T, c) -> length-25 array of expected steps (nan = invalid)
    for B, T, c in phases:
        # Valid positions: triggers would have fired on arrival.
        if c == 0:
            invalid = {bottom[j] for j in range(W) if B >> j & 1}
        else:
            invalid = {top[j] for j in range(W) if not (T >> j & 1)}
        valid = [p for p in range(cells) if p not in invalid]
        idx = {p: i for i, p in enumerate(valid)}
        n = len(valid)
        A = np.eye(n)
        rhs = np.ones(n)
        for p in valid:
            i = idx[p]
            w = 1.0 / len(neigh[p])
            for q in neigh[p]:
                col = q % W
                if c == 0 and q < W and (B >> col & 1):
                    # pick up the seed at bottom column `col`
                    rhs[i] += w * E[(B & ~(1 << col), T, 1)][q]
                elif c == 1 and q >= cells - W and not (T >> col & 1):
                    if popcount(T) == 4:
                        pass  # last seed dropped: walk ends, E = 0
                    else:
                        rhs[i] += w * E[(B, T | (1 << col), 0)][q]
                else:
                    A[i, idx[q]] -= w
        sol = np.linalg.solve(A, rhs)
        full = np.full(cells, np.nan)
        full[valid] = sol
        E[(B, T, c)] = full

    center = (W // 2) * W + W // 2
    ans = E[(31, 0, 0)][center]
    return f"{ans:.6f}"

if __name__ == "__main__":
    print(solve())
