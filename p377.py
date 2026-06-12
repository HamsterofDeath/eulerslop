#!/usr/bin/env python3

MOD = 10 ** 9

def mat_mul(A, B):
    n = len(A)
    Bt = list(zip(*B))
    return [[sum(a * b for a, b in zip(row, col)) % MOD for col in Bt]
            for row in A]

def mat_pow(M, e):
    n = len(M)
    R = [[int(i == j) for j in range(n)] for i in range(n)]
    while e:
        if e & 1:
            R = mat_mul(R, M)
        M = mat_mul(M, M)
        e >>= 1
    return R

def solve():
    # Build numbers by appending a last digit d in 1..9: a number with digit
    # sum n is (prefix with digit sum n-d) * 10 + d, where the empty prefix
    # (c(0)=1, s(0)=0) yields the single digit d.  Hence for n >= 1
    #   c(n) = sum_{d=1..9} c(n-d)
    #   s(n) = sum_{d=1..9} (10*s(n-d) + d*c(n-d))
    # with c(m)=s(m)=0 for m<0.  This is a linear map on the 18-vector
    # v(n) = (c(n..n-8), s(n..n-8)), so v(N) = M^N v(0) with
    # v(0) = e_0.  f(13^i) mod 1e9 is the s-component (index 9) of M^(13^i) e_0,
    # and M^(13^i) is obtained by repeatedly raising to the 13th power.
    M = [[0] * 18 for _ in range(18)]
    for d in range(1, 10):
        M[0][d - 1] += 1            # c(n) += c(n-d)
        M[9][d - 1] += d            # s(n) += d*c(n-d)
        M[9][9 + d - 1] += 10       # s(n) += 10*s(n-d)
    for i in range(1, 9):           # shift registers
        M[i][i - 1] = 1
        M[9 + i][9 + i - 1] = 1

    total = 0
    A = mat_pow(M, 13)              # A = M^(13^1)
    for _ in range(17):
        total = (total + A[9][0]) % MOD   # s(13^i) = (M^(13^i) e_0)[9]
        A = mat_pow(A, 13)          # M^(13^(i+1))
    return total % MOD

if __name__ == "__main__":
    print(solve())
