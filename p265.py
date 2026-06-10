#!/usr/bin/env python3
# Project Euler 265: Binary Circles
#
# We need all binary de Bruijn sequences B(2, 5): circular arrangements of
# 2^5 = 32 bits in which every 5-bit clockwise window is distinct (hence each
# of the 32 possible 5-bit strings appears exactly once).
#
# Fixing the rotation so the sequence starts with the all-zero window 00000,
# we do a depth-first search over the remaining 27 bits, tracking which 5-bit
# windows have been used.  After placing the last bit we validate the four
# windows that wrap around the circle (their tails are the leading zeros).
# Each completed sequence is read as a 32-bit integer and summed.

def solve():
    N = 5
    L = 1 << N          # 32 bits around the circle
    WMASK = (1 << N) - 1
    used = [False] * L
    used[0] = True      # window 00000 occupies bits 0..4
    total = 0

    def dfs(pos, window, value):
        nonlocal total
        if pos == L:
            # Windows starting at positions L-4..L-1 wrap onto bits 0..3,
            # which are all zero.  They must be distinct and unused.
            w = window
            seen = []
            for _ in range(N - 1):
                w = (w << 1) & WMASK  # shift in a wrapped zero bit
                if used[w] or w in seen:
                    return
                seen.append(w)
            total += value
            return
        for b in (0, 1):
            w = ((window << 1) | b) & WMASK
            if not used[w]:
                used[w] = True
                dfs(pos + 1, w, (value << 1) | b)
                used[w] = False

    # bits 0..4 are zero; the window of the last 5 placed bits is 0.
    dfs(N, 0, 0)
    return total


if __name__ == "__main__":
    print(solve())
