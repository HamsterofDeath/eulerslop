#!/usr/bin/env python3
import numpy as np

P = 100000007  # prime

def build_transfer():
    # Layer-by-layer transfer matrix over 3x3 occupancy profiles:
    # T[s][s2] = number of ways to complete one 3x3 layer when the cells in
    # mask s are already filled by blocks sticking up from the layer below,
    # using in-layer 2x1 dominoes, with the cells in s2 holding blocks that
    # stick up into the next layer.  Then f(n) = (T^n)[0][0].
    T = np.zeros((512, 512), dtype=np.int64)
    def rec(start, s, s2, cell):
        while cell < 9 and (s >> cell) & 1:
            cell += 1
        if cell == 9:
            T[start, s2] += 1
            return
        r, c = divmod(cell, 3)
        rec(start, s | 1 << cell, s2 | 1 << cell, cell + 1)        # stick up
        if c < 2 and not (s >> (cell + 1)) & 1:                    # domino right
            rec(start, s | 1 << cell | 1 << (cell + 1), s2, cell + 1)
        if r < 2 and not (s >> (cell + 3)) & 1:                    # domino down
            rec(start, s | 1 << cell | 1 << (cell + 3), s2, cell + 1)
    for start in range(512):
        rec(start, start, 0, 0)
    return T

def berlekamp_massey(S, p):
    # Minimal linear recurrence of S over GF(p): returns C with C[0] = 1 and
    # sum_j C[j] * S[i-j] == 0 for all i >= len(C)-1.
    C, B, L, m, b = [1], [1], 0, 1, 1
    for i in range(len(S)):
        d = sum(C[j] * S[i - j] for j in range(L + 1)) % p
        if d == 0:
            m += 1
            continue
        coef = d * pow(b, -1, p) % p
        if len(B) + m > len(C):
            C = C + [0] * (len(B) + m - len(C))
        if 2 * L <= i:
            old = C[:]
            for j in range(len(B)):
                C[j + m] = (C[j + m] - coef * B[j]) % p
            L, B, b, m = i + 1 - L, old, d, 1
        else:
            for j in range(len(B)):
                C[j + m] = (C[j + m] - coef * B[j]) % p
            m += 1
    return C, L

def kitamasa(rec, init, K, p):
    # rec: b_i = sum_j rec[j] * b_{i-1-j} (len L); evaluates b_K via
    # x^K mod m(x) where m(x) = x^L - rec[0] x^{L-1} - ... - rec[L-1].
    L = len(rec)
    if K < L:
        return init[K]
    def mulmod(a, b):
        res = [0] * (len(a) + len(b) - 1)
        for i, ai in enumerate(a):
            if ai:
                for j, bj in enumerate(b):
                    res[i + j] += ai * bj
        for i in range(len(res) - 1, L - 1, -1):
            t = res[i] % p
            if t:
                for j in range(L):
                    res[i - 1 - j] += t * rec[j]
            res[i] = 0
        return [v % p for v in res[:L]]
    r = [1]            # x^0
    x = [0, 1]         # x
    for bit in bin(K)[2:]:
        r = mulmod(r, r)
        if bit == '1':
            r = mulmod(r, x)
    return sum(r[i] * init[i] for i in range(min(L, len(r)))) % p

def solve():
    T = build_transfer()
    # Layers come in parity pairs (popcount(s) + popcount(s2) must be odd),
    # so f(odd) = 0; work with the even subsequence b_k = f(2k) mod P.
    v = np.zeros(512, dtype=np.int64)
    v[0] = 1
    seq = []
    for _ in range(201):
        seq.append(int(v[0]))
        v = (T.T @ v) % P          # entries < P, dot of 512 terms fits int64
    b = seq[0::2]                  # 101 terms of f(2k)
    assert b[1] == 229 and b[2] == 117805 and b[5] == 96149360

    C, L = berlekamp_massey(b, P)
    # self-check: recurrence reproduces every computed term
    assert all(sum(C[j] * b[i - j] for j in range(L + 1)) % P == 0
               for i in range(L, len(b)))
    rec = [(-C[j + 1]) % P for j in range(L)]
    assert kitamasa(rec, b, 10 ** 6 // 2, P) == 30808124   # given f(10^6)

    return kitamasa(rec, b, 10 ** 10000 // 2, P)

if __name__ == "__main__":
    print(solve())
