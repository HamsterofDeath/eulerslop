#!/usr/bin/env python3
"""Project Euler Problem 1007: Alternating Difference.

The n pairs of parentheses turn F_0-F_1-...-F_n into all Catalan(n) full
binary trees; a tree's value is evaluated with subtraction, so leaf j
carries sign s_j = (-1)^{number of right edges on its root path}.  If
E(m,j) denotes the sum of the sign of position j over all trees on m
leaves, then A(n) = sum_j E(n+1,j) F_j.  Splitting trees at the root
gives, for the row polynomials R_m(t) = sum_j E(m,j) t^j,

    R_m(t) = sum_{a=1}^{m-1} [ Cat(m-a-1) R_a(t) - Cat(a-1) t^a R_{m-a}(t) ],

whose generating function collapses to

    q(z;t) = sum_m R_m(t) z^m = z / (1 - cnt(z) + cnt(tz)),

with cnt(z) = z C(z) the shifted Catalan series.  By linearity in
F_j = (phi^j - psi^j)/sqrt(5),

    A(n) = (R_{n+1}(phi) - R_{n+1}(psi)) / sqrt(5).

Everything is carried out mod p = 10^9+9 (5 is a quadratic residue
there).  R_{n+1}(t) is one coefficient of 1/(1 - cnt + cnt(tz)), so it
is obtained by Newton inversion of that power series to length ~10^7.
Exact products mod p are computed through three NTT-friendly primes and
CRT lifting; the two inversions run in parallel processes.  Verified
against A(3)=-6, A(10)=-177666 and A(100) = 71792794 (mod p).
"""

import os
import sys
import numpy as np

P = 10**9 + 9
NTT_PRIMES = [
    (2013265921, 31),   # 15*2^27+1
    (2281701377, 3),    # 17*2^27+1
    (1811939329, 13),   # 27*2^26+1
]

_TABLES = {}


def _ntt_tables(q, g, n, inverse):
    key = (q, n, inverse)
    tab = _TABLES.get(key)
    if tab is not None:
        return tab
    w = pow(g, (q - 1) // n, q)
    if inverse:
        w = pow(w, q - 2, q)
    half = n >> 1
    wp = np.empty(half, dtype=np.int64)
    wp[0] = 1
    blk, wb = 1, w
    while blk < half:
        end = min(2 * blk, half)
        wp[blk:end] = wp[:end - blk] * wb % q
        blk <<= 1
        wb = wb * wb % q
    bits = n.bit_length() - 1
    idx = np.arange(n, dtype=np.int64)
    rev = np.zeros(n, dtype=np.int64)
    for b in range(bits):
        rev = (rev << 1) | ((idx >> b) & 1)
    rev = rev.astype(np.int32)
    if len(_TABLES) > 8:
        _TABLES.clear()
    _TABLES[key] = (wp, rev)
    return wp, rev


def ntt(a, q, g, inverse=False):
    """Iterative Cooley-Tukey NTT over F_q; len(a) must be a power of two."""
    n = len(a)
    if n == 1:
        return a.copy()
    wp, rev = _ntt_tables(q, g, n, inverse)
    a2 = a[rev].astype(np.int64)
    length = 2
    while length <= n:
        hl = length >> 1
        tw = wp[:: n // length][:hl]
        a3 = a2.reshape(-1, 2, hl)
        u = a3[:, 0, :].copy()
        v = a3[:, 1, :] * tw % q
        a3[:, 0, :] = (u + v) % q
        a3[:, 1, :] = (u - v) % q
        length <<= 1
    if inverse:
        a2 *= pow(n, q - 2, q)
        a2 %= q
    return a2


def mul_trunc(a, b, outlen):
    """First outlen coefficients of a*b mod P via padded cyclic NTTs + CRT."""
    la = min(len(a), outlen)
    lb = min(len(b), outlen)
    size = 1
    while size < la + lb - 1:
        size <<= 1
    res = []
    qs = []
    for q, g in NTT_PRIMES:
        fa = ntt(np.concatenate([a[:la] % q, np.zeros(size - la, dtype=np.int64)]), q, g)
        fb = ntt(np.concatenate([b[:lb] % q, np.zeros(size - lb, dtype=np.int64)]), q, g)
        res.append(ntt(fa * fb % q, q, g, inverse=True))
        qs.append(q)
    q0, q1, q2 = qs
    xs = []
    for r in res:
        if len(r) < outlen:
            r = np.concatenate([r, np.zeros(outlen - len(r), dtype=np.int64)])
        xs.append(r[:outlen])
    x0, x1, x2 = xs
    t1 = (x1 - x0) % q1 * pow(q0, q1 - 2, q1) % q1
    r01 = x0 + q0 * t1                      # < q0*q1 ~ 4.6e18, fits int64
    t2 = (x2 - r01 % q2) % q2 * pow((q0 * q1) % q2, q2 - 2, q2) % q2
    return ((r01 % P + ((q0 * q1) % P) * t2) % P).astype(np.int64)


def mul_trunc_short(D, y, tgt):
    """First tgt coefficients of D*y where only y's first m=tgt//2 terms
    matter: split D at m to keep every NTT at size ~tgt instead of 2*tgt."""
    m = len(y)
    if m >= tgt:
        return mul_trunc(D, y, tgt)
    lo = np.array(D[:min(len(D), m)], dtype=np.int64)
    hi = np.array(D[m:tgt], dtype=np.int64)
    out = mul_trunc(lo, y, tgt)
    part2 = mul_trunc(hi, y, tgt - m)
    out[m:] = (out[m:] + part2) % P
    return out


def newton_inv(D, L):
    """Inverse of the power series D mod z^L (D[0] invertible)."""
    y = np.array([pow(int(D[0]), P - 2, P)], dtype=np.int64)
    m = 1
    while m < L:
        tgt = min(2 * m, L)
        w = mul_trunc_short(D, y, tgt)
        u = np.empty(tgt, dtype=np.int64)
        u[0] = (2 - int(w[0])) % P
        if tgt > 1:
            u[1:] = (-w[1:]) % P
        y = mul_trunc(u, y, tgt)
        m = tgt
    return y


def catalan_cnt(L):
    """cnt(z)=z*C(z): coefficients Cat(m-1) mod P, m=0..L-1."""
    inv = [0] * (L + 2)
    inv[1] = 1
    for i in range(2, L + 2):
        inv[i] = (P - (P // i) * inv[P % i]) % P
    cl = [0] * L
    cat = 1
    for m in range(1, L):
        cl[m] = cat
        cat = cat * 2 % P * (2 * m - 1) % P * inv[m + 1] % P
    return np.array(cl, dtype=np.int64)


def tonelli(a, p):
    q = p - 1
    s = 0
    while q % 2 == 0:
        q //= 2
        s += 1
    z = 2
    while pow(z, (p - 1) // 2, p) != p - 1:
        z += 1
    m, c, t, r = s, pow(z, q, p), pow(a, q, p), pow(a, (q + 1) // 2, p)
    while t != 1:
        i, t2 = 0, t
        while t2 != 1:
            t2 = t2 * t2 % p
            i += 1
        b = pow(c, 1 << (m - i - 1), p)
        m, c, t, r = i, b * b % p, t * b * b % p, r * b % p
    return r


_R5 = tonelli(5, P)
INV5 = pow(_R5, P - 2, P)
PHI = (1 + _R5) * pow(2, P - 2, P) % P
PSI = (1 - _R5) * pow(2, P - 2, P) % P


def inv_for(cnt, t, M):
    """R_M(t) = [z^{M-1}] 1/(1 - cnt(z) + cnt(tz)) mod P."""
    tp = np.empty(M, dtype=np.int64)
    tl = tp.tolist()
    tl[0] = 1
    cur = 1
    for i in range(1, M):
        cur = cur * t % P
        tl[i] = cur
    tp = np.array(tl, dtype=np.int64)
    D = (-cnt + cnt * tp % P) % P
    D[0] = (D[0] + 1) % P
    return int(newton_inv(D, M)[M - 1])


def _worker(args):
    cnt, t, M = args
    return inv_for(cnt, t, M)


def solve() -> int:
    M = 10**7 + 1
    cnt = catalan_cnt(M)

    import multiprocessing as mp
    ctx = mp.get_context("fork")
    with ctx.Pool(processes=2) as pool:
        rp, rq = pool.map(_worker, [(cnt, PHI, M), (cnt, PSI, M)])
    return (rp - rq) * INV5 % P


if __name__ == "__main__":
    print(solve())
