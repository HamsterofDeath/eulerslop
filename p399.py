#!/usr/bin/env python3
from math import gcd
from decimal import Decimal, getcontext
import numpy as np


def solve(target=10**8):
    # Let z(p) be the rank of apparition of p (smallest k with p | F_k); then
    # p | F_n iff z(p) | n.  Under Wall's conjecture p^2 does not divide
    # F_z(p), hence z(p^2) = p*z(p) and:  p^2 | F_n  <=>  p*z(p) | n.
    # So F_n is squarefree iff n is divisible by no m_p = p*z(p).  We find all
    # m_p <= B, count squarefree-index n <= X by inclusion-exclusion over the
    # m_p, and binary search for the target-th such n.
    B = 135_000_000  # safe upper bound for the answer's index (verified below)

    # If z(p) = k then k | p - (5|p) (p != 5), i.e. p = +-1 mod k and p >= k-1;
    # with p*k <= B this bounds k <= sqrt(B)+1.  Also p | F_k, so p <= F_k.
    K = 2
    while (K + 1) * K <= B:
        K += 1
    fib = [0, 1]
    for _ in range(K):
        fib.append(fib[-1] + fib[-2])

    # smallest prime factor table for k <= K (to test primitivity of p in F_k)
    spf = list(range(K + 1))
    for i in range(2, int(K**0.5) + 1):
        if spf[i] == i:
            for j in range(i * i, K + 1, i):
                if spf[j] == j:
                    spf[j] = i

    # primes up to the largest possible candidate min(F_k, B/k)
    pmax = max(min(fib[k], B // k) for k in range(3, K + 1))
    s = np.ones(pmax + 1, dtype=bool)
    s[:2] = False
    for i in range(2, int(pmax**0.5) + 1):
        if s[i]:
            s[i * i::i] = False
    primes_np = np.nonzero(s)[0].astype(np.int64)

    M = [25]  # p = 5 is special: z(5) = 5, m = 25
    for k in range(3, K + 1):
        bound = min(fib[k], B // k)
        if bound < 2:
            continue
        sub = primes_np[: np.searchsorted(primes_np, bound, side="right")]
        r = sub % k
        cand = sub[(r == 1) | (r == k - 1)]
        if cand.size == 0:
            continue
        if fib[k] < (1 << 62):  # vectorize the divisibility test when possible
            cand = cand[np.int64(fib[k]) % cand == 0]
        # prime divisors of k, for the primitivity check
        kk, qs = k, []
        while kk > 1:
            q = spf[kk]
            qs.append(k // q)
            while kk % q == 0:
                kk //= q
        fk = fib[k]
        for p in cand.tolist():
            if fk % p:
                continue
            if all(fib[d] % p for d in qs):  # z(p) is exactly k
                M.append(p * k)

    # remove redundant moduli (multiples of another modulus)
    M = sorted(set(M))
    minimal = []
    for m in M:
        if all(m % m2 for m2 in minimal):
            minimal.append(m)
    Ms = minimal

    # inclusion-exclusion nodes: all subset-lcms <= B with their signs
    lcms, signs = [], []
    arr = np.array(Ms, dtype=np.int64)

    def dfs(i, l, sign):
        g = np.gcd(arr[i:], l)
        nl = arr[i:] // g * l
        ok = np.nonzero(nl <= B)[0]
        for off, v in zip(ok.tolist(), nl[ok].tolist()):
            lcms.append(v)
            signs.append(sign)
            dfs(i + off + 1, v, -sign)

    dfs(0, 1, 1)
    lcm_a = np.array(lcms, dtype=np.int64)
    sign_a = np.array(signs, dtype=np.int64)

    def good(x):  # count of n <= x with F_n squarefree
        return x - int((sign_a * (x // lcm_a)).sum())

    assert good(B) >= target, "index bound B too small"
    lo, hi = 1, B
    while lo < hi:  # smallest x with good(x) >= target (x is then good itself)
        mid = (lo + hi) // 2
        if good(mid) >= target:
            hi = mid
        else:
            lo = mid + 1
    n = lo

    # last 16 digits of F_n by fast doubling mod 10^16
    mod = 10**16

    def fib_pair(k):  # (F_k, F_{k+1}) mod `mod`
        if k == 0:
            return 0, 1
        a, b = fib_pair(k >> 1)
        c = a * (2 * b - a) % mod
        d = (a * a + b * b) % mod
        return (d, (c + d) % mod) if k & 1 else (c, d)

    last16 = fib_pair(n)[0]

    # scientific notation via Binet: F_n ~ phi^n / sqrt5
    getcontext().prec = 60
    sqrt5 = Decimal(5).sqrt()
    log10f = Decimal(n) * ((1 + sqrt5) / 2).log10() - sqrt5.log10()
    exp = int(log10f)
    mant = (Decimal(10) ** (log10f - exp)).quantize(Decimal("0.1"))
    if mant >= 10:
        mant, exp = (mant / 10).quantize(Decimal("0.1")), exp + 1
    return f"{last16:016d},{mant}e{exp}"


if __name__ == "__main__":
    print(solve())
