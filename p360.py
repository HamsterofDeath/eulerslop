#!/usr/bin/env python3
import numpy as np

def manhattan_sum(R):
    # S(R) = sum over lattice points on x^2+y^2+z^2 = R^2 of |x|+|y|+|z|.
    # By symmetry S(R) = 3 * sum |z| = 6 * sum_{z=1}^{R} z * r2(R^2 - z^2),
    # where r2(n) counts (x,y) with x^2+y^2 = n (r2(0) = 1).
    # r2(n) = 4 * prod_{p|n, p%4==1} (e_p+1) if every prime p%4==3 divides n
    # to an even power, else 0.
    # R^2 - z^2 = (R-z)(R+z) and gcd(R-z, R+z) divides 2R, so for R = 5^10
    # the two factors share no primes except possibly 2 and 5.  Hence with
    # n = 2^a * 5^v * m (m coprime to 10), P(n) = prod_{p|m, p%4==1}(e_p+1),
    # Q(n) = [all p%4==3 exponents in m even]:
    #   r2((R-z)(R+z)) = 4 * (v5(R-z)+v5(R+z)+1) * P(R-z) * P(R+z)
    # when Q(R-z) and Q(R+z) hold, else 0.
    N = 2 * R
    rem = np.arange(N + 1, dtype=np.int64)
    P = np.ones(N + 1, dtype=np.int32)
    Q = np.ones(N + 1, dtype=bool)
    v5 = np.zeros(N + 1, dtype=np.int8)

    # primes up to sqrt(N); leftovers after dividing them out are prime
    lim = int(N ** 0.5) + 1
    sieve = np.ones(lim + 1, dtype=bool)
    sieve[:2] = False
    for i in range(2, int(lim ** 0.5) + 1):
        if sieve[i]:
            sieve[i * i::i] = False
    primes = np.flatnonzero(sieve)

    for p in primes:
        p = int(p)
        cnt = N // p
        e = np.ones(cnt, dtype=np.int8)  # exponent of p in p, 2p, 3p, ...
        q = p * p
        while q <= N:
            step = q // p
            e[step - 1::step] += 1  # multiples of q get one more
            q *= p
        rem[p::p] //= np.power(p, e.astype(np.int64))
        if p == 5:
            v5[5::5] = e
        elif p % 4 == 1:
            P[p::p] *= (e.astype(np.int32) + 1)
        elif p % 4 == 3:
            Q[p::p] &= (e & 1) == 0
        del e

    big = rem > 1  # leftover prime > sqrt(N), exponent 1 (cannot be 2 or 5)
    bp = rem[big] & 3
    P[big] *= np.where(bp == 1, 2, 1).astype(np.int32)
    Q[big] &= bp == 1
    del rem, big, bp

    # accumulate 6 * sum z * r2((R-z)(R+z)) in chunks; z = R gives r2(0) = 1
    total = 6 * R
    CH = 1 << 21
    for lo in range(1, R, CH):
        hi = min(lo + CH, R)
        z = np.arange(lo, hi, dtype=np.int64)
        a = R - z
        b = R + z
        ok = Q[a] & Q[b]
        t = (v5[a].astype(np.int64) + v5[b] + 1) * P[a] * P[b]
        total += 24 * int(np.dot(z, np.where(ok, t, 0)))
    return total

def solve():
    # If x^2+y^2+z^2 = (2s)^2 then x,y,z are all even (squares are 0/1 mod 4),
    # so points on radius 2s are exactly doubled points on radius s and
    # S(2s) = 2*S(s).  Thus S(10^10) = 2^10 * S(5^10).
    return 2 ** 10 * manhattan_sum(5 ** 10)

if __name__ == "__main__":
    print(solve())
