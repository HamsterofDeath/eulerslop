#!/usr/bin/env python3
import numpy as np

# Larry and Robin's memory game.
#
# Joint Markov chain over both players' memories, with the called numbers
# (1..10) being exchangeable: a state only needs the *pattern* of the two
# memories, so we canonicalize labels by first appearance.
#   L = Larry's memory, most recently called first (he evicts the least
#       recently called number; a hit refreshes recency).
#   R = Robin's memory, oldest first (he evicts the longest-stored number;
#       a hit does not change anything).
# For each canonical state we keep the full probability distribution of the
# score difference D = Larry - Robin (a vector over D in [-50, 50]), since a
# call gives Larry +1, Robin +1, both +1 or nothing, shifting D by +-1 or 0.
# Only ~1.5k canonical memory states exist, so 50 exact steps are cheap.

TURNS = 50
NUMS = 10
MEM = 5


def canon(L, R):
    # Relabel by order of first appearance scanning L then R.
    relab = {}
    for x in L + R:
        if x not in relab:
            relab[x] = len(relab)
    return tuple(relab[x] for x in L), tuple(relab[x] for x in R)


def step(states):
    new = {}
    for (L, R), vec in states.items():
        union = sorted(set(L) | set(R))
        u = len(union)
        # candidate called numbers: each known label (prob 1/10) plus a
        # single "fresh number" event with prob (10-u)/10.
        cands = [(x, 1.0) for x in union]
        if u < NUMS:
            cands.append((u, float(NUMS - u)))  # fresh label = u
        for x, w in cands:
            p = w / NUMS
            if x in L:
                dL = 1
                nL = (x,) + tuple(y for y in L if y != x)
            else:
                dL = 0
                nL = ((x,) + L)[:MEM]
            if x in R:
                dR = 1
                nR = R
            else:
                dR = 0
                nR = (R + (x,)) if len(R) < MEM else (R[1:] + (x,))
            key = canon(nL, nR)
            tgt = new.get(key)
            if tgt is None:
                tgt = new[key] = np.zeros(2 * TURNS + 1)
            d = dL - dR
            if d == 0:
                tgt += p * vec
            elif d == 1:
                tgt[1:] += p * vec[:-1]
            else:
                tgt[:-1] += p * vec[1:]
    return new


def expected_abs(turns):
    vec0 = np.zeros(2 * TURNS + 1)
    vec0[TURNS] = 1.0  # D = 0
    states = {((), ()): vec0}
    for _ in range(turns):
        states = step(states)
    absd = np.abs(np.arange(-TURNS, TURNS + 1))
    return sum(float(v @ absd) for v in states.values())


def solve():
    return "%.8f" % expected_abs(TURNS)


if __name__ == "__main__":
    print(solve())
