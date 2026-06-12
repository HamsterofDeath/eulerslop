#!/usr/bin/env python3
from fractions import Fraction

def solve():
    # A set with max element s_k generates a polygon iff it has >= 3 elements
    # and the other elements sum to more than s_k.  So with
    #   C_k = #{A subset of {s_1..s_{k-1}} : sum(A) <= s_k}
    # (empty set and singletons included; all s_i < s_k are automatically
    # allowed singletons) the good subsets with maximum s_k number
    #   G_k = (2^{k-1} - 1 - (k-1)) - (C_k - 1 - (k-1)) = 2^{k-1} - C_k,
    # hence f(n) = sum_{k=3}^n G_k = 2^n - 4 - sum_{k=3}^n C_k.
    N = 10 ** 18
    MOD = 10 ** 9

    # the sequence and its prefix sums (note sum_{i<=n} s_i = s_{n+3} - 3)
    K = 45
    s = [0, 1, 2, 3]
    while len(s) <= K + 1:
        s.append(s[-1] + s[-3])
    P = [0] * len(s)
    for i in range(1, len(s)):
        P[i] = P[i - 1] + s[i]

    # exact count of subsets of {s_1..s_i} with sum <= b; the geometric
    # growth of s keeps the number of reachable (i, b) states tiny
    memo = {}
    def count(i, b):
        if b < 0:
            return 0
        if b >= P[i]:
            return 1 << i
        if i == 0:
            return 1
        r = memo.get((i, b))
        if r is None:
            r = count(i - 1, b) + count(i - 1, b - s[i])
            memo[(i, b)] = r
        return r

    C = [count(k - 1, s[k]) for k in range(3, K + 1)]  # C[t] = C_{t+3}

    # sanity check against the values given in the problem statement
    for n, expected in ((5, 7), (10, 501), (25, 18635853)):
        assert sum((1 << (k - 1)) - C[k - 3] for k in range(3, n + 1)) == expected

    # C_k has a rational generating function, so it satisfies a linear
    # recurrence with integer coefficients; find the minimal one exactly
    def find_recurrence():
        for d in range(1, 16):
            A = [[Fraction(C[n - j]) for j in range(1, d + 1)] + [Fraction(C[n])]
                 for n in range(d, 2 * d)]
            ok = True
            for col in range(d):  # Gauss-Jordan over Q
                piv = next((r for r in range(col, d) if A[r][col]), None)
                if piv is None:
                    ok = False
                    break
                A[col], A[piv] = A[piv], A[col]
                pv = A[col][col]
                A[col] = [x / pv for x in A[col]]
                for r in range(d):
                    if r != col and A[r][col]:
                        f = A[r][col]
                        A[r] = [a - f * b for a, b in zip(A[r], A[col])]
            if not ok:
                continue
            c = [A[i][d] for i in range(d)]
            if all(x.denominator == 1 for x in c) and all(
                    C[n] == sum(c[j - 1] * C[n - j] for j in range(1, d + 1))
                    for n in range(d, len(C))):
                return [int(x) for x in c]
        raise AssertionError("no recurrence found")

    rec = find_recurrence()
    d = len(rec)

    # advance (C_k, ..., C_{k-d+1}, S_k) with S_k = sum_{j=3}^k C_j by
    # matrix power; recurrence verified valid for all computed k >= 3 + d
    D = d + 1
    M = [[0] * D for _ in range(D)]
    for j in range(d):
        M[0][j] = rec[j] % MOD          # C_{k+1} row
        M[D - 1][j] = rec[j] % MOD      # S_{k+1} = S_k + C_{k+1}
    for i in range(1, d):
        M[i][i - 1] = 1                 # shift
    M[D - 1][D - 1] = 1

    def mat_mul(X, Y):
        return [[sum(X[i][t] * Y[t][j] for t in range(D)) % MOD
                 for j in range(D)] for i in range(D)]

    def mat_vec(X, v):
        return [sum(X[i][t] * v[t] for t in range(D)) % MOD for i in range(D)]

    base = 3 + d - 1                    # k = base, with history C_base..C_3
    v = [C[base - 3 - i] % MOD for i in range(d)] + [sum(C[:base - 2]) % MOD]
    e = N - base
    R = [[int(i == j) for j in range(D)] for i in range(D)]
    while e:
        if e & 1:
            R = mat_mul(R, M)
        M = mat_mul(M, M)
        e >>= 1
    S = mat_vec(R, v)[D - 1]

    return (pow(2, N, MOD) - 4 - S) % MOD

if __name__ == "__main__":
    print(solve())
