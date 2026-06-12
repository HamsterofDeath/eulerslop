#!/usr/bin/env python3

def solve():
    # g(x) = x^3 - 2^n x^2 + n has three real roots a > b > 0 > c > -1 with
    # b <= 1 (g(0) = n > 0, g(1) = 1 - 2^n + n <= 0) and a the largest.
    # The power sums s_k = a^k + b^k + c^k are integers satisfying
    #   s_k = 2^n s_{k-1} - n s_{k-3},   s_0 = 3, s_1 = 2^n, s_2 = 4^n
    # (from e1 = 2^n, e2 = 0, e3 = -n).  Since b + c = 2^n - a > 0 we have
    # b > |c|, so for odd k the term b^k + c^k = b^k - |c|^k lies strictly
    # in (0, 1), hence floor(a^k) = s_k - 1.  Compute s_K mod 10^8 with a
    # 3x3 companion-matrix power.
    MOD = 10 ** 8
    K = 987654321

    def mat_mul(A, B):
        return [[sum(A[i][k] * B[k][j] for k in range(3)) % MOD
                 for j in range(3)] for i in range(3)]

    def mat_pow(A, e):
        R = [[int(i == j) for j in range(3)] for i in range(3)]
        while e:
            if e & 1:
                R = mat_mul(R, A)
            A = mat_mul(A, A)
            e >>= 1
        return R

    total = 0
    for n in range(1, 31):
        A = [[pow(2, n, MOD), 0, (-n) % MOD],
             [1, 0, 0],
             [0, 1, 0]]
        P = mat_pow(A, K - 2)
        s2, s1, s0 = pow(2, 2 * n, MOD), pow(2, n, MOD), 3
        s_K = (P[0][0] * s2 + P[0][1] * s1 + P[0][2] * s0) % MOD
        total += s_K - 1
    return total % MOD

if __name__ == "__main__":
    print(solve())
