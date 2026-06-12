#!/usr/bin/env python3
import math
import numpy as np

def allowed(n):
    # keep n iff its decimal digits never contain 3 equal consecutive digits
    s = str(n)
    return all(not (s[i] == s[i + 1] == s[i + 2]) for i in range(len(s) - 2))

def solve():
    # Baillie-style digit DP.  State of a number = (last digit, run length of
    # that digit capped at 2); appending digit d maps (ld,r) -> (d,1) if d!=ld,
    # (d,2) if d==ld and r==1, and is forbidden if d==ld and r==2.
    # For each state keep the power sums f_j = sum n^{-j} over allowed k-digit
    # numbers in that state.  Appending a digit gives n -> 10n+d and
    #   1/(10n+d)^i = sum_{j>=i} C(j-1,i-1) (-d)^{j-i} 10^{-j} n^{-j},
    # truncated at j<=J (relative error ~(9*10^-m)^J since n >= 10^{m-1}).
    # So the vector of all (state, j) power sums evolves linearly, F -> B*F,
    # with a constant matrix B.  Since the count of allowed k-digit numbers
    # grows like ((9+sqrt(117))/2)^k ~ 9.908^k, the spectral radius of B is
    # ~0.9908 < 1 and the whole tail sums exactly to e1^T (I-B)^{-1} B F.
    m, J = 5, 12

    # exact part: all allowed numbers below 10^m
    s0 = math.fsum(1.0 / n for n in range(1, 10 ** m) if allowed(n))

    # power sums of the m-digit allowed numbers, split by state
    F = np.zeros((20, J))
    for n in range(10 ** (m - 1), 10 ** m):
        if allowed(n):
            s = str(n)
            st = int(s[-1]) * 2 + (1 if s[-1] == s[-2] else 0)
            F[st] += [n ** -j for j in range(1, J + 1)]

    # one-digit-append transfer matrix over (state, power) pairs
    B = np.zeros((20 * J, 20 * J))
    for ld in range(10):
        for run in (1, 2):
            s1 = ld * 2 + run - 1
            for d in range(10):
                if d != ld:
                    s2 = d * 2
                elif run == 1:
                    s2 = d * 2 + 1
                else:
                    continue  # would create a run of 3 equal digits
                for i in range(1, J + 1):
                    for j in range(i, J + 1):
                        B[s2 * J + i - 1, s1 * J + j - 1] += (
                            math.comb(j - 1, i - 1) * (-float(d)) ** (j - i)
                            * 10.0 ** -j)

    # geometric sum of all blocks with more than m digits
    X = np.linalg.solve(np.eye(20 * J) - B, B @ F.reshape(-1))
    tail = X.reshape(20, J)[:, 0].sum()
    return f"{s0 + tail:.10f}"

if __name__ == "__main__":
    print(solve())
