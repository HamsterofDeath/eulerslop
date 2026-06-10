#!/usr/bin/env python3
"""Project Euler 288: An enormous factorial.

N(p, q) = sum_{n=0}^{q} T_n * p^n with T_n = S_n mod p, so the T_n are
exactly the base-p digits of N.  By Legendre's formula the exponent of p in
N! is
    NF = (N - digitsum_p(N)) / (p - 1)
       = sum_n T_n * (p^n - 1)/(p - 1)
       = sum_n T_n * (1 + p + ... + p^(n-1)).

Modulo p^e the geometric sum 1 + p + ... + p^(n-1) is constant for n >= e
(higher powers vanish), so
    NF mod p^e = sum_{n<e} T_n * rep(n) + R * sum_{n=e}^{q} T_n   (mod p^e)
with rep(n) = sum_{i<n} p^i and R = rep(e).  Only the running sum of the
T_n is needed, i.e. one pass of the BBS-like generator.
"""


def nf_mod(p, q, e):
    mod = p ** e
    # rep[n] = (1 + p + ... + p^(n-1)) mod p^e for n = 0..e
    rep = [0] * (e + 1)
    for n in range(1, e + 1):
        rep[n] = (rep[n - 1] + pow(p, n - 1, mod)) % mod

    s = 290797
    total = 0
    tail_sum = 0  # sum of T_n for n >= e
    for n in range(q + 1):
        t = s % p
        if n < e:
            total += t * rep[n]
        else:
            tail_sum += t
        s = s * s % 50515093
    return (total + rep[e] * tail_sum) % mod


def solve():
    assert nf_mod(3, 10000, 20) == 624955285  # given check value
    return nf_mod(61, 10 ** 7, 10)


if __name__ == "__main__":
    print(solve())
