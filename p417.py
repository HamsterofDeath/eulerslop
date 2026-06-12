"""Project Euler 417: sum of recurring-cycle lengths L(n) of 1/n for 3 <= n <= 10^8.

L(n) = multiplicative order of 10 modulo m, where m is n with all factors 2 and 5
removed (L = 0 if m = 1). Plan:
  1. For every prime p (not 2,5) up to N, compute ord_p(10): start with p-1 and,
     for each prime q | p-1, divide out q while 10^(o/q) = 1 (mod p). All of this
     is vectorised with numpy: primes p with q | p-1 are found by walking the
     arithmetic progression 1 (mod q), and the modular powers use a batched
     square-and-multiply (values < 2^27, so products fit exactly in int64).
     After removing prime factors q <= sqrt(N), the cofactor of p-1 is 1 or a
     single prime > sqrt(N) (two such factors would exceed N), handled directly.
  2. ord(p^k) lifts from ord(p^(k-1)) by a factor of 1 or p (only p <= sqrt(N)
     can have k >= 2). cur[n] = lcm of ord over the prime powers dividing n is
     accumulated by sieving: slice updates cur[q::q] for prime powers q of small
     primes, then - since any n <= N has at most one prime factor > sqrt(N) -
     one scatter update per cofactor j for the large primes.
  3. L(n) depends only on the 10-free part m of n, so the answer is
     sum over 2,5-smooth s of T(N // s) with T(x) = sum of cur[m] for m <= x
     coprime to 10, evaluated with one chunked pass over cur.
"""
import numpy as np


def pow10mod(e, m):
    # 10^e mod m, elementwise; m < 2^27 so all int64 products are exact
    e = e.astype(np.int64).copy()
    r = np.ones_like(m)
    b = np.full_like(m, 10) % m
    while e.any():
        r = np.where(e & 1, r * b % m, r)
        b = b * b % m
        e >>= 1
    return r


def solve(N=10**8):
    sieve = np.ones(N + 1, dtype=bool)
    sieve[:2] = False
    for i in range(2, int(N**0.5) + 1):
        if sieve[i]:
            sieve[i * i::i] = False

    P = np.flatnonzero(sieve).astype(np.int64)
    P = P[(P != 2) & (P != 5)]
    o = P - 1                  # will be reduced to ord_p(10)
    rem = (P - 1).copy()       # cofactor of p-1 after removing small primes

    sq = int(N**0.5)
    small_q = [int(q) for q in np.flatnonzero(sieve[: sq + 1])]

    for q in small_q:
        # primes p = 1 (mod q), i.e. q | p-1
        cand = np.arange(1 + q, N + 1, q, dtype=np.int64)
        cand = cand[sieve[cand]]
        idx = np.searchsorted(P, cand)
        ok = (idx < P.size) & (P[np.minimum(idx, P.size - 1)] == cand)
        idx = idx[ok]
        if idx.size == 0:
            continue
        # strip q from the cofactor
        r = rem[idx]
        while True:
            mm = r % q == 0
            if not mm.any():
                break
            r[mm] //= q
        rem[idx] = r
        # reduce the order by q while 10^(o/q) = 1 (mod p)
        cur_idx = idx
        while cur_idx.size:
            mm = o[cur_idx] % q == 0
            cur_idx = cur_idx[mm]
            if cur_idx.size == 0:
                break
            t = pow10mod(o[cur_idx] // q, P[cur_idx]) == 1
            cur_idx = cur_idx[t]
            o[cur_idx] //= q

    # one possible large prime factor of p-1 (multiplicity is necessarily 1)
    big = np.flatnonzero(rem > 1)
    if big.size:
        t = pow10mod(o[big] // rem[big], P[big]) == 1
        gb = big[t]
        o[gb] //= rem[gb]

    # cur[n] accumulates lcm of ord over prime-power components of n
    cur = np.ones(N + 1, dtype=np.int32)
    n_small = int(np.searchsorted(P, sq + 1))

    # phase 1: prime powers of primes <= sqrt(N); ord(p^k) | ord(p^(k+1)),
    # so re-lcm'ing the higher power over its multiples supersedes the lower one
    for i in range(n_small):
        p = int(P[i])
        ok_ord = int(o[i])
        q = p
        while q <= N:
            view = cur[q::q]
            np.floor_divide(view, np.gcd(view, np.int32(ok_ord)), out=view)
            view *= np.int32(ok_ord)
            qn = q * p
            if qn <= N and pow(10, ok_ord, qn) != 1:
                ok_ord *= p
            q = qn

    # phase 2: primes p > sqrt(N) (always to the first power); each n <= N has
    # at most one such factor, so for each cofactor j the indices j*p are unique
    P_large = P[n_small:]
    o_large = o[n_small:].astype(np.int32)
    jmax = N // int(P_large[0])
    for j in range(1, jmax + 1):
        if j % 2 == 0 or j % 5 == 0:
            continue  # such n are excluded from the final sum anyway
        hi = int(np.searchsorted(P_large, N // j, side="right"))
        pp = P_large[:hi]
        oo = o_large[:hi]
        idxn = pp * j
        c = cur[idxn]
        cur[idxn] = c // np.gcd(c, oo) * oo

    # final accumulation: answer = sum over 2,5-smooth s of T(N // s)
    from collections import Counter
    smooth = []
    a = 1
    while a <= N // 3:
        b = a
        while b <= N // 3:
            smooth.append(b)
            b *= 5
        a *= 2
    thr = Counter(N // s for s in smooth)
    thresholds = sorted(thr)

    cur[0] = 0
    cur[1] = 0
    cur[::2] = 0     # keep only m coprime to 10
    cur[5::5] = 0

    ans = 0
    running = 0
    ti = 0
    CH = 1 << 22
    for start in range(0, N + 1, CH):
        chunk = cur[start:start + CH].astype(np.int64)
        end = start + chunk.size - 1
        if ti < len(thresholds) and thresholds[ti] <= end:
            cs = np.cumsum(chunk)
            while ti < len(thresholds) and thresholds[ti] <= end:
                x = thresholds[ti]
                ans += thr[x] * (running + int(cs[x - start]))
                ti += 1
            running += int(cs[-1])
        else:
            running += int(chunk.sum())
    return ans


if __name__ == "__main__":
    print(solve())
