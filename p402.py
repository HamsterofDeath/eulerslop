"""Project Euler 402: Integer-valued polynomials.

M(a,b,c) = largest m dividing n^4 + a n^3 + b n^2 + c n for all n.
Since m divides the 4th finite difference (= 24), M | 24 and M depends
only on (a,b,c) mod 24.  Hence S(N) = sum_{0<a,b,c<=N} M is, with
N = 24q + s, an exact cubic in q with integer coefficients per s.

Sum S(F_k) for 2 <= k <= 1234567890123: F_k mod 24 has period 24 in k,
so per residue class j of k the term is a fixed cubic polynomial in F_k.
Track cubic monomials of (F_{k+1}, F_k) plus an accumulator in an 11x11
linear map advancing k by 24; matrix exponentiation mod 24^3 * 10^9
(numerators are divisible by 24^3 = 13824; divide at the end).
"""
from math import gcd
import numpy as np


def solve():
    P = 24
    K = 1234567890123
    MODBASE = 10**9
    mmod = 13824 * MODBASE  # 24^3 * 10^9

    # M table over residues mod 24: M = gcd(24, f(1), ..., f(24))
    M = np.zeros((P, P, P), dtype=np.int64)
    n4 = [n**4 for n in range(1, P + 1)]
    n3 = [n**3 for n in range(1, P + 1)]
    n2 = [n * n for n in range(1, P + 1)]
    n1 = list(range(1, P + 1))
    for a in range(P):
        for b in range(P):
            for c in range(P):
                g = 24
                for i in range(P):
                    g = gcd(g, n4[i] + a * n3[i] + b * n2[i] + c * n1[i])
                    if g == 1:
                        break
                M[a][b][c] = g

    # S(24q + s) = T q^3 + Bs[s] q^2 + Cs[s] q + Ds[s]
    # (counts of each residue in 1..N are q, plus 1 for residues 1..s)
    T = int(M.sum())
    m_a = M.sum(axis=(1, 2)); m_b = M.sum(axis=(0, 2)); m_c = M.sum(axis=(0, 1))
    m_ab = M.sum(axis=2); m_ac = M.sum(axis=1); m_bc = M.sum(axis=0)
    Bs = [0] * P; Cs = [0] * P; Ds = [0] * P
    for s in range(P):
        sl = slice(1, s + 1)
        Bs[s] = int(m_a[sl].sum() + m_b[sl].sum() + m_c[sl].sum())
        Cs[s] = int(m_ab[sl, sl].sum() + m_ac[sl, sl].sum() + m_bc[sl, sl].sum())
        Ds[s] = int(M[sl, sl, sl].sum())

    def S(N):
        q, s = divmod(N, P)
        return T * q**3 + Bs[s] * q * q + Cs[s] * q + Ds[s]

    assert S(10) == 1972 and S(10000) == 2024258331114

    def mat_mul(A, B, mod):
        Bt = list(zip(*B))
        return [[sum(x * y for x, y in zip(row, col)) % mod for col in Bt]
                for row in A]

    def mat_pow(A, e, mod):
        n = len(A)
        R = [[int(i == j) for j in range(n)] for i in range(n)]
        while e:
            if e & 1:
                R = mat_mul(R, A, mod)
            A = mat_mul(A, A, mod)
            e >>= 1
        return R

    # step-24 Fibonacci matrix: (F_{k+25}, F_{k+24}) = A2 (F_{k+1}, F_k)
    A2 = mat_pow([[1, 1], [1, 0]], P, mmod)
    al, be, ga, de = A2[0][0], A2[0][1], A2[1][0], A2[1][1]

    def build_mat(c3, c2, c1, c0, mod):
        # state: [x^3, x^2 y, x y^2, y^3, x^2, xy, y^2, x, y, 1, S]
        a, b, g, d = al, be, ga, de
        rows = [
            [a**3, 3*a*a*b, 3*a*b*b, b**3, 0, 0, 0, 0, 0, 0, 0],
            [a*a*g, a*a*d + 2*a*b*g, 2*a*b*d + b*b*g, b*b*d, 0, 0, 0, 0, 0, 0, 0],
            [a*g*g, 2*a*g*d + b*g*g, a*d*d + 2*b*g*d, b*d*d, 0, 0, 0, 0, 0, 0, 0],
            [g**3, 3*g*g*d, 3*g*d*d, d**3, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, a*a, 2*a*b, b*b, 0, 0, 0, 0],
            [0, 0, 0, 0, a*g, a*d + b*g, b*d, 0, 0, 0, 0],
            [0, 0, 0, 0, g*g, 2*g*d, d*d, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, a, b, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, g, d, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
            [0, 0, 0, c3, 0, 0, c2, 0, c1, c0, 1],  # S += poly(y), y = F_k
        ]
        return [[v % mod for v in r] for r in rows]

    FIB = [0, 1]
    for _ in range(28):
        FIB.append(FIB[-1] + FIB[-2])

    total = 0
    for j in range(P):
        k0 = j if j >= 2 else j + P  # smallest k >= 2 with k = j mod 24
        nj = (K - k0) // P + 1       # number of terms in this class
        s = FIB[k0] % P              # F_k mod 24, constant on the class
        # 13824 * S(F) = T(F-s)^3 + 24 B (F-s)^2 + 576 C (F-s) + 13824 D
        c3 = T
        c2 = -3*T*s + 24*Bs[s]
        c1 = 3*T*s*s - 48*Bs[s]*s + 576*Cs[s]
        c0 = -T*s**3 + 24*Bs[s]*s*s - 576*Cs[s]*s + 13824*Ds[s]
        Pm = mat_pow(build_mat(c3, c2, c1, c0, mmod), nj, mmod)
        x, y = FIB[k0 + 1] % mmod, FIB[k0] % mmod
        u0 = [x**3 % mmod, x*x*y % mmod, x*y*y % mmod, y**3 % mmod,
              x*x % mmod, x*y % mmod, y*y % mmod, x, y, 1, 0]
        total = (total + sum(Pm[10][i] * u0[i] for i in range(11))) % mmod

    assert total % 13824 == 0
    return (total // 13824) % MODBASE


if __name__ == "__main__":
    print(solve())
