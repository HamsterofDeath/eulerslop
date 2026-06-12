#!/usr/bin/env python3

def solve():
    # 12x^2+7xy-12y^2 = (3x+4y)(4x-3y) = 625.  In u=3x+4y, v=4x-3y the curve
    # is uv=625; a chord through parameters t_a,t_b (t = u-coordinate) has
    # slope -625/(t_a*t_b), so "P_i P_{i-1} parallel to P_{i-2} X" means
    # t_i*t_{i-1} = t_X*t_{i-2}, i.e. t_i = 25*t_{i-2}/t_{i-1}  (t_X = 25).
    # With s_i = t_i/25 (s_1=4, s_2=-3/2) we get s_i = s_{i-2}/s_{i-1}, so
    # s_n = s_1^{(-1)^{n+1}F_{n-2}} * s_2^{(-1)^n F_{n-1}}.  For odd n:
    #   t_n = eps * 25 * 2^M / 3^B,  A=F_{n-2}, B=F_{n-1}, M=2A+B, eps=(-1)^B.
    # Back-substituting x=(3u+4v)/25, y=(4u-3v)/25 and reducing (numerators
    # are coprime to 6 after pulling out the factor 12 from x's numerator):
    #   x = eps*(2^{2M-2}+3^{2B-1}) / (2^{M-2}*3^{B-1})
    #   y = eps*(2^{2M+2}-3^{2B+1}) / (2^M*3^B)
    MOD = 1_000_000_007

    def fib_pair(k, m):
        # (F_k, F_{k+1}) mod m by fast doubling
        if k == 0:
            return 0 % m, 1 % m
        a, b = fib_pair(k >> 1, m)
        c = a * (2 * b - a) % m
        d = (a * a + b * b) % m
        return ((d, (c + d) % m) if k & 1 else (c, d))

    def answer(n):
        # n must be odd; F_{n-1} is even iff 3 | (n-1)
        assert n & 1
        A, B = fib_pair(n - 2, MOD - 1)  # exponents mod MOD-1 (Fermat)
        eps = 1 if (n - 1) % 3 == 0 else -1
        M = (2 * A + B) % (MOD - 1)
        e = lambda base, exp: pow(base, exp % (MOD - 1), MOD)
        a = eps * (e(2, 2 * M - 2) + e(3, 2 * B - 1)) % MOD
        b = e(2, M - 2) * e(3, B - 1) % MOD
        c = eps * (e(2, 2 * M + 2) - e(3, 2 * B + 1)) % MOD
        d = e(2, M) * e(3, B) % MOD
        return (a + b + c + d) % MOD

    assert answer(7) == 806236837  # statement's check value
    return answer(11 ** 14)


if __name__ == "__main__":
    print(solve())
