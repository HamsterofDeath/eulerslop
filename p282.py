#!/usr/bin/env python3
# Project Euler 282: The Ackermann Function, sum A(n,n) for n=0..6 mod 14^8.
#
# A(0,0)..A(3,3) are tiny and computed by the plain recursion.
# For m >= 2 the Ackermann function is a hyperoperation:
#     A(m, n) = 2 ^^(m-2) (n + 3) - 3        (Knuth up-arrows, base 2)
# so A(4,4) = 2^^7 - 3 (a power tower of seven 2s) and A(5,5), A(6,6) are
# towers of astronomically large height.
#
# To evaluate a tower 2^^k mod m we use the generalised Euler lifting lemma:
# for any m and any x >= log2(m),  2^x = 2^((x mod phi(m)) + phi(m)) (mod m).
# (Proof by CRT on m = 2^a * t with t odd: both sides are 0 mod 2^a since
# x >= a, and mod t ordinary Euler applies because phi(t) | phi(m).)
# This handles the non-coprime modulus 14^8 = 2^8 * 7^8 correctly.
# The recursion descends through iterated totients, which reach 1 after
# O(log m) steps, so any tower of height >= ~40 gives the same residue;
# A(5,5) and A(6,6) therefore equal 2^^64 - 3 mod 14^8.

import sys
from functools import lru_cache

MOD = 14 ** 8


def ackermann_small(m, n, memo={}):
    key = (m, n)
    if key in memo:
        return memo[key]
    if m == 0:
        r = n + 1
    elif n == 0:
        r = ackermann_small(m - 1, 1)
    else:
        r = ackermann_small(m - 1, ackermann_small(m, n - 1))
    memo[key] = r
    return r


@lru_cache(maxsize=None)
def phi(n):
    result, p, m = n, 2, n
    while p * p <= m:
        if m % p == 0:
            result -= result // p
            while m % p == 0:
                m //= p
        p += 1
    if m > 1:
        result -= result // m
    return result


def tet(k, m):
    """2 ^^ k  (tower of k twos) mod m, for towers taller than 4."""
    if m == 1:
        return 0
    if k == 0:
        return 1 % m
    if k <= 4:
        # exact small towers: 2, 4, 16, 65536
        return (2, 4, 16, 65536)[k - 1] % m
    if k == 5:
        return pow(2, 65536, m)  # exponent known exactly
    # actual exponent 2^^(k-1) >= 65536 > log2(m), so the lemma applies
    f = phi(m)
    return pow(2, tet(k - 1, f) + f, m)


def solve():
    sys.setrecursionlimit(100000)
    total = sum(ackermann_small(n, n) for n in range(4))  # 1 + 3 + 7 + 61
    # A(4,4) = 2^^7 - 3
    total += tet(7, MOD) - 3
    # A(5,5) and A(6,6): tower heights are gigantic; residue is stable for
    # any height beyond the iterated-totient chain length, use height 64.
    total += 2 * (tet(64, MOD) - 3)
    return total % MOD


if __name__ == "__main__":
    print(solve())
