#!/usr/bin/env python3
# Project Euler 326 - Modulo Summations
#
# f(N,M) counts pairs (p,q) with sum a_p..a_q == 0 (mod M), i.e. pairs of
# equal values among the prefix sums S_0..S_N mod M, so f = sum C(cnt_v, 2).
#
# Empirically (verified against the recurrence for n <= 3*10^5), a_n is
# exactly linear in n with period-12 coefficients:
#   n mod 12 in {0,2,6,8}: a_n = n/2          {1,7}:  a_n = (2n+1)/3
#   n mod 12 in {3,9}:     a_n = (n-3)/6      {5,11}: a_n = (n-5)/6
#   n mod 12 in {4,10}:    a_n = n-1
# Hence S_n is quadratic in n on each class mod 12, and a quadratic mod M
# is periodic in its argument with period M, so S_n mod M has period
# L = 12*M. Tally residue counts over one period (numpy), scale by the
# number of full periods in N+1 terms plus the remainder, then sum C(c,2).

import numpy as np

def prefix_residues(L, M):
    """S_0..S_L mod M using the closed form for a_n."""
    nn = np.arange(1, L + 1, dtype=np.int64)
    r = nn % 12
    a = np.where(np.isin(r, (0, 2, 6, 8)), nn // 2,
        np.where(np.isin(r, (1, 7)), (2 * nn + 1) // 3,
        np.where(np.isin(r, (3, 9)), (nn - 3) // 6,
        np.where(np.isin(r, (5, 11)), (nn - 5) // 6, nn - 1))))
    return np.concatenate(([0], np.cumsum(a % M) % M))

def f(N, M):
    L = 12 * M
    S = prefix_residues(L, M)          # S_0..S_L
    assert S[L] == 0                   # confirms period L
    total = N + 1                      # residues S_0..S_N
    reps, rem = divmod(total, L)
    base = np.bincount(S[:L], minlength=M)
    extra = np.bincount(S[:rem], minlength=M)
    return sum(c * (c - 1) // 2 for c in (reps * base + extra).tolist())

def solve():
    # sanity check the closed form against the literal recurrence
    T, a1 = 0, []
    for n in range(1, 2001):
        an = 1 if n == 1 else T % n
        a1.append(an)
        T += n * an
    Schk = prefix_residues(2000, 10 ** 9)
    assert all(int(Schk[n] - Schk[n - 1]) == a1[n - 1] for n in range(1, 2001))

    assert f(10, 10) == 4
    assert f(10 ** 4, 10 ** 3) == 97158
    return f(10 ** 12, 10 ** 6)

if __name__ == "__main__":
    print(solve())
