#!/usr/bin/env python3
# Project Euler 244: Sliders
#
# 4x4 slider puzzle with 7 red and 8 blue counters (plus one empty cell).
# A move is named after the direction the COUNTER slides (so the empty cell
# moves in the opposite direction).  Checksum of a move sequence m1..mn:
#   checksum = 0;  checksum = (checksum * 243 + ascii(m_k)) mod 100000007
# Find the sum of checksums over ALL shortest paths from S to T.
#
# Identical-coloured counters are indistinguishable, so a state is just the
# colour pattern of the 16 cells plus the empty position.  BFS layer by
# layer, storing per state the number of shortest paths and the sum of their
# checksums (both mod 100000007).

MOD = 100000007


def _checksum(seq):
    c = 0
    for ch in seq:
        c = (c * 243 + ord(ch)) % MOD
    return c


def solve():
    # Sanity check against the example in the problem statement.
    assert _checksum("LULUR") == 19761398

    # State encoding: (colors, empty)
    #  - colors: 16-bit int, bit i set iff cell i holds a RED counter
    #    (cells numbered row-major, 0 = top-left); the empty cell's bit is 0.
    #  - empty: index of the empty cell.

    # S: empty top-left, red in the left two columns, blue in the right two.
    start_colors = 0
    for pos in range(16):
        if pos != 0 and pos % 4 < 2:
            start_colors |= 1 << pos
    start = (start_colors, 0)

    # T: empty top-left, checkerboard with red on (row+col) even cells.
    target_colors = 0
    for pos in range(16):
        if pos != 0 and ((pos // 4) + (pos % 4)) % 2 == 0:
            target_colors |= 1 << pos
    target = (target_colors, 0)

    # Move letter -> (offset of the sliding counter relative to the empty
    # cell, column/row constraint on the empty cell).  The counter slides
    # into the empty cell from the opposite side of the move direction:
    #   L: counter to the RIGHT of the empty slides left  (needs col < 3)
    #   R: counter to the LEFT slides right               (needs col > 0)
    #   U: counter BELOW slides up                        (needs row < 3)
    #   D: counter ABOVE slides down                      (needs row > 0)
    move_ascii = {"L": 76, "R": 82, "U": 85, "D": 68}

    def neighbours(state):
        colors, empty = state
        row, col = divmod(empty, 4)
        out = []
        if col < 3:
            out.append(("L", empty + 1))
        if col > 0:
            out.append(("R", empty - 1))
        if row < 3:
            out.append(("U", empty + 4))
        if row > 0:
            out.append(("D", empty - 4))
        res = []
        for letter, src in out:
            bit = (colors >> src) & 1
            new_colors = (colors & ~(1 << src)) | (bit << empty)
            res.append((move_ascii[letter], (new_colors, src)))
        return res

    # BFS layer by layer: per state keep (sum of checksums, path count).
    visited = {start}
    layer = {start: (0, 1)}
    while True:
        if target in layer:
            return layer[target][0] % MOD
        nxt = {}
        for state, (chk, cnt) in layer.items():
            for ascii_val, child in neighbours(state):
                if child in visited and child not in nxt:
                    continue
                add_chk = (chk * 243 + ascii_val * cnt) % MOD
                if child in nxt:
                    c0, n0 = nxt[child]
                    nxt[child] = ((c0 + add_chk) % MOD, (n0 + cnt) % MOD)
                else:
                    nxt[child] = (add_chk, cnt % MOD)
        visited.update(nxt)
        layer = nxt


if __name__ == "__main__":
    print(solve())
