#!/usr/bin/env python3
import numpy as np

def solve():
    # The step x/y -> (x+1)/(y-1) keeps x+y constant; reducing by gcd d
    # divides x+y by d.  Starting from 1/k the invariant is x+y = k+1, and the
    # walk x -> x+1 (mod nothing) hits a multiple of a prime q | x+y exactly
    # when x ≡ 0 mod q; one shows the sequence terminates at n/1 with
    # n+1 = largest prime factor of k+1, i.e. f(k) = lpf(k+1) - 1.
    # (Checks: f(20)=7-1=6, f(1)=1, f(2)=2, f(3)=1.)
    #
    # So f(k^3) = lpf(k^3 + 1) - 1 with k^3+1 = (k+1)(k^2-k+1).
    # For k <= N = 2*10^6:
    #   * lpf(k+1) via an ordinary largest-prime-factor sieve up to N+1.
    #   * lpf(k^2-k+1) by sieving the polynomial values: p | k^2-k+1 iff
    #     k ≡ (1 ± sqrt(-3))/2 (mod p), which has solutions for p = 3 (k≡2)
    #     and p ≡ 1 (mod 3) (sqrt via Tonelli-Shanks).  Divide out each such
    #     prime; since k^2-k+1 < (2*10^6)^2, whatever remains after removing
    #     all prime factors <= N is either 1 or a single prime > N.
    N = 2 * 10 ** 6

    # Largest prime factor of 2..N+1.
    lpf_lin = np.zeros(N + 2, dtype=np.int64)
    for p in range(2, N + 2):
        if lpf_lin[p] == 0:
            lpf_lin[p::p] = p
    primes = [p for p in range(2, N + 1) if lpf_lin[p] == p]

    def sqrt_mod(a, p):
        # Tonelli-Shanks: square root of a modulo odd prime p.
        if p % 4 == 3:
            return pow(a, (p + 1) // 4, p)
        q, s = p - 1, 0
        while q % 2 == 0:
            q //= 2
            s += 1
        z = 2
        while pow(z, (p - 1) // 2, p) != p - 1:
            z += 1
        m, c, t, r = s, pow(z, q, p), pow(a, q, p), pow(a, (q + 1) // 2, p)
        while t != 1:
            t2, i = t * t % p, 1
            while t2 != 1:
                t2 = t2 * t2 % p
                i += 1
            b = pow(c, 1 << (m - i - 1), p)
            m, c = i, b * b % p
            t, r = t * c % p, r * b % p
        return r

    # vals[k] = k^2 - k + 1, progressively divided by its small prime factors;
    # best[k] = largest prime factor <= N found so far.
    vals = (np.arange(N + 1, dtype=np.int64) ** 2
            - np.arange(N + 1, dtype=np.int64) + 1)
    best = np.zeros(N + 1, dtype=np.int64)

    def strip(p, root):
        # Remove all factors p from vals[k] for k ≡ root (mod p).
        idx = np.arange(root if root else p, N + 1, p, dtype=np.int64)
        if idx.size == 0:
            return
        sub = vals[idx]
        mask = sub % p == 0          # guards repeated roots (p = 3)
        idx = idx[mask]
        sub = sub[mask]
        sub //= p
        while True:
            more = sub % p == 0
            if not more.any():
                break
            sub[more] //= p
        vals[idx] = sub
        best[idx] = p

    strip(3, 2)                      # k ≡ 2 (mod 3) gives one factor 3
    for p in primes:
        if p % 3 != 1:
            continue
        s = sqrt_mod(p - 3, p)       # sqrt(-3) mod p
        inv2 = (p + 1) // 2
        r1 = (1 + s) * inv2 % p
        r2 = (1 - s) * inv2 % p
        strip(p, r1)
        if r2 != r1:
            strip(p, r2)

    # Remaining cofactor is 1 or a prime > N.
    lpf_quad = np.maximum(best, np.where(vals > 1, vals, 0))

    k = np.arange(1, N + 1)
    f = np.maximum(lpf_lin[k + 1], lpf_quad[1:]) - 1
    assert int(f[:100].sum()) == 118937
    return int(f.sum())

if __name__ == "__main__":
    print(solve())
