#!/usr/bin/env python3
import numpy as np

def divisor_counts(N):
    # d[m] = number of divisors of m, for m <= N. Each divisor pair (i, m/i)
    # with i <= sqrt(m) contributes 2, squares are corrected by -1.
    d = np.zeros(N + 1, np.int16)
    r = int(N ** 0.5)
    while (r + 1) * (r + 1) <= N:
        r += 1
    for i in range(1, r + 1):
        d[i * i::i] += 2
    sq = np.arange(1, r + 1, dtype=np.int64) ** 2
    d[sq] -= 1
    return d

def dT_values(n):
    # T(m) = m(m+1)/2 with gcd(m, m+1) = 1, so d(T(m)) splits multiplicatively:
    # m even: d(m/2) * d(m+1); m odd: d(m) * d((m+1)/2).
    d = divisor_counts(n + 1)
    dT = np.empty(n, np.int32)
    k = n // 2            # even m = 2,4,...,2k  -> dT[1::2]
    dT[1::2] = d[1:k + 1].astype(np.int32) * d[3:2 * k + 2:2]
    ko = (n + 1) // 2     # odd m = 1,3,...,2ko-1 -> dT[0::2]
    dT[0::2] = d[1:2 * ko:2].astype(np.int32) * d[1:ko + 1]
    return dT

def greater_before(vr, D, B=4096):
    # For each position j, count positions i < j with vr[i] > vr[j].
    # Split positions into blocks of size B:
    #  - cross-block pairs via a (value rank) x (block) count matrix with 2D
    #    exclusive prefix sums (suffix over larger ranks, prefix over earlier
    #    blocks) -- a flat Fenwick-style dominance count, fully vectorized;
    #  - within-block pairs via a bottom-up vectorized mergesort: at each
    #    level rows hold [sorted left run | sorted right run]; after a stable
    #    argsort, a right-run element with old column c at merged position m
    #    has exactly c - m left elements strictly greater than it.
    n = len(vr)
    NB = (n + B - 1) // B
    npad = NB * B
    blk = np.repeat(np.arange(NB, dtype=np.int32), B)[:n]

    flat = vr.astype(np.int64) * NB + blk
    M = np.bincount(flat, minlength=D * NB).reshape(D, NB).astype(np.int32)
    csum = np.cumsum(M[::-1], axis=0)[::-1]      # ranks >= c per block
    gtm = np.zeros_like(M)
    gtm[:-1] = csum[1:]                          # ranks > c per block
    G = np.zeros_like(M)
    G[:, 1:] = np.cumsum(gtm, axis=1)[:, :-1]    # strictly earlier blocks
    coarse = G.ravel()[flat]
    del flat, M, csum, gtm, G

    vals = np.empty(npad, np.int32)
    vals[:n] = vr
    vals[n:] = D                                 # sentinel above all ranks
    idx = np.arange(npad, dtype=np.int32)
    cnt = np.zeros(npad, np.int16)               # in-block counts < B

    # level s=1: compare adjacent pairs directly
    va, vb = vals[0::2], vals[1::2]
    ia, ib = idx[0::2], idx[1::2]
    m = va > vb
    cnt[ib[m]] += 1
    tv = va[m]; va[m] = vb[m]; vb[m] = tv
    ti = ia[m]; ia[m] = ib[m]; ib[m] = ti
    del va, vb, ia, ib, m, tv, ti

    s = 2
    while s < B:
        w = 2 * s
        chunk = max(1, (1 << 24) // w) * w
        cols = np.arange(w)
        for a in range(0, npad, chunk):
            V = vals[a:a + chunk].reshape(-1, w)
            I = idx[a:a + chunk].reshape(-1, w)
            o = np.argsort(V, axis=1, kind='stable')
            mv = np.take_along_axis(V, o, axis=1)
            mi = np.take_along_axis(I, o, axis=1)
            mask = o >= s
            cnt[mi[mask]] += (o - cols)[mask].astype(np.int16)
            V[:] = mv
            I[:] = mi
        s = w

    return coarse, cnt[:n]   # both indexed by original position

def trinc(n):
    # number of triples i<j<k with v_i > v_j > v_k equals sum_j L(j)*R(j),
    # L(j) = # earlier greater, R(j) = # later smaller.
    dT = dT_values(n)
    mx = int(dT.max())
    present = np.zeros(mx + 1, bool)
    present[dT] = True
    rmap = np.cumsum(present, dtype=np.int32) - 1
    D = int(rmap[-1]) + 1
    vr = rmap[dT]
    del dT, present, rmap

    coarse, inblk = greater_before(vr, D)

    cnts = np.bincount(vr, minlength=D)
    starts = np.zeros(D, np.int64)
    starts[1:] = np.cumsum(cnts)[:-1]            # # elements with smaller rank
    ordv = np.argsort(vr, kind='stable')
    eqb = np.empty(n, np.int32)
    eqb[ordv] = (np.arange(n, dtype=np.int64)
                 - np.repeat(starts, cnts)).astype(np.int32)
    del ordv

    total = 0
    step = 1 << 22
    for a in range(0, n, step):
        b = min(a + step, n)
        L = coarse[a:b].astype(np.int64) + inblk[a:b]
        lessb = np.arange(a, b, dtype=np.int64) - eqb[a:b] - L
        R = starts[vr[a:b]] - lessb
        prod = L * R                              # < n^2 ~ 3.6e15, fits int64
        # partial sums of <=2048 products stay below 2^63; combine in Python
        seg = np.add.reduceat(prod, np.arange(0, len(prod), 2048))
        total += sum(seg.tolist())
    return total

def solve():
    n = 60_000_000
    return trinc(n) % 10 ** 18   # last 18 digits

if __name__ == "__main__":
    print(solve())
