#!/usr/bin/env python3
import numpy as np

def S(N, primes1mod4, H):
    # T(R) = number of integer-sided triangles with circumradius exactly R.
    #
    # A triangle with integer sides a,b,c and circumradius R has sin A = a/(2R)
    # and cos A = (b^2+c^2-a^2)/(2bc), so each angle A gives a rational point
    # z = e^{iA} on the unit circle.  The reduced denominator q of such a point
    # is odd with all prime factors ≡ 1 mod 4, and a = 2R*sinA is an integer
    # iff q | R.  Rational points form the group <i> x (free abelian group with
    # one generator u_p = (pi_p/conj(pi_p)) per prime p ≡ 1 mod 4, where
    # p = pi_p * conj(pi_p) in Z[i]); the denominator of i^t * prod u_p^{e_p}
    # is prod p^{|e_p|}.  Hence T(R) depends only on the exponents c_1..c_k of
    # the primes ≡ 1 mod 4 in R.
    #
    # Counting: pass to central angles zeta = e^{2iA} = sigma * w(f)^2 with
    # sign sigma and exponent vector f, |f_j| <= c_j.  Ordered triples with
    # zeta1*zeta2*zeta3 = 1, all zeta != 1, split evenly into angle sums pi
    # and 2pi (conjugation is a fixed-point-free involution swapping them), so
    # the ordered triangle count is
    #   M = 2*prod(3c^2+3c+1) - 3*prod(2c+1) + 1
    # (prod(3c^2+3c+1) counts f1+f2+f3 = 0 in the box, 4 sign choices with
    # sigma1*sigma2*sigma3 = 1, minus inclusion-exclusion for zeta_X = 1, all
    # halved).  Equilateral is impossible (sin 60 irrational); isosceles
    # multisets number I = prod(2*floor(c/2)+1) - 1 (apex angle A < pi/2 with
    # 2f in the box).  Unordered count: T = (M + 3I)/6.
    #
    # S(N) = sum over q = products of primes ≡ 1 mod 4 (q <= N) of
    #        T(sig(q)) * q * H(N//q),
    # where H(x) sums the integers <= x with no prime factor ≡ 1 mod 4
    # (the possible cofactors R/q).
    total = 0
    np1 = len(primes1mod4)

    def dfs(i, q, PM, PL, PI):
        nonlocal total
        # 6*T for the signature accumulated in the partial products
        t6 = 2 * PM - 3 * PL + 3 * PI - 2
        if t6:
            total += t6 * q * int(H[N // q])
        for j in range(i, np1):
            p = primes1mod4[j]
            qq = q * p
            if qq > N:
                break
            c = 1
            while qq <= N:
                dfs(j + 1, qq,
                    PM * (3 * c * c + 3 * c + 1),
                    PL * (2 * c + 1),
                    PI * (2 * (c // 2) + 1))
                qq *= p
                c += 1

    dfs(0, 1, 1, 1, 1)
    assert total % 6 == 0
    return total // 6

def solve():
    N = 10 ** 7

    # primes up to N
    sieve = np.ones(N + 1, dtype=bool)
    sieve[:2] = False
    for i in range(2, int(N ** 0.5) + 1):
        if sieve[i]:
            sieve[i * i::i] = False
    primes = np.flatnonzero(sieve)
    p1 = primes[primes % 4 == 1]

    # H[x] = sum of m <= x with no prime factor ≡ 1 mod 4
    free = np.ones(N + 1, dtype=bool)
    free[0] = False
    for p in p1.tolist():
        free[p::p] = False
    H = np.cumsum(np.where(free, np.arange(N + 1, dtype=np.int64), 0))

    p1_list = p1.tolist()
    # sanity checks from the problem statement
    assert S(100, p1_list, H) == 4950
    assert S(1200, p1_list, H) == 1653605
    return S(N, p1_list, H)

if __name__ == "__main__":
    print(solve())
