#!/usr/bin/env python3
"""Project Euler 213: Flea Circus.

A 30x30 grid holds 900 fleas, one per square. Each bell ring, every flea
jumps to a uniformly random adjacent square (orthogonal). Find the expected
number of unoccupied squares after 50 rings, rounded to six decimal places.

Fleas move independently, so for each starting square we evolve that flea's
probability distribution for 50 steps (vectorized over all 900 starts with
numpy). A square is empty iff no flea is on it, so by independence
P(square empty) = prod over fleas of (1 - p_flea(square)), and the expected
count of empty squares is the sum of these probabilities.
"""

import numpy as np

N = 30
RINGS = 50


def solve():
    # Reciprocal of each square's degree (number of orthogonal neighbours).
    deg = np.full((N, N), 4.0)
    deg[0, :] -= 1
    deg[-1, :] -= 1
    deg[:, 0] -= 1
    deg[:, -1] -= 1
    inv_deg = 1.0 / deg

    # One distribution per starting square: shape (900, 30, 30).
    dist = np.zeros((N * N, N, N))
    idx = np.arange(N * N)
    dist[idx, idx // N, idx % N] = 1.0

    for _ in range(RINGS):
        w = dist * inv_deg  # mass leaving each square, split per neighbour
        new = np.zeros_like(dist)
        new[:, 1:, :] += w[:, :-1, :]
        new[:, :-1, :] += w[:, 1:, :]
        new[:, :, 1:] += w[:, :, :-1]
        new[:, :, :-1] += w[:, :, 1:]
        dist = new

    # Expected empty squares: sum over squares of prod over fleas (1 - p).
    empty_prob = np.prod(1.0 - dist, axis=0)
    return f"{empty_prob.sum():.6f}"


if __name__ == "__main__":
    print(solve())
