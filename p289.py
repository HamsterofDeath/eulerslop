#!/usr/bin/env python3
"""Project Euler 289: Non-crossing Eulerian circuits on a grid of circles.

E(m,n) is an m x n grid of unit-square-inscribing circles; adjacent circles
touch at lattice points.  Each circle consists of 4 arcs between the 4
lattice points it passes through, so the configuration is a planar 4-regular
multigraph on the lattice points (i,j), 0<=i<=m, 0<=j<=n (with doubled
edges).  An Eulerian circuit corresponds to choosing, at every lattice
point, a perfect pairing of the incident arc-ends (how the path transits
the point); the circuit is non-crossing iff every pairing is non-crossing
in the cyclic (angular) order of arc-ends around the point, and it is a
single circuit iff the resulting set of closed curves is one loop.

At a point P the up-to-8 arc-ends leave tangentially in the 4 diagonal
directions; resolving ties by curvature gives the counterclockwise order
  [E_up, N_right, N_left, W_up, W_down, S_left, S_right, E_down]
where e.g. E_up / E_down are the two arcs towards (i+1,j) bulging up/down,
N_left / N_right the arcs towards (i,j+1) bulging left/right, etc.

We sweep the lattice points in scanline order with a broken-profile DP.
The frontier crosses the dangling arc-ends; by planarity the partial paths
connect them in a non-crossing perfect matching, which is the DP state.
Processing a point consumes its W and S ends (contiguous on the frontier,
in order W_up, W_down, S_left, S_right) and emits its N and E ends (in
order N_left, N_right, E_up, E_down); for every non-crossing pairing at the
point we re-link the strands.  Closing a loop is only allowed at the very
last point with an otherwise empty frontier (a single closed curve must
cover every arc).  Frontier width <= 14 ends, so there are at most
Catalan(7) = 429 states and the whole DP is instantaneous.
"""

# Counterclockwise cyclic order of arc-ends around a lattice point.
CYC = ('EU', 'NR', 'NL', 'WU', 'WD', 'SL', 'SR', 'ED')


def noncrossing_matchings(lst):
    """All non-crossing perfect matchings of points in cyclic order lst.

    Crossing of two chords depends only on the cyclic order, so enumerating
    linearly non-crossing matchings of any fixed rotation is equivalent.
    """
    if not lst:
        return [[]]
    res = []
    a = lst[0]
    for k in range(1, len(lst), 2):
        b = lst[k]
        for mi in noncrossing_matchings(lst[1:k]):
            for mo in noncrossing_matchings(lst[k + 1:]):
                res.append([(a, b)] + mi + mo)
    return res


def L(m, n, mod):
    """Number of non-crossing Eulerian circuits of E(m,n), mod `mod`."""

    def present(i, j):
        # Which of the 8 arc-ends exist at point (i,j): each end belongs to
        # one of the four surrounding circles (which may be off-grid).
        return {
            'WU': i > 0 and j > 0,   'WD': i > 0 and j < n,   # arcs to west
            'SL': i < m and j > 0,   'SR': i > 0 and j > 0,   # arcs to south
            'NL': i < m and j < n,   'NR': i > 0 and j < n,   # arcs to north
            'EU': i < m and j > 0,   'ED': i < m and j < n,   # arcs to east
        }

    states = {(): 1}  # frontier matching (tuple of partner indices) -> count
    answer = 0
    for j in range(n + 1):
        for i in range(m + 1):
            pres = present(i, j)
            in_labels = [x for x in ('WU', 'WD', 'SL', 'SR') if pres[x]]
            out_labels = [x for x in ('NL', 'NR', 'EU', 'ED') if pres[x]]
            vms = noncrossing_matchings([x for x in CYC if pres[x]])
            k_in, k_out = len(in_labels), len(out_labels)
            # Frontier ends before the consumed block: the N-ends emitted by
            # points (0..i-1, j) earlier in this row.
            pos0 = sum((1 if present(i2, j)['NL'] else 0) +
                       (1 if present(i2, j)['NR'] else 0) for i2 in range(i))
            last = (i == m and j == n)
            out_pos = {lab: pos0 + t for t, lab in enumerate(out_labels)}
            label_of = {pos0 + t: lab for t, lab in enumerate(in_labels)}
            idx_of = {lab: pos0 + t for t, lab in enumerate(in_labels)}
            shift = k_out - k_in

            new_states = {}
            for state, cnt in states.items():
                L0 = len(state)
                for pairs in vms:
                    vm = {}
                    for a, b in pairs:
                        vm[a], vm[b] = b, a
                    visited = set()
                    new_pairs = []
                    # Path endpoints after this step: emitted out-ends and
                    # untouched old frontier ends.  Trace each partial path
                    # through alternating frontier / vertex links.
                    endpoints = [('out', o) for o in out_labels] + \
                                [('old', x) for x in range(L0)
                                 if not pos0 <= x < pos0 + k_in]
                    done = set()
                    for ep in endpoints:
                        if ep in done:
                            continue
                        done.add(ep)
                        if ep[0] == 'out':
                            nxt = vm[ep[1]]
                            if nxt not in idx_of:        # out-out chord
                                done.add(('out', nxt))
                                new_pairs.append((out_pos[ep[1]],
                                                  out_pos[nxt]))
                                continue
                            cur, via = idx_of[nxt], 'V'
                        else:
                            cur = state[ep[1]]
                            if not pos0 <= cur < pos0 + k_in:  # untouched pair
                                done.add(('old', cur))
                                p = ep[1] if ep[1] < pos0 else ep[1] + shift
                                q = cur if cur < pos0 else cur + shift
                                new_pairs.append((p, q))
                                continue
                            via = 'F'
                        while True:          # cur is a consumed in-end index
                            visited.add(cur)
                            if via == 'V':   # continue along old frontier link
                                y = state[cur]
                                if pos0 <= y < pos0 + k_in:
                                    cur, via = y, 'F'
                                else:
                                    other = ('old', y)
                                    break
                            else:            # continue along vertex pairing
                                t = vm[label_of[cur]]
                                if t in idx_of:
                                    cur, via = idx_of[t], 'V'
                                else:
                                    other = ('out', t)
                                    break
                        done.add(other)
                        a = out_pos[ep[1]] if ep[0] == 'out' else \
                            (ep[1] if ep[1] < pos0 else ep[1] + shift)
                        b = out_pos[other[1]] if other[0] == 'out' else \
                            (other[1] if other[1] < pos0 else other[1] + shift)
                        new_pairs.append((a, b))

                    # Consumed ends not on any traced path were joined into
                    # closed loops.
                    closures = 0
                    seen = set()
                    for x in range(pos0, pos0 + k_in):
                        if x in visited or x in seen:
                            continue
                        closures += 1
                        cur, via = x, 'V'
                        while cur not in seen:
                            seen.add(cur)
                            if via == 'V':
                                cur, via = state[cur], 'F'
                            else:
                                cur, via = idx_of[vm[label_of[cur]]], 'V'
                    if closures:
                        # A closed loop is only the full Eulerian circuit if
                        # it is the unique loop, formed at the final point,
                        # with nothing else dangling.
                        if last and closures == 1 and not new_pairs:
                            answer = (answer + cnt) % mod
                        continue

                    newst = [0] * (L0 + shift)
                    for a, b in new_pairs:
                        newst[a], newst[b] = b, a
                    key = tuple(newst)
                    new_states[key] = (new_states.get(key, 0) + cnt) % mod
            states = new_states
    return answer


def solve():
    MOD = 10 ** 10
    # Sanity checks from the problem statement.
    assert L(1, 2, MOD) == 2
    assert L(2, 2, MOD) == 37
    assert L(3, 3, MOD) == 104290
    return L(6, 10, MOD)


if __name__ == "__main__":
    print(solve())
