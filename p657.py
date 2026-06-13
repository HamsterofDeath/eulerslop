#!/usr/bin/env python3

MOD = 1_000_000_007


def modular_inverses(limit):
    inv = [0] * (limit + 1)
    inv[1] = 1
    for i in range(2, limit + 1):
        inv[i] = MOD - (MOD // i) * inv[MOD % i] % MOD
    return inv


def solve(alpha=10_000_000, n=10**12):
    if alpha == 1:
        return 1

    inv = modular_inverses(alpha)
    exponent = (n + 1) % (MOD - 1)
    one_sum = (n + 1) % MOD

    # Inclusion-exclusion with q = alpha - missing_count:
    # I(alpha,n) = sum_{q=0}^{alpha-1} (-1)^(alpha-q+1) C(alpha,q)
    #              * sum_{m=0}^n q^m.
    ans = 1 if alpha & 1 else MOD - 1

    term = (alpha % MOD) * one_sum % MOD
    if (alpha ^ 1) & 1:
        ans += term
    else:
        ans -= term
    ans %= MOD

    c = (alpha % MOD) * ((alpha - 1) % MOD) % MOD * inv[2] % MOD
    pow_mod = pow
    mod = MOD
    for q in range(2, alpha):
        geom = (pow_mod(q, exponent, mod) - 1) * inv[q - 1] % mod
        term = c * geom % mod
        if (alpha ^ q) & 1:
            ans += term
            if ans >= mod:
                ans -= mod
        else:
            ans -= term
            if ans < 0:
                ans += mod

        if q != alpha - 1:
            c = c * (alpha - q) % mod * inv[q + 1] % mod

    return ans


if __name__ == "__main__":
    assert solve(3, 0) == 1
    assert solve(3, 2) == 13
    assert solve(3, 4) == 79
    print(solve())
