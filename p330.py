#!/usr/bin/env python3
# Project Euler 330 - Euler's Number
#
# Writing a(n) = (A(n)e + B(n))/n!, the defining sum gives (EGFs):
#   A_hat(x) = 1/((1-x)(2-e^x)),  B_hat(x) = -e^x * A_hat(x)
# 1/(2-e^x) is the EGF of the Fubini (ordered Bell) numbers Fub(k), and
# 1/(1-x) is the EGF of n!, so
#   A(n) = sum_{k=0..n} n!/k! * Fub(k)
#   B(n) = -sum_{k=0..n} C(n,k) * A(k)        (call this -G(n))
#
# 77777777 = 7 * 11 * 73 * 101 * 137 (all small primes), so work mod each
# prime p and CRT. In the Hurwitz (binomial-convolution) series ring over
# F_p, e^x satisfies (e^x)^p = e^{px} = 1, so t = e^x is a p-th root of
# unity and 1/(2-t) = sum_{k<p} 2^{-k} t^k mod (t^p - 1). Reading off the
# n-th Hurwitz coefficient of t^k = e^{kx} (which is k^n) gives
#   Fub(n) == sum_{k=0}^{p-1} 2^{-k} k^n (mod p)        (0^0 = 1)
# The 1/(1-x) factor contributes falling factorials, which vanish mod p
# beyond p terms:
#   A(n) == sum_{m=0}^{p-1} fall(n,m) * Fub(n-m)            (mod p)
#   G(n) == sum_{m=0}^{p-1} fall(n,m) * Fub2(n-m)           (mod p)
# where fall(n,m) = n(n-1)...(n-m+1) and Fub2 uses coefficients of
# t * (1/(2-t)) mod (t^p - 1), i.e. the e^x-shifted Fubini power sum.
# Answer = A(N) + B(N) = A(N) - G(N) mod 77777777, N = 10^9.

from math import comb, factorial

def powmod_cyclic(k, s, p):
    """k^s mod p for s >= 0 using k^(p-1) = 1; 0^0 = 1."""
    if k == 0:
        return 1 if s == 0 else 0
    if s == 0:
        return 1
    e = s % (p - 1)
    if e == 0:
        e = p - 1
    return pow(k, e, p)

def S_mod_p(n, p):
    """(A(n) - G(n)) mod p via the power-sum formulas."""
    inv2 = pow(2, p - 2, p)
    u = [pow(inv2, k, p) for k in range(p)]          # 1/(2-t) coefficients
    v = [u[-1]] + u[:-1]                             # t/(2-t) mod (t^p - 1)

    def F(coeffs, s):
        # value at Hurwitz index s of sum coeffs[k] * e^{kx}
        return sum(c * powmod_cyclic(k, s, p) for k, c in enumerate(coeffs)) % p

    total = 0
    fall = 1
    for m in range(min(p, n + 1)):
        if m:
            fall = fall * ((n - m + 1) % p) % p
        s = n - m
        total = (total + fall * ((F(u, s) - F(v, s)) % p)) % p
    return total

def crt(rems, mods):
    x, M = 0, 1
    for r, m in zip(rems, mods):
        t = (r - x) * pow(M, -1, m) % m
        x += M * t
        M *= m
    return x % M

def solve():
    primes = [7, 11, 73, 101, 137]
    MOD = 77777777
    assert primes[0] * primes[1] * primes[2] * primes[3] * primes[4] == MOD

    # self-check the mod-p machinery against the exact recurrences
    NCHK = 30
    A = [1] + [0] * NCHK
    for n in range(1, NCHK + 1):
        A[n] = sum(comb(n, i) * A[n - i] for i in range(1, n + 1)) + factorial(n)
    S = [A[n] - sum(comb(n, k) * A[k] for k in range(n + 1)) for n in range(NCHK + 1)]
    for p in primes:
        for n in range(NCHK + 1):
            assert S_mod_p(n, p) == S[n] % p, (p, n)
    assert S[10] == 328161643 - 652694486  # a(10) from the statement

    N = 10 ** 9
    rems = [S_mod_p(N, p) for p in primes]
    return crt(rems, primes)

if __name__ == "__main__":
    print(solve())
