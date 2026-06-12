#!/usr/bin/env python3
from math import isqrt

def sum_floor_sqrt(j, n, a0):
    # sum_{x=1}^{n} floor(sqrt(j)*x) for non-square j, via the Euclidean-like
    # recursion S(alpha,n) = a*n(n+1)/2 + n*m - S(1/(alpha-a), m) with
    # a = floor(alpha), m = floor(alpha*n) - a*n.  The successive alphas are
    # exactly the continued-fraction states (sqrt(j)+b)/c of sqrt(j), so each
    # step needs only small integers plus one isqrt for floor(alpha*n).
    b, c = 0, 1
    total = 0
    sign = 1
    while n:
        a = (a0 + b) // c
        m = (isqrt(j * n * n) + b * n) // c - a * n  # floor(frac(alpha)*n)
        total += sign * (a * n * (n + 1) // 2 + n * m)
        sign = -sign
        b = a * c - b
        c = (j - b * b) // c
        n = m
    return total

def P(j, M, N):
    # number of lattice points with M < x <= N, M < y <= N and y < sqrt(j)*x
    s = isqrt(j)
    if s * s == j:
        # sqrt(j) = s integer: y <= s*x - 1
        B0 = N // s                       # s*x <= N exactly for x <= B0
        res = (N - min(max(B0, M), N)) * (N - M)   # x with s*x > N: full rows
        A = max(M + 1, (M + 1) // s + 1)  # smallest x with s*x - 1 > M
        B = min(B0, N)
        if A <= B:
            cnt = B - A + 1
            res += s * (A + B) * cnt // 2 - (M + 1) * cnt
        return res
    # irrational slope: y < sqrt(j)*x <=> y <= floor(sqrt(j)*x)
    B0 = isqrt(j * N * N) // j            # floor(N/sqrt(j)); x > B0 => row full
    res = (N - min(max(B0, M), N)) * (N - M)
    A0 = isqrt(j * (M + 1) * (M + 1)) // j  # floor((M+1)/sqrt(j))
    A = max(M + 1, A0 + 1)                # smallest x with floor(sqrt(j)x) > M
    B = min(B0, N)
    if A <= B:
        res += (sum_floor_sqrt(j, B, s) - sum_floor_sqrt(j, A - 1, s)
                - M * (B - A + 1))
    return res

def R(M, N):
    # floor(y^2/x^2) = k  <=>  sqrt(k)*x <= y < sqrt(k+1)*x, so the count for
    # odd k is P(k+1) - P(k) and summing over odd k gives the alternating sum
    # R = sum_{j>=1} (-1)^j P(j), truncated once floor(y^2/x^2) can't reach j.
    kmax = (N * N) // ((M + 1) * (M + 1))
    if kmax % 2 == 0:
        kmax -= 1
    total = 0
    for j in range(1, kmax + 2):
        total += P(j, M, N) if j % 2 == 0 else -P(j, M, N)
    return total

def solve():
    return R(2 * 10 ** 6, 10 ** 9)

if __name__ == "__main__":
    print(solve())
