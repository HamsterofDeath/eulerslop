#!/usr/bin/env python3

MOD = 1_000_000_007


def modular_inverses(limit):
    inv = [0] * (limit + 1)
    inv[1] = 1
    for i in range(2, limit + 1):
        inv[i] = MOD - (MOD // i) * inv[MOD % i] % MOD
    return inv


def solve(k=10_000_000, n=10**12):
    inv = modular_inverses(max(1, k))
    exponent = (n + 1) % (MOD - 1)
    one_sum = (n + 1) % MOD
    inv2 = (MOD + 1) // 2

    # For fixed k, the coefficient of G(q)=sum_{m=0}^n q^m is
    # [x^q] sum_{a=1}^k (x^a - (x-1)^a).  Let
    # D_q = [x^q] sum_{a=0}^k (x-1)^a.  From
    # (x-2) sum D_q x^q = (x-1)^(k+1)-1,
    # D_q = (D_{q-1} - rhs_q) / 2.
    k1 = k + 1
    d_prev = 0
    choose = 1
    ans = 0
    pow_mod = pow
    mod = MOD

    for q in range(k):
        if (k1 - q) & 1:
            rhs = mod - choose
        else:
            rhs = choose
        if q == 0:
            rhs = (rhs - 1) % mod

        d_q = (d_prev - rhs) * inv2 % mod
        coeff = 1 - d_q
        if coeff < 0:
            coeff += mod

        if q == 0:
            geom = 1
        elif q == 1:
            geom = one_sum
        else:
            geom = (pow_mod(q, exponent, mod) - 1) * inv[q - 1] % mod

        ans += coeff * geom % mod
        if ans >= mod:
            ans -= mod

        d_prev = d_q
        if q != k - 1:
            choose = choose * (k1 - q) % mod * inv[q + 1] % mod

    return ans


if __name__ == "__main__":
    assert solve(4, 4) == 406
    assert solve(8, 8) == 27_902_680
    assert solve(10, 100) == 983_602_076
    print(solve())
