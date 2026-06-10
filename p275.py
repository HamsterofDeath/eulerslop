#!/usr/bin/env python3
# Problem 275: Balanced Sculptures
#
# The plinth sits at (0,0) and only touches blocks via (0,1), so a sculpture of
# order N is exactly a connected polyomino P of N cells in the half plane
# y >= 1 that contains the cell (0,1) and has sum(x) = 0 over its cells.
# Counting mirror pairs once, the answer is (A + B) / 2 where
#   A = number of such polyominoes counted with reflections distinct,
#   B = number of mirror-symmetric ones.
#
# A: transfer-matrix DP over the cells of the bounding columns, left to right,
# bottom to top (rows 1..N, the leftmost column is column 0). The state is
#   (boundary, n, m, V):
#   boundary = canonical labelling of the connected components on the last N
#              decided cells (one per row),
#   n        = cells placed, m = whether the plinth cell has been "marked".
# Exactly one row-1 cell is marked as the plinth cell (x = 0); validity means
# sum(x_c) - N*x_mark = 0. We track V = sum_placed(x_c - j) - N*(x_mark - j)*m
# relative to the current column j: placing/marking adds 0, moving to the next
# column adds N*m - n, and a finished sculpture needs V = 0. On any completable
# path V stays in [-R(R+1)/2, 0] with R = N - n cells remaining.
# Pruning: components that lose all boundary cells kill the state; an MST lower
# bound (edge = min row distance between two components) on the cells still
# needed to reconnect all components, plus the cells needed to reach down to
# row 1 from the lowest boundary row while the mark is missing, must fit in R.
#
# B: a symmetric sculpture is determined by its closed right half: a connected
# polyomino in x >= 0 whose column 0 (the mirror axis) has an even cell count
# and contains (0,1); cells in columns >= 1 count twice. Same DP without
# torque/marking.
#
# Verified against the stated values for orders 6 (18), 10 (964), 15 (360505).

def canon(lst):
    # renumber component labels by first occurrence
    mp = {0: 0}
    out = []
    nxt = 1
    for x in lst:
        v = mp.get(x)
        if v is None:
            v = mp[x] = nxt
            nxt += 1
        out.append(v)
    return tuple(out)

def needed_info(bound):
    # (MST lower bound on future cells needed to connect all components,
    #  lowest occupied row index, number of components)
    rows = {}
    bmin = -1
    for r, l in enumerate(bound):
        if l:
            rows.setdefault(l, []).append(r)
            if bmin < 0:
                bmin = r
    comps = list(rows.values())
    k = len(comps)
    if k <= 1:
        return (0, max(bmin, 0), k)
    INF = 10 ** 9
    dist = [INF] * k
    used = [False] * k
    dist[0] = 0
    mst = 0
    for _ in range(k):
        best, bi = INF, -1
        for i in range(k):
            if not used[i] and dist[i] < best:
                best, bi = dist[i], i
        used[bi] = True
        mst += best
        ci = comps[bi]
        for i in range(k):
            if not used[i]:
                g = dist[i]
                for a in ci:
                    for b in comps[i]:
                        d = a - b
                        if d < 0:
                            d = -d
                        if d < g:
                            g = d
                dist[i] = g
    return (mst, bmin, k)

class Trans:
    # interned boundaries plus cached per-row cell transitions
    def __init__(self, H):
        self.H = H
        self.bounds = [tuple([0] * H)]
        self.b2id = {self.bounds[0]: 0}
        self.info = [needed_info(self.bounds[0])]
        self.tr = [dict() for _ in range(H)]

    def intern(self, b):
        bid = self.b2id.get(b)
        if bid is None:
            bid = len(self.bounds)
            self.b2id[b] = bid
            self.bounds.append(b)
            self.info.append(needed_info(b))
        return bid

    def get(self, bid, r):
        t = self.tr[r].get(bid)
        if t is not None:
            return t
        bound = self.bounds[bid]
        left = bound[r]
        down = bound[r - 1] if r > 0 else 0
        # skip the cell: the left neighbour's component must survive elsewhere
        lb = list(bound)
        lb[r] = 0
        if left != 0 and left not in lb:
            sbid = -1
            mst_s = bmin_s = 0
        else:
            sbid = self.intern(canon(lb))
            mst_s, bmin_s, _ = self.info[sbid]
        # place the cell: union the left and down components
        lb = list(bound)
        if left == 0 and down == 0:
            lb[r] = max(bound) + 1
        elif left == 0:
            lb[r] = down
        elif down == 0 or left == down:
            lb[r] = left
        else:
            lb = [down if x == left else x for x in lb]
            lb[r] = down
        pbid = self.intern(canon(lb))
        mst_p, bmin_p, pcomps = self.info[pbid]
        t = (sbid, pbid, mst_s, bmin_s, mst_p, bmin_p, pcomps)
        self.tr[r][bid] = t
        return t

def count_A(NT):
    H = NT
    T = Trans(H)
    # states: (bid, n, m) -> {V: count}
    states = {(0, 0, 0): {0: 1}}
    total = 0
    for col in range(NT):
        for r in range(H):
            new = {}
            for (bid, n, m), vd in states.items():
                sbid, pbid, mst_s, bmin_s, mst_p, bmin_p, pcomps = T.get(bid, r)
                rem = NT - n
                if sbid >= 0 and mst_s + (max(1, bmin_s) if m == 0 else 0) <= rem:
                    key = (sbid, n, m)
                    dst = new.get(key)
                    if dst is None:
                        new[key] = dict(vd)
                    else:
                        for v, c in vd.items():
                            dst[v] = dst.get(v, 0) + c
                n2 = n + 1
                if n2 == NT:
                    # last cell placed: single component, marked, V == 0
                    # (an unmarked state may mark this final row-1 cell)
                    if pcomps == 1 and (m == 1 or r == 0):
                        total += vd.get(0, 0)
                else:
                    rem2 = NT - n2
                    if mst_p <= rem2:
                        if m == 1 or mst_p + max(1, bmin_p) <= rem2:
                            key = (pbid, n2, m)
                            dst = new.get(key)
                            if dst is None:
                                new[key] = dict(vd)
                            else:
                                for v, c in vd.items():
                                    dst[v] = dst.get(v, 0) + c
                        if m == 0 and r == 0:
                            # also place this row-1 cell as the marked one
                            key = (pbid, n2, 1)
                            dst = new.get(key)
                            if dst is None:
                                new[key] = dict(vd)
                            else:
                                for v, c in vd.items():
                                    dst[v] = dst.get(v, 0) + c
            states = new
        # column wrap: shift V, prune unreachable torques; empty first column
        # (n == 0) is dropped so column 0 is the true leftmost column
        new = {}
        for (bid, n, m), vd in states.items():
            if n == 0:
                continue
            R = NT - n
            shift = NT * m - n
            lo = -(R * (R + 1)) // 2
            nd = {}
            for v, c in vd.items():
                v2 = v + shift
                if 0 >= v2 >= lo:
                    nd[v2] = c
            if nd:
                new[(bid, n, m)] = nd
        states = new
    return total

def count_B(NT):
    H = NT
    T = Trans(H)
    states = {(0, 0): 1}
    total = 0
    # column 0 = mirror axis, cells cost 1
    for r in range(H):
        new = {}
        for (bid, n), cnt in states.items():
            sbid, pbid, mst_s, bmin_s, mst_p, bmin_p, pcomps = T.get(bid, r)
            if sbid >= 0:
                key = (sbid, n)
                new[key] = new.get(key, 0) + cnt
            n2 = n + 1
            if n2 == NT:
                if pcomps == 1:
                    total += cnt
            else:
                # future cells (columns >= 1) cost 2 each
                if 2 * mst_p <= NT - n2:
                    key = (pbid, n2)
                    new[key] = new.get(key, 0) + cnt
        states = new
    # axis column: even size (NT - |C| must be twice the half count) and it
    # must contain the plinth cell (0,1), i.e. row 1
    states = {(bid, n): c for (bid, n), c in states.items()
              if n > 0 and n % 2 == NT % 2 and T.bounds[bid][0] != 0}
    # columns >= 1: each placed cell also adds its mirror image, cost 2
    for col in range(1, NT):
        for r in range(H):
            new = {}
            for (bid, n), cnt in states.items():
                sbid, pbid, mst_s, bmin_s, mst_p, bmin_p, pcomps = T.get(bid, r)
                if sbid >= 0:
                    key = (sbid, n)
                    new[key] = new.get(key, 0) + cnt
                n2 = n + 2
                if n2 == NT:
                    if pcomps == 1:
                        total += cnt
                elif n2 < NT:
                    if 2 * mst_p <= NT - n2:
                        key = (pbid, n2)
                        new[key] = new.get(key, 0) + cnt
            states = new
    return total

def solve():
    N = 18
    return (count_A(N) + count_B(N)) // 2

if __name__ == "__main__":
    print(solve())
