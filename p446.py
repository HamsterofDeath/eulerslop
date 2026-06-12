import numpy as np

MOD = 1_000_000_007


def solve(N=10_000_000):
    # R(n): f(f(x))=f(x) for all x  <=>  n | a(a-1) and n | ab.
    # a ranges over idempotents mod n (unitary divisors u||n, gcd(a,n)=u),
    # each giving gcd(a,n)=u choices of b; excluding a=0 (u=n):
    #   R(n) = sigma*(n) - n  where sigma*(n) = prod(p^e + 1) over p^e || n.
    #
    # Sophie Germain: n^4+4 = A*B, A=(n-1)^2+1, B=(n+1)^2+1.
    #   n odd : A,B odd and coprime           -> sigma*(AB) = sigma*(A)*sigma*(B)
    #   n even: gcd(A,B)=2, 2||A, 2||B, 4||AB -> sigma*(AB) = 5*sigma*(A)*sigma*(B)/9
    # So it suffices to know U(m) = sigma*(m^2+1) mod MOD for all m <= N+1.
    M = N + 1

    # sieve primes up to M; only p=2 and p ≡ 1 mod 4 can divide m^2+1
    sieve = np.ones(M + 1, dtype=bool)
    sieve[:2] = False
    for i in range(2, int(M ** 0.5) + 1):
        if sieve[i]:
            sieve[i * i::i] = False
    pr = np.flatnonzero(sieve)
    ps = pr[pr & 3 == 1]  # primes ≡ 1 (mod 4)

    mm = np.arange(M + 1, dtype=np.int64)
    val = mm * mm + 1          # residual cofactor of m^2+1 (fits int64, <= ~1e14)
    res = np.ones(M + 1, dtype=np.int64)  # sigma*(m^2+1) mod MOD accumulator

    # p = 2: m odd -> m^2+1 ≡ 2 (mod 8), so exactly one factor 2
    val[1::2] >>= 1
    res[1::2] = 3

    limit2 = M * M + 1
    for p in ps:
        p = int(p)
        # sqrt(-1) mod p: r = g^((p-1)/4) for any quadratic non-residue g
        g = 2
        while pow(g, (p - 1) >> 1, p) != p - 1:
            g += 1
        r = pow(g, (p - 1) >> 2, p)
        inv2r = pow(2 * r, -1, p)  # for Hensel lifts

        e, pe = 1, p
        prev_pe_mod = 1
        while True:
            lo = r if r <= pe - r else pe - r
            if lo > M:
                break
            pe_mod = pe % MOD
            if e == 1:
                mult = p + 1
            else:
                mult = (pe_mod + 1) * pow(prev_pe_mod + 1, MOD - 2, MOD) % MOD
            for s in (r, pe - r):
                if s <= M:
                    v = val[s::pe]
                    v //= p
                    w = res[s::pe]
                    w *= mult
                    w %= MOD
            # Hensel-lift root to mod p^(e+1)
            t = (-((r * r + 1) // pe) * inv2r) % p
            r += t * pe
            pe *= p
            prev_pe_mod = pe_mod
            e += 1
            if pe > limit2:
                break

        # leftover cofactor is 1 or a single prime > M (since m^2+1 < (M+1)^2)
    mask = val > 1
    res[mask] = res[mask] * (val[mask] % MOD + 1) % MOD

    # combine: n = 1..N, A-index n-1, B-index n+1
    prod = res[0:N] * res[2:N + 2] % MOD
    c_even = 5 * pow(9, MOD - 2, MOD) % MOD
    prod[1::2] = prod[1::2] * c_even % MOD  # even n (index n-1 odd)
    total = int(prod.sum() % MOD)  # 1e7 values < MOD: sum fits in int64

    # subtract sum of (n^4 + 4) mod MOD
    n = np.arange(1, N + 1, dtype=np.int64)
    n2 = n * n % MOD
    n4 = n2 * n2 % MOD
    total = (total - int(n4.sum() % MOD) - 4 * N) % MOD
    return total


if __name__ == "__main__":
    print(solve())
