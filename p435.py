MOD = 1307674368000  # 15!
N = 10 ** 15


def mat_mul(A, B, m):
    # 3x3 matrix product mod m
    return [[sum(A[i][k] * B[k][j] for k in range(3)) % m for j in range(3)]
            for i in range(3)]


def mat_pow(M, e, m):
    R = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    while e:
        if e & 1:
            R = mat_mul(R, M, m)
        M = mat_mul(M, M, m)
        e >>= 1
    return R


def F(n, x, m):
    # a_i = f_i * x^i satisfies a_i = x*a_{i-1} + x^2*a_{i-2}; S_n = sum a_i.
    # State v_n = (a_{n+1}, a_n, S_n), v_0 = (x, 0, 0), v_{n+1} = M v_n.
    xm = x % m
    M = [[xm, xm * xm % m, 0], [1, 0, 0], [1, 0, 1]]
    P = mat_pow(M, n, m)
    # S_n = third row of P applied to v_0
    return (P[2][0] * xm + P[2][1] * 0 + P[2][2] * 0) % m


def solve():
    # sanity check from the statement: F_7(11) = 268357683
    assert F(7, 11, 10 ** 12) == 268357683
    return sum(F(N, x, MOD) for x in range(101)) % MOD


if __name__ == "__main__":
    print(solve())
