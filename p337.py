#!/usr/bin/env python3
import numpy as np

def solve(N=20_000_000, MOD=10**8, L=2048, R=256):
    # Let f(a) = number of valid sequences starting at a (each sequence may
    # stop anywhere).  A step a -> b is allowed iff b > a and
    # phi(a) < phi(b) < a, so f(a) = 1 + sum f(b) over such b, and the
    # answer is f(6).  Primes are inert: a prime p can neither follow
    # anything (phi(p) = p-1 leaves the empty window (p-1, p) for its
    # predecessor's value) nor be followed (phi(b) must lie in the empty
    # interval (p-1, p)), so only composites matter.
    #
    # Process a = N..6 in blocks of L.  Contributions from already-solved
    # b > a are 2D dominance sums "phi(a) < phi(b) <= a-1" over points
    # keyed by phi(b) with weight f(b).  Three tiers keep it fast in Python:
    #   * old blocks: a dense prefix-sum array over phi, rebuilt every R
    #     blocks (O(1) numpy gathers per query);
    #   * recent blocks: Bentley-Saxe sorted-by-phi runs with cumulative
    #     sums, queried via vectorized searchsorted;
    #   * same block: a small Fenwick tree over the block's compressed phi
    #     values, driven by a tight pure-Python loop (the only sequential
    #     part, since within a block f(a) depends on larger b in the block).

    # --- primality sieve and totient sieve ---
    comp = np.zeros(N + 1, dtype=bool)
    comp[:2] = True
    for i in range(2, int(N ** 0.5) + 1):
        if not comp[i]:
            comp[i * i::i] = True
    phi = np.arange(N + 1, dtype=np.int32)
    primes = np.flatnonzero(~comp)
    for p in primes[primes <= N // 2].tolist():
        sl = phi[p::p]
        sl -= sl // p
    big = primes[primes > N // 2]
    phi[big] = (big - 1).astype(np.int32)

    counts = np.zeros(N + 1, dtype=np.int64)   # f(b) summed by phi(b), old blocks
    prefix = np.zeros(N + 1, dtype=np.int64)   # cumsum of counts
    runs = []          # [level, sorted phi, f in that order, cumsum-with-0]
    blocks_in_window = 0
    ans = 0

    hi = N + 1
    while hi > 6:
        lo = max(6, hi - L)
        vals = np.flatnonzero(comp[lo:hi]).astype(np.int64) + lo  # composites, ascending
        if len(vals):
            pa = phi[vals].astype(np.int64)
            # cross contributions from b >= hi: sum of f(b) with phi(b) in (phi(a), a)
            c = prefix[vals - 1] - prefix[pa]
            for _, P, _, CF in runs:
                c += CF[np.searchsorted(P, vals)] - CF[np.searchsorted(P, pa, side='right')]
            c %= MOD
            # within-block Fenwick over compressed phi values
            K = np.unique(pa)
            U = len(K)
            qhi = np.searchsorted(K, vals)                 # keys < a, i.e. <= a-1
            qlo = np.searchsorted(K, pa, side='right')     # keys <= phi(a)
            ins = np.searchsorted(K, pa) + 1               # 1-indexed insert position
            tree = [0] * (U + 1)
            fs = []
            push = fs.append
            for qh, ql, ii, cc in zip(qhi[::-1].tolist(), qlo[::-1].tolist(),
                                      ins[::-1].tolist(), c[::-1].tolist()):
                s = 1 + cc
                i = qh
                while i:
                    s += tree[i]
                    i &= i - 1
                i = ql
                while i:
                    s -= tree[i]
                    i &= i - 1
                s %= MOD
                push(s)
                i = ii
                while i <= U:
                    tree[i] += s
                    i += i & -i
            if lo == 6:
                ans = fs[-1]                      # f(6): smallest value, processed last
            f_arr = np.array(fs[::-1], dtype=np.int64)     # aligned with vals
            order = np.argsort(pa, kind='stable')
            P_new, F_new = pa[order], f_arr[order]
            runs.append([0, P_new, F_new,
                         np.concatenate(([0], np.cumsum(F_new)))])
            while len(runs) > 1 and runs[-1][0] == runs[-2][0]:
                lev, P2, F2, _ = runs.pop()
                _, P1, F1, _ = runs.pop()
                Pm = np.concatenate((P1, P2))
                Fm = np.concatenate((F1, F2))
                o = np.argsort(Pm, kind='stable')
                Pm, Fm = Pm[o], Fm[o]
                runs.append([lev + 1, Pm, Fm,
                             np.concatenate(([0], np.cumsum(Fm)))])
        blocks_in_window += 1
        if blocks_in_window >= R and lo > 6:
            for _, P, F, _ in runs:
                np.add.at(counts, P, F)           # totals stay < 2e15, no overflow
            runs = []
            blocks_in_window = 0
            np.cumsum(counts, out=prefix)
        hi = lo

    return ans % MOD

if __name__ == "__main__":
    print(solve())
