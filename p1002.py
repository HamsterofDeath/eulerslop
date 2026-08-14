#!/usr/bin/env python3
"""Project Euler Problem 1002: Connections II.

Every value pair is drawn either above or below the row, and two arcs on
the same side must not cross, so each side's intervals form a laminar
family.  Two values with properly overlapping intervals (l1 < l2 < r1 <
r2) are forced onto opposite sides; the overlap graph is therefore
bipartite (given) and the maximum number of above connections is the sum
over its connected components of max(|A|, |B|) for the two colour classes.

The sweep processes the positions left to right.  For each side the
active intervals form a nesting chain of "blocks" (groups forced to one
colour, created whenever an interval overlaps a whole prefix of one or
both chains).  When v starts at l_v it must lie opposite every active
interval ending before r_v, so all leading blocks of both chains whose
smallest active right end is < r_v merge into one block, and v's own
block is linked to it with opposite parity in a weighted union-find.
Chain blocks keep their right ends in sorted lists (merged small-into-
large) and are popped from the innermost end as their right ends pass.
"""

import heapq
from collections import defaultdict, deque
from pathlib import Path

DATA = Path(__file__).resolve().parent / "1002_input.txt"


def _connectivity_answer(arr):
    n = len(arr) // 2
    size = len(arr)
    pos1 = [0] * n
    pos2 = [0] * n
    for i, x in enumerate(arr, 1):
        if pos1[x]:
            pos2[x] = i
        else:
            pos1[x] = i
    first_at = [-1] * (size + 1)
    for v in range(n):
        first_at[pos1[v]] = v

    parent = list(range(n))
    parity = [0] * n

    def find(x):
        orig = x
        acc = 0
        while parent[x] != x:
            acc ^= parity[x]
            x = parent[x]
        root = x
        x = orig
        pend = acc
        while parent[x] != x:
            p = parent[x]
            q = parity[x]
            parent[x] = root
            parity[x] = pend
            pend = q ^ pend
            x = p
        return root, acc

    def union(a, b, p):
        ra, pa = find(a)
        rb, pb = find(b)
        if ra == rb:
            assert (pa ^ pb) == p, "overlap graph is not bipartite"
            return
        parent[ra] = rb
        parity[ra] = pa ^ pb ^ p

    top = deque()
    bottom = deque()
    rights = []   # sorted list of active right ends per block
    curs = []     # next unpopped index per block
    nodes = []    # union-find node per block

    def pop_chain(chain, p):
        while chain:
            b = chain[0]
            lst = rights[b]
            cur = curs[b]
            if cur >= len(lst):
                chain.popleft()
                continue
            if lst[cur] <= p:
                curs[b] = cur + 1
                continue
            break

    for p in range(1, size + 1):
        pop_chain(top, p)
        pop_chain(bottom, p)
        v = first_at[p]
        if v < 0:
            continue
        r = pos2[v]
        overlapping = []
        for chain in (top, bottom):
            while chain:
                b = chain[0]
                lst = rights[b]
                cur = curs[b]
                if cur < len(lst) and lst[cur] < r:
                    overlapping.append(b)
                    chain.popleft()
                else:
                    break
        vb = len(rights)
        rights.append([r])
        curs.append(0)
        nodes.append(v)
        if overlapping:
            big = overlapping[0]
            for b in overlapping[1:]:
                if len(rights[b]) - curs[b] > len(rights[big]) - curs[big]:
                    big = b
            merged = rights[big][curs[big]:]
            for b in overlapping:
                if b != big:
                    merged = list(heapq.merge(merged, rights[b][curs[b]:]))
                    union(nodes[big], nodes[b], 0)
            rights[big] = merged
            curs[big] = 0
            union(nodes[big], v, 1)
            top.appendleft(big)
            bottom.appendleft(vb)
        else:
            top.appendleft(vb)

    tally = defaultdict(lambda: [0, 0])
    for v in range(n):
        root, px = find(v)
        tally[root][px] += 1
    return sum(max(side) for side in tally.values())


def solve() -> int:
    arr = [int(tok) for tok in DATA.read_text().split(",")]
    return _connectivity_answer(arr)


if __name__ == "__main__":
    print(solve())
