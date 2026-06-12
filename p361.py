#!/usr/bin/env python3
"""Project Euler 361: Subsequence of Thue-Morse sequence.

A(n) = n-th smallest integer whose binary expansion occurs as a (contiguous)
factor of the Thue-Morse word T = 0110100110010110...  Find the last 9 digits
of sum A(10^k), k = 1..18.

Method.  T is the fixed point of mu: 0->01, 1->10 and is overlap-free, so any
factor of length >= 5 has a UNIQUE block parse  w = [a] mu(u) [b]  (a = dangling
second half of a block, b = dangling first half).  This gives a bijection
between factors of length n and factors of length ~n/2 (carrying the dangling
letters as context), hence:
  * factor counts:  p(2m) = p(m) + p(m+1),  p(2m+1) = 2 p(m+1),
  * the bijection is lex-order-preserving for a fixed prefix, so the j-th
    factor of length n with prefix P maps to the j-th factor of length ~n/2
    with the halved prefix.  Selecting the k-th factor therefore needs only
    O(log n) levels; counts with short prefixes recurse the same way and are
    memoized.
T's factor set is closed under complement, so exactly p(L)/2 factors of length
L start with '1'; partial sums S(L) = sum p(l) (computed by the same halving
recursion) locate the bit-length of A(N), then a prefix-rank descent selects
the word.  A(10^18) has ~1.1e9 bits, so the selected word is kept implicitly
as its desubstitution chain; its value mod 10^9 = 2^9 * 5^9 comes from CRT:
  * mod 5^9: bottom-up over the chain using value_b(mu(K)) =
    (b-1)*value_{b^2}(K) + (b^{2t}-1)/(b^2-1); powers of 2 are invertible
    mod 5^9 so stripping dangling letters is exact,
  * mod 2^9: the last 9 bits, tracked explicitly alongside the chain.
"""
import bisect
import sys
from functools import lru_cache

sys.setrecursionlimit(100000)

MOD = 10 ** 9
MOD5 = 5 ** 9   # 1953125
M2 = 1 << 9     # 512;  MOD5 * M2 = 10^9
NBASE = 64      # lengths <= NBASE handled by explicit factor tables
KEEP = 100      # how many trailing bits to track explicitly


def solve():
    # --- Thue-Morse prefix; long enough to contain every factor of length
    # <= 130 (T is linearly recurrent with constant ~10; verified below by
    # matching counts against the p-recursion).
    pref_len = 1 << 15
    tm = bytearray([0])
    while len(tm) < pref_len:
        tm.extend(1 - b for b in tm)
    tm = tm[:pref_len]

    # explicit factor tables: length -> sorted list of factor values
    self_test_lengths = [65, 81, 100, 128]
    facs = {}
    for L in list(range(1, NBASE + 3)) + self_test_lengths:
        s = set()
        v = 0
        mask = (1 << L) - 1
        for i, b in enumerate(tm):
            v = ((v << 1) | b) & mask
            if i >= L - 1:
                s.add(v)
        facs[L] = sorted(s)
    fac_sets = {L: set(facs[L]) for L in facs if L <= 16}

    def tup_val(P):
        v = 0
        for b in P:
            v = (v << 1) | b
        return v

    def is_factor(P):
        return tup_val(P) in fac_sets[len(P)]

    # --- factor complexity p(L) and partial sums S(L) ---
    @lru_cache(maxsize=None)
    def pcnt(L):
        if L <= 6:
            return len(facs[L])
        if L % 2 == 0:
            m = L // 2
            return pcnt(m) + pcnt(m + 1)
        return 2 * pcnt((L + 1) // 2)

    # cross-validate tables against the recursion (also proves completeness)
    for L in facs:
        assert len(facs[L]) == pcnt(L)

    sbase = [0]
    for i in range(1, 7):
        sbase.append(sbase[-1] + len(facs[i]))
    # sum_{l=6}^{2M+1} p(l) = sum_{m=3}^{M} (p(m) + 3 p(m+1))
    const = sbase[5] - sbase[2] - 3 * sbase[3]

    @lru_cache(maxsize=None)
    def S(L):
        if L <= 0:
            return 0
        if L <= 6:
            return sbase[L]
        if L % 2 == 1:
            m = (L - 1) // 2
            return S(m) + 3 * S(m + 1) + const
        return S(L + 1) - pcnt(L + 1)

    acc = 0
    for L in range(1, 200):
        acc += pcnt(L)
        assert S(L) == acc

    # --- unique desubstitution parse of a factor P (len >= 5) ---
    @lru_cache(maxsize=None)
    def parse(P):
        # P = [a] mu(u) [bp]; returns (a or None, next-level prefix)
        # where the next-level word is [1-a-context] u [bp] ...; overlap-
        # freeness of T makes the block parse unique for len >= 5.
        res = []
        for off in (0, 1):
            body = P[off:]
            u = []
            ok = True
            for i in range(0, len(body) - 1, 2):
                if body[i + 1] != 1 - body[i]:
                    ok = False
                    break
                u.append(body[i])
            if ok:
                bp = body[-1] if (len(body) % 2 == 1) else None
                res.append((off, tuple(u), bp))
        assert len(res) == 1
        off, u, bp = res[0]
        a = P[0] if off else None
        nxt = ((1 - P[0],) if off else ()) + u + ((bp,) if bp is not None else ())
        return a, nxt

    def child_len(n, a):
        # factor w of length n, parse [a] mu(K) [c]: child word = [1-a] K [c]
        r = n - (1 if a is not None else 0)
        has_c = bool(r & 1)
        n1 = (1 if a is not None else 0) + r // 2 + (1 if has_c else 0)
        return n1, has_c

    # --- count factors of length n with prefix P ---
    cmemo = {}

    def count(n, P):
        if n == len(P):
            return 1
        key = (n, P)
        r = cmemo.get(key)
        if r is not None:
            return r
        if n <= NBASE:
            lst = facs[n]
            lo = tup_val(P) << (n - len(P))
            hi = lo + (1 << (n - len(P)))
            res = bisect.bisect_left(lst, hi) - bisect.bisect_left(lst, lo)
        elif len(P) < 5:
            res = sum(count(n, P + (c,)) for c in (0, 1) if is_factor(P + (c,)))
        else:
            a, nxt = parse(P)
            n1, _ = child_len(n, a)
            res = count(n1, nxt)
        cmemo[key] = res
        return res

    # --- select j-th factor of length n with prefix P; returns the
    # desubstitution chain (top-down nodes) plus an explicit base word ---
    def sel(n, P, j):
        if n <= NBASE:
            lst = facs[n]
            lo = tup_val(P) << (n - len(P))
            i0 = bisect.bisect_left(lst, lo)
            assert i0 + j < bisect.bisect_left(lst, lo + (1 << (n - len(P))))
            return [], (n, lst[i0 + j])
        if len(P) < 5:
            for c in (0, 1):
                Q = P + (c,)
                if is_factor(Q):
                    cnt = count(n, Q)
                    if j < cnt:
                        return sel(n, Q, j)
                    j -= cnt
            raise AssertionError("rank out of range")
        a, nxt = parse(P)
        n1, has_c = child_len(n, a)
        nodes, basew = sel(n1, nxt, j)
        return [(n, a, has_c)] + nodes, basew

    def geo(q, t):
        # sum_{i=0}^{t-1} q^i mod MOD5 (q not invertible-safe: use halving)
        if t == 0:
            return 0
        if t % 2 == 1:
            return (geo(q, t - 1) * q + 1) % MOD5
        h = geo(q, t // 2)
        return (h * (1 + pow(q, t // 2, MOD5))) % MOD5

    def evaluate(nodes, basew):
        # bottom-up: value of the selected word mod 5^9, plus trailing bits.
        # level j word is valued in base 2^(2^j) mod 5^9 (top j = 0, base 2).
        d = len(nodes)
        B = [pow(2, 1 << j, MOD5) for j in range(d + 1)]
        nb, val = basew
        bits = [(val >> (nb - 1 - i)) & 1 for i in range(nb)]
        x = 0
        for b_ in bits:
            x = (x * B[d] + b_) % MOD5
        tail = bits[:]
        cur_len = nb
        for idx in range(d - 1, -1, -1):
            n_j, a, has_c = nodes[idx]
            b, b2 = B[idx], B[idx + 1]
            full = (len(tail) == cur_len)
            # strip the known dangling letters off the child word -> K
            y = x
            if a is not None:
                if full:
                    assert tail[0] == 1 - a
                y = (y - (1 - a) * pow(b2, cur_len - 1, MOD5)) % MOD5
            c = None
            if has_c:
                c = tail[-1]
                y = ((y - c) * pow(b2, -1, MOD5)) % MOD5
            na, nc = (1 if a is not None else 0), (1 if has_c else 0)
            t = cur_len - na - nc
            assert 2 * t + na + nc == n_j
            # w = [a] mu(K) [c]
            x = ((b - 1) * y + geo(b2, t)) % MOD5
            if has_c:
                x = (x * b + c) % MOD5
            if a is not None:
                x = (x + a * pow(b, n_j - 1, MOD5)) % MOD5
            # update explicit tail bits
            tk = tail[:-1] if has_c else tail[:]
            if a is not None and full:
                tk = tk[1:]
            mu = []
            for bb in tk:
                mu.append(bb)
                mu.append(1 - bb)
            nt = ([a] if (a is not None and full) else []) + mu + ([c] if has_c else [])
            if len(nt) > KEEP:
                nt = nt[-KEEP:]
            tail, cur_len = nt, n_j
        return x, tail

    inv5 = pow(MOD5 % M2, -1, M2)

    def A(N):
        # (exact value if small enough else None, value mod 10^9)
        if N == 0:
            return 0, 0
        hi = 1
        while 1 + S(hi) // 2 <= N:   # elements with <= L bits: 1 + S(L)/2
            hi <<= 1
        lo = hi >> 1
        while lo < hi:
            mid = (lo + hi) // 2
            if 1 + S(mid) // 2 > N:
                hi = mid
            else:
                lo = mid + 1
        L = lo
        r = N - 1 - S(L - 1) // 2    # rank among L-bit members ('1'-prefixed)
        assert 0 <= r < pcnt(L) // 2
        nodes, basew = sel(L, (1,), r)
        if not nodes:
            return basew[1], basew[1] % MOD
        x5, tail = evaluate(nodes, basew)
        r2 = tup_val(tuple(tail[-9:]))
        return None, (x5 + MOD5 * (((r2 - x5) * inv5) % M2)) % MOD

    # --- self-tests ---
    # full pipeline (chain selection + modular evaluation) vs brute force
    for L in self_test_lengths:
        bf = [v for v in facs[L] if (v >> (L - 1)) == 1]
        assert len(bf) == pcnt(L) // 2 == count(L, (1,))
        for j in {0, 1, len(bf) // 2, len(bf) - 1}:
            nodes, basew = sel(L, (1,), j)
            x5, tail = evaluate(nodes, basew)
            r2 = tup_val(tuple(tail[-9:]))
            got = (x5 + MOD5 * (((r2 - x5) * inv5) % M2)) % MOD
            assert got == bf[j] % MOD
    # values given in the statement
    for n, want in enumerate([0, 1, 2, 3, 4, 5, 6, 9, 10, 11, 12, 13, 18]):
        assert A(n)[0] == want
    assert A(100)[0] == 3251
    assert A(1000)[0] == 80852364498

    return sum(A(10 ** k)[1] for k in range(1, 19)) % MOD


if __name__ == "__main__":
    print(solve())
