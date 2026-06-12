#!/usr/bin/env python3
import numpy as np

MOD = 1 << 30


def step(s):
    # one look-and-say iteration
    out = []
    i, n = 0, len(s)
    while i < n:
        j = i + 1
        while j < n and s[j] == s[i]:
            j += 1
        out.append(str(j - i) + s[i])
        i = j
    return ''.join(out)


def splits_ok(left, right, k=12):
    # empirical non-interaction: evolving the parts separately must match
    # evolving the whole string, for k generations
    l, r, w = left, right, left + right
    for _ in range(k):
        l, r, w = step(l), step(r), step(w)
        if l + r != w:
            return False
    return True


def decompose(s):
    # greedy leftmost valid splits -> list of atomic chunks
    # (a split mid-run is never valid, so only try where adjacent chars differ)
    parts = []
    while True:
        pos = next((i for i in range(1, len(s))
                    if s[i - 1] != s[i] and splits_ok(s[:i], s[i:])), None)
        if pos is None:
            parts.append(s)
            return parts
        parts.append(s[:pos])
        s = s[pos:]


def solve():
    # --- discover atoms (Conway elements + transients) from seed "1" ---
    index = {'1': 0}
    order = ['1']
    children = [None]
    i = 0
    while i < len(order):
        kids = []
        for c in decompose(step(order[i])):
            if c not in index:
                index[c] = len(order)
                order.append(c)
                children.append(None)
            kids.append(index[c])
        children[i] = kids
        i += 1
    m = len(order)

    # transition matrix: T[i][j] = multiplicity of atom j in step(atom i)
    T = np.zeros((m, m), dtype=np.int64)
    for a, kids in enumerate(children):
        for b in kids:
            T[a, b] += 1

    # digit counts per atom
    D = [(a.count('1'), a.count('2'), a.count('3')) for a in order]

    # --- cross-validation: direct simulation vs exact matrix evolution ---
    s = '1'
    v = [0] * m
    v[0] = 1  # term 1 is the atom "1"
    for term in range(2, 46):
        s = step(s)
        v = [sum(v[a] * children[a].count(b) for a in range(m) if v[a])
             for b in range(m)]
        got = tuple(sum(v[a] * D[a][d] for a in range(m)) for d in range(3))
        want = (s.count('1'), s.count('2'), s.count('3'))
        assert got == want, f"matrix/simulation mismatch at term {term}"
        if term == 40:
            assert want == (31254, 20259, 11625), "statement check failed"

    # --- modular matrix power to reach term 10^12 ---
    def matmul_mod(A, B):
        # (A @ B) mod 2^30 via 15-bit limbs so products fit in int64
        A0, A1 = A & 0x7FFF, A >> 15
        B0, B1 = B & 0x7FFF, B >> 15
        return ((A0 @ B0) + (((A0 @ B1 + A1 @ B0) & 0x7FFF) << 15)) & (MOD - 1)

    def matpow(M, e):
        R = np.eye(m, dtype=np.int64)
        while e:
            if e & 1:
                R = matmul_mod(R, M)
            M = matmul_mod(M, M)
            e >>= 1
        return R

    n = 10 ** 12
    row = matpow(T, n - 1)[0]  # counts of each atom in term n, mod 2^30
    ans = [sum(int(row[a]) * D[a][d] for a in range(m)) % MOD for d in range(3)]
    return ','.join(map(str, ans))


if __name__ == "__main__":
    print(solve())
