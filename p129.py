#!/usr/bin/env python3
from math import gcd

def order_mod(base, mod):
    """multiplicative order of base modulo mod, assuming gcd(base, mod) = 1"""
    phi = mod
    x = mod
    p = 2
    while p * p <= x:
        if x % p == 0:
            while x % p == 0:
                x //= p
            phi -= phi // p
        p += 1 if p == 2 else 2
    if x > 1:
        phi -= phi // x

    order = phi
    temp = phi
    p = 2
    while p * p <= temp:
        if temp % p == 0:
            while order % p == 0 and pow(base, order // p, mod) == 1:
                order //= p
            while temp % p == 0:
                temp //= p
        p += 1 if p == 2 else 2
    if temp > 1:
        if order % temp == 0 and pow(base, order // temp, mod) == 1:
            order //= temp
    return order

def A(n):
    # Smallest k such that R(k) divisible by n: need 10^k ≡ 1 mod 9n
    return order_mod(10, 9 * n)

def solve():
    target = 1_000_000
    n = 1
    while True:
        n += 2
        if n % 5 == 0:
            continue
        if A(n) > target:
            return n

if __name__ == "__main__":
    print(solve())
