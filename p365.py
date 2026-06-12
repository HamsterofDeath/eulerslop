#!/usr/bin/env python3
import numpy as np

def solve():
    # M(n,k,m) = C(n,k) mod m for m = p*q*r squarefree.
    # 1) Lucas' theorem gives a_p = C(10^18, 10^9) mod p for each prime p:
    #    write n and k in base p, multiply the small binomials C(n_i, k_i) mod p.
    # 2) For each pair p < q, CRT-combine (a_p mod p, a_q mod q) into x_pq mod pq.
    # 3) For each triple p < q < r, the CRT lift is
    #       x_pqr = x_pq + pq * ((a_r - x_pq) * inv(pq mod r) mod r)
    #    Summing over all ~21M triples is vectorised with numpy: for each r,
    #    process all pairs (p,q) with q < r at once (pairs ordered by max index
    #    so they form a prefix of the pair arrays).
    n, k = 10 ** 18, 10 ** 9

    # primes strictly between 1000 and 5000
    limit = 5000
    sieve = np.ones(limit, dtype=bool)
    sieve[:2] = False
    for i in range(2, int(limit ** 0.5) + 1):
        if sieve[i]:
            sieve[i * i::i] = False
    primes = [int(p) for p in np.flatnonzero(sieve) if p > 1000]

    def binom_mod_p(p):
        # Lucas: C(n,k) mod p = prod C(n_i, k_i) mod p over base-p digits.
        fact = [1] * p
        for i in range(1, p):
            fact[i] = fact[i - 1] * i % p
        res, nn, kk = 1, n, k
        while kk:
            nd, kd = nn % p, kk % p
            if kd > nd:
                return 0
            res = res * fact[nd] * pow(fact[kd] * fact[nd - kd] % p, p - 2, p) % p
            nn //= p
            kk //= p
        return res

    A = [binom_mod_p(p) for p in primes]
    m = len(primes)

    # All pairs (i, j) with i < j, ordered by j so that for any k the pairs
    # with j < k form a prefix of length k*(k-1)//2.
    pq_list, x_list = [], []
    for j in range(m):
        q, aq = primes[j], A[j]
        for i in range(j):
            p, ap = primes[i], A[i]
            # CRT for the pair: x = ap (mod p), x = aq (mod q)
            x = ap + p * ((aq - ap) * pow(p, -1, q) % q)
            pq_list.append(p * q)
            x_list.append(x)
    PQ = np.array(pq_list, dtype=np.int64)
    X = np.array(x_list, dtype=np.int64)

    total = 0
    for kk in range(2, m):
        r, ar = primes[kk], A[kk]
        # modular inverse table mod r via inv[i] = -(r//i)*inv[r%i] mod r
        inv = [0] * r
        inv[1] = 1
        for i in range(2, r):
            inv[i] = (r - r // i) * inv[r % i] % r
        inv = np.array(inv, dtype=np.int64)
        cnt = kk * (kk - 1) // 2
        pq = PQ[:cnt]
        x = X[:cnt]
        t = (ar - x) % r * inv[pq % r] % r  # lift coefficient mod r
        total += int(x.sum()) + int((pq * t).sum())
    return total

if __name__ == "__main__":
    print(solve())
