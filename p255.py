#!/usr/bin/env python3
import numpy as np

# Rounded-square-root by integer Heron iteration: x' = floor((x + ceil(n/x))/2).
# Key observation: for a fixed current estimate x, ceil(n/x) is constant (= q)
# on each block n in ((q-1)x, qx].  So all n in such a block move to the same
# next estimate x' = (x+q)//2.  We therefore process whole intervals of n at
# once, splitting them into q-blocks level by level (one level = one Heron
# iteration for every still-active n).  A block terminates when x' == x (that
# final iteration is still counted, as in the problem's example).
# Consecutive q with x+q even give the same x', so blocks pair up; we also
# merge adjacent child blocks with equal x' to keep the arrays small.
# Everything is vectorized with numpy int64 (values < 2^63).

def total_iterations(x0, n_lo, n_hi, chunks=16):
    total = 0
    # split the initial q-range into chunks to bound memory
    q_lo = -(-n_lo // x0)
    q_hi = -(-n_hi // x0)
    bounds = np.linspace(q_lo, q_hi + 1, chunks + 1).astype(np.int64)
    for ci in range(chunks):
        a, b = int(bounds[ci]), int(bounds[ci + 1]) - 1
        if b < a:
            continue
        q = np.arange(a, b + 1, dtype=np.int64)
        X = np.full(q.shape, x0, dtype=np.int64)
        LO = np.maximum((q - 1) * x0 + 1, n_lo)
        HI = np.minimum(q * x0, n_hi)
        Xn = (X + q) >> 1
        while True:
            # every n in every block consumes one iteration this level
            total += int(np.sum(HI - LO + 1))
            keep = Xn != X
            if not np.any(keep):
                break
            X, LO, HI = Xn[keep], LO[keep], HI[keep]
            # merge adjacent blocks with identical estimate and contiguous range
            if X.size > 1:
                same = (X[1:] == X[:-1]) & (LO[1:] == HI[:-1] + 1)
                starts = np.flatnonzero(np.concatenate(([True], ~same)))
                ends = np.concatenate((starts[1:] - 1, [X.size - 1]))
                X, LO, HI = X[starts], LO[starts], HI[ends]
            # split each block into q-blocks (q = ceil(n/X))
            ql = (LO + X - 1) // X
            qh = (HI + X - 1) // X
            nq = qh - ql + 1
            S = int(nq.sum())
            rep = np.repeat(np.arange(X.size), nq)
            base = np.concatenate(([0], np.cumsum(nq)[:-1]))
            qc = ql[rep] + (np.arange(S, dtype=np.int64) - base[rep])
            Xp = X[rep]
            X = Xp
            LO = np.maximum(LO[rep], (qc - 1) * Xp + 1)
            HI = np.minimum(HI[rep], qc * Xp)
            Xn = (Xp + qc) >> 1
    return total

def solve():
    n_lo, n_hi = 10 ** 13, 10 ** 14 - 1   # all 14-digit numbers
    x0 = 7 * 10 ** 6                       # d = 14 even -> x0 = 7*10^(d-2)/2
    total = total_iterations(x0, n_lo, n_hi)
    cnt = n_hi - n_lo + 1
    # round total/cnt to 10 decimal places with exact integer arithmetic
    scaled = (total * 10 ** 10 * 2 + cnt) // (2 * cnt)
    return f"{scaled // 10 ** 10}.{scaled % 10 ** 10:010d}"

if __name__ == "__main__":
    print(solve())
