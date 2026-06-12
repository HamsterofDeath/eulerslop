#!/usr/bin/env python3
from fractions import Fraction
from itertools import combinations, permutations
from math import factorial


def cycle_type(p):
    # sorted tuple of cycle lengths of permutation p (0-indexed mapping)
    n = len(p)
    seen = [False] * n
    cyc = []
    for i in range(n):
        if not seen[i]:
            l, j = 0, i
            while not seen[j]:
                seen[j] = True
                j = p[j]
                l += 1
            cyc.append(l)
    return tuple(sorted(cyc))


def all_partitions(n, maxpart=None):
    if maxpart is None:
        maxpart = n
    if n == 0:
        yield ()
        return
    for k in range(min(n, maxpart), 0, -1):
        for rest in all_partitions(n - k, k):
            yield rest + (k,)


def class_size(part, n):
    # n! / (prod cycle lengths * prod multiplicities!)
    s = factorial(n)
    mult = {}
    for c in part:
        s //= c
        mult[c] = mult.get(c, 0) + 1
    for m in mult.values():
        s //= factorial(m)
    return s


def expected_shuffles(n):
    # One step: pick 3 positions uniformly among C(n,3) triples, then apply a
    # uniformly random permutation of those 3 entries (6 equally likely,
    # including doing nothing).  Each move multiplies the current permutation
    # by an element of a conjugation-invariant multiset of S_n, so the chain
    # projected onto conjugacy classes (cycle types = partitions of n) is
    # still Markov.  Identity (sorted) is absorbing.
    parts = sorted(all_partitions(n))
    idx = {p: i for i, p in enumerate(parts)}
    ident = (1,) * n
    nonid = [p for p in parts if p != ident]

    # enumerate all (triple, rearrangement) moves as full permutations of n
    moves = []
    for tri in combinations(range(n), 3):
        for perm in permutations(tri):
            m = list(range(n))
            for a, b in zip(tri, perm):
                m[a] = b
            moves.append(tuple(m))
    total = len(moves)  # C(n,3) * 6

    # transition counts between cycle types, using one representative per type
    trans = {}
    for part in nonid:
        # canonical representative: consecutive cycles
        rep = list(range(n))
        pos = 0
        for c in part:
            for k in range(c):
                rep[pos + k] = pos + (k + 1) % c
            pos += c
        row = {}
        for m in moves:
            t = cycle_type(tuple(m[rep[i]] for i in range(n)))
            row[t] = row.get(t, 0) + 1
        trans[part] = row

    # h[C] = expected shuffles from class C: h = 1 + Q h  =>  (I - Q) h = 1
    k = len(nonid)
    ni_idx = {p: i for i, p in enumerate(nonid)}
    A = [[Fraction(0)] * k for _ in range(k)]
    b = [Fraction(1)] * k
    for p in nonid:
        i = ni_idx[p]
        A[i][i] += 1
        for t, cnt in trans[p].items():
            if t != ident:
                A[i][ni_idx[t]] -= Fraction(cnt, total)

    # exact Gaussian elimination
    for col in range(k):
        piv = next(r for r in range(col, k) if A[r][col] != 0)
        A[col], A[piv] = A[piv], A[col]
        b[col], b[piv] = b[piv], b[col]
        inv = 1 / A[col][col]
        A[col] = [x * inv for x in A[col]]
        b[col] *= inv
        for r in range(k):
            if r != col and A[r][col] != 0:
                f = A[r][col]
                A[r] = [x - f * y for x, y in zip(A[r], A[col])]
                b[r] -= f * b[col]

    # average over all n! starting permutations (identity contributes 0)
    tot = sum(class_size(p, n) * b[ni_idx[p]] for p in nonid)
    return Fraction(tot, factorial(n))


def solve():
    assert expected_shuffles(4) == Fraction(55, 2)  # 27.5 from the statement
    e = expected_shuffles(11)
    # round to nearest integer
    return (2 * e.numerator + e.denominator) // (2 * e.denominator)


if __name__ == "__main__":
    print(solve())
