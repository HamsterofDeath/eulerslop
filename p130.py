#!/usr/bin/env python3
from math import gcd

def is_prime(n):
    if n < 2: return False
    if n < 4: return True
    if n % 2 == 0 or n % 3 == 0: return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0: return False
        i += 6
    return True

def order_mod(base, mod):
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
    return order_mod(10, 9 * n)

def solve():
    composites = []
    n = 7
    while len(composites) < 25:
        n += 2
        if n % 5 == 0:
            continue
        if is_prime(n):
            continue
        if gcd(n, 10) != 1:
            continue
        if (n - 1) % A(n) == 0:
            composites.append(n)
    return sum(composites)

if __name__ == "__main__":
    print(solve())
