#!/usr/bin/env python3
import numpy as np

def powmod_vec(base, exp, mod):
    # vectorized modular exponentiation; values < 10^8 so products fit int64
    res = np.ones_like(mod)
    b = np.asarray(base % mod, dtype=np.int64)
    e = exp.copy()
    while True:
        odd = (e & 1).astype(bool)
        if odd.any():
            res[odd] = res[odd] * b[odd] % mod[odd]
        e >>= 1
        if not e.any():
            break
        b = b * b % mod
    return res

def tonelli_shanks(a, p):
    # sqrt of a mod p for p % 8 == 1 (a known QR)
    q, s = p - 1, 0
    while q % 2 == 0:
        q //= 2
        s += 1
    z = 2
    while pow(z, (p - 1) // 2, p) != p - 1:
        z += 1
    m, c, t, r = s, pow(z, q, p), pow(a, q, p), pow(a, (q + 1) // 2, p)
    while t != 1:
        i, t2 = 0, t
        while t2 != 1:
            t2 = t2 * t2 % p
            i += 1
        b = pow(c, 1 << (m - i - 1), p)
        m, c = i, b * b % p
        t, r = t * c % p, r * b % p
    return r

def solve(limit=10 ** 8):
    # A Fibonacci primitive root g satisfies g^2 = g + 1 mod p, i.e. g is a
    # root of x^2 - x - 1, which exists iff 5 is a QR mod p: p = 5 or
    # p = +-1 mod 5.  p qualifies if either root g = (1 +- sqrt5)/2 is a
    # primitive root (g^((p-1)/q) != 1 for every prime q | p-1).
    sieve = np.ones(limit, dtype=bool)
    sieve[:2] = False
    for i in range(2, int(limit ** 0.5) + 1):
        if sieve[i]:
            sieve[i * i::i] = False
    primes = np.flatnonzero(sieve).astype(np.int64)
    small = primes[primes * primes < limit]  # for trial-dividing p-1
    p = primes[(primes % 5 == 1) | (primes % 5 == 4)]
    n = len(p)

    # s = sqrt(5) mod p, vectorized for p = 3 mod 4 and p = 5 mod 8
    s = np.zeros(n, dtype=np.int64)
    m3 = (p & 3) == 3
    s[m3] = powmod_vec(np.int64(5), (p[m3] + 1) >> 2, p[m3])
    m5 = (p & 7) == 5
    p5 = p[m5]
    s5 = powmod_vec(np.int64(5), (p5 + 3) >> 3, p5)
    fix = s5 * s5 % p5 != 5
    s5[fix] = s5[fix] * powmod_vec(np.int64(2), (p5[fix] - 1) >> 2, p5[fix]) % p5[fix]
    s[m5] = s5
    m1 = np.flatnonzero((p & 7) == 1)
    s[m1] = [tonelli_shanks(5, q) for q in p[m1].tolist()]
    assert (s * s % p == 5).all()

    inv2 = (p + 1) >> 1
    g1 = (1 + s) * inv2 % p
    g2 = (p + 1 - s) * inv2 % p

    # distinct prime factors of p-1: trial division by sieved small primes,
    # compacting entries whose cofactor is proven prime (or 1)
    pair_idx, pair_q = [], []
    act_idx = np.arange(n, dtype=np.int64)
    act_val = p - 1
    for k, q in enumerate(small.tolist()):
        hit = act_val % q == 0
        if hit.any():
            h = np.flatnonzero(hit)
            pair_idx.append(act_idx[h])
            pair_q.append(np.full(len(h), q, dtype=np.int64))
            v = act_val[h] // q
            while True:
                again = v % q == 0
                if not again.any():
                    break
                v[again] //= q
            act_val[h] = v
        if k % 64 == 63:  # cofactor <= q^2 means it is 1 or prime: finalize
            done = act_val <= q * q
            if done.any():
                d = np.flatnonzero(done & (act_val > 1))
                pair_idx.append(act_idx[d])
                pair_q.append(act_val[d])
                keep = ~done
                act_idx, act_val = act_idx[keep], act_val[keep]
    big = act_val > 1  # remaining cofactors are prime (no factor <= sqrt(limit))
    pair_idx.append(act_idx[big])
    pair_q.append(act_val[big])
    idx = np.concatenate(pair_idx)
    q = np.concatenate(pair_q)

    # g primitive root <=> g^((p-1)/q) != 1 for all prime q | p-1
    e = (p[idx] - 1) // q
    bad1 = np.bincount(idx[powmod_vec(g1[idx], e, p[idx]) == 1],
                       minlength=n) > 0
    retry = bad1[idx]  # only test g2 where g1 failed
    i2 = idx[retry]
    bad2 = np.bincount(i2[powmod_vec(g2[i2], e[retry], p[i2]) == 1],
                       minlength=n) > 0
    good = ~bad1 | ~bad2
    return int(p[good].sum()) + 5  # p = 5 has FPR g = 3

if __name__ == "__main__":
    print(solve())
