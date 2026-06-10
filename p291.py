#!/usr/bin/env python3
# Panaitopol primes p = (x^4 - y^4)/(x^3 + y^3) are exactly the primes of the form
# p = n^2 + (n+1)^2 = 2n^2 + 2n + 1 (equivalently 2p - 1 is an odd square; take
# x = n+1, y = n).  So count n in [1, 49999999] (2n^2+2n+1 < 5*10^15) for which
# 2n^2 + 2n + 1 is prime.
#
# Sieve instead of testing each candidate: 2*(2n^2+2n+1) = (2n+1)^2 + 1, so every
# prime factor q of a candidate satisfies (2n+1)^2 ≡ -1 (mod q), i.e. q ≡ 1 (mod 4).
# For each prime q ≡ 1 (mod 4) up to sqrt(5e15) ≈ 7.08e7 compute i = sqrt(-1) mod q;
# then 2n^2+2n+1 ≡ 0 (mod q) iff n ≡ (±i - 1)/2 (mod q), and we cross out those
# arithmetic progressions.  Any candidate surviving the sieve up to sqrt has no
# prime factor <= sqrt(value), hence is prime.  Square roots of -1 are computed
# for all q at once with vectorised binary exponentiation (numpy int64; products
# stay below 2^54).

import numpy as np

LIMIT = 5 * 10 ** 15
NMAX = 49999999          # largest n with 2n^2+2n+1 < 5e15
QMAX = 70710678          # floor(sqrt(5e15))


def small_sieve(limit):
    s = np.ones(limit + 1, dtype=bool)
    s[:2] = False
    for p in range(2, int(limit ** 0.5) + 1):
        if s[p]:
            s[p * p:: p] = False
    return np.nonzero(s)[0]


def pow_mod_vec(base, exp, mod):
    # base, exp, mod: int64 arrays; computes base**exp % mod elementwise.
    result = np.ones_like(mod)
    b = base % mod
    e = exp.copy()
    while np.any(e):
        odd = (e & 1).astype(bool)
        result[odd] = result[odd] * b[odd] % mod[odd]
        b = b * b % mod
        e >>= 1
    return result


def solve():
    primes = small_sieve(QMAX)
    q = primes[primes % 4 == 1].astype(np.int64)

    # Find a quadratic non-residue a for each q, then i = a^((q-1)/4) mod q.
    a = np.zeros_like(q)
    a[q % 8 == 5] = 2                      # 2 is a non-residue iff q ≡ 5 (mod 8)
    need = np.nonzero(a == 0)[0]           # q ≡ 1 (mod 8)
    trial = 3
    while need.size:
        qq = q[need]
        euler = pow_mod_vec(np.full_like(qq, trial), (qq - 1) >> 1, qq)
        nr = euler == qq - 1
        a[need[nr]] = trial
        need = need[~nr]
        trial += 2
    i_root = pow_mod_vec(a, (q - 1) >> 2, q)

    # Roots of 2n^2+2n+1 ≡ 0 (mod q):  n ≡ (±i - 1) * inv2  (mod q).
    inv2 = (q + 1) >> 1
    n1 = (i_root - 1) % q * inv2 % q
    n2 = (q - 1 - n1) % q

    is_cand = np.ones(NMAX + 1, dtype=bool)
    is_cand[0] = False
    ql = q.tolist()
    n1l = n1.tolist()
    n2l = n2.tolist()
    for k in range(len(ql)):
        qi = ql[k]
        r = n1l[k]
        if r <= NMAX:
            is_cand[r::qi] = False
        r = n2l[k]
        if r <= NMAX:
            is_cand[r::qi] = False

    # Candidates whose value is itself a sieving prime (value <= QMAX) were
    # crossed out by themselves; recheck small n directly.
    prime_set = set(int(p) for p in primes)
    n = 1
    while True:
        v = 2 * n * n + 2 * n + 1
        if v > QMAX:
            break
        is_cand[n] = v in prime_set
        n += 1

    return int(np.count_nonzero(is_cand))


if __name__ == "__main__":
    print(solve())
