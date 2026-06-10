#!/usr/bin/env python3
import numpy as np


def solve():
    M = 20300713
    S0 = 14025256
    K = 2 * 10**15

    # Generate one full period of the Blum Blum Shub sequence.
    # (The sequence returns to s0, i.e. it is purely periodic.)
    parts = []
    s = S0
    while True:
        parts.append(str(s))
        s = s * s % M
        if s == S0:
            break
    w = "".join(parts)
    n = len(w)  # digits per period

    # Digit values and prefix sums C(0..n); S = digit sum of one period.
    digits = np.frombuffer(w.encode(), dtype=np.uint8).astype(np.int64) - 48
    c = np.empty(n + 1, dtype=np.int64)
    c[0] = 0
    np.cumsum(digits, out=c[1:])
    s_total = int(c[n])

    # A substring starting at position i (1-based) has digit sums
    # {C(j) - C(i-1) : j >= i}.  Over one period window these sums are
    # exactly the values in (0, S] of the form v - C(i-1) with v a prefix
    # value, and appending whole periods adds multiples of S.  Hence k is
    # achievable from i  iff  s = ((k-1) mod S) + 1 is achievable, so
    # p(k) = first_pos[s].  Since C is non-decreasing, v = C(i-1) + s > C(i-1)
    # guarantees the matching prefix index is >= i, and minimizing the start
    # position is the same as minimizing the prefix value c = C(i-1).
    cvals, cidx = np.unique(c[:n], return_index=True)  # distinct prefix values, first index
    vall = np.concatenate([cvals, cvals + s_total])  # all prefix values below 2S, sorted

    first_pos = np.zeros(s_total + 1, dtype=np.int32)
    remaining = s_total
    leftover = None
    for j in range(len(cvals)):
        cv = int(cvals[j])
        pos = int(cidx[j]) + 1
        lo = np.searchsorted(vall, cv, side="right")
        hi = np.searchsorted(vall, cv + s_total, side="right")
        sv = vall[lo:hi] - cv  # sums in (0, S] achievable from position pos
        new = sv[first_pos[sv] == 0]
        first_pos[new] = pos
        remaining -= new.size
        if remaining == 0:
            break
        if j >= 5000:
            leftover = np.nonzero(first_pos[1:] == 0)[0] + 1
            break

    if remaining and leftover is not None:
        # Fallback for stragglers: for each unfilled s find the smallest
        # prefix value cv with cv + s among the prefix values.
        for s_val in leftover:
            cand = np.intersect1d(cvals, vall - int(s_val))
            if cand.size:
                j = int(np.searchsorted(cvals, cand[0]))
                first_pos[s_val] = int(cidx[j]) + 1

    # Sanity check from the problem statement: sum of p(k) for k <= 1000.
    assert int(first_pos[1:1001].sum(dtype=np.int64)) == 4742

    # Sum p(k) for k = 1..K using the period S of p in k.
    full_cycles, rem = divmod(K, s_total)
    sum_all = int(first_pos[1:].sum(dtype=np.int64))
    sum_rem = int(first_pos[1:rem + 1].sum(dtype=np.int64))
    return full_cycles * sum_all + sum_rem


if __name__ == "__main__":
    print(solve())
