import numpy as np
from math import isqrt

MOD = 1_000_000_007
INV2 = pow(2, MOD - 2, MOD)


def mobius_sieve(limit):
    # Mobius function for 1..limit via prime sieve.
    mu = np.ones(limit + 1, dtype=np.int8)
    is_comp = np.zeros(limit + 1, dtype=bool)
    for p in range(2, limit + 1):
        if is_comp[p]:
            continue
        is_comp[p * p::p] = True
        mu[p::p] *= -1
        mu[p * p::p * p] = 0
    return mu


def sigma_sum_mod(x):
    # D(x) = sum_{k<=x} sigma(k) = sum_{d*e<=x} d, mod MOD, via hyperbola method.
    if x <= 0:
        return 0
    k = isqrt(x)
    d = np.arange(1, k + 1, dtype=np.int64)
    q = x // d
    qm = q % MOD
    tq = qm * ((q + 1) % MOD) % MOD * INV2 % MOD  # T(q) mod p
    s1 = int((d * qm % MOD).sum() % MOD)          # sum d * floor(x/d)
    s2 = int(tq.sum() % MOD)                      # sum T(floor(x/e))
    tk = k % MOD * ((k + 1) % MOD) % MOD * INV2 % MOD
    return (s1 + s2 - k % MOD * tk) % MOD


def solve():
    # f(f(x)) == f(x) mod n for all x  <=>  a^2 == a and a*b == 0 (mod n).
    # Idempotents a mod n correspond to subsets S of prime powers p^e || n
    # (a == 0 mod p^e for p in S, a == 1 mod the rest), and #b = gcd(a, n)
    # = prod_{p in S} p^e.  Summing over all a (excluding a = 0) gives
    #   R(n) = prod_{p^e || n} (p^e + 1) - n = sigmastar(n) - n,
    # the unitary divisor sum minus n (verified by brute force for n <= 200).
    # Dirichlet series: sum sigmastar(n)/n^s = zeta(s) zeta(s-1) / zeta(2s-1),
    # so sigmastar(n) = sum_{m^2 | n} mu(m) * m * sigma(n / m^2) and
    #   F(N) = sum_{m <= sqrt(N)} mu(m) * m * D(N // m^2)  -  T(N),
    # where D(X) = sum_{k<=X} sigma(k) is O(sqrt(X)) by the hyperbola method.
    N = 10 ** 14
    root = isqrt(N)
    mu = mobius_sieve(root)

    # Split: small m -> hyperbola D; large m -> X = N//m^2 small, use a
    # sieved prefix table of sigma.
    L = 4_000_000
    m0 = min(isqrt(N // L), root)
    total = 0

    for m in range(1, m0 + 1):
        if mu[m]:
            total += int(mu[m]) * m % MOD * sigma_sum_mod(N // (m * m)) % MOD

    if m0 < root:
        lim = N // ((m0 + 1) ** 2)  # max X needed in the tail
        sig = np.zeros(lim + 1, dtype=np.int64)
        for d in range(1, lim + 1):
            sig[d::d] += d
        pref = np.cumsum(sig % MOD) % MOD
        m_arr = np.arange(m0 + 1, root + 1, dtype=np.int64)
        mu_t = mu[m0 + 1:root + 1].astype(np.int64)
        keep = mu_t != 0
        m_arr, mu_t = m_arr[keep], mu_t[keep]
        x = N // (m_arr * m_arr)
        total += int((m_arr % MOD * pref[x] % MOD * mu_t).sum() % MOD)

    tn = N % MOD * ((N + 1) % MOD) % MOD * INV2 % MOD  # sum_{n<=N} n
    return (total - tn) % MOD


if __name__ == "__main__":
    print(solve())
